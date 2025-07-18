#!/usr/bin/env python3
"""
Streamlit app for the plagiarism detector.
"""

import os
import tempfile
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from plagiarism_detector import PlagiarismDetector

# Set page configuration
st.set_page_config(
    page_title="Code Plagiarism Detector",
    page_icon="🔍",
    layout="wide"
)

# App title and description
st.title("Code Plagiarism Detector")
st.markdown("""
This app detects plagiarism in code submissions using the following algorithms:
- **Rabin-Karp Algorithm**: For efficient string matching
- **Graph Algorithms (BFS/DFS)**: For clustering similar submissions
- **Greedy Algorithms**: For selecting representative submissions
- **B+ Tree**: For efficient metadata storage
""")

# Create sidebar for settings
st.sidebar.header("Settings")

# Similarity threshold slider
similarity_threshold = st.sidebar.slider(
    "Similarity Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.05,
    help="Minimum similarity score to consider two submissions similar (0.0 to 1.0)"
)

# Display threshold as percentage
st.sidebar.write(f"Threshold: {similarity_threshold:.0%}")

# Advanced settings
with st.sidebar.expander("Advanced Settings"):
    k_gram_size = st.number_input(
        "K-gram Size",
        min_value=3,
        max_value=10,
        value=5,
        help="Size of the k-grams (sequences) to compare"
    )
    
    max_representatives = st.number_input(
        "Max Representatives",
        min_value=1,
        max_value=5,
        value=2,
        help="Maximum number of representatives to select per cluster"
    )

# File upload section
st.header("Upload Code Files")
uploaded_files = st.file_uploader(
    "Upload one or more code files",
    accept_multiple_files=True,
    type=["py", "java", "cpp", "c", "js", "html", "css", "txt"]
)

# Metadata upload (optional)
st.subheader("Upload Metadata (Optional)")
st.markdown("Metadata file should be a CSV with columns: filename, student_id, timestamp")
metadata_file = st.file_uploader(
    "Upload metadata file (CSV)",
    type=["csv", "txt"]
)

