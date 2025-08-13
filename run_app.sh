#!/bin/bash

echo "🧬 DNA Hamming Distance Calculator"
echo "=================================="
echo ""

# Check if pixi is available and use it (fastest option)
if command -v pixi &> /dev/null && [ -f "pixi.toml" ]; then
    echo "Using Pixi for fast dependency management..."
    if [ ! -d ".pixi" ]; then
        echo "Installing dependencies with Pixi..."
        pixi install
    fi
    echo "Starting application with Pixi..."
    pixi run start
    exit 0
fi

# Check if conda is available and bc_calc environment exists
if command -v conda &> /dev/null; then
    if conda env list | grep -q "bc_calc"; then
        echo "Activating conda environment 'bc_calc'..."
        eval "$(conda shell.bash hook)"
        conda activate bc_calc
    elif [ -f "environment.yml" ]; then
        echo "Creating conda environment 'bc_calc'..."
        conda env create -f environment.yml
        eval "$(conda shell.bash hook)"
        conda activate bc_calc
    fi
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Installing required dependencies with pip..."
    pip install -r requirements.txt
    echo ""
fi

echo "Starting the Streamlit application..."
echo "The app will open in your browser automatically."
echo ""
echo "Press Ctrl+C to stop the application."
echo ""

streamlit run dna_hamming_calculator.py