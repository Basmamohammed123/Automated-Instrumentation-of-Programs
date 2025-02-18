def analyze_numbers(nums):
    """Processes a list of numbers, applying different operations based on conditions."""
    total = 0
    even_count = 0

    # Loop through the list
    for num in nums:
        if num % 2 == 0:
            even_count += 1  # Track even numbers
        else:
            total += num  # Sum of odd numbers
            if total > 10:
                break  # Stop if sum of odd numbers exceeds 10

    # While loop that runs under a condition
    i = 0
    while i < len(nums):
        if nums[i] < 0:
            total -= nums[i]  # Adjust for negative numbers
        i += 1

    # Final check
    if even_count > 2:
        total += 100  # Bonus if more than two even numbers

    return total











if __name__ == "__main__":
    print(analyze_numbers([1]))  # Sum of odd numbers stops at 10
    #print(analyze_numbers([2, 4, 6, 8]))  # More than 2 evens, adds 100
    #print(analyze_numbers([-2, -4, 3, 6]))  # Adjusts negatives, even count = 2

