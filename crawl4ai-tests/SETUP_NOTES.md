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

## Comprehensive Solutions for Browser Installation Issues

### Solution 1: Environment Variables for Proxy/Network Configuration

If you're behind a firewall or corporate proxy, configure these environment variables:

```bash
# Activate venv
source venv/bin/activate

# Configure proxy for downloads
export HTTPS_PROXY=https://your-proxy:port
export HTTP_PROXY=http://your-proxy:port

# Increase timeout for slow connections (milliseconds)
export PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=60000

# Then install
crawl4ai-setup
# Or directly:
python -m playwright install chromium
```

**Custom Download Host** (for internal mirror/artifact repository):
```bash
export PLAYWRIGHT_DOWNLOAD_HOST=http://your-mirror.com
# Or per-browser:
export PLAYWRIGHT_CHROMIUM_DOWNLOAD_HOST=http://your-mirror.com/chromium
python -m playwright install chromium
```

**Custom Browser Storage Location**:
```bash
export PLAYWRIGHT_BROWSERS_PATH=$HOME/pw-browsers
python -m playwright install chromium
```

### Solution 2: Manual Offline Browser Installation

Download browsers on a machine with internet access, then transfer to restricted environment:

**Step 1: Download browser archive**
- URL format: `https://playwright.azureedge.net/builds/chromium/1200/chromium-linux.zip`
- Replace `1200` with your Playwright version's browser build number
- For other platforms: `chromium-mac.zip`, `chromium-win64.zip`

**Step 2: Extract to Playwright cache directory**
```bash
# Create directory structure
mkdir -p ~/.cache/ms-playwright/chromium-1200/chrome-linux

# Extract downloaded archive
unzip chromium-linux.zip -d ~/.cache/ms-playwright/chromium-1200/

# Create marker files (REQUIRED for Playwright to recognize installation)
touch ~/.cache/ms-playwright/chromium-1200/INSTALLATION_COMPLETE
touch ~/.cache/ms-playwright/chromium-1200/DEPENDENCIES_VALIDATED
```

**Step 3: Verify installation**
```bash
playwright install --dry-run chromium
```

### Solution 3: Use Crawl4AI's Bundled Browser Configuration

Configure Crawl4AI to use Playwright's bundled Chromium (no system Chrome needed):

```python
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig

# Use bundled Chromium (most portable)
browser_config = BrowserConfig(
    browser_type="chromium",
    chrome_channel=None,  # Use bundled browser, not system Chrome
    headless=True
)

async with AsyncWebCrawler(config=browser_config, verbose=True) as crawler:
    result = await crawler.arun(url="https://example.com")
```

**Alternative channels** (if system browsers are available):
- `chrome_channel="chrome"` - Use system Google Chrome
- `chrome_channel="msedge"` - Use Microsoft Edge

### Solution 4: Whitelist Required URLs

Request your IT/network team to whitelist these domains:
- `playwright.azureedge.net`
- `playwright-akamai.azureedge.net`
- `playwright-verizon.azureedge.net`
- `cdn.playwright.dev`
- `playwright.download.prss.microsoft.com`

Then retry installation:
```bash
source venv/bin/activate
crawl4ai-setup
```

### Solution 5: Docker Deployment (Recommended for Production)

Use the official Crawl4AI Docker image which includes all browsers pre-installed:

```bash
# Pull latest image
docker pull unclecode/crawl4ai:latest

# Run with proper memory allocation
docker run -d -p 11235:11235 --name crawl4ai \
  --shm-size=1g \
  unclecode/crawl4ai:latest

# Access monitoring dashboard
open http://localhost:11235/dashboard

# Test via API
curl http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com"], "priority": 10}'
```

### Solution 6: Skip Browser Download During Installation

If managing browsers separately or using Docker:

```bash
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
pip install crawl4ai
# Then manually install browsers later when network allows
```

### Solution 7: SSL Certificate Issues

If your proxy intercepts SSL with custom certificates:

```bash
export NODE_EXTRA_CA_CERTS=/path/to/your/custom-ca.crt
python -m playwright install chromium
```

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

## References & Sources

These solutions are based on official documentation and community-validated workarounds:

1. [Playwright Browser Installation - Official Docs](https://playwright.dev/python/docs/browsers)
2. [Crawl4AI Issue #377 - Chromium distribution not found](https://github.com/unclecode/crawl4ai/issues/377)
3. [Crawl4AI Issue #503 - Browser path detection failing](https://github.com/unclecode/crawl4ai/issues/503)
4. [Playwright Python Issue #1292 - Manual browser installation](https://github.com/microsoft/playwright-python/issues/1292)
5. [Playwright Issue #3960 - Download failed 403 errors](https://github.com/microsoft/playwright/issues/3960)
6. [Playwright Issue #20984 - Firewall and proxy browser download](https://github.com/microsoft/playwright/issues/20984)
7. [How to Solve Playwright 403 Forbidden Error - ZenRows](https://www.zenrows.com/blog/playwright-403)
8. [How to Install Playwright - Comprehensive Guide 2026](https://www.testmu.ai/learning-hub/how-to-install-playwright/)
