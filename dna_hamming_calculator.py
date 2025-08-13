import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from typing import List, Tuple, Dict
import re

# Configure page
st.set_page_config(
    page_title="DNA Hamming Distance Calculator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme
try:
    st._config.set_option('theme.base', 'light')
    st._config.set_option('theme.backgroundColor', '#ffffff')
    st._config.set_option('theme.secondaryBackgroundColor', '#f0f2f6')
    st._config.set_option('theme.textColor', '#262730')
except:
    pass

# Ultra-Modern CSS with 2025 Design Trends
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* HAYA Therapeutics inspired color system - Precision Medicine Palette */
    :root {
        --primary-gradient: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #2d4059 100%);
        --biotech-gradient: linear-gradient(135deg, #1a2332 0%, #2d4059 50%, #ffa500 100%);
        --dark-genome: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
        --precision-gradient: linear-gradient(135deg, #2d4059 0%, #00ff88 50%, #4a90e2 100%);
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
        --shadow-soft: 0 8px 32px 0 rgba(15, 20, 25, 0.4);
        --shadow-glow: 0 0 40px 0 rgba(45, 64, 89, 0.3);
        --text-primary: #ffffff;
        --text-secondary: #ffffff;
        --text-light: #ffffff;
        --accent-biotech: #ffa500;
        --accent-precision: #00ff88;
        --accent-rna: #4a90e2;
    }
    
    /* Global app styling - HAYA Therapeutics inspired dark genome theme */
    .stApp {
        background: var(--primary-gradient);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container with glassmorphism */
    .main .block-container {
        padding: 2rem;
        max-width: 1200px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-soft);
        margin: 1rem auto;
        color: #ffffff !important;
    }
    
    /* Force ALL text to be white */
    * {
        color: #ffffff !important;
    }
    
    /* Ensure all elements have white text */
    body, .stApp, .main, .block-container, p, div, span, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .element-container, .row-widget, .stSelectbox, .stRadio, 
    .stTextInput, .stTextArea, label, .metric-container {
        color: #ffffff !important;
    }
    
    /* Precision Medicine header with HAYA-inspired gradient */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: var(--precision-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
        font-weight: 600;
        background: var(--biotech-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* HAYA-inspired dark genome info boxes */
    .info-box {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        color: #ffffff !important;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-soft);
        position: relative;
        overflow: hidden;
    }
    
    .info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--precision-gradient);
    }
    
    .info-box * {
        color: #ffffff !important;
    }
    
    .info-box strong {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    .info-box ul li {
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Success box with precision medicine theme */
    .success-box {
        background: linear-gradient(135deg, rgba(107, 142, 35, 0.15) 0%, rgba(74, 103, 65, 0.15) 100%);
        backdrop-filter: blur(20px);
        color: #ffffff !important;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(107, 142, 35, 0.3);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(107, 142, 35, 0.2);
    }
    
    .success-box * {
        color: #ffffff !important;
    }
    
    /* Error box with dark genome styling */
    .error-box {
        background: rgba(220, 53, 69, 0.15);
        backdrop-filter: blur(20px);
        color: #ffffff !important;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(220, 53, 69, 0.3);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(220, 53, 69, 0.2);
    }
    
    /* HAYA-inspired precision medicine buttons */
    .stButton > button {
        background: var(--precision-gradient);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px 0 rgba(107, 142, 35, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px 0 rgba(107, 142, 35, 0.6);
        background: var(--biotech-gradient);
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Precision medicine input styling with dark text for readability */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-precision) !important;
        box-shadow: 0 0 0 3px rgba(107, 142, 35, 0.2) !important;
        transform: scale(1.02);
    }
    
    /* Selectbox modern styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div > div {
        color: #000000 !important;
    }
    
    /* HAYA-inspired radio buttons */
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.3s ease !important;
        color: #ffffff !important;
    }
    
    .stRadio > div > label:hover {
        background: rgba(107, 142, 35, 0.15) !important;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(107, 142, 35, 0.2);
        border-color: rgba(107, 142, 35, 0.3) !important;
    }
    
    .stRadio > div > label > div {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* File uploader modern styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px);
        border-radius: 16px !important;
        border: 2px dashed rgba(78, 205, 196, 0.5) !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader:hover {
        border-color: var(--accent-teal) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* HAYA dark genome sidebar */
    section[data-testid="stSidebar"] {
        background: var(--dark-genome) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        padding: 2rem 1rem !important;
    }
    
    /* Sidebar headers with precision medicine gradient */
    .css-1d391kg h2 {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        background: var(--precision-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem !important;
    }
    
    /* Sidebar text styling - white on dark */
    .css-1d391kg, .css-1d391kg * {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .css-1d391kg label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .css-1d391kg .stMarkdown {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    .css-1d391kg .stMarkdown em {
        color: rgba(255, 255, 255, 0.6) !important;
        font-style: italic;
    }
    
    /* Input placeholders */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
        font-style: italic;
    }
    
    /* Metrics with modern cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px);
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease !important;
        color: #ffffff !important;
    }
    
    /* Ensure all metric text is white */
    div[data-testid="metric-container"] * {
        color: #ffffff !important;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-glow);
    }
    
    /* DataFrames with glassmorphism */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px);
        border-radius: 16px !important;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
    }
    
    /* Ensure dataframe text is white */
    .stDataFrame * {
        color: #ffffff !important;
    }
    
    .stDataFrame table {
        color: #ffffff !important;
    }
    
    .stDataFrame th, .stDataFrame td {
        color: #ffffff !important;
    }
    
    /* Hide Streamlit branding with style */
    .css-1rs6os, .css-17ziqus, .css-1rjjcn4 {
        visibility: hidden;
    }
    
    /* Plotly charts background */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px);
        padding: 1rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        .info-box {
            padding: 1.5rem;
        }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main .block-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* HAYA-inspired custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--precision-gradient);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--biotech-gradient);
    }
</style>
""", unsafe_allow_html=True)

def calculate_hamming_distance(seq1: str, seq2: str) -> int:
    """
    Calculate the Hamming distance between two DNA sequences.
    
    Args:
        seq1: First DNA sequence
        seq2: Second DNA sequence
        
    Returns:
        Hamming distance (number of positions where sequences differ)
    """
    if len(seq1) != len(seq2):
        raise ValueError(f"Sequences must be of equal length. Got {len(seq1)} and {len(seq2)}")
    
    return sum(c1 != c2 for c1, c2 in zip(seq1.upper(), seq2.upper()))

def validate_dna_sequence(sequence: str) -> bool:
    """
    Validate if a string is a valid DNA sequence (contains only A, T, G, C).
    
    Args:
        sequence: String to validate
        
    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r'^[ATGC]+$', sequence.upper().strip()))

