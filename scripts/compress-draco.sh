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
        ratio=$(echo "scale=1; 100 * ($original_size - $compressed_size) / $original_size" | bc)
        
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

# Compresser un fichier avec options agressives
compress_file_aggressive() {
    local input_file="$1"
    local q_pos="$2"
    local q_norm="$3"
    local q_tex="$4"
    
    local output_file="${input_file%.glb}_draco_aggressive.glb"
    
    print_info "Compression agressive de: $(basename "$input_file")"
    print_info "Avec bits de quantification: POS=$q_pos, NORMAL=$q_norm, TEXCOORD=$q_tex"
    
    # Sauvegarde de l'original
    mkdir -p "$BACKUP_DIR"
    cp "$input_file" "$BACKUP_DIR/"
    
    # Compression
    npx gltf-transform draco "$input_file" "$output_file" \
        --quantize-position "$q_pos" \
        --quantize-normal "$q_norm" \
        --quantize-texcoord "$q_tex"
    
    if [ $? -eq 0 ]; then
        # Comparaison des tailles
        original_size=$(stat -c%s "$input_file")
        compressed_size=$(stat -c%s "$output_file")
        
        original_mb=$(echo "scale=2; $original_size / 1048576" | bc)
        compressed_mb=$(echo "scale=2; $compressed_size / 1048576" | bc)
        ratio=$(echo "scale=1; 100 * ($original_size - $compressed_size) / $original_size" | bc)
        
        print_success "Compression réussie!"
        echo "  Original:  ${original_mb} MB"
        echo "  Compressé: ${compressed_mb} MB"
        echo "  Ratio:     ${ratio}%"
        
        # Remplacer l'original par le compressé
        mv "$output_file" "$input_file"
        print_info "Fichier original remplacé"
    else
        print_error "Échec de la compression agressive"
        return 1
    fi
}

# Optimiser les textures (redimensionner + compresser)
optimize_textures() {
    local input_file="$1"
    local resolution="$2"
    
    local resized_file="${input_file%.glb}_resized.glb"
    local webp_file="${input_file%.glb}_webp.glb"
    
    print_info "Optimisation des textures pour: $(basename "$input_file")"
    print_info "Résolution cible: ${resolution}x${resolution}"
    
    # Sauvegarde de l'original
    mkdir -p "$BACKUP_DIR"
    cp "$input_file" "$BACKUP_DIR/"
    
    # 1. Redimensionner
    print_info "Étape 1/2: Redimensionnement des textures..."
    npx gltf-transform resize "$input_file" "$resized_file" --width "$resolution" --height "$resolution"
    
    if [ $? -ne 0 ]; then
        print_error "Échec du redimensionnement des textures."
        rm "$resized_file" &> /dev/null
        return 1
    fi
    
    # 2. Compresser en WebP
    print_info "Étape 2/2: Compression des textures en WebP..."
    npx gltf-transform webp "$resized_file" "$webp_file"
    
    if [ $? -ne 0 ]; then
        print_error "Échec de la compression WebP."
        rm "$resized_file" "$webp_file" &> /dev/null
        return 1
    fi
    
    # Nettoyage du fichier intermédiaire
    rm "$resized_file"
    
    # Comparaison des tailles
    original_size=$(stat -c%s "$input_file")
    compressed_size=$(stat -c%s "$webp_file")
    
    original_mb=$(echo "scale=2; $original_size / 1048576" | bc)
    compressed_mb=$(echo "scale=2; $compressed_size / 1048576" | bc)
    ratio=$(echo "scale=1; 100 * ($original_size - $compressed_size) / $original_size" | bc)
    
    print_success "Optimisation des textures réussie!"
    echo "  Original:  ${original_mb} MB"
    echo "  Optimisé:  ${compressed_mb} MB"
    echo "  Ratio:     ${ratio}%"
    
    # Remplacer l'original par le fichier optimisé
    mv "$webp_file" "$input_file"
    print_info "Fichier original remplacé"
}

# Menu principal
main() {
    echo "========================================"
    echo "  OUTIL DE COMPRESSION DRACO LOCAL"
    echo "========================================"
    
    check_dependencies
    
    echo ""
    echo "Options:"
    echo "  1) Compresser tout le dossier public/ (Normal)"
    echo "  2) Compresser un fichier spécifique (Normal)"
    echo "  3) Compresser un fichier (compression géométrie agressive)"
    echo "  4) Optimiser les textures (redimensionner + compresser)"
    echo "  5) Quitter"
    echo ""
    
    read -r "choice?Choisissez une option (1-5): "
    
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
            read -r "filepath?Chemin du fichier GLB: "
            # Remove surrounding quotes if present
            filepath="${filepath%\"}"
            filepath="${filepath#\"}"
            filepath="${filepath%\'}"
            filepath="${filepath#\'}"
            if [ -f "$filepath" ]; then
                read -r "q_pos?Bits pour POSITION (défaut 10): "
                q_pos=${q_pos:-10}
                read -r "q_norm?Bits pour NORMAL (défaut 8): "
                q_norm=${q_norm:-8}
                read -r "q_tex?Bits pour TEXCOORD (défaut 8): "
                q_tex=${q_tex:-8}
                
                compress_file_aggressive "$filepath" "$q_pos" "$q_norm" "$q_tex"
            else
                print_error "Fichier non trouvé: $filepath"
            fi
            ;;
        4)
            read -r "filepath?Chemin du fichier GLB: "
            # Remove surrounding quotes if present
            filepath="${filepath%\"}"
            filepath="${filepath#\"}"
            filepath="${filepath%\'}"
            filepath="${filepath#\'}"
            if [ -f "$filepath" ]; then
                read -r "resolution?Résolution cible pour les textures (défaut 1024): "
                resolution=${resolution:-1024}
                optimize_textures "$filepath" "$resolution"
            else
                print_error "Fichier non trouvé: $filepath"
            fi
            ;;
        5)
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
