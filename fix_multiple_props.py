#!/usr/bin/env python3
"""
Script pour fusionner plusieurs $props() en un seul
"""
import re
from pathlib import Path

def fix_multiple_props(content: str) -> str:
    """Fusionne plusieurs $props() en un seul"""
    
    # Trouver toutes les lignes avec $props()
    lines = content.split('\n')
    props_lines = []
    props_indices = []
    
    for i, line in enumerate(lines):
        if '$props()' in line and 'let {' in line:
            props_lines.append(line)
            props_indices.append(i)
    
    if len(props_lines) <= 1:
        return content
    
    # Extraire les props de chaque ligne
    all_props = []
    all_types = []
    
    for line in props_lines:
        # Pattern: let { var = default }: { var?: type } = $props();
        match = re.match(r'let\s*\{\s*(\w+)\s*=\s*([^}]+)\s*\}\s*:\s*\{\s*(\w+)\?:\s*([^}]+)\s*\}\s*=\s*\$props\(\);', line)
        if match:
            var_name = match.group(1)
            default_value = match.group(2).strip()
            type_name = match.group(4).strip()
            all_props.append(f"{var_name} = {default_value}")
            all_types.append(f"{var_name}?: {type_name}")
    
    if not all_props:
        return content
    
    # Créer la nouvelle ligne fusionnée
    props_str = ',\n    '.join(all_props)
    types_str = ';\n    '.join(all_types)
    new_line = f"  let {{\n    {props_str}\n  }}: {{\n    {types_str};\n  }} = $props();"
    
    # Remplacer toutes les lignes par la nouvelle
    new_lines = lines[:]
    # Supprimer les anciennes lignes (en ordre inverse pour garder les indices)
    for idx in reversed(props_indices):
        del new_lines[idx]
    
    # Insérer la nouvelle ligne à la position de la première
    new_lines.insert(props_indices[0], new_line)
    
    return '\n'.join(new_lines)

def process_file(file_path: Path):
    """Traite un fichier"""
    try:
        content = file_path.read_text(encoding='utf-8')
        if content.count('$props()') > 1:
            new_content = fix_multiple_props(content)
            if new_content != content:
                file_path.write_text(new_content, encoding='utf-8')
                print(f"✓ Corrigé: {file_path}")
                return True
    except Exception as e:
        print(f"✗ Erreur sur {file_path}: {e}")
    return False

if __name__ == '__main__':
    src_dir = Path('src/routes')
    converted = 0
    
    for svelte_file in src_dir.rglob('*.svelte'):
        if 'svelte-demo' in str(svelte_file):
            continue
        if process_file(svelte_file):
            converted += 1
    
    print(f"\n{converted} fichiers corrigés")


