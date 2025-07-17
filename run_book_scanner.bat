@echo off
echo Checking for conda environment...
conda info --envs | findstr book-scanner >nul
if %errorlevel% == 0 (
    echo Running with conda environment: book-scanner
    conda run -n book-scanner python run_book_scanner.py
) else (
    echo Conda environment 'book-scanner' not found, running with system Python...
    python run_book_scanner.py
)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running application. Please check the error messages above.
    echo Make sure you have:
    echo 1. Created conda environment: conda create -n book-scanner python=3.9
    echo 2. Or run setup: python setup.py
    echo.
    pause
)
