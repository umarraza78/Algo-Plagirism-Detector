#!/usr/bin/env python3
"""
B+ Tree Module
This module implements a B+ Tree for efficient metadata storage and retrieval.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

class BPlusTreeNode:
    """Base class for B+ Tree nodes."""
    
    def __init__(self, order: int):
        """
        Initialize a B+ Tree node.
        
        Args:
            order: Order of the B+ Tree
        """
        self.order = order
        self.keys = []
        self.parent = None
    
    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf node.
        
        Returns:
            True if the node is a leaf node, False otherwise
        """
        return isinstance(self, BPlusTreeLeafNode)

class BPlusTreeLeafNode(BPlusTreeNode):
    """Leaf node in a B+ Tree."""
    
    def __init__(self, order: int):
        """
        Initialize a leaf node.
        
        Args:
            order: Order of the B+ Tree
        """
        super().__init__(order)
        self.values = []  # Values corresponding to keys
        self.next_leaf = None  # Pointer to the next leaf node
    
    def insert(self, key: str, value: Any) -> Optional[Tuple[str, 'BPlusTreeNode', 'BPlusTreeNode']]:
        """
        Insert a key-value pair into the leaf node.
        
        Args:
            key: Key to insert
            value: Value to associate with the key
            
        Returns:
            None if no split occurred, or a tuple (median_key, left_node, right_node) if split occurred
        """
        # Find the position to insert the key
        i = 0
        while i < len(self.keys) and self.keys[i] < key:
            i += 1
        
        # If the key already exists, update the value
        if i < len(self.keys) and self.keys[i] == key:
            self.values[i] = value
            return None
        
        # Insert the key and value at position i
        self.keys.insert(i, key)
        self.values.insert(i, value)
        
        # If the node is not full, we're done
        if len(self.keys) <= self.order - 1:
            return None
        
        # Otherwise, split the node
        median = len(self.keys) // 2
        
        # Create a new leaf node
        new_node = BPlusTreeLeafNode(self.order)
        new_node.keys = self.keys[median:]
        new_node.values = self.values[median:]
        new_node.next_leaf = self.next_leaf
        self.next_leaf = new_node
        
        # Update this node
        self.keys = self.keys[:median]
        self.values = self.values[:median]
        
        # Return the median key and the two nodes
        return (new_node.keys[0], self, new_node)
    
    def search(self, key: str) -> Optional[Any]:
        """
        Search for a key in the leaf node.
        
        Args:
            key: Key to search for
            
        Returns:
            Value associated with the key, or None if the key is not found
        """
        for i, k in enumerate(self.keys):
            if k == key:
                return self.values[i]
        return None

class BPlusTreeInternalNode(BPlusTreeNode):
    """Internal node in a B+ Tree."""
    
    def __init__(self, order: int):
        """
        Initialize an internal node.
        
        Args:
            order: Order of the B+ Tree
        """
        super().__init__(order)
        self.children = []  # Child nodes
    
    def insert(self, key: str, left_child: BPlusTreeNode, right_child: BPlusTreeNode) -> Optional[Tuple[str, 'BPlusTreeNode', 'BPlusTreeNode']]:
        """
        Insert a key and children into the internal node.
        
        Args:
            key: Key to insert
            left_child: Left child node
            right_child: Right child node
            
        Returns:
            None if no split occurred, or a tuple (median_key, left_node, right_node) if split occurred
        """
        # Find the position to insert the key
        i = 0
        while i < len(self.keys) and self.keys[i] < key:
            i += 1
        
        # Insert the key and right child
        self.keys.insert(i, key)
        self.children.insert(i + 1, right_child)
        
        # Set parent pointers
        left_child.parent = self
        right_child.parent = self
        
        # If the node is not full, we're done
        if len(self.keys) <= self.order - 1:
            return None
        
        # Otherwise, split the node
        median = len(self.keys) // 2
        median_key = self.keys[median]
        
        # Create a new internal node
        new_node = BPlusTreeInternalNode(self.order)
        new_node.keys = self.keys[median + 1:]
        new_node.children = self.children[median + 1:]
        
        # Update parent pointers for the children of the new node
        for child in new_node.children:
            child.parent = new_node
        
        # Update this node
        self.keys = self.keys[:median]
        self.children = self.children[:median + 1]
        
        # Return the median key and the two nodes
        return (median_key, self, new_node)
    
    def search(self, key: str) -> BPlusTreeNode:
        """
        Search for the child node that should contain the key.
        
        Args:
            key: Key to search for
            
        Returns:
            Child node that should contain the key
        """
        i = 0
        while i < len(self.keys) and key >= self.keys[i]:
            i += 1
        return self.children[i]

