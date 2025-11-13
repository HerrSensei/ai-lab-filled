# Projekt-Vision: Das Autonome Lebens-Betriebssystem

## 1. Leitsatz: Unsere Vision

Wir erschaffen ein intelligentes, sich selbst verwaltendes digitales Ökosystem, das den Alltag proaktiv vereinfacht, die volle Kontrolle über die eigenen Daten sicherstellt und als dynamische Plattform für kontinuierliches Lernen und Experimentieren im Bereich der künstlichen Intelligenz dient.

**Das Ziel ist nicht, die Technologie zu verwalten. Das Ziel ist, dass die Technologie unser Leben verwaltet – unsichtbar, proaktiv und intelligent.**

---

## 2. Die Drei Säulen der Vision

Unsere Vision ruht auf drei fundamentalen Säulen, die das technische Fundament in greifbare Ziele verwandeln.

### Vision I: Die Unsichtbare Infrastruktur
*   **Das Ziel:** Die gesamte technische Infrastruktur – vom Homeserver bis zum VPS – läuft autonom, ist resilient und heilt sich selbst. Manuelle Eingriffe werden zur absoluten Ausnahme. Das System wird zu einer verlässlichen, unsichtbaren Grundlage.
*   **Die Umsetzung:**
    *   **Orchestrierung mit Kubernetes (k3s):** Alle Dienste laufen als Container in einem einheitlichen Cluster, der sich über den Homeserver und den VPS erstreckt.
    *   **Automatisierung mit GitOps (Argo CD / FluxCD):** Jede Änderung – ein neuer Dienst, ein Update, eine Konfigurationsanpassung – wird in einem Git-Repository deklariert. Das System setzt den gewünschten Zustand automatisch um. **Git ist die einzige Quelle der Wahrheit.**

### Vision II: Der Proaktive Digitale Assistent
*   **Das Ziel:** Ein KI-Agent, der nicht auf Befehle wartet, sondern als proaktiver digitaler Butler agiert. Er überwacht die Systeme, antizipiert Bedürfnisse, führt komplexe Aufgaben aus und automatisiert das Management des gesamten Ökosystems.
*   **Die Umsetzung (Hybrid-Architektur):**
    *   **Design Layer (Agent OS):** Strukturierte Entwicklung und Verwaltung von Agent-Tasks und Context. Spec-driven Development für konsistente Agent-Verhaltensweisen und lernende Systeme.
    *   **Orchestration Layer (n8n):** Visuelle Workflow-Orchestrierung für komplexe Prozess-Ketten, Fehlerbehandlung und Business-Logik. Flexible Steuerung von Lebensprozessen und System-Interaktionen.
    *   **Runtime Control Layer (MCP):** Standardisierte, sichere Anbindung an Kubernetes-Cluster und externe Systeme. Tool-Discovery und Runtime-Operationen mit voller Audit-Fähigkeit.
    *   **Das Gehirn (Ollama & ai-lab):** Der im `ai-lab` entwickelte Agent nutzt lokale Sprachmodelle via Ollama, um zu planen, zu entscheiden und zu kommunizieren.
    *   **Die Hände (Hybrid-Stack):** Der Agent steuert über MCP den Kubernetes-Cluster, startet n8n-Workflows zur Automatisierung von Lebensprozessen, verwaltet Home Assistant und führt Wartungsaufgaben aus.

### Vision III: Die Souveräne Private Cloud
*   **Das Ziel:** Die vollständige Souveränität und Kontrolle über die eigenen digitalen Daten. Wir schaffen ein privates, sicheres und absolut verlässliches Zuhause für Fotos, Dokumente, Backups und persönliche Dienste – unabhängig von den großen Tech-Konzernen.
*   **Hinweis:** Diese Vision beschreibt ein **eigenständiges Projekt**, das eng mit dem AI Lab Framework zusammenarbeitet, aber nicht direkt Teil seiner Kernfunktionalität ist. Das AI Lab Framework bietet die Werkzeuge und die Intelligenz, um solche privaten Cloud-Infrastrukturen zu verwalten und zu automatisieren.
*   **Die Umsetzung:**
    *   **Sichere Dienste:** Alle privaten Dienste (z.B. `Immich` für Fotos, `Calibre-Web` für Bücher, File-Sync) laufen gekapselt im eigenen Kubernetes-Cluster.
    *   **Absolute Datensicherheit (3-2-1-Regel):** Eine kompromisslose Backup-Strategie mit `Kopia` oder `restic` sorgt dafür, dass Daten niemals verloren gehen – mit lokalen und verschlüsselten externen Kopien.
    *   **Geschützte Privatsphäre:** `AdGuard` blockiert unerwünschte Inhalte auf Netzwerkebene, während `Tailscale` einen sicheren, privaten Tunnel zu allen Diensten von überall auf der Welt schafft.

---

## 3. Die Roadmap zur Vision

Der Weg zu diesem Ziel ist ein iterativer Prozess, den wir in vier Phasen gliedern:

*   **Phase 1: Das Fundament legen**
    *   Netzwerk-Stabilität sicherstellen (Tailscale SSH).
    *   Einen ersten `k3s` Kubernetes-Cluster auf dem Homeserver aufsetzen.
    *   Einen ersten Dienst (z.B. AdGuard) testweise auf Kubernetes deployen.

*   **Phase 2: Die Automatisierung etablieren**
    *   GitOps mit Argo CD / FluxCD einführen.
    *   Alle bestehenden Dienste (n8n, Ollama, Immich etc.) schrittweise nach Kubernetes migrieren.
    *   Den VPS ebenfalls als k3s-Node einbinden.

*   **Phase 3: Die Intelligenz erschaffen (Hybrid-Architektur)**
    *   **Agent OS Integration:** Spec-driven Development für Agent-Tasks und Context-Management etablieren.
    *   **MCP Server Entwicklung:** Kubernetes-Steuerung via Model Context Protocol implementieren.
    *   **n8n Workflow Orchestrierung:** Visuelle Prozess-Ketten für System-Management und Lebensautomatisierung aufbauen.
    *   **3-Schichten-Integration:** Agent OS → n8n → MCP → Kubernetes für vollautomatisierte System-Verwaltung.
    *   Den "Autonomous Homelab Management" Workflow als ersten großen Anwendungsfall der Hybrid-Architektur umsetzen.

*   **Phase 4: Konsolidieren & Absichern**
    *   Die 3-2-1-Backup-Strategie vollständig implementieren.
    *   Das System-Monitoring und die Selbstheilungsfähigkeiten des Agenten verfeinern.
