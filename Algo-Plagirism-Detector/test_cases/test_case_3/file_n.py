"""
Group 2: File N - Similar to File M with minor changes.
"""

def binary_search(numbers, value):
    """
    Implementation of binary search algorithm with different variable names.
    
    Args:
        numbers: Sorted list to search in
        value: Value to search for
        
    Returns:
        Index of the value if found, -1 otherwise
    """
    start = 0
    end = len(numbers) - 1
    
    while start <= end:
        middle = (start + end) // 2
        
        # Check if value is present at middle
        if numbers[middle] == value:
            return middle
        
        # If value is greater, ignore left half
        elif numbers[middle] < value:
            start = middle + 1
        
        # If value is smaller, ignore right half
        else:
            end = middle - 1
    
    # Value is not present in the array
    return -1

def main():
    # Test the binary search algorithm with different test data
    sorted_array = [11, 12, 22, 25, 34, 64, 90]
    search_value = 25
    
    index = binary_search(sorted_array, search_value)
    
    if index != -1:
        print(f"Element {search_value} is present at index {index}")
    else:
        print(f"Element {search_value} is not present in the array")

if __name__ == "__main__":
    main()
