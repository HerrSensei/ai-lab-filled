# Hybrid-Architektur Schnittstellen

## Zweck

Definiert standardisierte Schnittstellen zwischen den drei Schichten der Hybrid-Architektur: Agent OS (Design Layer), n8n (Orchestration Layer), und MCP (Runtime Control Layer).

## Architektur-Überblick

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent OS      │    │      n8n        │    │      MCP        │
│  Design Layer   │◄──►│Orchestration    │◄──►│Runtime Control  │
│                 │    │Layer            │    │Layer            │
│ • AI Agents     │    │ • Workflows     │    │ • K8s Tools     │
│ • Specs         │    │ • Automation    │    │ • Resources     │
│ • Planning      │    │ • Integration   │    │ • Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Standard-Kommunikationsprotokolle

### 1. Agent OS → n8n (Design → Orchestration)

#### Workflow-Generierung
```python
# Agent OS generiert Workflow-Spezifikation
workflow_spec = {
    "name": "system_health_check",
    "version": "1.0.0",
    "trigger": {
        "type": "cron",
        "schedule": "*/5 * * * *"  # Alle 5 Minuten
    },
    "nodes": [
        {
            "id": "get_cluster_health",
            "type": "mcp_call",
            "tool": "get_cluster_health",
            "parameters": {}
        },
        {
            "id": "check_thresholds",
            "type": "function",
            "code": "return health.status === 'healthy'"
        },
        {
            "id": "send_alert",
            "type": "webhook",
            "url": "{{ $env.ALERT_WEBHOOK }}",
            "condition": "{{ $json.check_thresholds === false }}"
        }
    ],
    "connections": [
        {"from": "get_cluster_health", "to": "check_thresholds"},
        {"from": "check_thresholds", "to": "send_alert"}
    ]
}

# Send an n8n
n8n_api.create_workflow(workflow_spec)
```

#### Context-Synchronisation
```python
# Agent OS Context an n8n übergeben
context_sync = {
    "session_id": "agent-os-session-123",
    "correlation_id": "correlation-456",
    "agent_specs": {
        "purpose": "system_monitoring",
        "requirements": ["high_availability", "auto_scaling"],
        "constraints": {"max_cost": 100}
    },
    "metadata": {
        "created_by": "agent-os",
        "timestamp": "2025-11-09T10:00:00Z"
    }
}

n8n_api.set_workflow_context("system_health_check", context_sync)
```

### 2. n8n → MCP (Orchestration → Runtime)

#### Tool-Aufrufe
```python
# n8n Workflow ruft MCP Tool auf
mcp_request = {
    "tool": "get_cluster_health",
    "parameters": {
        "namespace": "default",
        "timeout": 30
    },
    "context": {
        "workflow_id": "system_health_check",
        "execution_id": "exec-789",
        "correlation_id": "correlation-456"
    }
}

# MCP Antwort
mcp_response = {
    "success": True,
    "data": {
        "status": "healthy",
        "nodes": 3,
        "pods": 12,
        "cpu_usage": 45.2,
        "memory_usage": 67.8
    },
    "execution_time": 1.23,
    "context": {
        "tool": "get_cluster_health",
        "correlation_id": "correlation-456"
    }
}
```

#### Event-Streaming
```python
# MCP sendet Events an n8n
event_stream = {
    "type": "kubernetes_event",
    "timestamp": "2025-11-09T10:05:00Z",
    "data": {
        "event_type": "pod_restart",
        "namespace": "default",
        "pod_name": "web-server-xyz",
        "reason": "OOMKilled",
        "severity": "warning"
    },
    "context": {
        "source": "mcp_runtime",
        "correlation_id": "correlation-456"
    }
}

n8n_api.trigger_webhook("kubernetes_events", event_stream)
```

### 3. MCP → Agent OS (Runtime → Design)

#### Performance-Metriken
```python
# MCP sendet Performance-Daten an Agent OS
performance_metrics = {
    "tool": "auto_scale_service",
    "timeframe": "2025-11-09",
    "metrics": {
        "executions": 144,
        "success_rate": 98.6,
        "avg_execution_time": 2.34,
        "errors": [
            {"type": "timeout", "count": 2},
            {"type": "resource_limit", "count": 1}
        ]
    },
    "optimization_suggestions": [
        "Increase timeout threshold",
        "Add resource limits check"
    ]
}

agent_os_api.submit_metrics(performance_metrics)
```

#### Learning-Feedback
```python
# MCP liefert Lern-Daten für Agent OS
learning_feedback = {
    "pattern_type": "auto_scaling_efficiency",
    "observations": [
        {
            "situation": "high_cpu_usage",
            "action": "scale_up",
            "result": "optimal_performance",
            "confidence": 0.92
        }
    ],
    "recommendations": {
        "threshold_adjustments": {
            "cpu_scale_up": 75.0,  # von 80.0
            "cpu_scale_down": 25.0  # von 30.0
        }
    }
}

agent_os_api.submit_learning(learning_feedback)
```

## Standardisierte Datenformate

### Context-Header
```json
{
    "x-correlation-id": "correlation-456",
    "x-session-id": "session-123",
    "x-source-layer": "agent-os|n8n|mcp",
    "x-target-layer": "agent-os|n8n|mcp",
    "x-timestamp": "2025-11-09T10:00:00Z",
    "x-request-id": "req-789"
}
```

### Error-Format
```json
{
    "error": {
        "code": "TOOL_EXECUTION_FAILED",
        "message": "MCP tool auto_scale_service failed",
        "details": {
            "tool": "auto_scale_service",
            "parameters": {"replicas": 5},
            "cause": "insufficient_resources"
        },
        "context": {
            "correlation_id": "correlation-456",
            "layer": "mcp",
            "timestamp": "2025-11-09T10:00:00Z"
        },
        "recovery_actions": [
            "check_resource_quotas",
            "retry_with_lower_replicas"
        ]
    }
}
```

