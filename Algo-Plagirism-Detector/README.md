# Plagiarism Detector

A system for automatically detecting plagiarism in programming assignments.

## Overview

This plagiarism detector uses several algorithms to identify similar code submissions:

1. **Rabin-Karp Algorithm**: For efficient string matching to find similar code sequences
2. **Graph Algorithms (BFS/DFS)**: For clustering similar submissions
3. **Greedy Algorithms**: For selecting representative submissions from each cluster
4. **B+ Tree**: For efficient metadata storage and retrieval
5. **Real-time Processing**: For incrementally updating the similarity graph as new submissions arrive

## Project Structure

- `plagiarism_detector.py`: Main module that orchestrates the entire process
- `code_parser.py`: Module for parsing code files into tokens
- `rabin_karp.py`: Implementation of the Rabin-Karp algorithm
- `similarity_graph.py`: Graph representation of code similarity
- `clustering.py`: Implementation of clustering algorithms
- `greedy_selection.py`: Implementation of greedy selection algorithms
- `bplus_tree.py`: Implementation of B+ Tree for metadata storage
- `run_tests.py`: Script for running tests on the plagiarism detector
- `app.py`: Streamlit web application for interactive plagiarism detection
- `test_cases/`: Directory containing test cases

## Usage

### Streamlit Web Application

The easiest way to use the plagiarism detector is through the Streamlit web application:

```bash
# Install required dependencies
pip install -r requirements.txt

# Run the Streamlit app (any of these methods)
python run_app.py
# OR
streamlit run app.py
# OR on Windows, double-click run_app.bat
```

This will open a web interface where you can:
- Upload code files for analysis
- Adjust the similarity threshold using a slider
- View detailed plagiarism detection results with visualizations
- See similarity percentages between all files

### Command Line Usage

```bash
python plagiarism_detector.py --directory <submissions_directory> [--metadata <metadata_file>] [--threshold <similarity_threshold>]
```

### Running Tests

```bash
python run_tests.py [--test-case <test_case_number>] [--threshold <similarity_threshold>]
```

## Test Cases

The project includes three test cases:

### Test Case 1: Basic Functionality

- File A: Original simple code (calculates sum)
- File B: Exact copy of File A
- File C: Slightly modified copy of File A (variable names changed)
- File D: Completely different code (calculates product)

### Test Case 2: Constraint & Edge Case

- File E: Original code (medium size)
- File F: Copy of E with comments added/removed, whitespace changes
- File G: Copy of E with large block of code moved/reordered
- File H: Code in a different programming language
- File I: Empty file

### Test Case 3: Algorithm Integration & Complexity

- Group 1 (Files J, K, L): Similar implementations of bubble sort
- Group 2 (Files M, N): Similar implementations of binary search
- Files O, P: Unique implementations of merge sort and quick sort

## Implementation Details

### Code Parser

The code parser tokenizes code files, handling different programming languages and normalizing variable names to focus on structural similarities rather than superficial differences.

### Rabin-Karp Algorithm

The Rabin-Karp algorithm efficiently finds matching sequences between code submissions by using hash values to quickly identify potential matches.

### Similarity Graph

The similarity graph represents code submissions as nodes, with edges between similar submissions weighted by their similarity score.

### Clustering

The clustering module uses BFS or DFS to find connected components in the similarity graph, identifying clusters of similar submissions.

### Greedy Selection

The greedy selection module selects representative submissions from each cluster based on criteria like highest average similarity.

### B+ Tree

The B+ Tree provides efficient storage and retrieval of metadata associated with each submission.

### Real-time Processing

The system can incrementally update the similarity graph and clusters as new submissions arrive, making it suitable for real-time use.

## Requirements

- Python 3.6 or higher
- Required packages (install with `pip install -r requirements.txt`):
  - streamlit
  - pandas
  - matplotlib
  - seaborn
  - networkx

## Screenshots

### Streamlit App Interface
![Streamlit App Interface](screenshots/app_interface.png)

### Similarity Matrix Visualization
![Similarity Matrix](screenshots/similarity_matrix.png)

### Network Graph Visualization
![Network Graph](screenshots/network_graph.png)
