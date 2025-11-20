#!/usr/bin/env python3
"""
Meeting Service Test Runner

Usage:
    python run_tests.py phase1      # Run Phase 1 tests only
    python run_tests.py phase2      # Run Phase 2 tests only
    python run_tests.py phase3      # Run Phase 3 tests only
    python run_tests.py phase4      # Run Phase 4 tests only
    python run_tests.py phase5      # Run Phase 5 tests only
    python run_tests.py all         # Run all tests

Examples:
    python run_tests.py phase1
    python run_tests.py all
"""

import sys
import unittest
import importlib

# Phase mapping
PHASES = {
    'phase1': ('tests.test_phase1', 'Phase 1: Pydantic Models'),
    'phase2': ('tests.test_phase2', 'Phase 2: CRUD Operations'),
    'phase3': ('tests.test_phase3', 'Phase 3: Availability Algorithm'),
    'phase4': ('tests.test_phase4', 'Phase 4: Pre-Meeting Prep'),
    'phase5': ('tests.test_phase5', 'Phase 5: Error Handling'),
}


def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def run_phase(phase_name):
    """Run tests for a specific phase"""
    if phase_name == 'all':
        return run_all_phases()

    if phase_name not in PHASES:
        print(f"❌ Unknown phase: {phase_name}")
        print(f"\nAvailable phases: {', '.join(PHASES.keys())}, all")
        return 1

    module_name, phase_title = PHASES[phase_name]

    print_banner(phase_title)

    try:
        # Import the test module
        module = importlib.import_module(module_name)

        # Load and run tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        # Print summary
        print("\n" + "=" * 70)
        if result.wasSuccessful():
            print(f"✅ {phase_name.upper()} - ALL TESTS PASSED ({result.testsRun} tests)")
        else:
            print(f"❌ {phase_name.upper()} - SOME TESTS FAILED")
            print(f"   Tests run: {result.testsRun}")
            print(f"   Failures: {len(result.failures)}")
            print(f"   Errors: {len(result.errors)}")
        print("=" * 70 + "\n")

        return 0 if result.wasSuccessful() else 1

    except ImportError as e:
        print(f"❌ Error importing {module_name}: {e}")
        print(f"   Make sure {module_name}.py exists and has no syntax errors")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def run_all_phases():
    """Run all phase tests in sequence"""
    print_banner("Running All Phases")

    results = {}
    total_tests = 0
    total_failures = 0
    total_errors = 0

    for phase_name in PHASES.keys():
        module_name, phase_title = PHASES[phase_name]

        print(f"\n{'─' * 70}")
        print(f"  {phase_title}")
        print(f"{'─' * 70}\n")

        try:
            module = importlib.import_module(module_name)
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)
            runner = unittest.TextTestRunner(verbosity=1)
            result = runner.run(suite)

            results[phase_name] = result.wasSuccessful()
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)

            if result.wasSuccessful():
                print(f"✅ {phase_name}: PASSED ({result.testsRun} tests)")
            else:
                print(f"❌ {phase_name}: FAILED ({len(result.failures)} failures, {len(result.errors)} errors)")

        except Exception as e:
            print(f"❌ {phase_name}: ERROR - {e}")
            results[phase_name] = False

    # Final summary
    print_banner("FINAL SUMMARY")

    for phase_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {phase_name}: {status}")

    print(f"\n  Total tests run: {total_tests}")
    print(f"  Total failures: {total_failures}")
    print(f"  Total errors: {total_errors}")

    all_passed = all(results.values())
    print(f"\n  Overall: {'✅ ALL PHASES PASSED' if all_passed else '❌ SOME PHASES FAILED'}")
    print("=" * 70 + "\n")

    return 0 if all_passed else 1


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <phase>")
        print(f"\nAvailable phases:")
        for phase, (_, title) in PHASES.items():
            print(f"  {phase:10} - {title}")
        print(f"  {'all':10} - Run all phases")
        print("\nExample:")
        print("  python run_tests.py phase1")
        print("  python run_tests.py all")
        return 1

    phase = sys.argv[1].lower()
    return run_phase(phase)


if __name__ == '__main__':
    sys.exit(main())
