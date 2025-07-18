#!/usr/bin/env python3
"""
Similarity Graph Module
This module implements a graph representation of code similarity.
"""

from typing import Dict, List, Set, Tuple, Any

class SimilarityGraph:
    """
    Graph representation of code similarity where nodes are submissions
    and edges represent similarity between submissions.
    """
    
    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize the similarity graph.
        
        Args:
            similarity_threshold: Threshold for considering two submissions similar (0.0 to 1.0)
        """
        self.graph = {}  # Adjacency list representation
        self.similarity_threshold = similarity_threshold
    
    def add_node(self, node_id: str) -> None:
        """
        Add a node to the graph.
        
        Args:
            node_id: Unique identifier for the node
        """
        if node_id not in self.graph:
            self.graph[node_id] = {}
    
    def add_edge(self, node1: str, node2: str, weight: float) -> None:
        """
        Add an edge between two nodes with a given weight.
        
        Args:
            node1: First node
            node2: Second node
            weight: Edge weight (similarity score)
        """
        # Only add edge if weight is above threshold
        if weight < self.similarity_threshold:
            return
            
        # Add nodes if they don't exist
        self.add_node(node1)
        self.add_node(node2)
        
        # Add edges in both directions (undirected graph)
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight
    
    def get_neighbors(self, node: str) -> Dict[str, float]:
        """
        Get all neighbors of a node.
        
        Args:
            node: Node to get neighbors for
            
        Returns:
            Dictionary mapping neighbor node IDs to edge weights
        """
        if node not in self.graph:
            return {}
        return self.graph[node]
    
    def get_nodes(self) -> List[str]:
        """
        Get all nodes in the graph.
        
        Returns:
            List of node IDs
        """
        return list(self.graph.keys())
    
    def get_edge_weight(self, node1: str, node2: str) -> float:
        """
        Get the weight of an edge between two nodes.
        
        Args:
            node1: First node
            node2: Second node
            
        Returns:
            Edge weight or 0.0 if no edge exists
        """
        if node1 not in self.graph or node2 not in self.graph[node1]:
            return 0.0
        return self.graph[node1][node2]
    
    def remove_node(self, node: str) -> None:
        """
        Remove a node and all its edges from the graph.
        
        Args:
            node: Node to remove
        """
        if node not in self.graph:
            return
            
        # Remove edges to this node from all neighbors
        for neighbor in self.graph[node]:
            if node in self.graph[neighbor]:
                del self.graph[neighbor][node]
        
        # Remove the node
        del self.graph[node]
    
    def get_average_similarity(self, node: str) -> float:
        """
        Calculate the average similarity between a node and its neighbors.
        
        Args:
            node: Node to calculate average similarity for
            
        Returns:
            Average similarity or 0.0 if the node has no neighbors
        """
        if node not in self.graph or not self.graph[node]:
            return 0.0
            
        total_similarity = sum(self.graph[node].values())
        return total_similarity / len(self.graph[node])
    
    def get_subgraph(self, nodes: List[str]) -> 'SimilarityGraph':
        """
        Create a subgraph containing only the specified nodes.
        
        Args:
            nodes: List of nodes to include in the subgraph
            
        Returns:
            New SimilarityGraph instance representing the subgraph
        """
        subgraph = SimilarityGraph(self.similarity_threshold)
        
        for node in nodes:
            if node in self.graph:
                for neighbor, weight in self.graph[node].items():
                    if neighbor in nodes:
                        subgraph.add_edge(node, neighbor, weight)
        
        return subgraph
    
    def to_adjacency_matrix(self) -> Tuple[List[str], List[List[float]]]:
        """
        Convert the graph to an adjacency matrix representation.
        
        Returns:
            Tuple of (node_ids, matrix) where node_ids is a list of node IDs
            and matrix is a 2D list representing the adjacency matrix
        """
        nodes = self.get_nodes()
        n = len(nodes)
        
        # Create a mapping from node IDs to indices
        node_to_index = {node: i for i, node in enumerate(nodes)}
        
        # Initialize the matrix with zeros
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Fill in the matrix
        for i, node1 in enumerate(nodes):
            for node2, weight in self.graph[node1].items():
                j = node_to_index[node2]
                matrix[i][j] = weight
        
        return nodes, matrix
