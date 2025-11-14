#!/bin/bash

# Homelab Agent OS Framework Setup Script
# This script sets up the complete homelab environment

set -e

echo "🚀 Setting up Homelab Agent OS Framework..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Node.js (for n8n custom nodes)
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    echo "✅ All prerequisites are installed"
}

# Create necessary directories
setup_directories() {
    echo "📁 Creating directories..."
    
    mkdir -p data/{agent_os,n8n,redis,prometheus,grafana}
    mkdir -p logs
    mkdir -p config/{nginx,ssl}
    
    echo "✅ Directories created"
}

# Generate configuration files
setup_config() {
    echo "⚙️ Setting up configuration..."
    
    # Generate environment file
    cat > .env << EOF
# Homelab Agent OS Environment Configuration
COMPOSE_PROJECT_NAME=homelab-agent-os

# Agent OS Configuration
AGENT_OS_PORT=8080
AGENT_OS_LOG_LEVEL=INFO
AGENT_OS_DATABASE_URL=sqlite:///data/agent_os.db

# n8n Configuration
N8N_PORT=5678
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=homeserver123
N8N_HOST=localhost
N8N_PROTOCOL=http

# Redis Configuration
REDIS_PORT=6379

# Monitoring Configuration
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
GRAFANA_ADMIN_PASSWORD=admin123

# SSL Configuration (optional)
SSL_ENABLED=false
SSL_CERT_PATH=./config/ssl/cert.pem
SSL_KEY_PATH=./config/ssl/key.pem
EOF

    # Generate nginx configuration
    cat > config/nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream agent_os {
        server agent-os:8080;
    }
    
    upstream n8n {
        server n8n:5678;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # Agent OS API
        location /api/ {
            proxy_pass http://agent_os/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # n8n Web Interface
        location /n8n/ {
            proxy_pass http://n8n/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Default redirect to n8n
        location / {
            proxy_pass http://n8n/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

    # Generate prometheus configuration
    cat > deployment/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'agent-os'
    static_configs:
      - targets: ['agent-os:8080']
    metrics_path: '/metrics'
    
  - job_name: 'n8n'
    static_configs:
      - targets: ['n8n:5678']
    metrics_path: '/metrics'
    
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF

    echo "✅ Configuration files generated"
}

# Setup n8n custom nodes
setup_n8n_nodes() {
    echo "🔌 Setting up n8n custom nodes..."
    
    # Create package.json for custom nodes
    cat > n8n-nodes/package.json << 'EOF'
{
  "name": "n8n-nodes-agent-os",
  "version": "1.0.0",
  "description": "Custom n8n nodes for Agent OS integration",
  "main": "index.js",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "keywords": ["n8n", "agent-os", "automation"],
  "dependencies": {
    "n8n-workflow": "^1.0.0",
    "n8n-core": "^1.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
  }
}
EOF

    # Create TypeScript configuration
    cat > n8n-nodes/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "es2020",
    "outDir": "./dist",
    "rootDir": "./",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
EOF

    # Convert Python nodes to TypeScript (simplified version)
    cat > n8n-nodes/AgentOSNode.ts << 'EOF'
import { IExecuteFunctions, INodeExecutionData, INodeType, INodeTypeDescription } from 'n8n-workflow';

export class AgentOSNode implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Agent OS',
        name: 'agentOS',
        group: ['transform'],
        version: 1,
        description: 'Interact with Homelab Agent OS framework',
        defaults: {
            name: 'Agent OS',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [],
        properties: [
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'options',
                options: [
                    {
                        name: 'Create Agent',
                        value: 'createAgent',
                    },
                    {
                        name: 'List Agents',
                        value: 'listAgents',
                    },
                    {
                        name: 'Stop Agent',
                        value: 'stopAgent',
                    },
                ],
                default: 'listAgents',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const operation = this.getNodeParameter('operation', 0) as string;
        const returnData: INodeExecutionData[] = [];

        for (let i = 0; i < items.length; i++) {
            // Execute operation based on selection
            if (operation === 'listAgents') {
                // Make HTTP request to Agent OS API
                const response = await this.helpers.httpRequest({
                    method: 'GET',
                    url: 'http://agent-os:8080/agents',
                    json: true,
                });
                
                returnData.push({
                    json: response,
                });
            }
            // Add other operations...
        }

        return [returnData];
    }
}
EOF

    echo "✅ n8n custom nodes setup completed"
}

# Build and start services
start_services() {
    echo "🐳 Building and starting services..."
    
    # Build custom Docker images
    docker-compose build agent-os
    
    # Start all services
    docker-compose up -d
    
    echo "✅ Services started"
}

# Wait for services to be ready
wait_for_services() {
    echo "⏳ Waiting for services to be ready..."
    
    # Wait for Agent OS API
    echo "Waiting for Agent OS API..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:8080/health &>/dev/null; then
            echo "✅ Agent OS API is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        echo "❌ Agent OS API failed to start"
        exit 1
    fi
    
    # Wait for n8n
    echo "Waiting for n8n..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:5678 &>/dev/null; then
            echo "✅ n8n is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        echo "❌ n8n failed to start"
        exit 1
    fi
}

# Create initial agents
setup_initial_agents() {
    echo "🤖 Setting up initial agents..."
    
    # Create a monitor agent
    curl -X POST http://localhost:8080/agents \
        -H "Content-Type: application/json" \
        -d '{
            "name": "System Monitor",
            "type": "monitor",
            "config": {
                "heartbeat_interval": 30,
                "check_interval": 60,
                "service_config": {
                    "monitored_services": ["agent-os", "n8n", "redis"],
                    "alert_threshold": 3
                }
            }
        }'
    
    # Create a service agent
    curl -X POST http://localhost:8080/agents \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Task Processor",
            "type": "service",
            "config": {
                "heartbeat_interval": 15,
                "check_interval": 30,
                "service_config": {
                    "max_concurrent_tasks": 5,
                    "task_timeout": 300
                }
            }
        }'
    
    echo "✅ Initial agents created"
}

# Print access information
print_access_info() {
    echo ""
    echo "🎉 Homelab Agent OS Framework is now running!"
    echo ""
    echo "📊 Access URLs:"
    echo "  Agent OS API:     http://localhost:8080"
    echo "  Agent OS Docs:    http://localhost:8080/docs"
    echo "  n8n Interface:    http://localhost:5678"
    echo "  Grafana:          http://localhost:3000 (admin/admin123)"
    echo "  Prometheus:       http://localhost:9090"
    echo ""
    echo "🔧 Management Commands:"
    echo "  View logs:        docker-compose logs -f"
    echo "  Stop services:    docker-compose down"
    echo "  Restart services: docker-compose restart"
    echo "  Check status:     docker-compose ps"
    echo ""
    echo "📚 Next Steps:"
    echo "  1. Open n8n at http://localhost:5678"
    echo "  2. Create workflows using Agent OS custom nodes"
    echo "  3. Monitor agents via Grafana dashboard"
    echo "  4. Check API documentation at http://localhost:8080/docs"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_directories
    setup_config
    setup_n8n_nodes
    start_services
    wait_for_services
    setup_initial_agents
    print_access_info
}

# Run main function
main "$@"