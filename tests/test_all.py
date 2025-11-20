"""
All Tests - Run all phases together

This file imports and runs all test phases in sequence.
Run with: python run_tests.py all
"""

import unittest
import sys

# Import all test modules
import test_phase1
import test_phase2
import test_phase3
import test_phase4
import test_phase5


def suite():
    """Create test suite with all phases"""
    test_suite = unittest.TestSuite()

    # Add each phase's tests
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_phase1))
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_phase2))
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_phase3))
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_phase4))
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_phase5))

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
