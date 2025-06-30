#!/bin/bash

# Test runner script for STEM Vocacional WebApp
# This script runs all tests for both backend and frontend

set -e  # Exit on any error

echo "🚀 Starting STEM Vocacional WebApp Test Suite"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "TESTING.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Backend Tests
echo ""
print_status "Running Backend Tests (Flask + pytest)"
echo "---------------------------------------"

cd backend-flask

# Check if test dependencies are installed
if ! python -c "import pytest" 2>/dev/null; then
    print_warning "pytest not found. Installing test dependencies..."
    pip install -r requirements-test.txt
fi

# Run backend tests
print_status "Executing backend test suite..."
if pytest --cov=app --cov-report=term-missing --cov-report=html -v; then
    print_success "Backend tests passed!"
    BACKEND_TESTS_PASSED=true
else
    print_error "Backend tests failed!"
    BACKEND_TESTS_PASSED=false
fi

cd ..

# Frontend Tests
echo ""
print_status "Running Frontend Tests (React + Jest)"
echo "--------------------------------------"

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_warning "node_modules not found. Installing dependencies..."
    npm install
fi

# Run frontend tests
print_status "Executing frontend test suite..."
if npm test -- --coverage --watchAll=false; then
    print_success "Frontend tests passed!"
    FRONTEND_TESTS_PASSED=true
else
    print_error "Frontend tests failed!"
    FRONTEND_TESTS_PASSED=false
fi

cd ..

# Summary
echo ""
echo "🏁 Test Suite Summary"
echo "===================="

if [ "$BACKEND_TESTS_PASSED" = true ]; then
    print_success "✅ Backend Tests: PASSED"
else
    print_error "❌ Backend Tests: FAILED"
fi

if [ "$FRONTEND_TESTS_PASSED" = true ]; then
    print_success "✅ Frontend Tests: PASSED"
else
    print_error "❌ Frontend Tests: FAILED"
fi

# Coverage reports
echo ""
print_status "Coverage Reports:"
echo "  Backend: backend-flask/htmlcov/index.html"
echo "  Frontend: frontend/coverage/lcov-report/index.html"

# Final status
if [ "$BACKEND_TESTS_PASSED" = true ] && [ "$FRONTEND_TESTS_PASSED" = true ]; then
    echo ""
    print_success "🎉 All tests passed! Ready for deployment."
    exit 0
else
    echo ""
    print_error "💥 Some tests failed. Please fix before deploying."
    exit 1
fi