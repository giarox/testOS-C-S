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

### 3. Lidl Flyer Scraper (`test_lidl_scraper.py`) - Real World Example
Real-world scraper for Lidl Italy weekly flyers. Extracts products, prices, and offers from retail catalogs.

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the scraper
python test_lidl_scraper.py

# Or use the test runner
./run_tests.sh lidl
```

**Features demonstrated:**
- Scraping multi-page catalogs with pagination
- Structured data extraction (products, prices, discounts)
- JavaScript execution for lazy-loaded content
- Screenshot capture for verification
- JSON export of structured data
- Markdown content extraction

### 4. Code Demonstration (`demo_code.py`)
Comprehensive code examples showing all major Crawl4AI features. Runs without a browser.

```bash
# No browser needed for this
python demo_code.py
```

## Quick Start

```bash
# Activate environment
source venv/bin/activate

# Run specific test
./run_tests.sh basic     # Basic crawling
./run_tests.sh advanced  # Advanced features
./run_tests.sh lidl      # Real-world Lidl scraper
./run_tests.sh demo      # Code examples (no browser)
./run_tests.sh all       # Run all tests
```

## Project Structure

```
crawl4ai-tests/
├── README.md                    # This file
├── SETUP_NOTES.md              # Detailed setup and troubleshooting
├── requirements.txt            # Python dependencies
├── run_tests.sh                # Test runner script
├── install_browser.sh          # Automated browser installer
├── manual_browser_install.sh   # Manual offline browser installation
├── test_basic.py               # Basic crawling test
├── test_advanced.py            # Advanced features test
├── test_lidl_scraper.py        # Real-world Lidl flyer scraper
├── demo_code.py                # Code examples (no browser needed)
├── venv/                       # Virtual environment (pre-configured)
└── output/                     # Generated test outputs
    ├── basic_test_output.md
    ├── advanced_*_output.md
    └── lidl_scraper/           # Lidl scraper results
        ├── *.json              # Structured product data
        ├── *.html              # Raw HTML files
        ├── *.md                # Clean Markdown
        └── *_screenshot.png    # Page screenshots
```

## Documentation

Official documentation: https://docs.crawl4ai.com
GitHub repository: https://github.com/unclecode/crawl4ai