def parse_sequences_from_text(text: str) -> List[str]:
    """
    Parse DNA sequences from text input.
    Expects each sequence on a new line.
    
    Args:
        text: Input text containing sequences
        
    Returns:
        List of cleaned DNA sequences
    """
    sequences = []
    lines = text.strip().split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
            
        # Remove any labels/identifiers (anything before a colon or space)
        if ':' in line:
            line = line.split(':', 1)[1].strip()
        elif ' ' in line and not validate_dna_sequence(line):
            parts = line.split()
            # Take the longest part that looks like a DNA sequence
            valid_parts = [part for part in parts if validate_dna_sequence(part)]
            if valid_parts:
                line = max(valid_parts, key=len)
        
        if validate_dna_sequence(line):
            sequences.append(line.upper())
        else:
            st.error(f"Invalid DNA sequence at line {i}: {line[:50]}...")
            
    return sequences

def parse_sequences_from_file(file) -> List[str]:
    """
    Parse DNA sequences from uploaded file.
    Supports .txt, .fasta, .fa files.
    
    Args:
        file: Uploaded file object
        
    Returns:
        List of DNA sequences
    """
    sequences = []
    
    try:
        # Read file content
        content = file.read().decode('utf-8')
        
        # Handle FASTA format
        if file.name.endswith(('.fasta', '.fa')):
            lines = content.strip().split('\n')
            current_seq = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('>'):
                    if current_seq:
                        if validate_dna_sequence(current_seq):
                            sequences.append(current_seq.upper())
                        current_seq = ""
                else:
                    current_seq += line
            
            # Add the last sequence
            if current_seq and validate_dna_sequence(current_seq):
                sequences.append(current_seq.upper())
        
        # Handle plain text format
        else:
            sequences = parse_sequences_from_text(content)
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        
    return sequences

def get_color_for_distance(distance: int) -> str:
    """
    Get color based on Hamming distance thresholds with HAYA precision medicine palette.
    
    Args:
        distance: Hamming distance value
        
    Returns:
        Color string for the distance
    """
    if distance < 2:
        return '#ff4444'  # Red - very similar sequences (critical)
    elif 2 <= distance <= 3:
        return '#ffa500'  # Orange - moderately similar sequences
    else:
        return '#4a90e2'  # Blue - different sequences (safe)

