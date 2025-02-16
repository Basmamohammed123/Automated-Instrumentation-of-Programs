def process_numbers(numbers):
    """Processes a list of numbers. Returns the sum of positive numbers or a message if the list is empty."""
    if not numbers:
        print("No numbers to process.")
        return 0

    total = 0
    i = 0
    while i < len(numbers):
        if numbers[i] > 0:
            total += numbers[i]
        i += 1

    return total

if __name__ == "__main__":
    process_numbers([1, -2, 3, 4])  # Covers the while loop and if condition
    process_numbers([])            # Covers the empty list check
