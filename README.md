A Python-based application that detects plagiarism in code submissions using classic algorithms like Rabin-Karp for string matching, Graph algorithms (BFS/DFS) for clustering, Greedy techniques for representative selection, and B+ Trees for efficient metadata handling.

Overview
This project provides a comprehensive system for automatically detecting plagiarism in programming assignments. It leverages a combination of algorithms to analyze code submissions, identify similarities, and present the findings in an understandable format. The core of the detector is built on fundamentals of algorithm design, demonstrating their practical application.

The system includes a user-friendly web interface built with Streamlit, allowing for interactive analysis, visualization of results, and easy adjustment of detection parameters.

Key Features
Multi-Algorithm Approach: Utilizes a suite of classic algorithms for robust detection:
Rabin-Karp: For efficient string matching to find similar code sequences.
Graph Theory (BFS/DFS): For clustering similar submissions into plagiarism groups.
Greedy Algorithm: For selecting the most representative examples of plagiarism from each cluster.
B+ Tree: For efficient storage and retrieval of submission metadata.
Robust Code Parsing: The parser normalizes code by removing comments, abstracting variable names, and handling different language syntaxes, focusing on structural similarity over superficial differences.
Block Insensitive Analysis: The parser can tokenize code in a way that is insensitive to the reordering of functions or classes, making it harder to bypass detection by simply moving code blocks around.
Interactive Web UI: A Streamlit application provides a graphical interface to upload files, adjust the similarity threshold, and view detailed results through tables, a similarity heatmap, and a network graph.
Command-Line Interface: The detector can also be run from the command line for batch processing or integration into automated workflows.
Real-time Processing: The system is designed to incrementally update its similarity graph as new submissions are added, making it suitable for real-time analysis environments.
How It Works
The plagiarism detection process follows several key steps:

Code Parsing: Each source code file is parsed into a sequence of tokens. Comments are removed, strings are replaced with a placeholder, and variable/function names are normalized (e.g., calculate_sum and compute_total are both treated as VAR_0). This focuses the comparison on the code's underlying structure and logic.

Similarity Calculation (Rabin-Karp): The token streams are compared using the Rabin-Karp algorithm. K-grams (sequences of k tokens) are generated from each file, and their hash values are compared to efficiently find matches. The similarity score between two files is calculated using the Jaccard index: (Intersection of k-gram sets) / (Union of k-gram sets).

Graph Construction: A similarity graph is built where each code submission is a node. An edge is created between two nodes if their similarity score exceeds a specified threshold. The weight of the edge corresponds to the calculated similarity score.

Clustering (BFS/DFS): The system finds connected components in the similarity graph using a Breadth-First Search (BFS). Each component represents a "cluster" of submissions that are considered plagiarized from one another.

Representative Selection (Greedy Algorithm): Within each cluster, a greedy algorithm selects one or more representative submissions. It does this by identifying the nodes with the highest average similarity to all other nodes in the cluster, effectively finding the "most central" examples of plagiarism.

Metadata Management (B+ Tree): An optional B+ Tree data structure is used to store and quickly retrieve metadata associated with each submission, such as student IDs and submission timestamps, providing valuable context to the detection results.

Installation
Ensure you have Python 3.6 or higher installed.

Clone the repository:

git clone https://github.com/umarraza78/Algo-Plagirism-Detector.git
cd Algo-Plagirism-Detector/Algo-Plagirism-Detector
Install the required dependencies:

pip install -r requirements.txt
Usage
Streamlit Web Application (Recommended)
The easiest way to use the detector is through the interactive web application.

Run the app from the Algo-Plagirism-Detector directory:

streamlit run app.py
Alternatively, you can use the provided helper scripts: python run_app.py or run_app.bat on Windows.

Once the web page opens:

Upload the code files you want to analyze.
Optionally, upload a metadata file.
Adjust the "Similarity Threshold" slider to control detection sensitivity.
Click "Detect Plagiarism" to begin the analysis.
Explore the results in the "Clusters", "Similarity Matrix", and "Network Graph" tabs.
Command-Line Usage
You can run the detector on a directory of files directly from the command line. This is useful for batch processing and viewing detailed terminal output.

Run the detector on one of the provided test cases:

python run_detector.py --test-case 1 --threshold 0.7
Run the detector on a custom directory:

python run_detector.py --directory /path/to/your/submissions --threshold 0.5
Test Cases
The repository includes three test cases to demonstrate the detector's capabilities:

Test Case 1: Basic Functionality
Contains an original file, an exact copy, a copy with renamed variables, and a completely different file. This tests the core detection and normalization logic.
Test Case 2: Constraints & Edge Cases
Includes files with changes to comments and whitespace, reordered code blocks, code in a different language (Java), and an empty file. This tests the robustness of the parser.
Test Case 3: Algorithm Integration & Complexity
Contains two groups of similar algorithm implementations (Bubble Sort, Binary Search) and two unique algorithm implementations (Merge Sort, Quick Sort). This tests the ability to cluster related but distinct groups of code.
