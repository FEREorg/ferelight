#!/usr/bin/env python3
"""
Simple test script to verify that the ferelight package can be imported.
"""
import os
import sys

# Add the parent directory to the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import ferelight
    print("Successfully imported ferelight package.")
    print(f"Version: {ferelight.__version__ if hasattr(ferelight, '__version__') else 'unknown'}")
    print("Package seems to be correctly installed.")
except ImportError as e:
    print(f"Error importing ferelight: {e}")
    print("Package may not be correctly installed.")
    exit(1)
