import random
import string

def generate_complex_string(length=12):
    # Include letters, digits, and special characters
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly select characters
    result = ''.join(random.choice(characters) for _ in range(length))
    return result

# Example usage
print("Generated string:", generate_complex_string(20))