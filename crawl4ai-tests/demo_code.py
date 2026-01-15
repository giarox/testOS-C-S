#!/usr/bin/env python3
"""
Crawl4AI Code Demonstration
This script shows the code structure and API usage without requiring a browser.
Use this to understand how Crawl4AI works before running actual tests.
"""

def demonstrate_basic_usage():
    """
    Demonstrates basic Crawl4AI usage patterns.
    """
    print("=" * 70)
    print("CRAWL4AI CODE DEMONSTRATION")
    print("=" * 70)

    print("\n1. BASIC CRAWLING")
    print("-" * 70)
    print("""
Basic web crawling with clean Markdown extraction:

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://example.com")

        print(f"Success: {result.success}")
        print(f"Markdown: {result.markdown}")
        print(f"HTML: {result.html}")
        print(f"Links: {result.links}")

asyncio.run(main())
```

What you get:
- result.markdown: Clean, LLM-ready Markdown
- result.html: Raw HTML content
- result.links: All links found on page
- result.media: Images, videos, audio elements
- result.metadata: Page info (title, description, etc.)
""")

    print("\n2. JAVASCRIPT EXECUTION")
    print("-" * 70)
    print("""
Execute JavaScript for dynamic content:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

browser_config = BrowserConfig(headless=True)

run_config = CrawlerRunConfig(
    js_code=[
        "window.scrollTo(0, document.body.scrollHeight);",
        "await new Promise(r => setTimeout(r, 2000));"  # Wait 2 seconds
    ],
    wait_for="css:.dynamic-content",  # Wait for element
    delay_before_return_html=1.0
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(
        url="https://example.com/dynamic",
        config=run_config
    )
```

Use cases:
- Lazy-loaded content
- Infinite scroll pages
- JavaScript-rendered SPAs
- Dynamic forms and interactions
""")

    print("\n3. STRUCTURED DATA EXTRACTION")
    print("-" * 70)
    print("""
Extract specific data using CSS selectors:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# Define extraction schema
schema = {
    "name": "Product List",
    "baseSelector": "div.product",
    "fields": [
        {
            "name": "title",
            "selector": "h2.product-title",
            "type": "text"
        },
        {
            "name": "price",
            "selector": "span.price",
            "type": "text"
        },
        {
            "name": "image",
            "selector": "img",
            "type": "attribute",
            "attribute": "src"
        }
    ]
}

extraction_strategy = JsonCssExtractionStrategy(schema)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://shop.example.com/products",
        config=CrawlerRunConfig(extraction_strategy=extraction_strategy)
    )

    # result.extracted_content contains structured JSON
    import json
    products = json.loads(result.extracted_content)
```

Outputs structured data like:
```json
[
  {
    "title": "Product Name",
    "price": "$29.99",
    "image": "https://example.com/image.jpg"
  },
  ...
]
```
""")

    print("\n4. LLM-BASED EXTRACTION")
    print("-" * 70)
    print("""
Use AI models for intelligent content extraction:

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

# Define what you want to extract
extraction_strategy = LLMExtractionStrategy(
    provider="openai",
    api_token="your-api-key",
    instruction="Extract all product names, prices, and descriptions"
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com",
        config=CrawlerRunConfig(extraction_strategy=extraction_strategy)
    )
```

Benefits:
- Intelligent content understanding
- No manual CSS selector mapping
- Handles varying page structures
- Natural language instructions
""")

    print("\n5. ADVANCED CONFIGURATION")
    print("-" * 70)
    print("""
Fine-tune crawler behavior:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# Browser configuration
browser_config = BrowserConfig(
    headless=True,
    browser_type="chromium",  # or "firefox", "webkit"
    user_agent="Custom Bot/1.0",
    extra_headers={
        "Accept-Language": "en-US,en;q=0.9",
        "X-Custom-Header": "value"
    },
    viewport_width=1920,
    viewport_height=1080,
    use_managed_browser=True,  # Reuse browser instance
    text_mode=False  # Set True for text-only (no images)
)

# Run configuration
run_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,  # BYPASS, READ_ONLY, WRITE_ONLY, ENABLED
    page_timeout=30000,  # 30 seconds
    js_only=False,
    bypass_cache=False,
    screenshot=True,  # Take screenshot
    pdf=False,  # Generate PDF
    wait_until="networkidle",  # or "load", "domcontentloaded"
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(
        url="https://example.com",
        config=run_config,
        session_id="my-session"  # Persistent session
    )

    # Access screenshot
    if result.screenshot:
        with open("page.png", "wb") as f:
            f.write(result.screenshot)
```
""")

    print("\n6. BATCH CRAWLING")
    print("-" * 70)
    print("""
Crawl multiple URLs efficiently:

```python
import asyncio
from crawl4ai import AsyncWebCrawler

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

async def crawl_multiple():
    async with AsyncWebCrawler() as crawler:
        # Sequential
        results = []
        for url in urls:
            result = await crawler.arun(url=url)
            results.append(result)

        # Or use asyncio.gather for parallel crawling
        results = await asyncio.gather(*[
            crawler.arun(url=url) for url in urls
        ])

        return results

results = asyncio.run(crawl_multiple())
```
""")

    print("\n7. CONTENT FILTERING")
    print("-" * 70)
    print("""
Filter and clean content intelligently:

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

run_config = CrawlerRunConfig(
    word_count_threshold=10,  # Min words to keep content
    excluded_tags=['nav', 'footer', 'aside'],  # Remove these tags
    only_text=True,  # Extract text only
    remove_overlay_elements=True  # Remove popups, modals
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com",
        config=run_config
    )

    # result.fit_markdown: Ultra-clean, AI-optimized Markdown
    # result.markdown: Standard Markdown
```
""")

    print("\n8. SESSION MANAGEMENT")
    print("-" * 70)
    print("""
Maintain state across requests:

```python
async with AsyncWebCrawler() as crawler:
    # Login
    login_result = await crawler.arun(
        url="https://example.com/login",
        config=CrawlerRunConfig(
            js_code=[
                "document.querySelector('#username').value = 'user';",
                "document.querySelector('#password').value = 'pass';",
                "document.querySelector('form').submit();"
            ]
        ),
        session_id="authenticated-session"
    )

    # Crawl protected page with same session
    protected = await crawler.arun(
        url="https://example.com/dashboard",
        session_id="authenticated-session"  # Reuse cookies/state
    )
```
""")

    print("\n9. ERROR HANDLING")
    print("-" * 70)
    print("""
Robust error handling:

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")

    if result.success:
        print(f"Crawled successfully: {len(result.markdown)} chars")
    else:
        print(f"Crawl failed: {result.error_message}")

    # Check specific conditions
    if result.status_code == 404:
        print("Page not found")
    elif result.status_code == 403:
        print("Access forbidden")
    elif result.status_code >= 500:
        print("Server error")
```
""")

    print("\n10. REAL-WORLD EXAMPLE: NEWS AGGREGATOR")
    print("-" * 70)
    print("""
Complete example - scraping news articles:

```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from pathlib import Path
import json

async def scrape_news():
    # Configure browser
    browser_config = BrowserConfig(
        headless=True,
        user_agent="NewsBot/1.0"
    )

    # Define article extraction schema
    schema = {
        "name": "News Articles",
        "baseSelector": "article.news-item",
        "fields": [
            {"name": "headline", "selector": "h2", "type": "text"},
            {"name": "summary", "selector": "p.summary", "type": "text"},
            {"name": "author", "selector": ".author", "type": "text"},
            {"name": "date", "selector": "time", "type": "attribute", "attribute": "datetime"},
            {"name": "url", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema)

    news_sites = [
        "https://news.example.com/tech",
        "https://news.example.com/business",
        "https://news.example.com/science"
    ]

    all_articles = []

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for site in news_sites:
            print(f"Scraping {site}...")

            result = await crawler.arun(
                url=site,
                config=CrawlerRunConfig(
                    extraction_strategy=extraction_strategy,
                    wait_for="article.news-item"
                )
            )

            if result.success:
                articles = json.loads(result.extracted_content)
                all_articles.extend(articles)
                print(f"  Found {len(articles)} articles")

    # Save results
    output_file = Path("news_articles.json")
    with open(output_file, "w") as f:
        json.dump(all_articles, f, indent=2)

    print(f"\\nSaved {len(all_articles)} articles to {output_file}")

asyncio.run(scrape_news())
```
""")

    print("\n" + "=" * 70)
    print("For actual execution, ensure browser is installed:")
    print("  python -m playwright install chromium")
    print("\nThen run: ./run_tests.sh")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_basic_usage()
