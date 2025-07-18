#!/usr/bin/env python3
"""
Test script for the plagiarism detector.
"""

import os
import sys
import argparse
from plagiarism_detector import PlagiarismDetector

def run_test_case(test_case_dir, similarity_threshold=0.7):
    """
    Run the plagiarism detector on a test case.

    Args:
        test_case_dir: Directory containing the test case files
        similarity_threshold: Threshold for considering two submissions similar
    """
    print(f"\n{'=' * 80}")
    print(f"Running test case: {os.path.basename(test_case_dir)}")
    print(f"{'=' * 80}")

    # Check if the test case directory exists
    if not os.path.isdir(test_case_dir):
        print(f"Error: Test case directory {test_case_dir} does not exist.")
        return

    print(f"Listing contents of {test_case_dir}:")
    try:
        for item in os.listdir(test_case_dir):
            item_path = os.path.join(test_case_dir, item)
            if os.path.isfile(item_path):
                print(f"  - File: {item}")
            elif os.path.isdir(item_path):
                print(f"  - Dir: {item}")
    except Exception as e:
        print(f"Error listing directory: {e}")

    # Check if there are any files in the test case directory
    files = [f for f in os.listdir(test_case_dir) if os.path.isfile(os.path.join(test_case_dir, f)) and f != "metadata.txt"]
    if not files:
        print(f"Error: No files found in test case directory {test_case_dir}.")
        return

    print(f"Found {len(files)} files to process: {', '.join(files)}")

    # Check if metadata file exists
    metadata_file = os.path.join(test_case_dir, "metadata.txt")
    if not os.path.isfile(metadata_file):
        print(f"Warning: Metadata file {metadata_file} does not exist.")
        metadata_file = None
    else:
        print(f"Found metadata file: {metadata_file}")

    # Create a plagiarism detector
    detector = PlagiarismDetector(similarity_threshold=similarity_threshold)

    # Process the test case
    results = detector.batch_process(test_case_dir, metadata_file)

    # Print results
    print(f"\n{'=' * 50}")
    print(f"PLAGIARISM DETECTION RESULTS")
    print(f"{'=' * 50}")

    if not results:
        print("\nNo clusters of similar submissions found.")
    else:
        print(f"\nFound {len(results)} clusters of similar submissions:")

        for i, result in enumerate(results):
            print(f"\n{'-' * 50}")
            print(f"CLUSTER {i+1}: {len(result['cluster'])} submissions")
            print(f"{'-' * 50}")

            # Get the representatives for this cluster
            representatives = result['representatives']

            # Print all submissions in the cluster, marking representatives
            print("\nSubmissions in this cluster:")
            for submission in result['cluster']:
                submission_id = submission['id']

                # Format metadata if available
                metadata_str = ""
                if submission.get('metadata'):
                    student_id = submission['metadata'].get('student_id', 'Unknown')
                    timestamp = submission['metadata'].get('timestamp', 'Unknown')
                    metadata_str = f" [Student ID: {student_id}, Submitted: {timestamp}]"

                # Mark representatives with an asterisk and bold formatting
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
    print(f"\n{'=' * 50}")
    print("PLAGIARISM PERCENTAGES FOR ALL FILES")
    print(f"{'=' * 50}")

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

    # Print summary of all submissions
    print(f"\n{'=' * 50}")
    print("SUMMARY OF ALL SUBMISSIONS")
    print(f"{'=' * 50}")

    # Group submissions by cluster
    clustered_submissions = set()
    for result in results:
        for submission in result['cluster']:
            clustered_submissions.add(submission['id'])

    # Get all submissions
    all_submissions = set(detector.submissions.keys())

    # Find submissions not in any cluster
    unclustered_submissions = all_submissions - clustered_submissions

    # Print clustered submissions
    print("\nSubmissions in clusters:")
    if clustered_submissions:
        for submission_id in sorted(clustered_submissions):
            print(f"  - {submission_id}")
    else:
        print("  None")

    # Print unclustered submissions
    print("\nSubmissions not in any cluster:")
    if unclustered_submissions:
        for submission_id in sorted(unclustered_submissions):
            print(f"  - {submission_id}")
    else:
        print("  None")

    # Print pairwise similarities if requested
    if '--debug' in sys.argv:
        print(f"\n{'=' * 50}")
        print("DETAILED SIMILARITY MATRIX")
        print(f"{'=' * 50}")

        submissions = sorted(detector.submissions.keys())
        print(f"{'':15}", end="")
        for s in submissions:
            print(f"{s[:10]:10}", end=" ")
        print()

        for s1 in submissions:
            print(f"{s1[:15]:15}", end="")
            for s2 in submissions:
                if s1 == s2:
                    similarity = 1.0
                else:
                    tokens1 = detector.submissions[s1]
                    tokens2 = detector.submissions[s2]
                    similarity = detector.rabin_karp.calculate_similarity(tokens1, tokens2)
                percentage = similarity * 100
                print(f"{percentage:5.1f}%   ", end="")
            print()

def main():
    """Main function to run the tests."""
    parser = argparse.ArgumentParser(description='Run tests for the plagiarism detector')
    parser.add_argument('--test-case', '-t', help='Specific test case to run (1, 2, or 3)')
    parser.add_argument('--threshold', '-s', type=float, default=0.7,
                        help='Similarity threshold (0.0 to 1.0)')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Enable debug output')
    args = parser.parse_args()

    # Enable debug output if requested
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_cases_dir = os.path.join(base_dir, "test_cases")
    print(f"Base directory: {base_dir}")
    print(f"Test cases directory: {test_cases_dir}")

    # Check if the test cases directory exists
    if not os.path.isdir(test_cases_dir):
        print(f"Error: Test cases directory {test_cases_dir} does not exist.")
        return

    # Run specific test case if specified
    if args.test_case:
        test_case_dir = os.path.join(test_cases_dir, f"test_case_{args.test_case}")
        if os.path.isdir(test_case_dir):
            run_test_case(test_case_dir, args.threshold)
        else:
            print(f"Error: Test case directory {test_case_dir} does not exist.")
    else:
        # Run all test cases
        for test_case in sorted(os.listdir(test_cases_dir)):
            test_case_dir = os.path.join(test_cases_dir, test_case)
            if os.path.isdir(test_case_dir):
                run_test_case(test_case_dir, args.threshold)

if __name__ == "__main__":
    main()
