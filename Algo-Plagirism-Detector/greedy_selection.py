#!/usr/bin/env python3
"""
Greedy Selection Module
This module implements a greedy algorithm for selecting representative submissions.
"""

from typing import List, Dict, Set, Tuple
from similarity_graph import SimilarityGraph

class GreedySelection:
    """
    Implementation of a greedy algorithm for selecting representative submissions.
    """
    
    def __init__(self, max_representatives: int = 2):
        """
        Initialize the greedy selection algorithm.
        
        Args:
            max_representatives: Maximum number of representatives to select per cluster
        """
        self.max_representatives = max_representatives
    
    def select_representatives(self, cluster: List[str], graph: SimilarityGraph) -> List[str]:
        """
        Select representative submissions from a cluster using a greedy approach.
        
        Args:
            cluster: List of submission IDs in the cluster
            graph: Similarity graph
            
        Returns:
            List of representative submission IDs
        """
        if not cluster:
            return []
            
        # If the cluster is small, return all submissions
        if len(cluster) <= self.max_representatives:
            return cluster
            
        # Calculate average similarity for each submission
        avg_similarities = {}
        for node in cluster:
            avg_similarities[node] = self._calculate_average_similarity(node, cluster, graph)
            
        # Sort submissions by average similarity (descending)
        sorted_submissions = sorted(
            avg_similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Select the top submissions as representatives
        representatives = [submission for submission, _ in sorted_submissions[:self.max_representatives]]
        
        return representatives
    
    def _calculate_average_similarity(self, node: str, cluster: List[str], graph: SimilarityGraph) -> float:
        """
        Calculate the average similarity between a node and all other nodes in the cluster.
        
        Args:
            node: Node to calculate average similarity for
            cluster: List of nodes in the cluster
            graph: Similarity graph
            
        Returns:
            Average similarity
        """
        total_similarity = 0.0
        count = 0
        
        for other_node in cluster:
            if other_node != node:
                similarity = graph.get_edge_weight(node, other_node)
                total_similarity += similarity
                count += 1
        
        if count == 0:
            return 0.0
            
        return total_similarity / count
    
    def select_representatives_coverage(self, cluster: List[str], graph: SimilarityGraph) -> List[str]:
        """
        Select representative submissions to maximize coverage of the cluster.
        
        Args:
            cluster: List of submission IDs in the cluster
            graph: Similarity graph
            
        Returns:
            List of representative submission IDs
        """
        if not cluster:
            return []
            
        # If the cluster is small, return all submissions
        if len(cluster) <= self.max_representatives:
            return cluster
            
        # Initialize set of covered nodes and representatives
        covered = set()
        representatives = []
        
        # Continue until we have enough representatives or all nodes are covered
        while len(representatives) < self.max_representatives and len(covered) < len(cluster):
            best_node = None
            best_coverage = -1
            
            # Find the node that covers the most uncovered nodes
            for node in cluster:
                if node in representatives:
                    continue
                    
                # Calculate coverage (number of nodes this node is similar to)
                coverage = 0
                for other_node in cluster:
                    if other_node != node and other_node not in covered:
                        if graph.get_edge_weight(node, other_node) > 0:
                            coverage += 1
                
                if coverage > best_coverage:
                    best_coverage = coverage
                    best_node = node
            
            if best_node is None or best_coverage == 0:
                # No more nodes can be covered, break
                break
                
            # Add the best node to representatives
            representatives.append(best_node)
            covered.add(best_node)
            
            # Add all nodes covered by this representative
            for other_node in cluster:
                if other_node != best_node and other_node not in covered:
                    if graph.get_edge_weight(best_node, other_node) > 0:
                        covered.add(other_node)
        
        # If we still need more representatives, add the nodes with highest average similarity
        if len(representatives) < self.max_representatives:
            remaining = [node for node in cluster if node not in representatives]
            avg_similarities = {}
            
            for node in remaining:
                avg_similarities[node] = self._calculate_average_similarity(node, cluster, graph)
                
            # Sort by average similarity (descending)
            sorted_remaining = sorted(
                avg_similarities.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Add more representatives until we reach the maximum
            for node, _ in sorted_remaining:
                if len(representatives) >= self.max_representatives:
                    break
                representatives.append(node)
        
        return representatives