# Process files when the user clicks the button
if st.button("Detect Plagiarism") and uploaded_files:
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create a temporary directory to store uploaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files to the temporary directory
        status_text.text("Saving uploaded files...")
        file_paths = []
        for i, uploaded_file in enumerate(uploaded_files):
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)
            progress_bar.progress((i + 1) / (len(uploaded_files) + 3))
        
        # Save metadata file if provided
        metadata_path = None
        if metadata_file:
            status_text.text("Processing metadata...")
            metadata_path = os.path.join(temp_dir, "metadata.csv")
            with open(metadata_path, "wb") as f:
                f.write(metadata_file.getbuffer())
        
        # Create a plagiarism detector
        status_text.text("Initializing plagiarism detector...")
        detector = PlagiarismDetector(
            similarity_threshold=similarity_threshold
        )
        progress_bar.progress((len(uploaded_files) + 1) / (len(uploaded_files) + 3))
        
        # Process the files
        status_text.text("Detecting plagiarism...")
        
        # Add each file to the detector
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            detector.add_submission(file_path, {"filename": file_name})
        
        # Detect plagiarism
        results = detector.detect_plagiarism()
        progress_bar.progress((len(uploaded_files) + 2) / (len(uploaded_files) + 3))
        
        # Calculate similarity matrix
        status_text.text("Generating similarity matrix...")
        submissions = list(detector.submissions.keys())
        similarity_matrix = []
        
        for s1 in submissions:
            row = []
            for s2 in submissions:
                if s1 == s2:
                    similarity = 1.0
                else:
                    tokens1 = detector.submissions[s1]
                    tokens2 = detector.submissions[s2]
                    similarity = detector.rabin_karp.calculate_similarity(tokens1, tokens2)
                row.append(similarity)
            similarity_matrix.append(row)
        
        progress_bar.progress(1.0)
        status_text.text("Analysis complete!")
        
        # Display results
        st.header("Plagiarism Detection Results")
        
        if not results:
            st.warning("No clusters of similar submissions found.")
        else:
            st.success(f"Found {len(results)} clusters of similar submissions.")
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["Clusters", "Similarity Matrix", "Network Graph"])
            
            with tab1:
                # Display clusters
                for i, result in enumerate(results):
                    with st.expander(f"Cluster {i+1} ({len(result['cluster'])} submissions)", expanded=True):
                        # Get the representatives for this cluster
                        representatives = result['representatives']
                        
                        # Create a table of submissions
                        cluster_data = []
                        for submission in result['cluster']:
                            submission_id = submission['id']
                            is_representative = submission_id in representatives
                            cluster_data.append({
                                "File": submission_id,
                                "Representative": "✓" if is_representative else "",
                                "Metadata": str(submission.get('metadata', {}))
                            })
                        
                        st.table(pd.DataFrame(cluster_data))
                        
                        # Show similarity information
                        st.subheader("Similarity Information")
                        similarity_data = []
                        for idx1, sub1 in enumerate(result['cluster']):
                            sub1_id = sub1['id']
                            for idx2, sub2 in enumerate(result['cluster']):
                                if idx1 < idx2:  # Only show each pair once
                                    sub2_id = sub2['id']
                                    similarity = detector.rabin_karp.calculate_similarity(
                                        detector.submissions[sub1_id], 
                                        detector.submissions[sub2_id]
                                    )
                                    similarity_data.append({
                                        "File 1": sub1_id,
                                        "File 2": sub2_id,
                                        "Similarity": f"{similarity:.2%}"
                                    })
                        
                        st.table(pd.DataFrame(similarity_data))
            
            with tab2:
                # Display similarity matrix as a heatmap
                st.subheader("Similarity Matrix Heatmap")
                
                # Create a DataFrame for the similarity matrix
                df_similarity = pd.DataFrame(
                    similarity_matrix,
                    index=submissions,
                    columns=submissions
                )
                
                # Create a heatmap
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(
                    df_similarity,
                    annot=True,
                    cmap="YlGnBu",
                    fmt=".2f",
                    linewidths=.5,
                    ax=ax
                )
                plt.title("Similarity Matrix")
                st.pyplot(fig)
                
                # Display the raw similarity matrix as a table
                st.subheader("Similarity Matrix Table")
                st.dataframe(df_similarity.style.format("{:.2%}"))
            
            with tab3:
                # Display network graph of similarities
                st.subheader("Similarity Network Graph")
                
                # Create a graph
                G = nx.Graph()
                
                # Add nodes
                for submission in submissions:
                    G.add_node(submission)
                
                # Add edges with weight >= threshold
                for i, s1 in enumerate(submissions):
                    for j, s2 in enumerate(submissions):
                        if i < j:  # Only add each edge once
                            similarity = similarity_matrix[i][j]
                            if similarity >= similarity_threshold:
                                G.add_edge(s1, s2, weight=similarity)
                
                # Draw the graph
                fig, ax = plt.subplots(figsize=(10, 8))
                pos = nx.spring_layout(G, seed=42)
                
                # Draw nodes
                nx.draw_networkx_nodes(G, pos, node_size=500, alpha=0.8)
                
                # Draw edges with width proportional to similarity
                for u, v, data in G.edges(data=True):
                    width = data['weight'] * 5  # Scale width
                    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=width, alpha=0.7)
                
                # Draw labels
                nx.draw_networkx_labels(G, pos, font_size=10)
                
                plt.title("Similarity Network (edges represent similarity ≥ threshold)")
                plt.axis("off")
                st.pyplot(fig)
        
        # Display summary of all submissions
        st.header("Summary of All Submissions")
        
        # Group submissions by cluster
        clustered_submissions = set()
        for result in results:
            for submission in result['cluster']:
                clustered_submissions.add(submission['id'])
        
        # Find submissions not in any cluster
        all_submissions = set(detector.submissions.keys())
        unclustered_submissions = all_submissions - clustered_submissions
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Submissions in Clusters")
            if clustered_submissions:
                for submission_id in sorted(clustered_submissions):
                    st.write(f"- {submission_id}")
            else:
                st.write("None")
        
        with col2:
            st.subheader("Submissions Not in Any Cluster")
            if unclustered_submissions:
                for submission_id in sorted(unclustered_submissions):
                    st.write(f"- {submission_id}")
            else:
                st.write("None")

# Add information about how to use the app
with st.expander("How to Use This App"):
    st.markdown("""
    1. **Upload Files**: Upload the code files you want to check for plagiarism.
    2. **Adjust Threshold**: Use the slider in the sidebar to set the similarity threshold.
    3. **Run Detection**: Click the "Detect Plagiarism" button to analyze the files.
    4. **View Results**: Explore the results in the different tabs:
        - **Clusters**: Shows groups of similar submissions and their representatives.
        - **Similarity Matrix**: Displays a heatmap of similarity scores between all files.
        - **Network Graph**: Visualizes the relationships between similar files.
    
    **Note**: Higher threshold values will only detect very similar files, while lower values may include files with less similarity.
    """)

# Footer
st.markdown("---")
st.markdown("Code Plagiarism Detector | Developed with Streamlit")
