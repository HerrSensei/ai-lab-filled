# 🎯 Agent-OS Deployment Guide

## Quick Start Commands

### **Deploy Roasting Agent for Meta-Roasting**
```bash
# Method 1: Claude Code (Recommended)
# Just type in Claude Code:
roast-agent --mode meta --target all-agents

# Method 2: Direct Command
roast-agent --mode meta --target agent-builder --style spicy
```

### **Deploy Any Agent**
```bash
# Using Agent Builder
agent-builder --create --type development --name "my-custom-agent"

# Using existing agent
homelab-manager --check-systems
project-manager --list-tasks --status in-progress
```

### **Group Roasting Session**
```bash
# Roast all agents as a group
roast-agent --mode group --personas "sassy-senior,security-paranoid,code-purist" --target all-agents

# Roast specific agent
roast-agent --target homelab-manager --intensity spicy
```

## 📋 Available Agents

### **Infrastructure Agents**
- `homelab-manager` - System monitoring and service control
- `repository-cleaner` - Repository cleanup and organization
- `github-operations` - Git and GitHub workflow management

### **Development Agents**
- `project-manager` - Task tracking and team coordination
- `agent-builder` - Create and improve other agents

### **Quality & Security Agents**
- `security-compliance` - Security scanning and compliance
- `roasting-agent` - Sassy code quality feedback

## 🔥 **Special Roasting Commands**

### **Meta-Roast All Agents**
```bash
roast-agent --mode meta --target all-agents --intensity nuclear
# Output: "I've seen better code on a Etch A Sketch - and it had more consistent naming"
```

### **Roast the Roasting Agent Itself**
```bash
roast-agent --target roasting-agent --intensity meta --style self-referential
# Output: "This roasting agent is so meta, it's like a snake eating its own tail while wearing a bow tie"
```

### **Custom Roast Configuration**
```bash
# Create custom roast style
roast-agent --style "tech-bro-with-hangover" --target homelab-manager

# Add custom personas
roast-agent --personas "startup-founder,enterprise-architect,caffeinated-dev" --target all-agents
```

## 🎭 **Agent Enhancement Workflow**

### **After Roast → Agent Improvement**
1. **Roast identifies issues** → **Agent Builder suggests enhancements**
2. **Implement improvements** → **Test enhanced agent**
3. **Repeat cycle** → **Continuously improve all agents**

### **Example Enhancement Cycle**
```bash
# Step 1: Roast current agent
roast-agent --target security-compliance --intensity spicy

# Step 2: Get enhancement suggestions
agent-builder --analyze --target security-compliance --from-roast

# Step 3: Apply enhancements
agent-builder --enhance --target security-compliance --improvements "better-error-handling,more-automation"

# Step 4: Test enhanced agent
security-compliance --test-mode comprehensive
```

## 🛠️ **Advanced Deployment**

### **Multi-Agent Coordination**
```bash
# Deploy multiple agents in coordination
deploy-agents --agents "homelab-manager,project-manager,security-compliance" --mode coordinated

# Agent orchestration
homelab-manager --orchestrate-with project-manager --shared-context "production-status"
```

### **Custom Agent Creation**
```bash
# Create specialized agent
agent-builder --template "ml-agent" --custom-context "homelab-iot-data" --name "homelab-ml-ops"

# From existing agent
agent-builder --clone --from "project-manager" --enhance "add-ai-predictions,better-automation"
```

## 📊 **Monitoring and Analytics**

### **Agent Performance Tracking**
```bash
# Track agent usage and effectiveness
agent-analytics --track-usage --agents all --period 30d

# Generate performance report
agent-analytics --report --type performance --format html --output agent-performance.html
```

### **Roast Effectiveness Metrics**
```bash
# How many roasts led to improvements?
roast-analytics --improvement-rate --period 90d

# Most common roast patterns
roast-analytics --common-issues --category "security,naming,performance"
```

## 🎪 **Troubleshooting**

### **Agent Not Found**
```bash
# Check if agent exists
list-agents --available | grep "roasting-agent"

# Install missing agent
agent-builder --create --type "quality" --name "roasting-agent" --template "roasting"
```

### **Agent Configuration Issues**
```bash
# Check agent configuration
validate-agent --name "homelab-manager" --check-syntax

# Fix configuration issues
fix-agent-config --name "homelab-manager" --issue "missing-workflows"
```

---

## 🚀 **Ready to Roast!**

Your Agent-OS ecosystem is fully deployed and ready for action! 

**Choose your deployment method:**
- **Quick**: Use existing agents directly
- **Advanced**: Use Agent Builder for custom agents  
- **Meta**: Deploy Roasting Agent for comprehensive feedback

**Remember**: The Roasting Agent works best when you're actually trying to improve your code - it's most effective when there's real code to critique! 

Now go forth and make your code both better AND more entertaining! 🔥🎯