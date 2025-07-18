"""
Unique file: File O - Merge sort implementation.
"""

def merge_sort(arr):
    """
    Implementation of merge sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Divide the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Recursively sort both halves
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)
    
    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left, right):
    """
    Merge two sorted lists.
    
    Args:
        left: First sorted list
        right: Second sorted list
        
    Returns:
        Merged sorted list
    """
    result = []
    i = j = 0
    
    # Compare elements from both lists and add the smaller one to the result
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements from left list
    while i < len(left):
        result.append(left[i])
        i += 1
    
    # Add remaining elements from right list
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result

def main():
    # Test the merge sort algorithm
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    
    sorted_array = merge_sort(test_array)
    print("Sorted array:", sorted_array)

if __name__ == "__main__":
    main()
