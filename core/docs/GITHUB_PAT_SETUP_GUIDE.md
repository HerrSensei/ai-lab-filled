# 🔐 GitHub PAT Setup - Interactive Guide

## 🚀 Jetzt verfügbar: Vollautomatisches Setup Script!

Das neue `setup_github_pat.sh` Script führt dich Schritt für Schritt durch den gesamten sicheren Setup-Prozess:

### 📋 Was das Script für dich tut:

**🔍 Schritt 0: Voraussetzungen prüfen**
- curl Verfügbarkeit testen
- macOS Keychain erkennen
- Projektverzeichnis validieren

**🌐 Schritt 1: GitHub Token erstellen**
- Öffnet automatisch die GitHub Token-Seite
- Zeigt detaillierte Anweisungen für Berechtigungen
- Warnt vor einmaliger Token-Anzeige

**📝 Schritt 2: Token Informationen sammeln**
- Sicherer Token-Eingabe (versteckt)
- Repository-Format-Validierung
- Längen-Prüfungen

**🔒 Schritt 3: Speicher-Methode wählen**
- **macOS Keychain** (sicherste Methode)
- **.env Datei** (Produktions-ready)
- **Environment Variable** (temporär)

**✅ Schritt 4: Token testen**
- GitHub API Authentifizierung
- Repository-Zugriff prüfen
- Berechtigungen validieren

**🛡️ Schritt 5: Sicherheits-Check**
- Automatischer Security Scan
- .gitignore Prüfung
- Hardcoded-Token-Erkennung

**⚙️ Schritt 6: GitHub Integration einrichten**
- Repository Labels erstellen
- Project Board vorbereiten
- Sync-Funktionalität testen

**🎯 Schritt 7: Nächste Schritte**
- Persönliche Anleitungen
- Nützliche Commands
- Sicherheitshinweise

## 🚀 Einfach starten:

```bash
cd /pfad/zum/ai-lab-framework
./scripts/setup_github_pat.sh
```

## 🎨 Features des Scripts:

### ✨ **User Experience**
- **Farbliche Ausgaben** für bessere Lesbarkeit
- **Schritt-für-Schritt** Anleitungen
- **Automatische Browser-Öffnung**
- **Sichere Passwort-Eingabe** (versteckt)

### 🔒 **Security First**
- **Minimale Berechtigungen** vorausgewählt
- **Automatische .gitignore** Updates
- **Sichere Dateiberechtigungen** (chmod 600)
- **Token-Rotation** Erinnerungen

### 🛠️ **Smart Detection**
- **Betriebssystem-Erkennung** (macOS/Linux)
- **Tool-Verfügbarkeit** prüfen
- **Projekt-Struktur** validierung
- **Fehlerbehandlung** mit Hinweisen

### 🎯 **Methoden im Detail**

#### **macOS Keychain (Empfohlen)**
```bash
# Automatisch gespeichert
security add-generic-password -a "$(whoami)" -s "github-token" -w "$TOKEN"

# Automatisch geladen
export GITHUB_TOKEN=$(security find-generic-password -a "$(whoami)" -s "github-token" -w)
```

#### **.env Datei (Produktion)**
```bash
# Automatisch erstellt mit sicheren Berechtigungen
chmod 600 .env

# Automatisch zu .gitignore hinzugefügt
echo ".env" >> .gitignore
```

#### **Environment Variable (Temporär)**
```bash
# Nur für aktuelle Sitzung
export GITHUB_TOKEN="$TOKEN"
export GITHUB_REPO="$owner/repo"
```

## 🎉 Ergebnis nach dem Setup:

**✅ Sicherheit validiert**
- Token hat richtige Berechtigungen
- Repository-Zugriff bestätigt
- .gitignore konfiguriert

**✅ GitHub bereit**
- Labels erstellt
- Project Board vorbereitet
- Sync getestet

**✅ Nächste Schritte klar**
- Persönliche Commands
- Security Check verfügbar
- Dashboard Integration

## 🔧 Manuelles Backup:

Falls das Script mal nicht funktioniert, hier die manuellen Schritte:

```bash
# 1. Token erstellen
open https://github.com/settings/tokens

# 2. Environment setzen
export GITHUB_TOKEN="dein_token"
export GITHUB_REPO="owner/repo"

# 3. Security Check
python scripts/github_pat_security.py --check

# 4. GitHub Setup
python src/ai_lab_framework/github_integration.py --action setup
```

---

**🚀 Bereit für den sicheren Setup? Einfach `./scripts/setup_github_pat.sh` ausführen!**