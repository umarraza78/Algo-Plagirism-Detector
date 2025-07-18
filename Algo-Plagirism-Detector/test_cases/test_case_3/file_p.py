"""
Unique file: File P - Quick sort implementation.
"""

def quick_sort(arr):
    """
    Implementation of quick sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Choose the pivot (using the middle element)
    pivot = arr[len(arr) // 2]
    
    # Partition the array
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Recursively sort the partitions and combine
    return quick_sort(left) + middle + quick_sort(right)

def main():
    # Test the quick sort algorithm
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    
    sorted_array = quick_sort(test_array)
    print("Sorted array:", sorted_array)

if __name__ == "__main__":
    main()
