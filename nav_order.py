import os
import re

def update_nav_order(file_path, new_order):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find where the front matter ends (i.e., second '---')
    try:
        start = lines.index('---\n')
        end = lines.index('---\n', start + 1)
    except ValueError:
        print(f"Front matter not found in {file_path}")
        return

    # Modify the nav_order
    for i in range(start + 1, end):
        if lines[i].startswith('nav_order:'):
            lines[i] = f'nav_order: {new_order}\n'
            break
    else:
        # If nav_order not found, add it before the closing ---
        lines.insert(end, f'nav_order: {new_order}\n')

    with open(file_path, 'w') as f:
        f.writelines(lines)


def process_files(directory='.'):
    pattern = re.compile(r'^\d{2}_.+\.md$')
    files = sorted(
        [f for f in os.listdir(directory) if pattern.match(f)]
    )

    for i, filename in enumerate(files, start=2):
        filepath = os.path.join(directory, filename)
        update_nav_order(filepath, i)
        print(f"[OK] {filename} -> nav_order: {i}")
        
        
process_files()