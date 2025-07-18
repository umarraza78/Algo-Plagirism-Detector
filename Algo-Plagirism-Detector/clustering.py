#!/usr/bin/env python3
"""
Clustering Module
This module implements clustering algorithms for finding groups of similar submissions.
"""

from typing import List, Set, Dict
from similarity_graph import SimilarityGraph

class Clustering:
    """
    Implementation of clustering algorithms for finding groups of similar submissions.
    """
    
    def __init__(self, min_cluster_size: int = 2):
        """
        Initialize the clustering algorithm.
        
        Args:
            min_cluster_size: Minimum size of a cluster to be considered valid
        """
        self.min_cluster_size = min_cluster_size
    
    def find_clusters(self, graph: SimilarityGraph) -> List[List[str]]:
        """
        Find clusters of similar submissions using BFS.
        
        Args:
            graph: Similarity graph
            
        Returns:
            List of clusters, where each cluster is a list of submission IDs
        """
        nodes = graph.get_nodes()
        visited = set()
        clusters = []
        
        # Use BFS to find connected components
        for node in nodes:
            if node in visited:
                continue
                
            # Start BFS from this node
            cluster = self._bfs(graph, node, visited)
            
            # Only consider clusters with at least min_cluster_size nodes
            if len(cluster) >= self.min_cluster_size:
                clusters.append(cluster)
        
        return clusters
    
    def _bfs(self, graph: SimilarityGraph, start_node: str, visited: Set[str]) -> List[str]:
        """
        Perform BFS to find a connected component.
        
        Args:
            graph: Similarity graph
            start_node: Node to start BFS from
            visited: Set of already visited nodes
            
        Returns:
            List of nodes in the connected component
        """
        queue = [start_node]
        cluster = []
        
        while queue:
            node = queue.pop(0)
            
            if node in visited:
                continue
                
            visited.add(node)
            cluster.append(node)
            
            # Add unvisited neighbors to the queue
            for neighbor in graph.get_neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return cluster
    
    def find_clusters_dfs(self, graph: SimilarityGraph) -> List[List[str]]:
        """
        Find clusters of similar submissions using DFS.
        
        Args:
            graph: Similarity graph
            
        Returns:
            List of clusters, where each cluster is a list of submission IDs
        """
        nodes = graph.get_nodes()
        visited = set()
        clusters = []
        
        # Use DFS to find connected components
        for node in nodes:
            if node in visited:
                continue
                
            # Start DFS from this node
            cluster = []
            self._dfs(graph, node, visited, cluster)
            
            # Only consider clusters with at least min_cluster_size nodes
            if len(cluster) >= self.min_cluster_size:
                clusters.append(cluster)
        
        return clusters
    
    def _dfs(self, graph: SimilarityGraph, node: str, visited: Set[str], cluster: List[str]) -> None:
        """
        Perform DFS to find a connected component.
        
        Args:
            graph: Similarity graph
            node: Current node
            visited: Set of already visited nodes
            cluster: List to store nodes in the connected component
        """
        if node in visited:
            return
            
        visited.add(node)
        cluster.append(node)
        
        # Visit all neighbors
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                self._dfs(graph, neighbor, visited, cluster)
    
    def find_clusters_with_threshold(self, graph: SimilarityGraph, threshold: float) -> List[List[str]]:
        """
        Find clusters of similar submissions using a custom threshold.
        
        Args:
            graph: Similarity graph
            threshold: Custom similarity threshold
            
        Returns:
            List of clusters, where each cluster is a list of submission IDs
        """
        # Create a new graph with the custom threshold
        custom_graph = SimilarityGraph(threshold)
        
        # Copy nodes and edges that meet the new threshold
        for node in graph.get_nodes():
            for neighbor, weight in graph.get_neighbors(node).items():
                if weight >= threshold:
                    custom_graph.add_edge(node, neighbor, weight)
        
        # Find clusters in the new graph
        return self.find_clusters(custom_graph)
    
    def hierarchical_clustering(self, graph: SimilarityGraph, thresholds: List[float]) -> Dict[float, List[List[str]]]:
        """
        Perform hierarchical clustering using multiple thresholds.
        
        Args:
            graph: Similarity graph
            thresholds: List of thresholds to use (in descending order)
            
        Returns:
            Dictionary mapping thresholds to clusters
        """
        results = {}
        
        # Sort thresholds in descending order
        sorted_thresholds = sorted(thresholds, reverse=True)
        
        for threshold in sorted_thresholds:
            clusters = self.find_clusters_with_threshold(graph, threshold)
            results[threshold] = clusters
        
        return results
