"""
Group 1: File K - Similar to File J with minor changes.
"""

def bubble_sort(numbers):
    """
    Implementation of bubble sort algorithm with different variable names.
    
    Args:
        numbers: List to be sorted
        
    Returns:
        Sorted list
    """
    length = len(numbers)
    
    # Traverse through all array elements
    for i in range(length):
        # Last i elements are already in place
        for j in range(0, length - i - 1):
            # Traverse the array from 0 to length-i-1
            # Swap if the element found is greater than the next element
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    
    return numbers

def main():
    # Test the sorting algorithm with different test data
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_data)
    
    result = bubble_sort(test_data.copy())
    print("Sorted array:", result)

if __name__ == "__main__":
    main()
