#!/usr/bin/env python3
"""
Plagiarism Detector - Main Module
This module orchestrates the entire plagiarism detection process.
"""

import os
import time
from typing import Dict, List, Set, Tuple, Any
import argparse

from code_parser import CodeParser
from rabin_karp import RabinKarp
from similarity_graph import SimilarityGraph
from clustering import Clustering
from greedy_selection import GreedySelection
from bplus_tree import BPlusTree

class PlagiarismDetector:
    """
    Main class for plagiarism detection in code submissions.
    """
    
    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize the plagiarism detector.
        
        Args:
            similarity_threshold: Threshold for considering two submissions similar (0.0 to 1.0)
        """
        self.parser = CodeParser()
        self.rabin_karp = RabinKarp()
        self.similarity_graph = SimilarityGraph(similarity_threshold)
        self.clustering = Clustering()
        self.greedy_selection = GreedySelection()
        self.metadata_store = BPlusTree()
        self.similarity_threshold = similarity_threshold
        self.submissions = {}  # Dictionary to store parsed submissions
        
    def add_submission(self, file_path: str, metadata: Dict[str, Any] = None) -> str:
        """
        Add a new submission to the detector.
        
        Args:
            file_path: Path to the submission file
            metadata: Additional metadata for the submission
            
        Returns:
            submission_id: Unique identifier for the submission
        """
        # Generate a submission ID based on file name
        submission_id = os.path.basename(file_path)
        
        # Parse the submission
        tokens = self.parser.parse_file(file_path)
        self.submissions[submission_id] = tokens
        
        # Store metadata
        if metadata:
            self.metadata_store.insert(submission_id, metadata)
        
        # Update similarity graph with the new submission
        self._update_graph_with_submission(submission_id)
        
        return submission_id
    
    def _update_graph_with_submission(self, new_submission_id: str) -> None:
        """
        Update the similarity graph with a new submission.
        
        Args:
            new_submission_id: ID of the new submission
        """
        new_tokens = self.submissions[new_submission_id]
        
        # Compare with all existing submissions
        for existing_id, existing_tokens in self.submissions.items():
            if existing_id == new_submission_id:
                continue
                
            # Calculate similarity using Rabin-Karp
            similarity = self.rabin_karp.calculate_similarity(new_tokens, existing_tokens)
            
            # Add edge to graph if similarity is above threshold
            if similarity >= self.similarity_threshold:
                self.similarity_graph.add_edge(new_submission_id, existing_id, similarity)
    
    def detect_plagiarism(self) -> List[Dict]:
        """
        Detect plagiarism in the current set of submissions.
        
        Returns:
            List of clusters, each containing similar submissions and representatives
        """
        # Find clusters of similar submissions
        clusters = self.clustering.find_clusters(self.similarity_graph)
        
        # Select representatives for each cluster
        results = []
        for cluster in clusters:
            if len(cluster) > 1:  # Only consider clusters with multiple submissions
                representatives = self.greedy_selection.select_representatives(
                    cluster, self.similarity_graph
                )
                
                # Get metadata for all submissions in the cluster
                submissions_metadata = []
                for submission_id in cluster:
                    metadata = self.metadata_store.search(submission_id)
                    submissions_metadata.append({
                        'id': submission_id,
                        'metadata': metadata
                    })
                
                results.append({
                    'cluster': submissions_metadata,
                    'representatives': representatives
                })
        
        return results
    
    def batch_process(self, directory: str, metadata_file: str = None) -> List[Dict]:
        """
        Process all submissions in a directory.
        
        Args:
            directory: Directory containing submission files
            metadata_file: Optional path to a file containing metadata for submissions
            
        Returns:
            Results of plagiarism detection
        """
        # Load metadata if provided
        metadata = {}
        if metadata_file and os.path.exists(metadata_file):
            # Simple metadata format: each line contains submission_id,key1=value1,key2=value2,...
            with open(metadata_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) > 1:
                        submission_id = parts[0]
                        submission_metadata = {}
                        for part in parts[1:]:
                            if '=' in part:
                                key, value = part.split('=', 1)
                                submission_metadata[key] = value
                        metadata[submission_id] = submission_metadata
        
        # Process all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                submission_id = self.add_submission(
                    file_path, 
                    metadata.get(os.path.basename(file_path), {})
                )
        
        # Detect plagiarism
        return self.detect_plagiarism()

def main():
    """Main function to run the plagiarism detector."""
    parser = argparse.ArgumentParser(description='Detect plagiarism in code submissions')
    parser.add_argument('--directory', '-d', required=True, help='Directory containing submissions')
    parser.add_argument('--metadata', '-m', help='File containing metadata for submissions')
    parser.add_argument('--threshold', '-t', type=float, default=0.7, 
                        help='Similarity threshold (0.0 to 1.0)')
    args = parser.parse_args()
    
    detector = PlagiarismDetector(similarity_threshold=args.threshold)
    results = detector.batch_process(args.directory, args.metadata)
    
    # Print results
    print(f"Found {len(results)} clusters of similar submissions:")
    for i, result in enumerate(results):
        print(f"\nCluster {i+1} ({len(result['cluster'])} submissions):")
        print("Submissions:")
        for submission in result['cluster']:
            print(f"  - {submission['id']}")
        print("Representatives:")
        for rep in result['representatives']:
            print(f"  - {rep}")
        print("-" * 40)

if __name__ == "__main__":
    main()
