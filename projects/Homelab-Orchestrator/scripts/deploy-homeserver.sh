#!/bin/bash

# Homelab Deployment Script
# Deploys the Agent OS framework to a Kubernetes homeserver

set -e

# Configuration
NAMESPACE="homelab"
CLUSTER_NAME="homelab-cluster"
REGISTRY="registry.homelab.local"
DOMAIN="homelab.local"

echo "🚀 Deploying Homelab Agent OS to Kubernetes..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl is not installed. Please install kubectl first."
        exit 1
    fi
    
    # Check cluster access
    if ! kubectl cluster-info &> /dev/null; then
        echo "❌ Cannot access Kubernetes cluster. Please check your kubeconfig."
        exit 1
    fi
    
    # Check helm
    if ! command -v helm &> /dev/null; then
        echo "❌ Helm is not installed. Please install Helm first."
        exit 1
    fi
    
    echo "✅ Prerequisites are installed"
}

# Setup namespace and prerequisites
setup_namespace() {
    echo "📁 Setting up namespace..."
    
    # Create namespace
    kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    
    # Add required helm repositories
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo add jetstack https://charts.jetstack.io
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    
    echo "✅ Namespace and helm repos ready"
}

# Install ingress controller
install_ingress() {
    echo "🌐 Installing ingress controller..."
    
    # Install NGINX ingress controller
    helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
        --namespace $NAMESPACE \
        --set controller.replicaCount=2 \
        --set controller.nodeSelector."kubernetes\.io/os"=linux \
        --set controller.admissionWebhooks.patch.nodeSelector."kubernetes\.io/os"=linux \
        --set controller.service.type=LoadBalancer \
        --set controller.service.externalTrafficPolicy=Local \
        --set controller.publishService.enabled=true
    
    echo "✅ Ingress controller installed"
}

# Install cert-manager for SSL
install_cert_manager() {
    echo "🔒 Installing cert-manager..."
    
    # Install cert-manager CRDs
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.crds.yaml
    
    # Install cert-manager helm chart
    helm upgrade --install cert-manager jetstack/cert-manager \
        --namespace $NAMESPACE \
        --set installCRDs=true \
        --set prometheus.enabled=true
    
    # Create cluster issuer for Let's Encrypt
    cat << EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@${DOMAIN}
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
    
    echo "✅ Cert-manager installed"
}

# Setup container registry
setup_registry() {
    echo "📦 Setting up container registry..."
    
    # Install docker registry (if not already present)
    helm upgrade --install docker-registry stable/docker-registry \
        --namespace $NAMESPACE \
        --set service.type=LoadBalancer \
        --set service.port=5000 \
        --set persistence.enabled=true \
        --set persistence.size=20Gi
    
    echo "✅ Container registry ready"
}

# Build and push images
build_images() {
    echo "🔨 Building and pushing container images..."
    
    # Build Agent OS image
    docker build -t ${REGISTRY}/agent-os:latest -f deployment/docker/Dockerfile.agent-os .
    
    # Push to registry
    docker push ${REGISTRY}/agent-os:latest
    
    echo "✅ Container images built and pushed"
}

# Create secrets
create_secrets() {
    echo "🔑 Creating secrets..."
    
    # Get secrets from user or environment
    read -s -p "Enter Google AI API Key: " google_api_key
    echo
    read -s -p "Enter n8n password: " n8n_password
    echo
    read -s -p "Enter PostgreSQL password: " postgres_password
    echo
    read -s -p "Enter secret key (or press Enter to generate): " secret_key
    
    if [ -z "$secret_key" ]; then
        secret_key=$(openssl rand -hex 32)
    fi
    echo
    
    # Create Kubernetes secret
    kubectl create secret generic agent-os-secrets \
        --namespace $NAMESPACE \
        --from-literal=google-ai-api-key="$google_api_key" \
        --from-literal=n8n-password="$n8n_password" \
        --from-literal=postgres-password="$postgres_password" \
        --from-literal=secret-key="$secret_key" \
        --dry-run=client -o yaml | kubectl apply -f -
    
    echo "✅ Secrets created"
}

