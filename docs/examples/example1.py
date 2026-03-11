"""
This script demonstrates a simple greeting and addition function.

Functions:
    greet: Prints a greeting message.
    add_numbers: Returns the sum of two numbers.
"""

def greet():
    print("Hello, World!")

def add_numbers(a, b):
    return a + b

if __name__ == "__main__":
    greet()
    result = add_numbers(3, 5)
    print(f"The sum of 3 and 5 is {result}")
