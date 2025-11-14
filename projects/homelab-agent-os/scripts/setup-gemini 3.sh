#!/bin/bash

# Gemini-CLI Setup Script for Homelab Agent OS
# Installs and configures gemini-cli with opencode integration

set -e

echo "🔮 Setting up Gemini-CLI integration..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        echo "❌ npm is not installed. Please install npm first."
        exit 1
    fi
    
    echo "✅ Prerequisites are installed"
}

# Install gemini-cli
install_gemini_cli() {
    echo "📦 Installing gemini-cli..."
    
    # Install gemini-cli globally
    npm install -g @google/generative-ai-cli
    
    # Install opencode CLI
    npm install -g opencode
    
    echo "✅ Gemini-CLI and opencode installed"
}

# Setup configuration
setup_config() {
    echo "⚙️ Setting up configuration..."
    
    # Create config directory
    mkdir -p ~/.gemini-cli
    
    # Create configuration file
    cat > ~/.gemini-cli/config.json << 'EOF'
{
  "model": "gemini-1.5-pro",
  "temperature": 0.7,
  "maxTokens": 2048,
  "topP": 0.8,
  "topK": 40,
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH", 
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
EOF

    # Create opencode configuration
    cat > ~/.opencode/config.json << 'EOF'
{
  "defaultModel": "gemini-1.5-pro",
  "contextWindow": 32768,
  "autoSave": true,
  "syntaxHighlighting": true,
  "theme": "dark"
}
EOF

    echo "✅ Configuration created"
}

# Setup API key
setup_api_key() {
    echo "🔑 Setting up API key..."
    
    # Check if API key already exists
    if [ -f ~/.gemini-cli/api-key.txt ]; then
        echo "API key file already exists. Skipping setup."
        return
    fi
    
    echo "Please enter your Google AI API key:"
    echo "You can get one from: https://makersuite.google.com/app/apikey"
    read -s -p "API Key: " api_key
    echo
    
    # Save API key
    echo "$api_key" > ~/.gemini-cli/api-key.txt
    chmod 600 ~/.gemini-cli/api-key.txt
    
    # Set environment variable
    echo "export GOOGLE_AI_API_KEY=\"$api_key\"" >> ~/.bashrc
    echo "export GOOGLE_AI_API_KEY=\"$api_key\"" >> ~/.zshrc 2>/dev/null || true
    
    echo "✅ API key configured"
}

# Create helper scripts
create_helpers() {
    echo "🛠️ Creating helper scripts..."
    
    # Create gemini prompt helper
    cat > /usr/local/bin/gemini-prompt << 'EOF'
#!/bin/bash

# Gemini prompt helper script
if [ $# -eq 0 ]; then
    echo "Usage: gemini-prompt <prompt>"
    echo "Example: gemini-prompt 'Write a Python function to sort a list'"
    exit 1
fi

PROMPT="$*"
gemini prompt "$PROMPT"
EOF

    # Create opencode helper
    cat > /usr/local/bin/opencode-agent << 'EOF'
#!/bin/bash

# Opencode helper for Agent OS
if [ $# -eq 0 ]; then
    echo "Usage: opencode-agent <file>"
    echo "Example: opencode-agent /path/to/code.py"
    exit 1
fi

FILE="$1"
opencode --model gemini-1.5-pro --context agent-os "$FILE"
EOF

    # Create gemini workflow helper
    cat > /usr/local/bin/gemini-workflow << 'EOF'
#!/bin/bash

# Gemini workflow helper for n8n integration
if [ $# -lt 2 ]; then
    echo "Usage: gemini-workflow <task-type> <prompt>"
    echo "Task types: code_generation, analysis, troubleshooting, planning, review"
    exit 1
fi

TASK_TYPE="$1"
PROMPT="${@:2}"

# Create JSON payload
cat << JSON | curl -X POST http://localhost:8080/agents/gemini/task \
    -H "Content-Type: application/json" \
    -d @-
{
    "task_type": "$TASK_TYPE",
    "prompt": "$PROMPT",
    "priority": "medium",
    "wait_for_completion": true,
    "timeout": 300
}
JSON
EOF

    # Make scripts executable
    chmod +x /usr/local/bin/gemini-prompt
    chmod +x /usr/local/bin/opencode-agent
    chmod +x /usr/local/bin/gemini-workflow
    
    echo "✅ Helper scripts created"
}

# Test installation
test_installation() {
    echo "🧪 Testing installation..."
    
    # Test gemini-cli
    if command -v gemini &> /dev/null; then
        echo "✅ gemini-cli is accessible"
    else
        echo "❌ gemini-cli not found in PATH"
        exit 1
    fi
    
    # Test opencode
    if command -v opencode &> /dev/null; then
        echo "✅ opencode is accessible"
    else
        echo "❌ opencode not found in PATH"
        exit 1
    fi
    
    # Test API key (if available)
    if [ -f ~/.gemini-cli/api-key.txt ]; then
        echo "✅ API key file exists"
    else
        echo "⚠️  API key not configured. Please run 'gemini-setup' again."
    fi
    
    echo "✅ Installation test completed"
}

# Create integration service
create_integration_service() {
    echo "🔌 Creating integration service..."
    
    # Create systemd service file
    cat > /etc/systemd/system/gemini-agent.service << 'EOF'
[Unit]
Description=Gemini Agent Integration Service
After=network.target

[Service]
Type=simple
User=agent-os
WorkingDirectory=/opt/agent-os
Environment=GOOGLE_AI_API_KEY_FILE=/home/agent-os/.gemini-cli/api-key.txt
ExecStart=/usr/bin/python3 -m agent-os.services.gemini_integration
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable gemini-agent
    
    echo "✅ Integration service created"
}

# Print usage information
print_usage() {
    echo ""
    echo "🎉 Gemini-CLI integration is now ready!"
    echo ""
    echo "📚 Available Commands:"
    echo "  gemini-prompt <prompt>           - Send prompt to Gemini"
    echo "  opencode-agent <file>            - Analyze file with opencode"
    echo "  gemini-workflow <type> <prompt>  - Send task to Agent OS"
    echo ""
    echo "🔗 Integration Points:"
    echo "  Agent OS API: http://localhost:8080/agents/gemini"
    echo "  n8n Custom Nodes: Agent OS AI Agent node"
    echo "  CLI Tools: gemini-prompt, opencode-agent"
    echo ""
    echo "📖 Documentation:"
    echo "  gemini --help                     - Gemini CLI help"
    echo "  opencode --help                   - Opencode help"
    echo ""
    echo "⚙️  Configuration:"
    echo "  Config file: ~/.gemini-cli/config.json"
    echo "  API key: ~/.gemini-cli/api-key.txt"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    install_gemini_cli
    setup_config
    setup_api_key
    create_helpers
    test_installation
    create_integration_service
    print_usage
}

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then
    echo "This script requires sudo privileges for system-wide installation."
    echo "Please run: sudo $0"
    exit 1
fi

# Run main function
main "$@"