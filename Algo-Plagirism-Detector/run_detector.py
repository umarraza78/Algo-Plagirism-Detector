#!/usr/bin/env python3
"""
Standalone script to run the plagiarism detector without requiring Streamlit.
This script will run the detector on the test cases and display the results.
"""

import os
import sys
import argparse
from plagiarism_detector import PlagiarismDetector

def print_header(text, char='=', width=80):
    """Print a header with the given text."""
    print(f"\n{char * width}")
    print(text)
    print(f"{char * width}")

def print_subheader(text, char='-', width=50):
    """Print a subheader with the given text."""
    print(f"\n{char * width}")
    print(text)
    print(f"{char * width}")

def run_detector(directory, similarity_threshold=0.7):
    """
    Run the plagiarism detector on the given directory.
    
    Args:
        directory: Directory containing the files to analyze
        similarity_threshold: Threshold for considering two submissions similar
    """
    print_header(f"Running plagiarism detector on: {directory}")
    
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory {directory} does not exist.")
        return
    
    # List files in the directory
    print("Files to analyze:")
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f != "metadata.txt"]
    for file in files:
        print(f"  - {file}")
    
    # Check for metadata file
    metadata_file = os.path.join(directory, "metadata.txt")
    if os.path.isfile(metadata_file):
        print(f"Found metadata file: {metadata_file}")
    else:
        print("No metadata file found.")
        metadata_file = None
    
    # Create a plagiarism detector
    print(f"\nInitializing plagiarism detector with threshold: {similarity_threshold:.2f}")
    detector = PlagiarismDetector(similarity_threshold=similarity_threshold)
    
    # Process the files
    print("Processing files...")
    
    # Add each file to the detector
    for file in files:
        file_path = os.path.join(directory, file)
        detector.add_submission(file_path)
    
    # Detect plagiarism
    results = detector.detect_plagiarism()
    
    # Display results
    print_header("PLAGIARISM DETECTION RESULTS")
    
    if not results:
        print("\nNo clusters of similar submissions found.")
    else:
        print(f"\nFound {len(results)} clusters of similar submissions:")
        
        for i, result in enumerate(results):
            print_subheader(f"CLUSTER {i+1}: {len(result['cluster'])} submissions")
            
            # Get the representatives for this cluster
            representatives = result['representatives']
            
            # Print all submissions in the cluster, marking representatives
            print("\nSubmissions in this cluster:")
            for submission in result['cluster']:
                submission_id = submission['id']
                
                # Format metadata if available
                metadata_str = ""
                if submission.get('metadata'):
                    metadata_str = f" - {submission['metadata']}"
                
                # Mark representatives with an asterisk
                if submission_id in representatives:
                    print(f"  * {submission_id}{metadata_str} [REPRESENTATIVE]")
                else:
                    print(f"    {submission_id}{metadata_str}")
            
            # Print similarity information
            print("\nSimilarity Information:")
            for idx1, sub1 in enumerate(result['cluster']):
                sub1_id = sub1['id']
                for idx2, sub2 in enumerate(result['cluster']):
                    if idx1 < idx2:  # Only print each pair once
                        sub2_id = sub2['id']
                        similarity = detector.rabin_karp.calculate_similarity(
                            detector.submissions[sub1_id], 
                            detector.submissions[sub2_id]
                        )
                        percentage = similarity * 100
                        print(f"  - {sub1_id} and {sub2_id}: {percentage:.2f}% similarity")
    
    # Print plagiarism percentages for all files
    print_header("PLAGIARISM PERCENTAGES FOR ALL FILES")
    
    # Get all submissions (excluding metadata.txt)
    all_submissions = [s for s in detector.submissions.keys() if s != "metadata.txt"]
    
    # Calculate and print plagiarism percentages
    print("\nPlagiarism percentages for each file compared to all other files:")
    for file1 in sorted(all_submissions):
        print(f"\n{file1} plagiarism percentages:")
        
        # Sort other files by similarity (highest first)
        similarities = []
        for file2 in all_submissions:
            if file1 != file2:
                similarity = detector.rabin_karp.calculate_similarity(
                    detector.submissions[file1],
                    detector.submissions[file2]
                )
                similarities.append((file2, similarity))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Print similarities as percentages
        for file2, similarity in similarities:
            percentage = similarity * 100
            status = ""
            if percentage >= similarity_threshold * 100:
                status = " [PLAGIARISM DETECTED]"
            print(f"  - {percentage:.2f}% similar to {file2}{status}")
    
    # Print summary
    print_header("SUMMARY")
    
    # Group submissions by cluster
    clustered_submissions = set()
    for result in results:
        for submission in result['cluster']:
            clustered_submissions.add(submission['id'])
    
    # Find submissions not in any cluster
    all_submissions = set(detector.submissions.keys())
    unclustered_submissions = all_submissions - clustered_submissions
    
    print("\nSubmissions in clusters:")
    if clustered_submissions:
        for submission_id in sorted(clustered_submissions):
            print(f"  - {submission_id}")
    else:
        print("  None")
    
    print("\nSubmissions not in any cluster:")
    if unclustered_submissions:
        for submission_id in sorted(unclustered_submissions):
            print(f"  - {submission_id}")
    else:
        print("  None")

def main():
    """Main function to run the plagiarism detector."""
    parser = argparse.ArgumentParser(description='Run the plagiarism detector on test cases')
    parser.add_argument('--test-case', '-t', type=int, choices=[1, 2, 3],
                        help='Test case to run (1, 2, or 3)')
    parser.add_argument('--directory', '-d', help='Directory containing files to analyze')
    parser.add_argument('--threshold', '-s', type=float, default=0.7,
                        help='Similarity threshold (0.0 to 1.0)')
    args = parser.parse_args()
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.test_case:
        # Run the detector on the specified test case
        test_case_dir = os.path.join(base_dir, "test_cases", f"test_case_{args.test_case}")
        run_detector(test_case_dir, args.threshold)
    elif args.directory:
        # Run the detector on the specified directory
        run_detector(args.directory, args.threshold)
    else:
        # Show usage information
        print("Please specify a test case or directory to analyze.")
        print("Usage examples:")
        print("  python run_detector.py --test-case 1")
        print("  python run_detector.py --test-case 2 --threshold 0.3")
        print("  python run_detector.py --directory path/to/files --threshold 0.5")

if __name__ == "__main__":
    main()
