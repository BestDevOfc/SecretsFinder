import os
import re
import math
from collections import Counter


class FindEntropies(object):
    def __init__(self) -> None:
        ...

    def calculate_entropy(self, string: str):
        """Calculate the Shannon entropy of a string."""
        if not string:
            return 0
            
        probabilities = [count / len(string) for count in Counter(string).values()]
        return -sum(p * math.log2(p) for p in probabilities)

    def is_high_entropy(self, string, min_length=8, min_entropy=4.0):
        """Check if a string is high-entropy based on length and entropy score."""
        return len(string) >= min_length and self.calculate_entropy(string) >= min_entropy

    def extract_high_entropy_strings(self, file_path):
        """Extract high-entropy strings from a file."""
        high_entropy_strings = []
        
        with open(file_path, 'r', errors='ignore') as file:
            for line in file:
                # Find all strings of length >= 8 (you can adjust this as needed)
                strings = re.findall(r'\S{8,}', line)
                for string in strings:
                    if self.is_high_entropy(string):
                        high_entropy_strings.append(string)

        return high_entropy_strings
