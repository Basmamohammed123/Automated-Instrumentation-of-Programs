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


def reverse_string(s: str) -> str:
    """Reverse the order of characters in a string."""
    return s[::-1]

# Test Cases:
# Input: "hello" → Output: "olleh"
# Input: "a" → Output: "a"
# Input: "" → Output: ""
# Input: "racecar" → Output: "racecar"

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

# Test Cases:
# Input: 7 → Output: True
# Input: 4 → Output: False
# Input: 1 → Output: False
# Input: 2 → Output: True


def get_quadrant(x: float, y: float) -> str:
    """Identify which quadrant a point lies in."""
    if x == 0 or y == 0:
        return "On axis"
    elif x > 0:
        return "Quadrant I" if y > 0 else "Quadrant IV"
    else:
        return "Quadrant II" if y > 0 else "Quadrant III"

# Test Cases:
# Input: (3, 4) → Output: "Quadrant I"
# Input: (-2, 5) → Output: "Quadrant II"
# Input: (0, 0) → Output: "On axis"
# Input: (4, -1) → Output: "Quadrant IV"


if __name__ == "__main__":
   # print(analyze_numbers([1]))  # Sum of odd numbers stops at 10
    #print(analyze_numbers([2, 4, 6, 8]))  # More than 2 evens, adds 100
    print(analyze_numbers([-2, -4, 3, 6]))  # Adjusts negatives, even count = 2
    print(reverse_string("hello"))
    print(is_prime(7))
    print(get_quadrant(3, 4))

