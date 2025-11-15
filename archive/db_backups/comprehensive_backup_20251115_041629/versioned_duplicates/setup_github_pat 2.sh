#!/bin/bash
# GitHub PAT Setup Script - Interactive Security Setup
# Führt dich Schritt für Schritt durch den sicheren Setup-Prozess

set -e

# Farben für bessere UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Hilfsfunktionen
print_header() {
    echo -e "${BLUE}🔐 GitHub Personal Access Token - Secure Setup${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_step() {
    echo -e "${PURPLE}📋 STEP $1: $2${NC}"
    echo -e "${PURPLE}----------------------------------------${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

check_prerequisites() {
    print_step "0" "Voraussetzungen prüfen"
    
    # Check if curl is available
    if ! command -v curl &> /dev/null; then
        print_error "curl ist nicht installiert. Bitte installiere curl zuerst."
        exit 1
    fi
    print_success "curl ist verfügbar"
    
    # Check if security command is available (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command -v security &> /dev/null; then
            print_warning "security command nicht gefunden (macOS Keychain nicht verfügbar)"
            USE_KEYCHAIN=false
        else
            print_success "macOS Keychain verfügbar"
            USE_KEYCHAIN=true
        fi
    else
        print_warning "Kein macOS erkannt, verwende .env Methode"
        USE_KEYCHAIN=false
    fi
    
    # Check if we're in the right directory
    if [[ ! -f "pyproject.toml" ]] && [[ ! -d "src/ai_lab_framework" ]]; then
        print_error "Nicht im AI Lab Framework Verzeichnis. Bitte navigiere zum Projektverzeichnis."
        exit 1
    fi
    print_success "Im richtigen Projektverzeichnis"
    
    echo ""
}

create_github_token() {
    print_step "1" "GitHub Token erstellen"
    
    echo "Ich öffne jetzt die GitHub Token-Erstellungsseite für dich..."
    echo ""
    print_info "Folge diesen Anweisungen auf der GitHub Seite:"
    echo "1. Klicke auf 'Generate new token (classic)'"
    echo "2. Token Name: 'AI Lab Framework Integration'"
    echo "3. Expiration: Wähle '30 days' oder 'Custom dates'"
    echo "4. Berechtigungen (nur diese auswählen):"
    echo "   ✅ repo - Full control of private repositories"
    echo "   ✅ issues - Read and write"
    echo "   ✅ projects - Read and write"
    echo "   ✅ labels - Read and write"
    echo "   ❌ Alle anderen deaktivieren lassen"
    echo ""
    read -p "Drücke ENTER um die GitHub Seite zu öffnen..."
    
    # Open GitHub token page
    if command -v open &> /dev/null; then
        open "https://github.com/settings/tokens"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "https://github.com/settings/tokens"
    else
        echo "Öffne manuell: https://github.com/settings/tokens"
    fi
    
    echo ""
    print_warning "⚠️  WICHTIG: Der Token wird NUR EINMAL angezeigt!"
    echo "   Kopiere ihn sofort und füge ihn im nächsten Schritt ein."
    echo ""
}

collect_token_info() {
    print_step "2" "Token Informationen sammeln"
    
    # Get the token
    echo ""
    read -s -p "🔑 Füge deinen GitHub Personal Access Token hier ein: " GITHUB_TOKEN
    echo ""
    
    if [[ -z "$GITHUB_TOKEN" ]]; then
        print_error "Token wurde nicht eingegeben. Bitte versuche es erneut."
        exit 1
    fi
    
    if [[ ${#GITHUB_TOKEN} -lt 20 ]]; then
        print_error "Token scheint zu kurz zu sein. Bitte überprüfe den Token."
        exit 1
    fi
    
    print_success "Token wurde eingegeben (Länge: ${#GITHUB_TOKEN})"
    
    # Get repository
    echo ""
    read -p "📂 GitHub Repository (owner/repo): " GITHUB_REPO
    
    if [[ -z "$GITHUB_REPO" ]]; then
        print_error "Repository wurde nicht eingegeben."
        exit 1
    fi
    
    if [[ ! "$GITHUB_REPO" =~ ^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$ ]]; then
        print_error "Repository Format sollte 'owner/repo' sein."
        exit 1
    fi
    
    print_success "Repository: $GITHUB_REPO"
    echo ""
}

choose_storage_method() {
    print_step "3" "Speicher-Methode wählen"
    
    if [[ "$USE_KEYCHAIN" == true ]]; then
        echo "Wähle die Speicher-Methode für deinen Token:"
        echo "1) macOS Keychain (Empfohlen - Sicherste Methode)"
        echo "2) .env Datei (Gut für Produktion)"
        echo "3) Environment Variable (Temporär)"
        echo ""
        
        while true; do
            read -p "Wähle eine Option [1-3]: " choice
            case $choice in
                1)
                    store_in_keychain
                    break
                    ;;
                2)
                    store_in_env_file
                    break
                    ;;
                3)
                    store_in_environment
                    break
                    ;;
                *)
                    print_error "Ungültige Wahl. Bitte wähle 1, 2 oder 3."
                    ;;
            esac
        done
    else
        echo "macOS Keychain nicht verfügbar. Wähle alternative Methode:"
        echo "1) .env Datei (Empfohlen)"
        echo "2) Environment Variable (Temporär)"
        echo ""
        
        while true; do
            read -p "Wähle eine Option [1-2]: " choice
            case $choice in
                1)
                    store_in_env_file
                    break
                    ;;
                2)
                    store_in_environment
                    break
                    ;;
                *)
                    print_error "Ungültige Wahl. Bitte wähle 1 oder 2."
                    ;;
            esac
        done
    fi
}

