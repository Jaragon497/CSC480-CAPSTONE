# Testing Documentation

Simple and clean testing suite for the Logistics Management System.

## Test Structure

```
testing/
├── README.md          # This documentation
├── run_tests.py       # Test runner script
└── test_suite.py      # Main test suite
```

## Running Tests

### Using the Test Runner (Recommended)

```bash
# Run all tests
python testing/run_tests.py

# Show help
python testing/run_tests.py --help
```

### Running Tests Directly

```bash
# Run the test suite directly
python testing/test_suite.py

# Using unittest
python -m unittest testing.test_suite
```

## What Gets Tested

The test suite verifies core functionality:

### Basic Functionality Tests
- **Database Connection**: Ensures database connectivity works
- **Model Creation**: Tests that data models can be created properly
- **Database Operations**: Verifies facilities, alerts, and messages can be retrieved
- **Service Integration**: Checks that weather and traffic services don't crash

### Database Operation Tests
- **Facility Queries**: Tests getting facilities by ID
- **Alert Retrieval**: Verifies alert system functionality
- **Message System**: Tests message retrieval operations

## Test Output

When tests run successfully, you'll see:
```
test_database_connection (TestBasicFunctionality) ... ok
test_facility_model (TestBasicFunctionality) ... ok
...
All tests passed!
```

If there are failures, detailed error information will be shown.

## Adding New Tests

To add new tests, edit `test_suite.py`:

```python
class TestNewFeature(unittest.TestCase):
    """Test new functionality"""
    
    def test_new_feature(self):
        """Test description"""
        # Your test code here
        result = some_function()
        self.assertIsNotNone(result)
```

## Troubleshooting

- **Import Errors**: Make sure you're running from the project root directory
- **Database Errors**: The tests use the existing application database
- **Service Errors**: Mock service failures are expected and handled gracefully

The tests are designed to be simple and reliable, focusing on core functionality rather than complex edge cases.