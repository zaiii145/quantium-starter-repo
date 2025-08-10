#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate virtual environment (adjust path if your venv is in a different location)
source venv/Scripts/activate

# Run the test suite with pytest
pytest -v -W ignore::DeprecationWarning test.py

# Store pytest exit code
RESULT=$?

# Deactivate virtual environment
deactivate

# Exit with 0 if all tests passed, otherwise 1
if [ $RESULT -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed!"
    exit 1
fi
