#!/usr/bin/env python3
"""
Book Scanner Application Launcher
Cross-platform launcher for the Book Scanner GUI
"""

import sys
import os
import subprocess

# Add the app directory to Python path
app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
sys.path.insert(0, app_dir)

def check_conda_env():
    """Check if the book-scanner conda environment exists"""
    try:
        result = subprocess.run("conda info --envs", shell=True, capture_output=True, text=True)
        return "book-scanner" in result.stdout
    except Exception:
        return False

def run_with_conda():
    """Run the application using conda environment"""
    try:
        print("Running with conda environment: book-scanner")
        # Use conda run to execute in the specific environment
        cmd = [
            "conda", "run", "-n", "book-scanner", "python", "-c",
            "import sys; sys.path.insert(0, 'app'); from book_scanner_gui import main; main()"
        ]
        subprocess.run(cmd)
        return True
    except Exception as e:
        print(f"Error running with conda: {e}")
        return False

def run_with_system_python():
    """Run the application using system Python"""
    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    try:
        # Import and run the application
        from book_scanner_gui import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error importing application: {e}")
        print("\nPlease make sure all dependencies are installed:")
        print("- For conda: conda env create -f environment.yml")
        print("- For pip: pip install -r requirements.txt")
        print("- Or run: python setup.py")
        sys.exit(1)
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)

def main():
    """Main launcher function"""
    print("Book Scanner Launcher - Starting...")
    
    # First try conda if available
    if check_conda_env():
        print("Found conda environment: book-scanner")
        if run_with_conda():
            return
        else:
            print("Conda run failed, falling back to system Python...")
    else:
        print("Conda environment 'book-scanner' not found, using system Python...")
    
    # Fallback to system Python
    run_with_system_python()

if __name__ == "__main__":
    main()
