#!/usr/bin/env python3
"""
Rabin-Karp Module
This module implements the Rabin-Karp algorithm for finding matching sequences in code.
"""

from typing import List, Set, Tuple, Dict
import hashlib

class RabinKarp:
    """
    Implementation of the Rabin-Karp algorithm for finding matching sequences in code.
    """
    
    def __init__(self, k_gram_size: int = 5):
        """
        Initialize the Rabin-Karp algorithm.
        
        Args:
            k_gram_size: Size of the k-grams (sequences) to compare
        """
        self.k_gram_size = k_gram_size
    
    def calculate_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """
        Calculate similarity between two token sequences using Rabin-Karp.
        
        Args:
            tokens1: First sequence of tokens
            tokens2: Second sequence of tokens
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        if not tokens1 or not tokens2:
            return 0.0
        
        # Generate k-grams and their hashes for both token sequences
        k_grams1 = self._generate_k_grams(tokens1)
        k_grams2 = self._generate_k_grams(tokens2)
        
        # Find matching k-grams
        matches = self._find_matches(k_grams1, k_grams2)
        
        # Calculate Jaccard similarity: |intersection| / |union|
        if not k_grams1 or not k_grams2:
            return 0.0
            
        union_size = len(k_grams1) + len(k_grams2) - len(matches)
        if union_size == 0:
            return 0.0
            
        return len(matches) / union_size
    
    def _generate_k_grams(self, tokens: List[str]) -> Dict[str, List[int]]:
        """
        Generate k-grams from a token sequence.
        
        Args:
            tokens: Sequence of tokens
            
        Returns:
            Dictionary mapping hash values to positions in the token sequence
        """
        k_grams = {}
        
        if len(tokens) < self.k_gram_size:
            return k_grams
        
        # Generate k-grams and their hash values
        for i in range(len(tokens) - self.k_gram_size + 1):
            k_gram = ' '.join(tokens[i:i+self.k_gram_size])
            hash_value = self._hash(k_gram)
            
            if hash_value not in k_grams:
                k_grams[hash_value] = []
            k_grams[hash_value].append(i)
        
        return k_grams
    
    def _hash(self, k_gram: str) -> str:
        """
        Hash a k-gram using MD5.
        
        Args:
            k_gram: String representation of a k-gram
            
        Returns:
            Hash value of the k-gram
        """
        return hashlib.md5(k_gram.encode()).hexdigest()
    
    def _find_matches(self, k_grams1: Dict[str, List[int]], k_grams2: Dict[str, List[int]]) -> Set[str]:
        """
        Find matching k-grams between two sequences.
        
        Args:
            k_grams1: K-grams from the first sequence
            k_grams2: K-grams from the second sequence
            
        Returns:
            Set of hash values of matching k-grams
        """
        matches = set()
        
        # Find hash values that appear in both sequences
        for hash_value in k_grams1:
            if hash_value in k_grams2:
                matches.add(hash_value)
        
        return matches
    
    def find_matching_sequences(self, tokens1: List[str], tokens2: List[str]) -> List[Tuple[int, int, int]]:
        """
        Find matching sequences between two token sequences.
        
        Args:
            tokens1: First sequence of tokens
            tokens2: Second sequence of tokens
            
        Returns:
            List of tuples (pos1, pos2, length) where pos1 is the position in tokens1,
            pos2 is the position in tokens2, and length is the length of the match
        """
        if not tokens1 or not tokens2:
            return []
        
        # Generate k-grams and their hashes for both token sequences
        k_grams1 = self._generate_k_grams(tokens1)
        k_grams2 = self._generate_k_grams(tokens2)
        
        # Find matching k-grams and extend them
        matches = []
        for hash_value in k_grams1:
            if hash_value in k_grams2:
                for pos1 in k_grams1[hash_value]:
                    for pos2 in k_grams2[hash_value]:
                        # Verify the match (in case of hash collision)
                        if tokens1[pos1:pos1+self.k_gram_size] == tokens2[pos2:pos2+self.k_gram_size]:
                            # Try to extend the match
                            length = self._extend_match(tokens1, tokens2, pos1, pos2)
                            matches.append((pos1, pos2, length))
        
        # Merge overlapping matches
        return self._merge_overlapping_matches(matches)
    
    def _extend_match(self, tokens1: List[str], tokens2: List[str], pos1: int, pos2: int) -> int:
        """
        Extend a match as far as possible.
        
        Args:
            tokens1: First sequence of tokens
            tokens2: Second sequence of tokens
            pos1: Starting position in tokens1
            pos2: Starting position in tokens2
            
        Returns:
            Length of the extended match
        """
        # Start with the k-gram size
        length = self.k_gram_size
        
        # Extend forward
        while (pos1 + length < len(tokens1) and 
               pos2 + length < len(tokens2) and 
               tokens1[pos1 + length] == tokens2[pos2 + length]):
            length += 1
        
        return length
    
    def _merge_overlapping_matches(self, matches: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """
        Merge overlapping matches.
        
        Args:
            matches: List of matches (pos1, pos2, length)
            
        Returns:
            List of merged matches
        """
        if not matches:
            return []
        
        # Sort matches by position in the first sequence
        sorted_matches = sorted(matches, key=lambda m: (m[0], m[1]))
        
        merged = []
        current = sorted_matches[0]
        
        for match in sorted_matches[1:]:
            pos1, pos2, length = match
            curr_pos1, curr_pos2, curr_length = current
            
            # Check if matches overlap
            if (pos1 < curr_pos1 + curr_length and 
                pos2 < curr_pos2 + curr_length):
                # Extend current match if needed
                new_length = max(curr_length, pos1 - curr_pos1 + length)
                current = (curr_pos1, curr_pos2, new_length)
            else:
                merged.append(current)
                current = match
        
        merged.append(current)
        return merged
