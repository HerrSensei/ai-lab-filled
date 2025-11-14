#!/bin/bash

# Validation Script for Homelab Agent OS Framework
# Performs comprehensive validation of all components

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validation results
VALIDATION_PASSED=0
VALIDATION_FAILED=0
VALIDATION_WARNINGS=0

echo -e "${BLUE}🔍 Homelab Agent OS Framework - Validation Suite${NC}"
echo "=================================================="
echo "Started at: $(date)"
echo ""

# Helper functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((VALIDATION_PASSED++))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    ((VALIDATION_FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((VALIDATION_WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Validate project structure
validate_structure() {
    echo -e "${BLUE}📁 Validating Project Structure...${NC}"
    
    # Check main directories
    dirs=("agent-os" "n8n-nodes" "deployment" "config" "scripts" "docs" "tests")
    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ]; then
            print_success "Directory $dir exists"
        else
            print_error "Directory $dir missing"
        fi
    done
    
    # Check key files
    files=("README.md" "docker-compose.yml")
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            print_success "File $file exists"
        else
            print_error "File $file missing"
        fi
    done
    
    # Check agent-os subdirectories
    agent_os_dirs=("agent-os/core" "agent-os/services" "agent-os/api")
    for dir in "${agent_os_dirs[@]}"; do
        if [ -d "$dir" ]; then
            print_success "Agent OS directory $dir exists"
        else
            print_error "Agent OS directory $dir missing"
        fi
    done
    
    echo ""
}

# Validate Python code
validate_python() {
    echo -e "${BLUE}🐍 Validating Python Code...${NC}"
    
    # Check Python syntax
    python_files=$(find . -name "*.py" -not -path "./tests/*" -not -path "./.venv/*")
    
    for file in $python_files; do
        if python3 -m py_compile "$file" 2>/dev/null; then
            print_success "Python syntax OK: $file"
        else
            print_error "Python syntax error: $file"
        fi
    done
    
    # Check imports
    if python3 -c "import agent_os.core.agent_manager" 2>/dev/null; then
        print_success "Core modules import correctly"
    else
        print_error "Core modules import failed"
    fi
    
    echo ""
}

# Validate Docker configuration
validate_docker() {
    echo -e "${BLUE}🐳 Validating Docker Configuration...${NC}"
    
    # Check docker-compose.yml syntax
    if command -v docker-compose &> /dev/null; then
        if docker-compose config > /dev/null 2>&1; then
            print_success "docker-compose.yml syntax is valid"
        else
            print_error "docker-compose.yml syntax error"
        fi
    else
        print_warning "Docker Compose not available for validation"
    fi
    
    # Check Dockerfiles
    dockerfiles=$(find . -name "Dockerfile*")
    for dockerfile in $dockerfiles; do
        if [ -f "$dockerfile" ]; then
            print_success "Dockerfile exists: $dockerfile"
        else
            print_error "Dockerfile missing: $dockerfile"
        fi
    done
    
    echo ""
}

# Validate Kubernetes configuration
validate_kubernetes() {
    echo -e "${BLUE}☸️  Validating Kubernetes Configuration...${NC}"
    
    # Check K8s files
    k8s_files=$(find deployment/k8s -name "*.yaml" 2>/dev/null || true)
    
    if [ -z "$k8s_files" ]; then
        print_warning "No Kubernetes files found"
    else
        for file in $k8s_files; do
            # Check YAML syntax
            if command -v python3 &> /dev/null; then
                if python3 -c "import yaml; yaml.safe_load_all(open('$file'))" 2>/dev/null; then
                    print_success "K8s YAML syntax OK: $file"
                else
                    print_error "K8s YAML syntax error: $file"
                fi
            else
                print_warning "Python3 not available for YAML validation"
            fi
        done
    fi
    
    echo ""
}

# Validate n8n integration
validate_n8n() {
    echo -e "${BLUE}🔌 Validating n8n Integration...${NC}"
    
    # Check n8n custom nodes
    if [ -f "n8n-nodes/agent_os_nodes.py" ]; then
        print_success "n8n custom nodes file exists"
        
        # Check Python syntax
        if python3 -m py_compile n8n-nodes/agent_os_nodes.py 2>/dev/null; then
            print_success "n8n nodes Python syntax OK"
        else
            print_error "n8n nodes Python syntax error"
        fi
    else
        print_error "n8n custom nodes file missing"
    fi
    
    # Check package.json for TypeScript nodes
    if [ -f "n8n-nodes/package.json" ]; then
        print_success "n8n nodes package.json exists"
    else
        print_warning "n8n nodes package.json missing (TypeScript nodes)"
    fi
    
    echo ""
}

# Validate Gemini integration
validate_gemini() {
    echo -e "${BLUE}🔮 Validating Gemini Integration...${NC}"
    
    # Check gemini service file
    if [ -f "agent-os/services/gemini_integration.py" ]; then
        print_success "Gemini integration service exists"
        
        # Check Python syntax
        if python3 -m py_compile agent-os/services/gemini_integration.py 2>/dev/null; then
            print_success "Gemini service Python syntax OK"
        else
            print_error "Gemini service Python syntax error"
        fi
    else
        print_error "Gemini integration service missing"
    fi
    
    # Check setup script
    if [ -f "scripts/setup-gemini.sh" ]; then
        print_success "Gemini setup script exists"
        if [ -x "scripts/setup-gemini.sh" ]; then
            print_success "Gemini setup script is executable"
        else
            print_error "Gemini setup script is not executable"
        fi
    else
        print_error "Gemini setup script missing"
    fi
    
    # Check for gemini-cli
    if command -v gemini &> /dev/null; then
        print_success "gemini-cli is installed"
    else
        print_warning "gemini-cli not installed"
    fi
    
    # Check for opencode
    if command -v opencode &> /dev/null; then
        print_success "opencode is installed"
    else
        print_warning "opencode not installed"
    fi
    
    echo ""
}

