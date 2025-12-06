#!/usr/bin/env python3
"""
Script pour convertir automatiquement $: en $effect ou $derived
"""
import re
from pathlib import Path

def convert_reactive_statements(content: str) -> str:
    """Convertit $: en $effect ou $derived selon le contexte"""
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Pattern pour $: variable = expression (dérivé)
        if re.match(r'^\s*\$:\s*(\w+)\s*=\s*(.+)$', line):
            match = re.match(r'^\s*\$:\s*(\w+)\s*=\s*(.+)$', line)
            var_name = match.group(1)
            expression = match.group(2).rstrip(';')
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + f"let {var_name} = $derived({expression});")
            i += 1
            continue
        
        # Pattern pour $: { bloc } (effect)
        if re.match(r'^\s*\$:\s*\{', line):
            indent = len(line) - len(line.lstrip())
            # Trouver la fin du bloc
            brace_count = 1
            block_lines = [line]
            j = i + 1
            while j < len(lines) and brace_count > 0:
                block_lines.append(lines[j])
                brace_count += lines[j].count('{') - lines[j].count('}')
                j += 1
            
            # Extraire le contenu du bloc
            block_content = '\n'.join(block_lines)
            block_match = re.match(r'^\s*\$:\s*\{(.+)\}\s*$', block_content, re.DOTALL)
            if block_match:
                inner_content = block_match.group(1).strip()
                new_lines.append(' ' * indent + f"$effect(() => {{")
                new_lines.append(' ' * (indent + 2) + inner_content)
                new_lines.append(' ' * indent + f"}});")
            else:
                # Fallback: convertir en $effect simple
                inner_content = '\n'.join([l[4:] if l.startswith('    ') else l for l in block_lines[1:-1]])
                new_lines.append(' ' * indent + f"$effect(() => {{")
                new_lines.append(inner_content)
                new_lines.append(' ' * indent + f"}});")
            i = j
            continue
        
        # Pattern pour $: if (condition) { ... } (effect)
        if re.match(r'^\s*\$:\s*if\s*\(', line):
            indent = len(line) - len(line.lstrip())
            # Trouver la fin du bloc if
            block_lines = [line]
            j = i + 1
            brace_count = line.count('{') - line.count('}')
            while j < len(lines) and brace_count > 0:
                block_lines.append(lines[j])
                brace_count += lines[j].count('{') - lines[j].count('}')
                j += 1
            
            # Reconstruire en $effect
            block_content = '\n'.join(block_lines)
            if_match = re.match(r'^\s*\$:\s*(if\s*\([^)]+\)\s*\{.+\})\s*$', block_content, re.DOTALL)
            if if_match:
                if_statement = if_match.group(1)
                new_lines.append(' ' * indent + f"$effect(() => {{")
                new_lines.append(' ' * (indent + 2) + if_statement)
                new_lines.append(' ' * indent + f"}});")
            i = j
            continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def process_file(file_path: Path):
    """Traite un fichier"""
    try:
        content = file_path.read_text(encoding='utf-8')
        if re.search(r'^\s*\$:', content, re.MULTILINE):
            new_content = convert_reactive_statements(content)
            if new_content != content:
                file_path.write_text(new_content, encoding='utf-8')
                print(f"✓ Converti: {file_path}")
                return True
    except Exception as e:
        print(f"✗ Erreur sur {file_path}: {e}")
        import traceback
        traceback.print_exc()
    return False

if __name__ == '__main__':
    src_dir = Path('src/routes')
    converted = 0
    
    for svelte_file in src_dir.rglob('*.svelte'):
        if 'svelte-demo' in str(svelte_file):
            continue
        if process_file(svelte_file):
            converted += 1
    
    print(f"\n{converted} fichiers convertis")





