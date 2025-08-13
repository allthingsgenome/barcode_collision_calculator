# 🧬 Barcode Distance Calculator

Calculate Hamming distances between DNA sequences and detect barcode collisions.

## Features

- **Input Methods**: Copy & paste or upload files (.txt, .fasta, .fa)
- **Interactive Heatmap**: Visual distance matrix
- **Collision Detection**: Identifies problematic sequence pairs
- **Color Coding**:
  - 🔵 **Blue**: Distance < 2 (critical risk)
  - 🟠 **Orange**: Distance = 2 (medium risk)  
  - 🟢 **Green**: Distance ≥ 4 (safe)

## Installation

### Using Pixi (Recommended)
```bash
pixi install
pixi run start
```

### Using Conda
```bash
conda env create -f environment.yml
conda activate bc_calc
streamlit run dna_hamming_calculator.py
```

### Using Pip
```bash
pip install -r requirements.txt
streamlit run dna_hamming_calculator.py
```

Open your browser to `http://localhost:8501`

## Usage

### Input Methods
- **Copy & Paste**: Enter sequences in the text area, one per line
- **File Upload**: Upload .txt, .fasta, or .fa files

### Requirements
- All sequences must have the same length
- Only valid DNA bases (A, T, G, C)
- Optional labels: `Seq1: ATGCATGC`

### Example
```
Seq1: ATGCATGCATGC
Seq2: ATGGATGCATGC
Seq3: TTGCATGCATGC
```

## What is Hamming Distance?

The number of positions where two sequences differ.

**Example:**
- `ATGC` vs `ATCC` = Distance of 1 (G ≠ C)

## Barcode Collisions

Shows sequence pairs that may cause conflicts:

- **🔵 Blue (< 2)**: Critical risk - sequences too similar
- **🟠 Orange (= 2)**: Medium risk - potential issues  
- **🟢 Green (≥ 4)**: Safe - sufficient distance

Each collision pair is shown only once.