class BPlusTree:
    """
    B+ Tree implementation for efficient metadata storage and retrieval.
    """
    
    def __init__(self, order: int = 4):
        """
        Initialize a B+ Tree.
        
        Args:
            order: Order of the B+ Tree (must be at least 3)
        """
        self.order = max(3, order)  # Ensure order is at least 3
        self.root = BPlusTreeLeafNode(self.order)
    
    def insert(self, key: str, value: Any) -> None:
        """
        Insert a key-value pair into the B+ Tree.
        
        Args:
            key: Key to insert
            value: Value to associate with the key
        """
        # Find the leaf node where the key should be inserted
        leaf = self._find_leaf(key)
        
        # Insert the key-value pair into the leaf node
        result = leaf.insert(key, value)
        
        # If the leaf node was split, update the tree
        if result:
            median_key, left_node, right_node = result
            
            # If the leaf node was the root, create a new root
            if leaf == self.root:
                new_root = BPlusTreeInternalNode(self.order)
                new_root.keys = [median_key]
                new_root.children = [left_node, right_node]
                left_node.parent = new_root
                right_node.parent = new_root
                self.root = new_root
            else:
                # Otherwise, insert the median key into the parent node
                self._insert_in_parent(leaf.parent, median_key, left_node, right_node)
    
    def _insert_in_parent(self, parent: BPlusTreeInternalNode, key: str, left_child: BPlusTreeNode, right_child: BPlusTreeNode) -> None:
        """
        Insert a key and children into a parent node.
        
        Args:
            parent: Parent node
            key: Key to insert
            left_child: Left child node
            right_child: Right child node
        """
        # Insert the key and children into the parent node
        result = parent.insert(key, left_child, right_child)
        
        # If the parent node was split, update the tree
        if result:
            median_key, left_node, right_node = result
            
            # If the parent node was the root, create a new root
            if parent == self.root:
                new_root = BPlusTreeInternalNode(self.order)
                new_root.keys = [median_key]
                new_root.children = [left_node, right_node]
                left_node.parent = new_root
                right_node.parent = new_root
                self.root = new_root
            else:
                # Otherwise, insert the median key into the grandparent node
                self._insert_in_parent(parent.parent, median_key, left_node, right_node)
    
    def search(self, key: str) -> Optional[Any]:
        """
        Search for a key in the B+ Tree.
        
        Args:
            key: Key to search for
            
        Returns:
            Value associated with the key, or None if the key is not found
        """
        leaf = self._find_leaf(key)
        return leaf.search(key)
    
    def _find_leaf(self, key: str) -> BPlusTreeLeafNode:
        """
        Find the leaf node where a key should be located.
        
        Args:
            key: Key to search for
            
        Returns:
            Leaf node where the key should be located
        """
        node = self.root
        
        # Traverse the tree until we reach a leaf node
        while not node.is_leaf():
            node = node.search(key)
        
        return node
    
    def range_search(self, start_key: str, end_key: str) -> List[Tuple[str, Any]]:
        """
        Search for all keys in a range.
        
        Args:
            start_key: Start of the range (inclusive)
            end_key: End of the range (inclusive)
            
        Returns:
            List of (key, value) pairs in the range
        """
        results = []
        
        # Find the leaf node where the start key should be located
        leaf = self._find_leaf(start_key)
        
        # Traverse the leaf nodes until we find the end key or run out of nodes
        while leaf:
            # Check each key in the current leaf node
            for i, key in enumerate(leaf.keys):
                if start_key <= key <= end_key:
                    results.append((key, leaf.values[i]))
                elif key > end_key:
                    return results
            
            # Move to the next leaf node
            leaf = leaf.next_leaf
        
        return results
