#!/usr/bin/env python3
"""
Basic Crawl4AI Test Script
This demonstrates simple web crawling with clean Markdown extraction.
"""

import asyncio
import os
from crawl4ai import AsyncWebCrawler
from pathlib import Path


async def basic_crawl_test():
    """
    Basic crawling test that extracts clean Markdown from a webpage.
    """
    print("=" * 60)
    print("Crawl4AI - Basic Test")
    print("=" * 60)

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Test URL - using a simple, reliable website
    test_url = "https://example.com"

    print(f"\n📍 Target URL: {test_url}")
    print("🚀 Starting crawler...\n")

    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
            # Perform the crawl
            result = await crawler.arun(url=test_url)

            # Display results
            print("\n" + "=" * 60)
            print("CRAWL RESULTS")
            print("=" * 60)

            print(f"\n✅ Success: {result.success}")
            print(f"📄 URL: {result.url}")
            print(f"⏱️  Time taken: {result.metadata.get('time_taken', 'N/A')} seconds")

            # Show markdown content
            print("\n📝 Markdown Content:")
            print("-" * 60)
            print(result.markdown[:500] if result.markdown else "No content")
            if result.markdown and len(result.markdown) > 500:
                print(f"\n... (truncated, total length: {len(result.markdown)} chars)")
            print("-" * 60)

            # Save to file
            output_file = output_dir / "basic_test_output.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# Crawl4AI Basic Test Results\n\n")
                f.write(f"**URL:** {result.url}\n\n")
                f.write(f"**Status:** {'Success' if result.success else 'Failed'}\n\n")
                f.write(f"## Content\n\n")
                f.write(result.markdown if result.markdown else "No content")

            print(f"\n💾 Output saved to: {output_file}")

            # Show metadata
            print("\n📊 Metadata:")
            for key, value in result.metadata.items():
                print(f"  • {key}: {value}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("✨ Basic test completed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    print("\n🔧 Crawl4AI Basic Test Script")
    print("   Testing simple web crawling with Markdown extraction\n")

    # Run the test
    success = asyncio.run(basic_crawl_test())

    exit(0 if success else 1)
