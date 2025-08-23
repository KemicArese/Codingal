import itertools

def digit_string_generator(min_len=6, max_len=20):
    digits = '0123456789'
    for length in range(min_len, max_len + 1):
        for combo in itertools.product(digits, repeat=length):
            yield ''.join(combo)

# Example: Print the first 5 combinations of length 6
gen = digit_string_generator()
for i, s in enumerate(gen):
    print(s)
    if i >= 10000000000000000000000000000000000000000000000000000000000000000000000000000000000:
        break