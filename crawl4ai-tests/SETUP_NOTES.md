# Crawl4AI Test Project - Setup Notes

## Project Status

✅ **Successfully Completed:**
- Python 3.11.14 environment verified
- Virtual environment created (`venv/`)
- Crawl4AI library installed
- Test scripts created (basic and advanced)
- Project structure and documentation complete

❌ **Known Issue:**
- Chromium browser download blocked by network restrictions (403 Forbidden)
- This prevents the crawler from running in the current environment

## Network Restriction Details

The Playwright browser download attempts to fetch from these URLs, all blocked:
- `https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1200/chromium-linux.zip`
- `https://playwright.download.prss.microsoft.com/dbazure/download/playwright/builds/chromium/1200/chromium-linux.zip`
- `https://cdn.playwright.dev/builds/chromium/1200/chromium-linux.zip`

Error: `Download failed: server returned code 403 body 'Host not allowed'`

## Workarounds for Different Environments

### Option 1: Docker Deployment (Recommended)
Use the official Crawl4AI Docker image which includes all browsers:

```bash
docker pull unclecode/crawl4ai:latest
docker run -d -p 11235:11235 --name crawl4ai unclecode/crawl4ai:latest

# Test via API
curl http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com"], "priority": 10}'
```

### Option 2: Manual Browser Installation
In environments without network restrictions:

```bash
# Activate venv
source venv/bin/activate

# Install browsers
python -m playwright install chromium

# Or with system dependencies
python -m playwright install --with-deps chromium
```

### Option 3: Use System Chrome/Chromium
Configure Crawl4AI to use an existing Chrome installation:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig

browser_config = BrowserConfig(
    browser_type="chromium",
    executable_path="/usr/bin/chromium-browser"  # Adjust path as needed
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(url="https://example.com")
```

### Option 4: Download Browser Manually
Download the browser archive from an unrestricted location and extract to:
- `~/.cache/ms-playwright/chromium-1200/`

## What the Test Scripts Do

### `test_basic.py`
Demonstrates:
- Simple async web crawling
- Markdown content extraction
- Result saving to file
- Basic error handling

Expected output:
- Clean Markdown representation of the webpage
- Metadata including load time, status
- Saved output in `output/basic_test_output.md`

### `test_advanced.py`
Demonstrates:
- JavaScript execution for dynamic content
- Structured data extraction with CSS selectors
- Custom headers and user agents
- Multiple URL crawling
- Advanced configurations

Expected output:
- Structured JSON data from webpages
- Multiple test result files in `output/`
- Performance metrics for batch operations

## Project Features Demonstrated

1. **LLM-Ready Output**
   - Clean Markdown format optimized for AI consumption
   - Removes navigation, ads, and irrelevant content
   - Preserves semantic structure

2. **Flexible Extraction**
   - CSS selector-based schemas
   - XPath support
   - LLM-driven extraction strategies

3. **Dynamic Content Handling**
   - JavaScript execution
   - Wait for specific elements
   - Lazy-load detection
   - Full-page scrolling

4. **Browser Control**
   - Session persistence
   - Custom headers
   - Proxy support
   - Multiple browser types (Chromium, Firefox, WebKit)

5. **Performance Features**
   - Caching to avoid redundant requests
   - Browser pooling
   - Async/await for concurrency

## Testing in a Different Environment

To test this project in an unrestricted environment:

```bash
# 1. Copy the entire project
scp -r crawl4ai-tests/ user@remote-host:/path/

# 2. On the remote host
cd /path/crawl4ai-tests
source venv/bin/activate
python -m playwright install chromium

# 3. Run tests
./run_tests.sh all
```

## Project Structure

```
crawl4ai-tests/
├── venv/                    # Virtual environment (with Crawl4AI installed)
├── output/                  # Generated test outputs (created on first run)
├── requirements.txt         # Python dependencies
├── README.md               # Main documentation
├── SETUP_NOTES.md          # This file - setup details and workarounds
├── test_basic.py           # Basic crawling test
├── test_advanced.py        # Advanced features test
├── run_tests.sh            # Test runner script
└── demo_code.py            # Code demonstration (no browser required)
```

## Example Use Cases

1. **Content Aggregation**: Crawl news sites and extract article content in clean Markdown
2. **Data Pipeline**: Scrape product information for e-commerce analytics
3. **RAG Systems**: Build knowledge bases from web content for AI assistants
4. **Monitoring**: Track changes on websites over time
5. **Research**: Collect data from multiple sources for analysis

## Next Steps

Once browser installation is resolved, the test scripts will:
1. Successfully crawl test URLs
2. Generate clean Markdown output
3. Extract structured data
4. Save results to `output/` directory
5. Display performance metrics

## Resources

- **Documentation**: https://docs.crawl4ai.com
- **GitHub**: https://github.com/unclecode/crawl4ai (58,600+ stars)
- **Docker Hub**: https://hub.docker.com/r/unclecode/crawl4ai
- **API Docs**: https://docs.crawl4ai.com/api/

## Support

For issues with Crawl4AI itself (not network restrictions):
- GitHub Issues: https://github.com/unclecode/crawl4ai/issues
- Documentation: https://docs.crawl4ai.com/troubleshooting
