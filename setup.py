#!/usr/bin/env python3
"""
Setup script for Book Scanner Application
Supports Windows and macOS
"""

import os
import sys
import subprocess
import platform

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"Running: {description if description else command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_conda():
    """Check if conda is installed"""
    try:
        result = subprocess.run("conda --version", shell=True, check=True, capture_output=True, text=True)
        print(f"Found conda: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        return False

def install_with_conda():
    """Install packages using conda environment"""
    print("Setting up conda environment for Book Scanner...")
    
    env_name = "book-scanner"
    
    # Check if environment already exists
    result = subprocess.run("conda info --envs", shell=True, capture_output=True, text=True)
    if env_name in result.stdout:
        print(f"✓ Found existing conda environment: {env_name}")
        print("Using existing environment...")
    else:
        # Check if environment.yml exists and use it
        if os.path.exists("environment.yml"):
            print(f"Found environment.yml, creating conda environment from file...")
            if not run_command(f"conda env create -f environment.yml", f"Creating conda environment from environment.yml"):
                print("Failed to create conda environment from yml file, trying manual creation...")
            else:
                print(f"Successfully created conda environment: {env_name}")
                return True
        
        # Fallback to manual creation
        print(f"Creating conda environment manually: {env_name}")
        
        if not run_command(f"conda create -n {env_name} python=3.9 -y", f"Creating conda environment '{env_name}'"):
            print("Failed to create conda environment!")
            return False
    
    # Install packages via conda-forge when possible, pip for others
    conda_packages = [
        "pillow",
        "numpy", 
        "opencv",
        "poppler"  # This will install poppler automatically
    ]
    
    pip_packages = [
        "pyautogui",
        "img2pdf", 
        "google-cloud-vision",
        "pdf2image"
    ]
    
    # Install conda packages
    conda_cmd = f"conda install -n {env_name} -c conda-forge {' '.join(conda_packages)} -y"
    if not run_command(conda_cmd, "Installing conda packages"):
        print("Warning: Some conda packages failed to install, continuing with pip...")
    
    # Install pip packages in the conda environment
    pip_cmd = f"conda run -n {env_name} pip install {' '.join(pip_packages)}"
    if not run_command(pip_cmd, "Installing pip packages in conda environment"):
        print("Failed to install pip packages!")
        return False
    
    print(f"Successfully created conda environment: {env_name}")
    return True

def install_with_pip():
    """Fallback to pip installation"""
    print("Installing Python packages with pip...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("Warning: Failed to upgrade pip, continuing anyway...")
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        print("Failed to install Python packages!")
        return False
    
    return True

def install_python_packages():
    """Install required Python packages - prefer conda, fallback to pip"""
    if check_conda():
        print("Conda found! Using conda for package management...")
        if install_with_conda():
            return True
        else:
            print("Conda installation failed, falling back to pip...")
            
    print("Using pip for package installation...")
    return install_with_pip()

def install_system_dependencies():
    """Install system-specific dependencies"""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        print("Detected macOS - Installing poppler via Homebrew...")
        
        # Check if Homebrew is installed
        if run_command("which brew", "Checking for Homebrew"):
            run_command("brew install poppler", "Installing poppler")
        else:
            print("Homebrew not found. Please install Homebrew first:")
            print("Visit: https://brew.sh/")
            print("Then run: brew install poppler")
            
    elif system == "windows":
        print("Detected Windows - poppler will be handled by pdf2image package")
        # pdf2image can download poppler automatically on Windows
        
    elif system == "linux":
        print("Detected Linux - Please install poppler manually:")
        print("Ubuntu/Debian: sudo apt-get install poppler-utils")
        print("CentOS/RHEL: sudo yum install poppler-utils")
        print("Arch: sudo pacman -S poppler")
        
    else:
        print(f"Unknown system: {system}")
        print("Please install poppler manually for pdf2image support")

def setup_google_vision():
    """Setup instructions for Google Vision API"""
    print("\n" + "="*60)
    print("GOOGLE VISION API SETUP")
    print("="*60)
    print("To use OCR functionality, you need to set up Google Vision API:")
    print("\n1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable the Vision API")
    print("4. Create a service account and download the JSON key file")
    print("5. Set the environment variable:")
    
    system = platform.system().lower()
    if system == "windows":
        print("   set GOOGLE_APPLICATION_CREDENTIALS=path\\to\\your\\credentials.json")
    else:
        print("   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json")
    
    print("\n6. Or edit src/google_vision_ocr.py and add the path directly")
    print("="*60)

def create_run_scripts():
    """Create convenience scripts to run the application"""
    
    # Check if conda environment was created
    conda_available = check_conda()
    
    if conda_available:
        # Python script content for conda
        python_script = f'''#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    # Check if conda environment exists
    try:
        result = subprocess.run("conda info --envs", shell=True, capture_output=True, text=True)
        if "book-scanner" in result.stdout:
            print("Running with conda environment: book-scanner")
            subprocess.run("conda run -n book-scanner python -c \\"import sys; sys.path.insert(0, '.'); from app.book_scanner_gui import main; main()\\"", shell=True)
        else:
            print("Conda environment not found, running with system Python...")
            run_with_system_python()
    except Exception as e:
        print(f"Error with conda: {{e}}")
        print("Falling back to system Python...")
        run_with_system_python()

def run_with_system_python():
    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    try:
        # Import and run the application
        from app.book_scanner_gui import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error importing application: {{e}}")
        print("\\nPlease make sure all dependencies are installed:")
        print("Run: python setup.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    else:
        # Python script content for regular pip
        python_script = f'''#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the application
from app.book_scanner_gui import main

if __name__ == "__main__":
    main()
'''
    
    # Write the Python launcher
    with open("run_book_scanner.py", "w") as f:
        f.write(python_script)
    
    # Make it executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("run_book_scanner.py", 0o755)
    
    # Create batch file for Windows
    if platform.system() == "Windows":
        if conda_available:
            batch_content = f'''@echo off
echo Checking for conda environment...
conda info --envs | findstr book-scanner >nul
if %errorlevel% == 0 (
    echo Running with conda environment: book-scanner
    conda run -n book-scanner python run_book_scanner.py
) else (
    echo Conda environment not found, running with system Python...
    python run_book_scanner.py
)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running application. Please check the error messages above.
    pause
)
'''
        else:
            batch_content = f'''@echo off
echo Starting Book Scanner Application...
python run_book_scanner.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running application. Please check the error messages above.
    echo Make sure you have run: python setup.py
    echo.
    pause
)
'''
        with open("run_book_scanner.bat", "w") as f:
            f.write(batch_content)
    
    # Create shell script for Unix
    else:
        if conda_available:
            shell_content = f'''#!/bin/bash