# Validate scripts
validate_scripts() {
    echo -e "${BLUE}🛠️  Validating Scripts...${NC}"
    
    scripts=("scripts/setup.sh" "scripts/setup-gemini.sh" "scripts/deploy-homeserver.sh")
    
    for script in "${scripts[@]}"; do
        if [ -f "$script" ]; then
            print_success "Script exists: $script"
            
            # Check if executable
            if [ -x "$script" ]; then
                print_success "Script is executable: $script"
            else
                print_error "Script is not executable: $script"
            fi
            
            # Check bash syntax
            if bash -n "$script" 2>/dev/null; then
                print_success "Script syntax OK: $script"
            else
                print_error "Script syntax error: $script"
            fi
        else
            print_error "Script missing: $script"
        fi
    done
    
    echo ""
}

# Validate configuration files
validate_config() {
    echo -e "${BLUE}⚙️  Validating Configuration...${NC}"
    
    # Check .env template
    if [ -f ".env.template" ]; then
        print_success ".env.template exists"
    else
        print_warning ".env.template missing"
    fi
    
    # Check config directory (created by setup)
    if [ -d "config" ]; then
        print_success "config directory exists"
        
        # Check nginx config
        if [ -f "config/nginx/nginx.conf" ]; then
            print_success "nginx configuration exists"
        else
            print_warning "nginx configuration missing"
        fi
    else
        print_warning "config directory not created (run setup.sh)"
    fi
    
    echo ""
}

# Validate tests
validate_tests() {
    echo -e "${BLUE}🧪 Validating Tests...${NC}"
    
    # Check test files
    if [ -f "tests/test_framework.py" ]; then
        print_success "Test framework exists"
        
        # Check if executable
        if [ -x "tests/test_framework.py" ]; then
            print_success "Test framework is executable"
        else
            print_error "Test framework is not executable"
        fi
        
        # Run syntax check
        if python3 -m py_compile tests/test_framework.py 2>/dev/null; then
            print_success "Test framework syntax OK"
        else
            print_error "Test framework syntax error"
        fi
    else
        print_error "Test framework missing"
    fi
    
    echo ""
}

# Validate documentation
validate_documentation() {
    echo -e "${BLUE}📚 Validating Documentation...${NC}"
    
    # Check README
    if [ -f "README.md" ]; then
        print_success "README.md exists"
        
        # Check README content
        if grep -q "Quick Start" README.md; then
            print_success "README contains Quick Start section"
        else
            print_warning "README missing Quick Start section"
        fi
    else
        print_error "README.md missing"
    fi
    
    # Check docs directory
    if [ -d "docs" ]; then
        print_success "docs directory exists"
        
        # Count documentation files
        doc_files=$(find docs -name "*.md" | wc -l)
        if [ "$doc_files" -gt 0 ]; then
            print_success "Found $doc_files documentation files"
        else
            print_warning "No markdown files in docs directory"
        fi
    else
        print_warning "docs directory missing"
    fi
    
    echo ""
}

# Run integration tests if services are running
validate_integration() {
    echo -e "${BLUE}🔗 Validating Integration...${NC}"
    
    # Test Agent OS API
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        print_success "Agent OS API is responding"
        
        # Test API endpoints
        if curl -s http://localhost:8080/stats > /dev/null 2>&1; then
            print_success "Agent OS API endpoints working"
        else
            print_error "Agent OS API endpoints not working"
        fi
    else
        print_warning "Agent OS API not running (start with docker-compose up)"
    fi
    
    # Test n8n
    if curl -s http://localhost:5678 > /dev/null 2>&1; then
        print_success "n8n is responding"
    else
        print_warning "n8n not running (start with docker-compose up)"
    fi
    
    # Test Docker services
    if command -v docker-compose &> /dev/null; then
        if docker-compose ps > /dev/null 2>&1; then
            print_success "Docker Compose services manageable"
        else
            print_warning "Docker Compose services not accessible"
        fi
    fi
    
    echo ""
}

# Generate validation report
generate_report() {
    echo -e "${BLUE}📊 Validation Report${NC}"
    echo "===================="
    echo -e "Passed:  ${GREEN}$VALIDATION_PASSED${NC}"
    echo -e "Failed:  ${RED}$VALIDATION_FAILED${NC}"
    echo -e "Warnings: ${YELLOW}$VALIDATION_WARNINGS${NC}"
    echo ""
    
    if [ $VALIDATION_FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 All critical validations passed!${NC}"
        if [ $VALIDATION_WARNINGS -eq 0 ]; then
            echo -e "${GREEN}✨ Perfect validation - no warnings!${NC}"
        else
            echo -e "${YELLOW}⚠️  Some warnings detected - review recommended${NC}"
        fi
        return 0
    else
        echo -e "${RED}❌ Some validations failed - please fix issues${NC}"
        return 1
    fi
}

# Main validation function
main() {
    echo "Starting comprehensive validation..."
    echo ""
    
    # Change to project directory
    cd "$(dirname "$0")/.."
    
    # Run all validations
    validate_structure
    validate_python
    validate_docker
    validate_kubernetes
    validate_n8n
    validate_gemini
    validate_scripts
    validate_config
    validate_tests
    validate_documentation
    validate_integration
    
    # Generate report
    generate_report
}

# Run main function
main "$@"