store_in_keychain() {
    print_info "Speichere Token in macOS Keychain..."
    
    # Store token in keychain
    if security add-generic-password -a "$(whoami)" -s "github-token" -w "$GITHUB_TOKEN" 2>/dev/null; then
        print_success "Token sicher in macOS Keychain gespeichert"
        
        # Store repository in keychain
        if security add-generic-password -a "$(whoami)" -s "github-repo" -w "$GITHUB_REPO" 2>/dev/null; then
            print_success "Repository in macOS Keychain gespeichert"
        else
            print_warning "Konnte Repository nicht speichern, verwende Environment Variable"
            export GITHUB_REPO="$GITHUB_REPO"
        fi
        
        # Create helper script for loading
        cat > load_github_env.sh << 'EOF'
#!/bin/bash
# Load GitHub credentials from macOS Keychain
export GITHUB_TOKEN=$(security find-generic-password -a "$(whoami)" -s "github-token" -w 2>/dev/null)
export GITHUB_REPO=$(security find-generic-password -a "$(whoami)" -s "github-repo" -w 2>/dev/null || echo "")
EOF
        chmod +x load_github_env.sh
        print_success "Hilfs-Script 'load_github_env.sh' erstellt"
        
        STORAGE_METHOD="keychain"
    else
        print_error "Konnte Token nicht in Keychain speichern. Fallback zu .env Methode."
        store_in_env_file
    fi
}

store_in_env_file() {
    print_info "Erstelle sichere .env Datei..."
    
    # Create .env file
    cat > .env << EOF
# GitHub Personal Access Token
GITHUB_TOKEN=$GITHUB_TOKEN

# GitHub Repository (owner/repo)
GITHUB_REPO=$GITHUB_REPO

# Sicherheitshinweise:
# 1. Diese Datei nicht teilen oder committen
# 2. Token regelmäßig rotieren (alle 30 Tage)
# 3. Bei Verdacht auf Kompromittierung sofort widerrufen
EOF
    
    # Set secure permissions
    chmod 600 .env
    
    print_success ".env Datei erstellt mit sicheren Berechtigungen (600)"
    
    # Verify .env is in .gitignore
    if ! grep -q "^\.env$" .gitignore; then
        echo "" >> .gitignore
        echo "# GitHub PAT Security" >> .gitignore
        echo ".env" >> .gitignore
        print_success ".env zu .gitignore hinzugefügt"
    fi
    
    STORAGE_METHOD="env_file"
}

store_in_environment() {
    print_warning "Environment Variable Methode (nicht persistent)"
    print_info "Token wird nur für aktuelle Sitzung geladen..."
    
    export GITHUB_TOKEN="$GITHUB_TOKEN"
    export GITHUB_REPO="$GITHUB_REPO"
    
    print_success "Token in Environment Variablen geladen"
    print_warning "⚠️  Diese Methode ist nicht persistent nach Neustart!"
    
    STORAGE_METHOD="environment"
}

