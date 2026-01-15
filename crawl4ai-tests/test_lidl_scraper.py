#!/usr/bin/env python3
"""
Lidl Flyer Scraper - Real World Crawl4AI Test
Extracts product information from Lidl Italy weekly flyers.
"""

import asyncio
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from datetime import datetime


async def scrape_lidl_flyer(url: str, max_pages: int = 3):
    """
    Scrape Lidl flyer pages and extract product information.

    Args:
        url: Base URL of the flyer (page 1)
        max_pages: Maximum number of pages to scrape
    """
    print("=" * 70)
    print("🛒 Lidl Flyer Scraper - Crawl4AI Real World Test")
    print("=" * 70)

    # Create output directory
    output_dir = Path("output/lidl_scraper")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📍 Target: {url}")
    print(f"📄 Scraping up to {max_pages} pages")
    print("")

    # Configure browser for dynamic content
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=True,
        # Use realistic user agent to avoid blocking
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Define extraction schema for product cards
    # This will need adjustment based on actual page structure
    product_schema = {
        "name": "Lidl Products",
        "baseSelector": "[data-product], .product-card, .offer-item, article.product",
        "fields": [
            {
                "name": "product_name",
                "selector": "h2, h3, .product-title, .offer-title",
                "type": "text"
            },
            {
                "name": "price",
                "selector": ".price, .product-price, .offer-price, [class*='price']",
                "type": "text"
            },
            {
                "name": "original_price",
                "selector": ".original-price, .old-price, [class*='old-price']",
                "type": "text"
            },
            {
                "name": "description",
                "selector": ".description, .product-description, p",
                "type": "text"
            },
            {
                "name": "image_url",
                "selector": "img",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "discount",
                "selector": ".discount, .badge, .offer-badge",
                "type": "text"
            }
        ]
    }

    all_products = []

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for page_num in range(1, max_pages + 1):
                # Construct page URL
                page_url = url.replace("/page/1", f"/page/{page_num}")

                print(f"\n{'='*70}")
                print(f"📄 Scraping Page {page_num}/{max_pages}")
                print(f"🔗 URL: {page_url}")
                print(f"{'='*70}")

                # Configure crawler for this page
                run_config = CrawlerRunConfig(
                    # Wait for page to load fully
                    wait_for="body",
                    delay_before_return_html=3.0,  # Wait 3 seconds for JS to render

                    # Execute JavaScript to scroll and load lazy images
                    js_code=[
                        "window.scrollTo(0, document.body.scrollHeight / 2);",
                        "await new Promise(r => setTimeout(r, 1000));",
                        "window.scrollTo(0, document.body.scrollHeight);",
                        "await new Promise(r => setTimeout(r, 1000));",
                    ],

                    # Use extraction strategy
                    extraction_strategy=JsonCssExtractionStrategy(product_schema),

                    # Cache settings
                    cache_mode=CacheMode.BYPASS,

                    # Take screenshot for debugging
                    screenshot=True,

                    # Page timeout
                    page_timeout=60000  # 60 seconds
                )

                # Perform the crawl
                result = await crawler.arun(url=page_url, config=run_config)

                if not result.success:
                    print(f"❌ Failed to scrape page {page_num}: {result.error_message}")
                    continue

                print(f"✅ Successfully crawled page {page_num}")
                print(f"📊 Status code: {result.status_code}")
                print(f"📄 Content length: {len(result.html)} chars")

                # Save screenshot
                if result.screenshot:
                    screenshot_path = output_dir / f"page_{page_num}_screenshot.png"
                    with open(screenshot_path, "wb") as f:
                        f.write(result.screenshot)
                    print(f"📸 Screenshot saved: {screenshot_path}")

                # Save raw HTML for debugging
                html_path = output_dir / f"page_{page_num}_raw.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(result.html)
                print(f"💾 HTML saved: {html_path}")

                # Save clean Markdown
                markdown_path = output_dir / f"page_{page_num}_markdown.md"
                with open(markdown_path, "w", encoding="utf-8") as f:
                    f.write(f"# Lidl Flyer - Page {page_num}\n\n")
                    f.write(f"**URL:** {page_url}\n\n")
                    f.write(f"**Scraped:** {datetime.now().isoformat()}\n\n")
                    f.write("---\n\n")
                    f.write(result.markdown if result.markdown else "No content")
                print(f"📝 Markdown saved: {markdown_path}")

                # Extract structured data
                if result.extracted_content:
                    try:
                        products = json.loads(result.extracted_content)

                        # Add page number to each product
                        for product in products:
                            product['page'] = page_num
                            product['url'] = page_url

                        all_products.extend(products)

                        print(f"🎯 Extracted {len(products)} products from page {page_num}")

                        # Show first product as sample
                        if products:
                            print("\n📦 Sample product:")
                            print(json.dumps(products[0], indent=2, ensure_ascii=False))

                    except json.JSONDecodeError as e:
                        print(f"⚠️  Could not parse extracted data: {e}")
                        print(f"Raw content: {result.extracted_content[:200]}...")

                # Be nice to the server
                await asyncio.sleep(2)

        # Save all products to JSON
        print(f"\n{'='*70}")
        print("💾 Saving Results")
        print(f"{'='*70}")

        products_file = output_dir / f"lidl_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(products_file, "w", encoding="utf-8") as f:
            json.dump({
                "scrape_date": datetime.now().isoformat(),
                "total_products": len(all_products),
                "pages_scraped": max_pages,
                "products": all_products
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(all_products)} products to: {products_file}")

        # Generate summary
        print(f"\n{'='*70}")
        print("📊 Scraping Summary")
        print(f"{'='*70}")
        print(f"✅ Total products extracted: {len(all_products)}")
        print(f"📄 Pages scraped: {max_pages}")
        print(f"💾 Output directory: {output_dir}")
        print(f"\nFiles created:")
        print(f"  - {len(all_products)} products in JSON")
        print(f"  - {max_pages} HTML files")
        print(f"  - {max_pages} Markdown files")
        print(f"  - {max_pages} Screenshots")

        # Show product statistics
        if all_products:
            print(f"\n🏷️  Product Statistics:")
            products_with_prices = [p for p in all_products if p.get('price')]
            print(f"  - Products with prices: {len(products_with_prices)}")

            products_with_images = [p for p in all_products if p.get('image_url')]
            print(f"  - Products with images: {len(products_with_images)}")

        return all_products

    except Exception as e:
        print(f"\n❌ Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def scrape_lidl_flyer_simple(url: str):
    """
    Simple scraping approach - just get the clean Markdown without structured extraction.
    Useful if the CSS selectors need adjustment.
    """
    print("=" * 70)
    print("🛒 Lidl Flyer Scraper - Simple Mode")
    print("=" * 70)

    output_dir = Path("output/lidl_scraper")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📍 Target: {url}")
    print("📝 Extracting clean Markdown content...\n")

    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=True
    )

    run_config = CrawlerRunConfig(
        wait_for="body",
        delay_before_return_html=3.0,
        js_code=[
            "window.scrollTo(0, document.body.scrollHeight);",
            "await new Promise(r => setTimeout(r, 2000));",
        ],
        cache_mode=CacheMode.BYPASS,
        screenshot=True
    )

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                # Save markdown
                markdown_file = output_dir / f"lidl_flyer_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(markdown_file, "w", encoding="utf-8") as f:
                    f.write(f"# Lidl Flyer\n\n")
                    f.write(f"**URL:** {url}\n")
                    f.write(f"**Scraped:** {datetime.now().isoformat()}\n\n")
                    f.write("---\n\n")
                    f.write(result.markdown if result.markdown else "No content")

                print(f"✅ Success!")
                print(f"📄 Content length: {len(result.markdown)} characters")
                print(f"💾 Saved to: {markdown_file}")

                # Save screenshot
                if result.screenshot:
                    screenshot_path = output_dir / f"lidl_flyer_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    with open(screenshot_path, "wb") as f:
                        f.write(result.screenshot)
                    print(f"📸 Screenshot: {screenshot_path}")

                # Show preview
                print(f"\n📝 Content Preview:")
                print("-" * 70)
                preview = result.markdown[:1000] if result.markdown else "No content"
                print(preview)
                if len(result.markdown) > 1000:
                    print(f"\n... (truncated, total: {len(result.markdown)} chars)")
                print("-" * 70)

                return result
            else:
                print(f"❌ Failed: {result.error_message}")
                return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """
    Main function - test both simple and structured extraction.
    """
    # The Lidl flyer URL (January 19-25, 2025)
    lidl_url = "https://www.lidl.it/l/it/volantini/offerte-valide-dal-19-01-al-25-01-volantino-settimanale-9e63be/view/flyer/page/1"

    print("\n🔧 Lidl Flyer Scraper - Crawl4AI Real World Test")
    print("   Testing Italian Lidl weekly flyer extraction\n")

    # First, try simple extraction to see the page structure
    print("\n" + "="*70)
    print("TEST 1: Simple Markdown Extraction")
    print("="*70)
    await scrape_lidl_flyer_simple(lidl_url)

    # Then try structured extraction
    print("\n" + "="*70)
    print("TEST 2: Structured Product Extraction")
    print("="*70)
    products = await scrape_lidl_flyer(lidl_url, max_pages=2)

    print("\n" + "="*70)
    print("✨ Scraping Complete!")
    print("="*70)
    print("\n💡 Tips:")
    print("  1. Check output/lidl_scraper/ for all extracted data")
    print("  2. Review screenshots to verify page loading")
    print("  3. Adjust CSS selectors in product_schema if needed")
    print("  4. Check HTML files if extraction seems incomplete")
    print("")


if __name__ == "__main__":
    print("\n🛒 Crawl4AI - Lidl Flyer Scraper")
    print("   Real-world test with Italian retail website\n")

    asyncio.run(main())
