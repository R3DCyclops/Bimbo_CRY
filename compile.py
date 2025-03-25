import subprocess
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

script_path = os.path.join(current_dir, "BimboCRY7.py")

output_dir = os.path.join(current_dir, "dist")

icon_path = os.path.join(current_dir, "ico.ico")

image_path = os.path.join(current_dir, "Group2.png")

command = [
    'pyinstaller', 
    '--onefile',
    '--noconsole',
    '--hidden-import=PySide6',
    '--hidden-import=pyperclip',
    '--hidden-import=random',
    '--icon', icon_path,
    '--distpath', output_dir,
    '--add-data', f'{icon_path};.',
    '--add-data', f'{image_path};.',
    script_path
]

subprocess.run(command)

print(f".exe сохранён в папке: {output_dir}")