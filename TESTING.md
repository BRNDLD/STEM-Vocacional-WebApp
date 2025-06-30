# Testing Guide for STEM Vocacional WebApp

This document provides comprehensive information about the testing infrastructure implemented for the STEM Vocacional WebApp.

## Overview

The testing system includes:
- **Backend Testing**: Unit and integration tests for Flask API using pytest
- **Frontend Testing**: Component and service tests for React app using Jest
- **Coverage Reporting**: Automated coverage analysis
- **CI/CD Integration**: Automated testing in GitHub Actions

## Backend Testing (Flask + pytest)

### Setup

1. Install test dependencies:
   ```bash
   cd backend-flask
   pip install -r requirements-test.txt
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. Run with coverage:
   ```bash
   pytest --cov=app --cov-report=html
   ```

### Test Structure

```
backend-flask/
├── tests/
│   ├── conftest.py          # Test configuration and fixtures
│   ├── test_app.py          # Test application factory
│   ├── test_models/         # Model unit tests
│   │   ├── test_usuario.py
│   │   ├── test_cognitiva.py
│   │   ├── test_educativa_familiar.py
│   │   ├── test_socioeconomica.py
│   │   └── test_autoeficacia.py
│   ├── test_routes/         # API route integration tests
│   │   ├── test_usuario_routes.py
│   │   └── test_cognitiva_routes.py
│   └── test_integration/    # Full workflow tests
│       └── test_api_integration.py
├── pytest.ini              # pytest configuration
└── requirements-test.txt    # Test dependencies
```

### Test Categories

#### Model Tests
- Data validation
- Model relationships
- Serialization (to_dict methods)
- Database constraints

#### Route Tests
- API endpoint functionality
- Request/response validation
- Error handling
- Authentication (when implemented)

#### Integration Tests
- End-to-end workflows
- Cross-service functionality
- Data consistency

### Running Specific Tests

```bash
# Run specific test file
pytest tests/test_models/test_usuario.py

# Run specific test class
pytest tests/test_models/test_usuario.py::TestUsuario

# Run specific test method
pytest tests/test_models/test_usuario.py::TestUsuario::test_create_usuario

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

## Frontend Testing (React + Jest)

### Setup

1. Install dependencies (if not already done):
   ```bash
   cd frontend
   npm install
   ```

2. Run tests:
   ```bash
   npm test
   ```

3. Run tests with coverage:
   ```bash
   npm test -- --coverage --watchAll=false
   ```

### Test Structure

```
frontend/
├── src/
│   ├── __tests__/
│   │   ├── components/      # Component tests
│   │   │   └── LandingPage.test.jsx
│   │   ├── services/        # Service/API tests
│   │   │   └── api.test.js
│   │   └── integration/     # Integration tests
│   └── components/          # Source components
```

### Test Categories

#### Component Tests
- Rendering verification
- User interaction simulation
- Props validation
- State management

#### Service Tests
- API call validation
- Data transformation
- Error handling
- Network failure scenarios

#### Integration Tests
- User flow testing
- Component interaction
- Route navigation

### Running Specific Frontend Tests

```bash
# Run all tests
npm test -- --watchAll=false

# Run specific test file
npm test -- --testPathPattern=api.test.js

# Run with coverage
npm test -- --coverage --watchAll=false
```

## Test Configuration

### Backend Configuration (pytest.ini)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### Test Database

- Uses SQLite in-memory database for isolation
- Automatic setup/teardown for each test
- Fixtures provide sample data

## Coverage Goals

- **Backend**: Minimum 80% code coverage
- **Frontend**: Minimum 70% code coverage
- **Critical paths**: 100% coverage for authentication, data validation

## Best Practices

### Writing Tests

1. **Use descriptive test names**: `test_create_usuario_with_valid_data`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **One assertion per test**: Focus on single responsibility
4. **Use fixtures**: Reuse common test data and setup
5. **Mock external dependencies**: Database, API calls, file system

### Test Data

1. **Use factories/fixtures**: Consistent test data generation
2. **Avoid hardcoded values**: Use variables and constants
3. **Clean up**: Ensure tests don't affect each other
4. **Realistic data**: Use data similar to production

### Debugging Tests

1. **Use verbose mode**: `pytest -v` or `npm test -- --verbose`
2. **Run single tests**: Isolate failing tests
3. **Print debugging**: Use `print()` or `console.log()` temporarily
4. **Use debugger**: `import pdb; pdb.set_trace()` for Python

## Common Issues and Solutions

### Backend Issues

1. **Import errors**: Ensure correct Python path in test environment
2. **Database connection**: Use test database configuration
3. **Fixture dependencies**: Check fixture scope and dependencies

### Frontend Issues

1. **Module not found**: Ensure all dependencies are installed
2. **Component mocking**: Mock external dependencies like react-router-dom
3. **Async testing**: Use proper async/await or return promises

## Continuous Integration

Tests are automatically run on:
- Pull requests
- Push to main branch
- Scheduled nightly builds

See `.github/workflows/tests.yml` for CI configuration.

## Contributing

When adding new features:

1. **Write tests first** (TDD approach recommended)
2. **Ensure tests pass** before submitting PR
3. **Maintain coverage** - don't decrease overall coverage
4. **Update documentation** if adding new test patterns

## Running All Tests

To run the complete test suite:

```bash
# Backend tests
cd backend-flask && pytest

# Frontend tests
cd frontend && npm test -- --watchAll=false

# Or use the provided script (if created)
./run_all_tests.sh
```