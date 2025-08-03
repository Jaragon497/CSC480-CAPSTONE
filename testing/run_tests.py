#!/usr/bin/env python3
# run_tests.py - Test runner for the logistics management system
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests():
    """Run the main test suite"""
    try:
        from testing.test_suite import run_simple_tests
        return run_simple_tests()
    except ImportError as e:
        print(f"Error importing test suite: {e}")
        return 1

def main():
    """Main test runner function"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h', 'help']:
            print("Logistics Management System Test Runner")
            print("Usage: python testing/run_tests.py [options]")
            print("")
            print("Options:")
            print("  --help, -h    Show this help message")
            print("  (no args)     Run all tests")
            print("")
            print("Examples:")
            print("  python testing/run_tests.py")
            print("  python testing/test_suite.py    # Run tests directly")
            return 0
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
            return 1
    
    print("Running Logistics Management System Tests...")
    print("=" * 50)
    return run_tests()

if __name__ == '__main__':
    sys.exit(main())