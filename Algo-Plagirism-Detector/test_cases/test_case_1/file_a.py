"""
Original simple code that calculates sum.
"""

def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total

if __name__ == "__main__":
    # Test the function
    test_numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(test_numbers)
    print(f"The sum of {test_numbers} is {result}")
