"""
Example usage of the error learner package.
"""

from error_learner import track

def test_demo_example():
    """Test the example from the demo."""
    @track
    def generate_errors():
        # Will be tracked extra carefully
        return 1/0  # First run: records error
                    # Third run: suggests fix!

    # Run the function multiple times to test error tracking
    for _ in range(3):
        try:
            generate_errors()
        except ZeroDivisionError:
            pass
        else:
            assert False, "Expected ZeroDivisionError" 