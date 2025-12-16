#!/bin/zsh

# Configuration
GLTF_TRANSFORM="npx gltf-transform"
PUBLIC_DIR="./static/public"
BACKUP_DIR="${PUBLIC_DIR}/backup_$(date +%Y%m%d_%H%M%S)"

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_info() {
    echo "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo "${RED}[ERROR]${NC} $1"
}

# Vérifier si gltf-transform est installé
check_dependencies() {
    if ! command -v bc &> /dev/null; then
        print_error "La calculatrice 'bc' n'est pas installée. Veuillez l'installer (ex: sudo apt-get install bc)."
        exit 1
    fi

    if ! command -v pnpm &> /dev/null; then
        print_error "pnpm n'est pas installé. Veuillez l'installer."
        exit 1
    fi
    
    if ! npx gltf-transform --version &> /dev/null; then
        print_warning "gltf-transform n'est pas installé. Installation avec pnpm..."
        pnpm add --save-dev @gltf-transform/cli
    fi
}

# Compresser un fichier individuel
compress_file() {
    local input_file="$1"
    local output_file="$2"
    
    if [ -z "$output_file" ]; then
        output_file="${input_file%.glb}_draco.glb"
    fi
    
    print_info "Compression de: $(basename "$input_file")"
    
    # Sauvegarde de l'original
    mkdir -p "$BACKUP_DIR"
    cp "$input_file" "$BACKUP_DIR/"
    
    # Compression
    npx gltf-transform draco "$input_file" "$output_file"
    
    if [ $? -eq 0 ]; then
        # Comparaison des tailles
        original_size=$(stat -c%s "$input_file")
        compressed_size=$(stat -c%s "$output_file")
        
        original_mb=$(echo "scale=2; $original_size / 1048576" | bc)
        compressed_mb=$(echo "scale=2; $compressed_size / 1048576" | bc)
        ratio=$(echo "scale=1; (1 - $compressed_size / $original_size) * 100" | bc)
        
        print_success "Compression réussie!"
        echo "  Original:  ${original_mb} MB"
        echo "  Compressé: ${compressed_mb} MB"
        echo "  Ratio:     ${ratio}%"
        
        # Remplacer l'original par le compressé
        mv "$output_file" "$input_file"
        print_info "Fichier original remplacé"
    else
        print_error "Échec de la compression"
        return 1
    fi
}

# Compresser tous les fichiers d'un dossier
compress_folder() {
    local folder="$1"
    
    print_info "Scan du dossier: $folder"
    
    # Trouver tous les fichiers GLB (sauf ceux déjà compressés)
    files=($folder/*.glb(N))
    
    if [ ${#files[@]} -eq 0 ]; then
        print_warning "Aucun fichier .glb trouvé"
        return
    fi
    
    print_info "${#files[@]} fichiers GLB trouvés"
    
    for file in "${files[@]}"; do
        if [[ ! "$file" =~ "_draco" ]]; then
            compress_file "$file"
            echo "─"*$(tput cols)
        fi
    done
    
    print_success "Tous les fichiers ont été compressés!"
    print_info "Backups disponibles dans: $BACKUP_DIR"
}

# Menu principal
main() {
    echo "========================================"
    echo "  OUTIL DE COMPRESSION DRACO LOCAL"
    echo "========================================"
    
    check_dependencies
    
    echo ""
    echo "Options:"
    echo "  1) Compresser tout le dossier public/"
    echo "  2) Compresser un fichier spécifique"
    echo "  3) Quitter"
    echo ""
    
    read -r "choice?Choisissez une option (1-3): "
    
    case $choice in
        1)
            compress_folder "$PUBLIC_DIR"
            ;;
        2)
            read -r "filepath?Chemin du fichier GLB: "
            # Remove surrounding quotes if present
            filepath="${filepath%\"}"
            filepath="${filepath#\"}"
            filepath="${filepath%\'}"
            filepath="${filepath#\'}"
            if [ -f "$filepath" ]; then
                compress_file "$filepath"
            else
                print_error "Fichier non trouvé: $filepath"
            fi
            ;;
        3)
            print_info "Au revoir!"
            exit 0
            ;;
        *)
            print_error "Option invalide"
            ;;
    esac
}

# Lancer le script
main "$@"
