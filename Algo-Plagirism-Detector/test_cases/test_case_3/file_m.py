"""
Group 2: File M - Binary search implementation.
"""

def binary_search(arr, target):
    """
    Implementation of binary search algorithm.
    
    Args:
        arr: Sorted list to search in
        target: Value to search for
        
    Returns:
        Index of the target if found, -1 otherwise
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
        
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        
        # If target is smaller, ignore right half
        else:
            right = mid - 1
    
    # Target is not present in the array
    return -1

def main():
    # Test the binary search algorithm
    test_array = [11, 12, 22, 25, 34, 64, 90]
    target = 22
    
    result = binary_search(test_array, target)
    
    if result != -1:
        print(f"Element {target} is present at index {result}")
    else:
        print(f"Element {target} is not present in the array")

if __name__ == "__main__":
    main()