# Deploy application
deploy_application() {
    echo "🚀 Deploying Agent OS application..."
    
    # Apply deployments
    kubectl apply -f deployment/k8s/deployments.yaml --namespace $NAMESPACE
    kubectl apply -f deployment/k8s/infrastructure.yaml --namespace $NAMESPACE
    
    # Wait for deployments to be ready
    echo "⏳ Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/agent-os-api --namespace $NAMESPACE
    kubectl wait --for=condition=available --timeout=300s deployment/n8n --namespace $NAMESPACE
    kubectl wait --for=condition=available --timeout=300s deployment/postgres --namespace $NAMESPACE
    kubectl wait --for=condition=available --timeout=300s deployment/redis --namespace $NAMESPACE
    
    echo "✅ Application deployed"
}

# Install monitoring
install_monitoring() {
    echo "📊 Installing monitoring stack..."
    
    # Install Prometheus
    helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
        --namespace $NAMESPACE \
        --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=20Gi \
        --set grafana.adminPassword=admin123 \
        --set grafana.persistence.enabled=true \
        --set grafana.persistence.size=5Gi
    
    # Import Grafana dashboards
    kubectl apply -f deployment/monitoring/grafana-dashboards.yaml --namespace $NAMESPACE
    
    echo "✅ Monitoring stack installed"
}

# Setup DNS and networking
setup_networking() {
    echo "🌐 Setting up networking..."
    
    # Get ingress IP
    INGRESS_IP=$(kubectl get service ingress-nginx-controller --namespace $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    
    if [ -z "$INGRESS_IP" ]; then
        echo "⚠️  Could not get ingress IP. Please configure DNS manually."
        echo "Expected DNS records:"
        echo "  agent-os.${DOMAIN} -> <INGRESS_IP>"
        echo "  n8n.${DOMAIN} -> <INGRESS_IP>"
        echo "  grafana.${DOMAIN} -> <INGRESS_IP>"
    else
        echo "📝 Configure your DNS to point to ${INGRESS_IP}:"
        echo "  agent-os.${DOMAIN} -> ${INGRESS_IP}"
        echo "  n8n.${DOMAIN} -> ${INGRESS_IP}"
        echo "  grafana.${DOMAIN} -> ${INGRESS_IP}"
    fi
    
    echo "✅ Networking configuration ready"
}

# Run post-deployment tests
run_tests() {
    echo "🧪 Running post-deployment tests..."
    
    # Test API health
    echo "Testing Agent OS API..."
    kubectl wait --for=condition=ready --timeout=60s pod -l app=agent-os,component=api --namespace $NAMESPACE
    
    # Test n8n
    echo "Testing n8n..."
    kubectl wait --for=condition=ready --timeout=60s pod -l app=agent-os,component=n8n --namespace $NAMESPACE
    
    # Test database connectivity
    echo "Testing database connectivity..."
    kubectl exec -n $NAMESPACE deployment/agent-os-api -- python -c "
import requests
response = requests.get('http://localhost:8080/health')
print(f'API Health Check: {response.status_code}')
"
    
    echo "✅ Post-deployment tests completed"
}

# Print deployment information
print_deployment_info() {
    echo ""
    echo "🎉 Homelab Agent OS deployment completed!"
    echo ""
    echo "📊 Access URLs:"
    echo "  Agent OS API:     https://agent-os.${DOMAIN}"
    echo "  Agent OS Docs:    https://agent-os.${DOMAIN}/docs"
    echo "  n8n Interface:    https://n8n.${DOMAIN}"
    echo "  Grafana:          https://grafana.${DOMAIN} (admin/admin123)"
    echo "  Prometheus:       https://prometheus.${DOMAIN}"
    echo ""
    echo "🔧 Management Commands:"
    echo "  View pods:        kubectl get pods -n $NAMESPACE"
    echo "  View services:    kubectl get services -n $NAMESPACE"
    echo "  View logs:        kubectl logs -f deployment/agent-os-api -n $NAMESPACE"
    echo "  Scale deployment: kubectl scale deployment agent-os-api --replicas=3 -n $NAMESPACE"
    echo ""
    echo "📈 Monitoring:"
    echo "  Grafana Dashboards: https://grafana.${DOMAIN}"
    echo "  Prometheus: https://prometheus.${DOMAIN}"
    echo ""
    echo "🔒 SSL Certificates:"
    echo "  Certificates will be automatically issued by Let's Encrypt"
    echo "  Check status: kubectl get certificates -n $NAMESPACE"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_namespace
    install_ingress
    install_cert_manager
    setup_registry
    build_images
    create_secrets
    deploy_application
    install_monitoring
    setup_networking
    run_tests
    print_deployment_info
}

# Run main function
main "$@"