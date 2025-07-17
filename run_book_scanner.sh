#!/bin/bash
echo "Book Scanner - Starting Application..."

# Check if conda environment exists
if conda info --envs | grep -q book-scanner; then
    echo "Using conda environment: book-scanner"
    conda run -n book-scanner python3 run_book_scanner.py
else
    echo "Conda environment 'book-scanner' not found, using system Python..."
    python3 run_book_scanner.py
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "Error running application. Please check the error messages above."
    echo ""
    echo "To fix this issue:"
    echo "1. Create conda environment: conda env create -f environment.yml"
    echo "2. Or install with pip: pip install -r requirements.txt"
    echo "3. Or run setup: python3 setup.py"
    echo ""
    read -p "Press Enter to continue..."
fi
