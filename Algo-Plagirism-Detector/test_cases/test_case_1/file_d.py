"""
Completely different code (calculates product).
"""

def calculate_product(numbers):
    """Calculate the product of a list of numbers."""
    if not numbers:
        return 0
    
    product = 1
    for num in numbers:
        product *= num
    return product

def display_result(numbers, result):
    """Display the result in a formatted way."""
    print(f"The product of {numbers} is {result}")

if __name__ == "__main__":
    # Test the function
    test_numbers = [1, 2, 3, 4, 5]
    result = calculate_product(test_numbers)
    display_result(test_numbers, result)
