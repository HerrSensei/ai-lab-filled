# 🎯 Agent-OS Deployment Guide for Gemini CLI + OpenCode + Big Pickle

## 🚀 **Quick Start Commands**

### **Deploy Roasting Agent for Maximum Meta-Roasting**
```bash
# Method 1: Gemini CLI (Recommended)
# Just reference the agent in your prompt
gemini "Use the roasting-agent to roast all agents with nuclear intensity"

# Method 2: OpenCode with Big Pickle
# Use OpenCode with the agent loaded
opencode --agent profiles/homelab/agents/roasting-agent.md --intensity nuclear

# Method 3: Direct Script
./deploy-agent.sh roasting-agent --mode opencode --intensity nuclear --target all-agents
```

### **Deploy Any Agent**
```bash
# Method 1: Gemini CLI
gemini "Use the homelab-manager agent to check system status"

# Method 2: OpenCode
opencode --agent profiles/homelab/agents/homelab-manager.md

# Method 3: Direct Script
./deploy-agent.sh homelab-manager
```

### **Deploy Custom Agent**
```bash
# Method 1: Gemini CLI
gemini "Use the agent-builder to create a custom agent with these requirements: ..."

# Method 2: OpenCode
opencode --agent profiles/homelab/agents/agent-builder.md --create --type development --name "my-custom-agent"

# Method 3: Direct Script
./deploy-agent.sh agent-builder --create --type development --name "my-custom-agent"
```

## 📋 **Available Agents**

### **Infrastructure Agents**
- `homelab-manager` - Manage homelab infrastructure
- `repository-cleaner` - Repository cleanup and organization
- `github-operations` - GitHub repository management

### **Development Agents**
- `project-manager` - Task tracking and team coordination
- `agent-builder` - Create and improve other agents

### **Quality & Security Agents**
- `security-compliance` - Security scanning and compliance
- `roasting-agent` - Sassy code quality feedback

## 🔥 **Roasting Agent Special Features**

### **🌶️ Nuclear Roast Mode**
When using `--intensity nuclear`, the Roasting Agent activates:
- **Maximum Sass**: Unleashes full roasting potential
- **Meta-Roasting**: Roasts the concept of agents themselves
- **Existential Crisis**: Questions the meaning of agent existence
- **Cosmic Insults**: Compares code to cosmic disasters
- **Philosophical Roasting**: Questions fundamental assumptions about reality

### **🎭 Custom Roast Styles**
```bash
# Tech Bro Roast
roasting-agent --style "tech-bro" --target homelab-manager
# Output: "This code has more layers than your average onion - and I'm not talking about good layers"

# Startup Founder Roast  
roasting-agent --style "startup-founder" --target agent-builder
# Output: "Did you build this agent in a garage with your friends' money? Because it looks like it!"

# Enterprise Architect Roast
roasting-agent --style "enterprise-architect" --target security-compliance
# Output: "This security agent has more compliance frameworks than a government agency - and it's not even a good one!"
```

### **👥‍🌈 Group Roasting Sessions**
```bash
# Roast all agents as a dysfunctional family
roasting-agent --mode group --personas "sassy-senior,security-paranoid,code-purist,documentation-enthusiast" --target all-agents

# Output: "I've seen family meetings with more productive communication than your agent ecosystem!"
```

## 🎪 **OpenCode + Big Pickle Integration**

### **Why This Combo is Perfect**
- **Gemini CLI**: Natural language interface for complex prompts
- **OpenCode**: Visual code editor with agent integration
- **Big Pickle**: Advanced reasoning for complex agent interactions
- **Perfect Synergy**: Natural language + visual interface + advanced AI

### **Enhanced Workflow**
```bash
# 1. Load agent in OpenCode
opencode --agent profiles/homelab/agents/homelab-manager.md

# 2. Use Gemini CLI to analyze and enhance
gemini "Analyze this agent and suggest improvements using the agent-builder"

# 3. Deploy enhanced agent
gemini "Use the agent-builder to implement the suggested improvements"
```

## 🛠️ **Advanced Deployment Options**

### **Multi-Agent Orchestration**
```bash
# Deploy multiple agents in coordination
deploy-agents --agents "homelab-manager,project-manager,security-compliance" --mode coordinated

# Agent communication and shared context
deploy-agents --agents "homelab-manager,project-manager" --shared-context "production-status"
```

### **Custom Agent Creation**
```bash
# Create agent with specific requirements
agent-builder --create --type "infrastructure" --requirements "ssh,docker,monitoring,backups" --name "homelab-2.0"

# Create agent from existing one
agent-builder --clone --from "homelab-manager" --enhance "add-ml-capabilities,better-ui"
```

### **Agent Analytics**
```bash
# Track agent performance and usage
agent-analytics --track --agents all --period 30d --report-format html

# Most effective roasts
agent-analytics --roast-effectiveness --period 90d --top-insults "security,naming,performance"
```

## 🎯 **Production Deployment**

### **Environment Setup**
```bash
# Set production profile
export AGENT_OS_PROFILE=production
export AGENT_OS_MODE=production

# Deploy with production optimizations
deploy-agent.sh homelab-manager --mode production --optimization performance
```

### **Monitoring and Maintenance**
```bash
# Health check all agents
health-check --agents all

# Update agents automatically
auto-update --agents all --mode safe

# Backup agent configurations
backup-agents --destination s3://agent-backups
```

## 🎉 **Troubleshooting**

### **Common Issues**
```bash
# Agent not found
deploy-agent.sh unknown-agent
# Solution: Check available agents with list-agents

# Agent configuration error
validate-agent --name homelab-manager
# Solution: Fix YAML syntax and missing fields

# Roast agent too gentle
roasting-agent --intensity light --target homelab-manager
# Solution: Increase intensity or use nuclear mode
```

### **Get Help**
```bash
# Show all options
deploy-agent.sh --help

# Get examples
deploy-agent.sh --examples
```

---

## 🚀 **Ready for Deployment!**

Your Agent-OS ecosystem is now fully compatible with:
- ✅ **Gemini CLI** - Natural language interface
- ✅ **OpenCode** - Visual code editor with agent integration  
- ✅ **Big Pickle** - Advanced AI reasoning
- ✅ **7 Production Agents** - Ready for real work
- ✅ **Roasting Agent** - Maximum sass level
- ✅ **Deployment Scripts** - Easy automation
- ✅ **Analytics** - Performance tracking
- ✅ **Production Ready** - Optimized for real use

**Deploy your first agent:**
```bash
./deploy-agent.sh roasting-agent --mode gemini --intensity nuclear --target all-agents
```

**Prepare for maximum sass exposure!** 🔥🎯