test_token() {
    print_step "4" "Token testen"
    
    print_info "Teste GitHub API Verbindung..."
    
    # Test authentication
    response=$(curl -s -w "%{http_code}" -o /tmp/github_user.json \
        -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/user")
    
    if [[ "$response" == "200" ]]; then
        username=$(cat /tmp/github_user.json | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
        print_success "Authentifizierung erfolgreich als: $username"
    else
        print_error "Authentifizierung fehlgeschlagen (HTTP $response)"
        print_error "Bitte überprüfe deinen Token und Berechtigungen."
        exit 1
    fi
    
    # Test repository access
    response=$(curl -s -w "%{http_code}" \
        -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_REPO")
    
    if [[ "$response" == "200" ]]; then
        print_success "Repository-Zugriff bestätigt: $GITHUB_REPO"
    else
        print_error "Kein Zugriff auf Repository $GITHUB_REPO (HTTP $response)"
        print_error "Bitte überprüfe Repository-Namen und Berechtigungen."
        exit 1
    fi
    
    # Clean up
    rm -f /tmp/github_user.json
    
    echo ""
}

run_security_check() {
    print_step "5" "Sicherheits-Check durchführen"
    
    if [[ -f "scripts/github_pat_security.py" ]]; then
        if [[ -f "venv/bin/activate" ]]; then
            source venv/bin/activate
            python scripts/github_pat_security.py --check
        else
            print_warning "Virtuelle Umgebung nicht gefunden, überspringe Security Check"
        fi
    else
        print_warning "Security Check Script nicht gefunden"
    fi
    
    echo ""
}

setup_github_integration() {
    print_step "6" "GitHub Integration einrichten"
    
    print_info "Richte GitHub Repository Labels ein..."
    
    if [[ -f "src/ai_lab_framework/github_integration.py" ]]; then
        if [[ -f "venv/bin/activate" ]]; then
            source venv/bin/activate
            python src/ai_lab_framework/github_integration.py --action setup
            print_success "GitHub Repository Labels eingerichtet"
        else
            print_warning "Virtuelle Umgebung nicht gefunden, überspringe GitHub Setup"
        fi
    else
        print_warning "GitHub Integration Script nicht gefunden"
    fi
    
    echo ""
}

show_next_steps() {
    print_step "7" "Nächste Schritte"
    
    echo "🎉 Setup abgeschlossen! Hier sind deine nächsten Schritte:"
    echo ""
    
    case $STORAGE_METHOD in
        "keychain")
            echo "1️⃣  Token laden (bei jeder neuen Sitzung):"
            echo "   source load_github_env.sh"
            echo ""
            echo "2️⃣  GitHub Integration starten:"
            echo "   source venv/bin/activate"
            echo "   python src/ai_lab_framework/github_integration.py --action sync-all"
            ;;
        "env_file")
            echo "1️⃣  Token laden (bei jeder neuen Sitzung):"
            echo "   export \$(grep -v '^#' .env | xargs)"
            echo ""
            echo "2️⃣  GitHub Integration starten:"
            echo "   source venv/bin/activate"
            echo "   python src/ai_lab_framework/github_integration.py --action sync-all"
            ;;
        "environment")
            echo "1️⃣  GitHub Integration starten (Token ist bereits geladen):"
            echo "   source venv/bin/activate"
            echo "   python src/ai_lab_framework/github_integration.py --action sync-all"
            ;;
    esac
    
    echo ""
    echo "📚 Nützliche Commands:"
    echo "   • Security Check: python scripts/github_pat_security.py --check"
    echo "   • Dashboard: python dashboard/dashboard_generator_sqlite.py"
    echo "   • Ideas auflisten: python scripts/list_ideas_sqlite.py --stats"
    echo ""
    echo "🔐 Sicherheitshinweise:"
    echo "   • Rotiere den Token alle 30 Tage"
    echo "   • Überwache GitHub Aktivität"
    echo "   • Teile den Token mit niemandem"
    echo ""
    
    print_success "Setup erfolgreich abgeschlossen! 🚀"
}

# Hauptprogramm
main() {
    print_header
    
    check_prerequisites
    create_github_token
    collect_token_info
    choose_storage_method
    test_token
    run_security_check
    setup_github_integration
    show_next_steps
}

# Script ausführen
main "$@"