echo "Checking for conda environment..."
if conda info --envs | grep -q book-scanner; then
    echo "Running with conda environment: book-scanner"
    conda run -n book-scanner python3 run_book_scanner.py
else
    echo "Conda environment not found, running with system Python..."
    python3 run_book_scanner.py
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "Error running application. Please check the error messages above."
    echo "Make sure you have run: python3 setup.py"
    echo ""
    read -p "Press Enter to continue..."
fi
'''
        else:
            shell_content = f'''#!/bin/bash
echo "Starting Book Scanner Application..."
python3 run_book_scanner.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error running application. Please check the error messages above."
    echo "Make sure you have run: python3 setup.py"
    echo ""
    read -p "Press Enter to continue..."
fi
'''
        with open("run_book_scanner.sh", "w") as f:
            f.write(shell_content)
        os.chmod("run_book_scanner.sh", 0o755)

def main():
    """Main setup function"""
    print("Book Scanner Application Setup")
    print("==============================")
    print(f"Detected OS: {platform.system()}")
    print(f"Python version: {sys.version}")
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found!")
        print("Please run this script from the book-scanner directory")
        sys.exit(1)
    
    # Check for conda
    conda_available = check_conda()
    if conda_available:
        print("✓ Conda is available - will use conda environment for better dependency management")
    else:
        print("⚠ Conda not found - will use pip (consider installing Anaconda/Miniconda)")
        print("  Download from: https://docs.conda.io/en/latest/miniconda.html")
    
    # Install system dependencies
    install_system_dependencies()
    
    # Install Python packages
    if not install_python_packages():
        print("Setup failed!")
        sys.exit(1)
    
    # Create run scripts
    create_run_scripts()
    
    # Show Google Vision setup instructions
    setup_google_vision()
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    
    if conda_available:
        print("✓ Conda environment 'book-scanner' created successfully!")
        print("\nTo activate the environment manually:")
        print("  conda activate book-scanner")
        print("\nTo run the application:")
    else:
        print("To run the application:")
    
    if platform.system() == "Windows":
        print("  - Double-click run_book_scanner.bat")
        print("  - Or run: python run_book_scanner.py")
    else:
        print("  - Run: ./run_book_scanner.sh")
        print("  - Or run: python3 run_book_scanner.py")
    
    if conda_available:
        print("\nThe run scripts will automatically use the conda environment.")
        print("If you want to run manually with conda:")
        print("  conda run -n book-scanner python app/book_scanner_gui.py")
    
    print("\nMake sure to set up Google Vision API credentials for OCR functionality!")
    print("="*60)

if __name__ == "__main__":
    main()
