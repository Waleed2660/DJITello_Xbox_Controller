import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def suppress_stdout():
    # Create a StringIO object to capture stdout
    new_stdout = StringIO()
    # Store the original stdout
    old_stdout = sys.stdout
    # Replace stdout with the new StringIO object
    sys.stdout = new_stdout
    try:
        yield new_stdout
    finally:
        # Restore the original stdout
        sys.stdout = old_stdout
