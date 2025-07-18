"""
Slightly modified copy of File A (variable names changed).
"""

def compute_sum(array):
    """Calculate the sum of a list of numbers."""
    result = 0
    for element in array:
        result += element
    return result

if __name__ == "__main__":
    # Test the function
    sample_data = [1, 2, 3, 4, 5]
    output = compute_sum(sample_data)
    print(f"The sum of {sample_data} is {output}")
