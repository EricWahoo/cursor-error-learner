"""
Demo application showing how the error tracker works in practice.
"""

import logging
from error_learner.extension import tracker

# Set up logging to see the suggestions
logging.basicConfig(level=logging.INFO)

def process_user_data(user_dict):
    """Process user data with potential errors."""
    # This might raise KeyError
    name = user_dict['name']
    
    # This might raise ZeroDivisionError
    age = user_dict.get('age', 0)
    if age == 0:
        age_ratio = 0  # Default value when age is 0
    else:
        age_ratio = 100 / age
    
    # This might raise TypeError
    score = user_dict.get('score', '0') + 10
    
    return f"{name} has ratio {age_ratio} and score {score}"

def main():
    """Run the demo with various error cases."""
    # Case 1: KeyError
    try:
        process_user_data({})
    except Exception as e:
        print(f"Error 1: {e}")
    
    # Case 2: ZeroDivisionError
    try:
        process_user_data({'name': 'John', 'age': 0})
    except Exception as e:
        print(f"Error 2: {e}")
    
    # Case 3: TypeError
    try:
        process_user_data({'name': 'John', 'age': 25, 'score': '95'})
    except Exception as e:
        print(f"Error 3: {e}")
    
    # Repeat to trigger suggestions
    for _ in range(2):
        try:
            process_user_data({})
        except Exception as e:
            print(f"Repeated error: {e}")

if __name__ == "__main__":
    main() 