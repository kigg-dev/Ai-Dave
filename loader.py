import os
import subprocess
import sys

def check_ollama():
    try:
        subprocess.run(['ollama', 'list'], check=True, capture_output=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: Ollama is not installed!")
        print("Please install Ollama from https://ollama.com")
        return False

def check_model():
    try:
        result = subprocess.run(['ollama', 'list'], check=True, capture_output=True, text=True)
        return 'gemma3:1b' in result.stdout
    except Exception as e:
        print(f"Error checking installed models: {e}")
        return False

def download_model():
    if not check_model():
        print("Downloading model gemma3:1b...")
        subprocess.run(['ollama', 'pull', 'gemma3:1b'], check=True)
    else:
        print("Model gemma3:1b is already installed")

def main():
    if check_ollama():
        download_model()

if __name__ == '__main__':
    main()
