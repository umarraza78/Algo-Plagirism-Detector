#!/usr/bin/env python3
"""
Code Parser Module
This module handles parsing code files into tokens for comparison.
"""

import re
import os
from typing import List, Dict, Set, Tuple

class CodeParser:
    """
    Parser for code files that converts them into tokens for comparison.
    """

    # Common keywords across programming languages
    COMMON_KEYWORDS = {
        'if', 'else', 'for', 'while', 'return', 'function', 'class', 'def',
        'int', 'float', 'string', 'bool', 'true', 'false', 'null', 'None',
        'public', 'private', 'protected', 'static', 'void', 'import', 'from'
    }

    # Regex patterns for different languages
    LANGUAGE_PATTERNS = {
        'python': {
            'comment': r'#.*?$|""".*?"""|\'\'\'.*?\'\'\'',
            'string': r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
            'token': r'[A-Za-z_][A-Za-z0-9_]*|\d+|\S'
        },
        'java': {
            'comment': r'//.*?$|/\*.*?\*/',
            'string': r'"(?:\\.|[^"\\])*"',
            'token': r'[A-Za-z_][A-Za-z0-9_]*|\d+|\S'
        },
        'cpp': {
            'comment': r'//.*?$|/\*.*?\*/',
            'string': r'"(?:\\.|[^"\\])*"',
            'token': r'[A-Za-z_][A-Za-z0-9_]*|\d+|\S'
        },
        'javascript': {
            'comment': r'//.*?$|/\*.*?\*/',
            'string': r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`',
            'token': r'[A-Za-z_][A-Za-z0-9_]*|\d+|\S'
        }
    }

    def __init__(self):
        """Initialize the code parser."""
        # Compile regex patterns for better performance
        self.compiled_patterns = {}
        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            self.compiled_patterns[lang] = {
                'comment': re.compile(patterns['comment'], re.MULTILINE | re.DOTALL),
                'string': re.compile(patterns['string'], re.MULTILINE | re.DOTALL),
                'token': re.compile(patterns['token'])
            }

    def detect_language(self, file_path: str) -> str:
        """
        Detect the programming language based on file extension.

        Args:
            file_path: Path to the code file

        Returns:
            Language identifier or 'generic' if unknown
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext in ['.py']:
            return 'python'
        elif ext in ['.java']:
            return 'java'
        elif ext in ['.cpp', '.c', '.h', '.hpp']:
            return 'cpp'
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            return 'javascript'
        else:
            return 'generic'

    def parse_file(self, file_path: str) -> List[str]:
        """
        Parse a code file into a list of tokens.

        Args:
            file_path: Path to the code file

        Returns:
            List of tokens representing the code
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            language = self.detect_language(file_path)

            # Use block-insensitive tokenization for Python files
            if language == 'python':
                return self.tokenize_block_insensitive(content, language)
            else:
                return self.tokenize(content, language)
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return []

    def tokenize_block_insensitive(self, code: str, language: str = 'python') -> List[str]:
        """
        Tokenize code content in a way that is insensitive to block order.
        This helps detect plagiarism even when code blocks are moved around.

        Args:
            code: Code content as string
            language: Programming language identifier

        Returns:
            List of tokens representing the code, sorted to be insensitive to block order
        """
        # First, tokenize the code normally
        tokens = self.tokenize(code, language)

        # Extract function and class definitions
        blocks = self._extract_blocks(tokens)

        # Sort blocks by their content to make the comparison insensitive to block order
        sorted_blocks = sorted(blocks, key=lambda b: ''.join(b))

        # Flatten the sorted blocks back into a single token list
        flattened_tokens = []
        for block in sorted_blocks:
            flattened_tokens.extend(block)

        return flattened_tokens

    def _extract_blocks(self, tokens: List[str]) -> List[List[str]]:
        """
        Extract code blocks (functions, classes, etc.) from a token list.

        Args:
            tokens: List of tokens

        Returns:
            List of blocks, where each block is a list of tokens
        """
        blocks = []
        current_block = []
        block_level = 0

        for token in tokens:
            # Start a new block on class or function definition
            if token in ['class', 'def']:
                if block_level == 0:
                    # If we were already collecting a block, add it to the list
                    if current_block:
                        blocks.append(current_block)
                    current_block = [token]
                else:
                    current_block.append(token)
                block_level += 1
            # Track block nesting level
            elif token == '{':
                current_block.append(token)
                block_level += 1
            elif token == '}':
                current_block.append(token)
                block_level -= 1
                # End of a top-level block
                if block_level == 0 and current_block:
                    blocks.append(current_block)
                    current_block = []
            # Add token to current block
            else:
                current_block.append(token)

        # Add the last block if there is one
        if current_block:
            blocks.append(current_block)

        return blocks

    def tokenize(self, code: str, language: str = 'generic') -> List[str]:
        """
        Tokenize code content.

        Args:
            code: Code content as string
            language: Programming language identifier

        Returns:
            List of tokens
        """
        # Use language-specific patterns if available, otherwise use Python patterns
        patterns = self.compiled_patterns.get(language, self.compiled_patterns['python'])

        # Remove comments
        code = patterns['comment'].sub('', code)

        # Replace strings with a placeholder to avoid tokenizing their contents
        strings = []

        def replace_string(match):
            strings.append(match.group(0))
            return 'STRING_LITERAL'

        code = patterns['string'].sub(replace_string, code)

        # Tokenize the code
        tokens = patterns['token'].findall(code)

        # Normalize tokens: convert variable names to placeholders but keep structure
        normalized_tokens = []
        var_map = {}  # Map original variable names to normalized names
        var_counter = 0

        for token in tokens:
            # Skip whitespace
            if token.isspace() or not token:
                continue

            # Keep keywords, operators, and punctuation as is
            if (token in self.COMMON_KEYWORDS or
                not token[0].isalpha() or
                token == 'STRING_LITERAL'):
                normalized_tokens.append(token)
            # Normalize variable and function names
            elif token[0].isalpha() or token[0] == '_':
                if token not in var_map:
                    var_map[token] = f"VAR_{var_counter}"
                    var_counter += 1
                normalized_tokens.append(var_map[token])
            # Keep numbers and other tokens as is
            else:
                normalized_tokens.append(token)

        return normalized_tokens
