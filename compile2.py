import subprocess
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

script_path = os.path.join(current_dir, "cry.py")

output_dir = os.path.join(current_dir, "dist")

icon_path = os.path.join(current_dir, "ico.ico")

group2_path = os.path.join(current_dir, "Group2.png")
group3_path = os.path.join(current_dir, "Group3.png")

style_path = os.path.join(current_dir, "style.qss")

command = [
    'pyinstaller', 
    '--onefile',
    '--noconsole',
    '--hidden-import=PySide6',
    '--hidden-import=pyperclip',
    '--hidden-import=random',
    '--hidden-import=collections.defaultdict',
    '--hidden-import=PIL',
    '--hidden-import=PIL.Image',
    '--icon', icon_path,
    '--distpath', output_dir,
    '--add-data', f'{group2_path};.',
    '--add-data', f'{group3_path};.',
    '--add-data', f'{icon_path};.',
    '--add-data', f'{style_path};.',
    script_path
]

subprocess.run(command)

print(f".exe сохранён в папке: {output_dir}")