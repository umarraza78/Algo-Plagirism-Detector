"""
Group 1: File J - Sorting algorithm implementation.
"""

def bubble_sort(arr):
    """
    Implementation of bubble sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr

def main():
    # Test the sorting algorithm
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    
    sorted_array = bubble_sort(test_array.copy())
    print("Sorted array:", sorted_array)

if __name__ == "__main__":
    main()