def create_distance_matrix_plot(sequences: List[str], labels: List[str] = None) -> go.Figure:
    """
    Create an interactive heatmap of Hamming distances.
    
    Args:
        sequences: List of DNA sequences
        labels: Optional labels for sequences
        
    Returns:
        Plotly figure object
    """
    n = len(sequences)
    
    if labels is None:
        labels = [f"Seq_{i+1}" for i in range(n)]
    
    # Calculate distance matrix
    distance_matrix = np.zeros((n, n))
    colors = []
    
    for i in range(n):
        color_row = []
        for j in range(n):
            if i == j:
                distance = 0
            else:
                distance = calculate_hamming_distance(sequences[i], sequences[j])
            distance_matrix[i][j] = distance
            color_row.append(get_color_for_distance(distance))
        colors.append(color_row)
    
    # Create HAYA-inspired precision medicine heatmap with distinct colors
    fig = go.Figure(data=go.Heatmap(
        z=distance_matrix,
        x=labels,
        y=labels,
        colorscale=[
            [0, '#ff4444'],      # Red for low distances (critical)
            [0.33, '#ffa500'],   # Orange for medium distances  
            [0.66, '#4a90e2'],   # Blue for medium-high distances (safe)
            [1, '#1a2332']       # Dark genome for high distances (very different)
        ],
        showscale=True,
        colorbar=dict(
            title=dict(
                text="Hamming Distance",
                side="right",
                font=dict(size=14, color="#ffffff", family="Inter")
            ),
            thickness=20,
            tickfont=dict(size=12, color="#ffffff", family="Inter"),
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1,
            bgcolor="rgba(255,255,255,0.05)"
        ),
        text=distance_matrix.astype(int),
        texttemplate="%{text}",
        textfont={"size": 14, "color": "white", "family": "Inter"},
        hovertemplate="<b style='color:#ffffff'>%{y}</b> vs <b style='color:#ffffff'>%{x}</b><br><b>Distance: %{z}</b><extra></extra>"
    ))
    
    fig.update_layout(
        title={
            'text': "Sequence Distance Matrix",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#ffffff', 'family': 'Inter'}
        },
        xaxis_title="DNA Sequences",
        yaxis_title="DNA Sequences",
        width=800,
        height=600,
        font=dict(size=14, color="#ffffff", family="Inter"),
        plot_bgcolor='rgba(255,255,255,0.02)',
        paper_bgcolor='rgba(255,255,255,0.05)',
        xaxis=dict(
            tickfont=dict(size=12, color="#ffffff"),
            title=dict(
                font=dict(size=14, color="#ffffff", family="Inter")
            ),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            tickfont=dict(size=12, color="#ffffff"),
            title=dict(
                font=dict(size=14, color="#ffffff", family="Inter")
            ),
            gridcolor='rgba(255,255,255,0.1)'
        ),
        hoverlabel=dict(
            bgcolor="rgba(26, 35, 50, 0.95)",
            bordercolor="rgba(107, 142, 35, 0.7)",
            font=dict(size=12, color="#ffffff", family="Inter")
        )
    )
    
    return fig

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">Barcode Distance Calculator</h1>', unsafe_allow_html=True)
    
    # Info section
    st.markdown("""
    <div class="info-box">
        <strong>Barcode Analysis Platform:</strong><br>
        <br>
        Calculate that computes the hamming distance between DNA sequences:
        <ul>
            <li><span style="color: #ff4444; font-weight: 600;">🔴 Red:</span> Distance < 2 (nearly identical sequences - barcode conflicts - BAD)</li>
            <li><span style="color: #ffa500; font-weight: 600;">🟠 Orange:</span> Distance 2-3 (similar sequences with potential issues - PROCEED WITH CARE)</li>
            <li><span style="color: #4a90e2; font-weight: 600;">🔵 Blue:</span> Distance ≥ 4 (sufficiently different sequences - safe barcodes - GOOD)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for input options
    st.sidebar.markdown('<h2 class="sub-header">Input Options</h2>', unsafe_allow_html=True)
    
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["📝 Copy & Paste", "📁 Upload File"],
        help="Select how you want to provide your DNA sequences"
    )
    
    sequences = []
    
    if input_method == "📝 Copy & Paste":
        st.sidebar.markdown("**Paste your DNA sequences below:**")
        st.sidebar.markdown("One sequence per line. Labels are optional (e.g., 'Seq1: ATGC')")
        
        text_input = st.sidebar.text_area(
            "DNA Sequences:",
            height=200,
            placeholder="Example:\nSeq1: ATGCATGC\nSeq2: ATGGATGC\nSeq3: TTGCATGC\nPress command/control + enter to submit",
            help="Enter each sequence on a new line"
        )
        
        if text_input:
            sequences = parse_sequences_from_text(text_input)
    
    else:  # File upload
        st.sidebar.markdown("**Upload a file containing DNA sequences:**")
        uploaded_file = st.sidebar.file_uploader(
            "Choose a file:",
            type=['txt', 'fasta', 'fa'],
            help="Supported formats: .txt, .fasta, .fa"
        )
        
        if uploaded_file:
            sequences = parse_sequences_from_file(uploaded_file)
    
    # Main content area
    if sequences:
        # Validate all sequences have the same length
        seq_lengths = [len(seq) for seq in sequences]
        if len(set(seq_lengths)) > 1:
            st.markdown("""
            <div class="error-box">
                <strong>⚠️ Error:</strong> All DNA sequences must have the same length for Hamming distance calculation.
                <br>Current lengths: """ + str(seq_lengths) + """
            </div>
            """, unsafe_allow_html=True)
            return
        
        st.markdown(f"""
        <div class="success-box">
            <strong>✅ Success:</strong> Found {len(sequences)} valid DNA sequences of length {len(sequences[0])}.
        </div>
        """, unsafe_allow_html=True)
        
        # Barcode Collisions - sequences with distance <= 2
        st.markdown('<h3 class="sub-header">⚠️ Barcode Collisions</h3>', unsafe_allow_html=True)
        
        # Find unique collision pairs (distance <= 2) - no duplicates
        collision_pairs = []
        red_collision_count = 0
        orange_collision_count = 0
        
        for i in range(len(sequences)):
            for j in range(i+1, len(sequences)):
                distance = calculate_hamming_distance(sequences[i], sequences[j])
                
                if distance <= 2:  # Collision detected
                    collision_type = "🔴 Red" if distance < 2 else "🟠 Orange"
                    collision_color = "Red" if distance < 2 else "Orange"
                    
                    if distance < 2:
                        red_collision_count += 1
                    else:
                        orange_collision_count += 1
                    
                    collision_pairs.append({
                        'Sequence 1': f'Seq_{i+1}',
                        'Sequence 1 DNA': sequences[i],
                        'Sequence 2': f'Seq_{j+1}',
                        'Sequence 2 DNA': sequences[j],
                        'Distance': distance,
                        'Risk Level': collision_type,
                        'Color Category': collision_color
                    })
        
        if collision_pairs:
            st.markdown("""
            <div class="error-box">
                <strong>⚠️ Collision Alert:</strong> Found sequence pairs with insufficient distance (≤2). These may cause barcode conflicts in multiplexed applications.
            </div>
            """, unsafe_allow_html=True)
            
            # Create collision dataframe - each row is a unique collision pair
            collision_df = pd.DataFrame(collision_pairs)
            collision_df = collision_df.sort_values('Distance')  # Sort by distance (most critical first)
            
            # Style the collision dataframe based on risk level
            def highlight_collision_severity(row):
                if row['Color Category'] == 'Red':  # Distance < 2 - highest severity
                    return ['background-color: rgba(255, 68, 68, 0.3)'] * len(row)  # Red highlight
                else:  # Distance = 2 - medium severity
                    return ['background-color: rgba(255, 165, 0, 0.3)'] * len(row)  # Orange highlight
            
            styled_collision_df = collision_df.style.apply(highlight_collision_severity, axis=1)
            st.dataframe(styled_collision_df, use_container_width=True)
            
            # Collision summary statistics
            col1, col2, col3 = st.columns(3)
            
            total_collision_pairs = len(collision_pairs)
            unique_sequences = set()
            for pair in collision_pairs:
                unique_sequences.add(pair['Sequence 1'])
                unique_sequences.add(pair['Sequence 2'])
            
            with col1:
                st.metric("⚠️ Total Collision Pairs", total_collision_pairs)
            with col2:
                st.metric("🔴 Red Collisions (< 2)", red_collision_count)
            with col3:
                st.metric("🟠 Orange Collisions (= 2)", orange_collision_count)
            
            # Additional info about affected sequences
            st.markdown(f"""
            <div class="info-box">
                <strong>📊 Impact Summary:</strong> {len(unique_sequences)} out of {len(sequences)} sequences are involved in collisions.
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="success-box">
                <strong>✅ No Collisions Detected:</strong> All sequences have sufficient distance (> 2) for barcode applications.
            </div>
            """, unsafe_allow_html=True)
        
        # Display distance matrix
        st.markdown('<h3 class="sub-header">🎯 Distance Matrix</h3>', unsafe_allow_html=True)
        
        # Create and display the heatmap
        fig = create_distance_matrix_plot(sequences)
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.markdown("""
        <div class="info-box">
            <strong>Hello there!</strong><br>
            <br>
            <strong>🎯 Guidelines:</strong>
            <ul>
                <li>🧬 Ensure all sequences have identical lengths for regulatory comparison</li>
                <li>🔬 Use only valid nucleotides (A, T, G, C) for therapeutic analysis</li>
                <li>🏷️ Sequences can be labeled like "Target_1: ATGC" for tracking, but not required</li>
                <li>📁 Upload FASTA files or paste sequences - both formats supported for biotech workflows</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()