import subprocess
import sys

def install_dependencies():
    required_packages = ['PySide6', 'pyperclip']

    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} уже установлен.")
        except ImportError:
            print(f"Устанавливаю {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_dependencies()

    print("Зависимости установлены")