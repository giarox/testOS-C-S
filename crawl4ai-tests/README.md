# Crawl4AI Test Project

This project tests the Crawl4AI open-source web crawler/scraper.

## About Crawl4AI

Crawl4AI is an LLM-ready web crawler that converts web content into clean Markdown format, perfect for RAG systems, AI agents, and data pipelines.

**Key Features:**
- Clean Markdown generation optimized for AI consumption
- LLM-driven structured data extraction
- JavaScript execution and dynamic content handling
- Browser session management with authentication
- Proxy support and custom headers
- Screenshot and PDF generation

## Installation

This project uses a Python virtual environment to avoid dependency conflicts.

```bash
# Activate the virtual environment
source venv/bin/activate

# The dependencies are already installed, but if needed:
pip install -r requirements.txt
crawl4ai-setup
```

**Note on Browser Installation:**
The Chromium browser download may fail due to network restrictions. If you encounter browser issues when running tests, manually install it:

```bash
# Activate venv first
source venv/bin/activate

# Then install Chromium manually
python -m playwright install --with-deps chromium
```

## Test Scripts

### 1. Basic Test (`test_basic.py`)
Simple web crawling to extract clean Markdown from a webpage.

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the test
python test_basic.py
```

### 2. Advanced Test (`test_advanced.py`)
Demonstrates structured data extraction, JavaScript execution, and various crawler features.

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the test
python test_advanced.py
```

## Project Structure

```
crawl4ai-tests/
├── README.md
├── requirements.txt
├── test_basic.py
├── test_advanced.py
└── output/
    └── (generated test outputs)
```

## Documentation

Official documentation: https://docs.crawl4ai.com
GitHub repository: https://github.com/unclecode/crawl4ai