### Event-Format
```json
{
    "event": {
        "id": "evt-123",
        "type": "system_state_change",
        "source": "mcp_runtime",
        "timestamp": "2025-11-09T10:00:00Z",
        "data": {
            "previous_state": "degraded",
            "current_state": "healthy",
            "change_reason": "pod_restart_successful"
        },
        "context": {
            "correlation_id": "correlation-456",
            "affected_resources": ["web-server-pod-xyz"]
        }
    }
}
```

## API-Schnittstellen

### Agent OS API
```python
class AgentOSAPI:
    def create_spec(self, spec_type: str, requirements: dict) -> str:
        """Erstellt neue Spezifikation"""
        pass

    def submit_metrics(self, metrics: dict) -> bool:
        """Reicht Performance-Metriken ein"""
        pass

    def submit_learning(self, feedback: dict) -> bool:
        """Reicht Lern-Feedback ein"""
        pass

    def get_optimization_suggestions(self, context: dict) -> list:
        """Holt Optimierungsvorschläge"""
        pass
```

### n8n API
```python
class N8nAPI:
    def create_workflow(self, workflow_spec: dict) -> str:
        """Erstellt neuen Workflow"""
        pass

    def trigger_workflow(self, workflow_id: str, data: dict) -> str:
        """Triggert Workflow-Ausführung"""
        pass

    def set_workflow_context(self, workflow_id: str, context: dict) -> bool:
        """Setzt Workflow-Kontext"""
        pass

    def trigger_webhook(self, webhook_name: str, data: dict) -> bool:
        """Triggert Webhook"""
        pass
```

### MCP API
```python
class MCPAPI:
    def execute_tool(self, tool_name: str, parameters: dict, context: dict) -> dict:
        """Führt MCP Tool aus"""
        pass

    def subscribe_events(self, event_types: list, callback: callable) -> str:
        """Abonniert Events"""
        pass

    def get_tool_status(self, tool_name: str) -> dict:
        """Holt Tool-Status"""
        pass

    def register_tool(self, tool_spec: dict) -> bool:
        """Registriert neues Tool"""
        pass
```

## Sicherheits- und Authentifizierungsschichten

### 1. Inter-Layer Authentication
```python
# JWT Token für Layer-Kommunikation
layer_token = {
    "iss": "agent-os",
    "sub": "workflow-generator",
    "aud": ["n8n", "mcp"],
    "exp": 1731165600,  # 1 Stunde
    "permissions": [
        "workflow:create",
        "workflow:execute"
    ]
}
```

### 2. Resource Access Control
```python
# RBAC für MCP Tools
rbac_policies = {
    "agent-os": {
        "allowed_tools": ["get_cluster_health", "get_resource_usage"],
        "forbidden_tools": ["delete_namespace", "modify_secrets"]
    },
    "n8n": {
        "allowed_tools": ["*"],  # Alle Tools für Orchestration
        "rate_limits": {
            "get_cluster_health": "10/minute",
            "auto_scale_service": "5/hour"
        }
    }
}
```

## Monitoring und Observability

### 1. Distributed Tracing
```python
# Trace über alle Layer
trace = {
    "trace_id": "trace-123",
    "spans": [
        {
            "layer": "agent-os",
            "operation": "generate_workflow_spec",
            "start_time": "2025-11-09T10:00:00Z",
            "duration_ms": 1500
        },
        {
            "layer": "n8n",
            "operation": "create_workflow",
            "start_time": "2025-11-09T10:00:01.5Z",
            "duration_ms": 800
        },
        {
            "layer": "mcp",
            "operation": "execute_tool",
            "start_time": "2025-11-09T10:00:02.3Z",
            "duration_ms": 1200
        }
    ]
}
```

### 2. Health Checks
```python
# Layer Health Status
health_status = {
    "agent-os": {
        "status": "healthy",
        "last_check": "2025-11-09T10:00:00Z",
        "metrics": {
            "active_agents": 3,
            "queue_size": 12,
            "response_time_ms": 150
        }
    },
    "n8n": {
        "status": "healthy",
        "last_check": "2025-11-09T10:00:00Z",
        "metrics": {
            "active_workflows": 8,
            "executions_per_minute": 45,
            "success_rate": 98.2
        }
    },
    "mcp": {
        "status": "degraded",
        "last_check": "2025-11-09T10:00:00Z",
        "metrics": {
            "available_tools": 12,
            "active_connections": 8,
            "error_rate": 2.1
        },
        "issues": ["High memory usage in kubernetes_client"]
    }
}
```

## Implementierungs-Roadmap

### Phase 1: Grundlegende APIs (2 Wochen)
- [ ] Agent OS API implementieren
- [ ] n8n API Wrapper erstellen
- [ ] MCP API erweitern
- [ ] Basis-Authentifizierung

### Phase 2: Event-Streaming (1 Woche)
- [ ] Event-Bus implementieren
- [ ] Webhook-Integration
- [ ] Event-Filterung und Routing

### Phase 3: Security & Monitoring (1 Woche)
- [ ] JWT Authentication
- [ ] RBAC Policies
- [ ] Distributed Tracing
- [ ] Health Checks

### Phase 4: Optimization & Learning (1 Woche)
- [ ] Performance-Metriken
- [ ] Auto-Optimierung
- [ ] Pattern Recognition
- [ ] Feedback Loops

---

*Erstellt:* 2025-11-09
*Version:* 1.0
*Status:* ✅ Ready for Implementation
