#!/bin/bash

# Helper script to run Crawl4AI tests

echo "=========================================="
echo "Crawl4AI Test Runner"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please create it first: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Function to run a test
run_test() {
    local test_file=$1
    local test_name=$2

    echo ""
    echo "=========================================="
    echo "Running: $test_name"
    echo "=========================================="
    echo ""

    if [ -f "$test_file" ]; then
        python "$test_file"
        local exit_code=$?

        if [ $exit_code -eq 0 ]; then
            echo "✅ $test_name completed successfully"
        else
            echo "❌ $test_name failed with exit code: $exit_code"
        fi

        return $exit_code
    else
        echo "❌ Test file not found: $test_file"
        return 1
    fi
}

# Parse command line arguments
case "${1:-all}" in
    basic)
        run_test "test_basic.py" "Basic Test"
        ;;
    advanced)
        run_test "test_advanced.py" "Advanced Test"
        ;;
    all)
        echo "Running all tests..."
        run_test "test_basic.py" "Basic Test"
        basic_result=$?

        run_test "test_advanced.py" "Advanced Test"
        advanced_result=$?

        echo ""
        echo "=========================================="
        echo "Test Summary"
        echo "=========================================="
        echo "Basic Test: $([ $basic_result -eq 0 ] && echo '✅ Passed' || echo '❌ Failed')"
        echo "Advanced Test: $([ $advanced_result -eq 0 ] && echo '✅ Passed' || echo '❌ Failed')"
        ;;
    *)
        echo "Usage: $0 [basic|advanced|all]"
        echo ""
        echo "Options:"
        echo "  basic    - Run basic test only"
        echo "  advanced - Run advanced test only"
        echo "  all      - Run all tests (default)"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Done!"
echo "=========================================="
