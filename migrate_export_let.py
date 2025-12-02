#!/usr/bin/env python3
"""
Script pour convertir automatiquement export let en $props() pour Svelte 5 runes
"""
import re
import sys
from pathlib import Path

def convert_export_let_to_props(content: str) -> str:
    """Convertit export let en syntaxe runes $props()"""
    
    # Pattern pour capturer: export let variable: type = defaultValue;
    # ou export let variable = defaultValue;
    pattern = r'export\s+let\s+(\w+)(?:\s*:\s*([^=]+))?\s*(?:=\s*([^;]+))?;'
    
    def replace_export(match):
        var_name = match.group(1)
        var_type = match.group(2).strip() if match.group(2) else None
        default_value = match.group(3).strip() if match.group(3) else None
        
        # Construire la nouvelle syntaxe
        if var_type and default_value:
            return f"let {{ {var_name} = {default_value} }}: {{ {var_name}?: {var_type} }} = $props();"
        elif default_value:
            return f"let {{ {var_name} = {default_value} }} = $props();"
        elif var_type:
            return f"let {{ {var_name} }}: {{ {var_name}: {var_type} }} = $props();"
        else:
            return f"let {{ {var_name} }} = $props();"
    
    # Remplacer tous les export let
    new_content = re.sub(pattern, replace_export, content)
    
    # Si on a trouvé des export let, ajouter $props() au début du script si pas déjà présent
    if 'export let' in content and '$props()' not in content.split('<script')[1].split('</script>')[0]:
        # Chercher la position après <script
        script_match = re.search(r'<script[^>]*>', new_content)
        if script_match:
            script_end = script_match.end()
            # Vérifier si $props est déjà importé/utilisé
            script_section = new_content[script_end:].split('</script>')[0]
            if '$props' not in script_section:
                # Ajouter après les imports si possible
                imports_end = re.search(r'(import[^;]+;[\s\n]*)+', script_section)
                if imports_end:
                    insert_pos = script_end + imports_end.end()
                    new_content = new_content[:insert_pos] + '\n\n  // Props en mode runes\n' + new_content[insert_pos:]
    
    return new_content

def process_file(file_path: Path):
    """Traite un fichier Svelte"""
    try:
        content = file_path.read_text(encoding='utf-8')
        if 'export let' in content:
            new_content = convert_export_let_to_props(content)
            if new_content != content:
                file_path.write_text(new_content, encoding='utf-8')
                print(f"✓ Converti: {file_path}")
                return True
    except Exception as e:
        print(f"✗ Erreur sur {file_path}: {e}")
    return False

if __name__ == '__main__':
    src_dir = Path('src/routes')
    if not src_dir.exists():
        print(f"Erreur: {src_dir} n'existe pas")
        sys.exit(1)
    
    converted = 0
    for svelte_file in src_dir.rglob('*.svelte'):
        if 'svelte-demo' in str(svelte_file):
            continue
        if process_file(svelte_file):
            converted += 1
    
    print(f"\n{converted} fichiers convertis")


