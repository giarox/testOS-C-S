#!/usr/bin/env python3
"""
Advanced Crawl4AI Test Script
Demonstrates various features including structured data extraction,
JavaScript execution, and advanced crawler configurations.
"""

import asyncio
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


async def test_with_javascript():
    """
    Test crawling with JavaScript execution.
    Useful for dynamic content that loads after page load.
    """
    print("\n" + "=" * 60)
    print("TEST 1: JavaScript Execution")
    print("=" * 60)

    test_url = "https://example.com"

    browser_config = BrowserConfig(
        headless=True,
        verbose=True
    )

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        js_code=[
            "window.scrollTo(0, document.body.scrollHeight);",
            "console.log('Scrolled to bottom');"
        ],
        wait_for="body",
        delay_before_return_html=2.0
    )

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=test_url,
                config=run_config
            )

            print(f"✅ Success: {result.success}")
            print(f"📄 Content length: {len(result.markdown)} characters")
            print(f"🔧 JS executed: {len(run_config.js_code)} scripts")

            return result

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


async def test_structured_extraction():
    """
    Test structured data extraction using CSS selectors.
    Extracts specific elements into a structured format.
    """
    print("\n" + "=" * 60)
    print("TEST 2: Structured Data Extraction")
    print("=" * 60)

    test_url = "https://example.com"

    # Define extraction schema using CSS selectors
    schema = {
        "name": "Example Page Data",
        "baseSelector": "body",
        "fields": [
            {
                "name": "title",
                "selector": "h1",
                "type": "text"
            },
            {
                "name": "content",
                "selector": "p",
                "type": "text"
            },
            {
                "name": "links",
                "selector": "a",
                "type": "attribute",
                "attribute": "href"
            }
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema)

    browser_config = BrowserConfig(
        headless=True,
        verbose=True
    )

    run_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS
    )

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=test_url,
                config=run_config
            )

            print(f"✅ Success: {result.success}")

            if result.extracted_content:
                print("\n📦 Extracted Data:")
                print("-" * 60)
                try:
                    extracted = json.loads(result.extracted_content)
                    print(json.dumps(extracted, indent=2))
                except json.JSONDecodeError:
                    print(result.extracted_content)
                print("-" * 60)

            return result

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


async def test_with_custom_headers():
    """
    Test crawling with custom headers and user agent.
    """
    print("\n" + "=" * 60)
    print("TEST 3: Custom Headers & User Agent")
    print("=" * 60)

    test_url = "https://example.com"

    browser_config = BrowserConfig(
        headless=True,
        verbose=True,
        user_agent="Crawl4AI-TestBot/1.0 (Educational Testing)",
        extra_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml"
        }
    )

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS
    )

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=test_url,
                config=run_config
            )

            print(f"✅ Success: {result.success}")
            print(f"📄 URL: {result.url}")
            print(f"🤖 Custom User Agent: {browser_config.user_agent}")

            return result

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


async def test_multiple_urls():
    """
    Test crawling multiple URLs in sequence.
    """
    print("\n" + "=" * 60)
    print("TEST 4: Multiple URL Crawling")
    print("=" * 60)

    test_urls = [
        "https://example.com",
        "https://example.org",
    ]

    browser_config = BrowserConfig(
        headless=True,
        verbose=False
    )

    results = []

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for i, url in enumerate(test_urls, 1):
                print(f"\n🔄 Crawling {i}/{len(test_urls)}: {url}")

                result = await crawler.arun(
                    url=url,
                    config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
                )

                results.append({
                    "url": url,
                    "success": result.success,
                    "content_length": len(result.markdown) if result.markdown else 0
                })

                print(f"   ✅ Status: {'Success' if result.success else 'Failed'}")
                print(f"   📊 Content: {results[-1]['content_length']} chars")

            print(f"\n📊 Summary: {len([r for r in results if r['success']])}/{len(results)} successful")

            return results

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


async def main():
    """
    Run all advanced tests.
    """
    print("=" * 60)
    print("Crawl4AI - Advanced Test Suite")
    print("=" * 60)

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    results = {}

    # Run tests
    print("\n🧪 Running advanced tests...\n")

    results["javascript"] = await test_with_javascript()
    results["structured"] = await test_structured_extraction()
    results["headers"] = await test_with_custom_headers()
    results["multiple"] = await test_multiple_urls()

    # Save results
    print("\n" + "=" * 60)
    print("💾 Saving Results")
    print("=" * 60)

    for test_name, result in results.items():
        if result and not isinstance(result, list):
            output_file = output_dir / f"advanced_{test_name}_output.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# Crawl4AI Advanced Test: {test_name.title()}\n\n")
                f.write(f"**URL:** {result.url}\n\n")
                f.write(f"**Status:** {'Success' if result.success else 'Failed'}\n\n")
                if hasattr(result, 'markdown') and result.markdown:
                    f.write(f"## Markdown Content\n\n{result.markdown}\n\n")
                if hasattr(result, 'extracted_content') and result.extracted_content:
                    f.write(f"## Extracted Data\n\n```json\n{result.extracted_content}\n```\n")

            print(f"📄 {test_name}: {output_file}")

    print("\n" + "=" * 60)
    print("✨ Advanced test suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    print("\n🔧 Crawl4AI Advanced Test Script")
    print("   Testing advanced features and configurations\n")

    asyncio.run(main())
