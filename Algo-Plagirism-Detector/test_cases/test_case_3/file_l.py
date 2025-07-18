"""
Group 1: File L - Similar to Files J and K with added comments and minor changes.
"""

def bubble_sort(data):
    """
    Implementation of bubble sort algorithm with extensive comments.
    
    Args:
        data: List to be sorted
        
    Returns:
        Sorted list
    """
    # Get the length of the array
    size = len(data)
    
    # Outer loop: traverse through all array elements
    for i in range(size):
        # Flag to optimize if no swaps occur in inner loop
        swapped = False
        
        # Inner loop: compare adjacent elements
        # Last i elements are already in place
        for j in range(0, size - i - 1):
            # Compare adjacent elements
            if data[j] > data[j + 1]:
                # Swap the elements if they are in wrong order
                data[j], data[j + 1] = data[j + 1], data[j]
                # Set flag to True to indicate a swap occurred
                swapped = True
        
        # If no swapping occurred in this pass, array is sorted
        if not swapped:
            break
    
    return data

def main():
    # Test the sorting algorithm
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_data)
    
    # Create a copy to avoid modifying the original
    sorted_data = bubble_sort(test_data.copy())
    print("Sorted array:", sorted_data)

if __name__ == "__main__":
    main()
