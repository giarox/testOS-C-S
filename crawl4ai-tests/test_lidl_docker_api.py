#!/usr/bin/env python3
"""
Lidl Flyer Scraper - Using Crawl4AI Docker API
Scrapes Lidl flyers using the Crawl4AI Docker container REST API.
No browser installation needed - uses the Docker container's browsers.
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime


class Crawl4AIDockerClient:
    """Client for interacting with Crawl4AI Docker API."""

    def __init__(self, base_url="http://localhost:11235"):
        """
        Initialize the client.

        Args:
            base_url: Base URL of the Crawl4AI Docker API (default: http://localhost:11235)
        """
        self.base_url = base_url
        self.crawl_endpoint = f"{base_url}/crawl"
        self.health_endpoint = f"{base_url}/health"

    def check_health(self):
        """Check if the Docker API is running and healthy."""
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            return False

    def crawl(self, url, wait_time=3, js_code=None, screenshot=True, priority=10):
        """
        Crawl a URL using the Docker API.

        Args:
            url: URL to crawl
            wait_time: Seconds to wait before extracting content
            js_code: JavaScript code to execute (list of strings)
            screenshot: Whether to capture screenshot
            priority: Priority level (1-10, higher = more important)

        Returns:
            dict with crawl results
        """
        payload = {
            "urls": [url],
            "priority": priority,
            "wait_time": wait_time,
            "screenshot": screenshot
        }

        if js_code:
            payload["js_code"] = js_code

        try:
            response = requests.post(
                self.crawl_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "message": response.text
                }

        except requests.exceptions.RequestException as e:
            return {
                "error": "Request failed",
                "message": str(e)
            }


def scrape_lidl_with_docker(base_url="http://localhost:11235", max_pages=2):
    """
    Scrape Lidl flyer using Docker API.

    Args:
        base_url: Docker API base URL
        max_pages: Number of pages to scrape
    """
    print("=" * 70)
    print("🛒 Lidl Flyer Scraper - Docker API Mode")
    print("=" * 70)

    # Create output directory
    output_dir = Path("output/lidl_docker")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize client
    client = Crawl4AIDockerClient(base_url)

    # Check if Docker API is available
    print(f"\n🔍 Checking Docker API at {base_url}...")
    if not client.check_health():
        print(f"❌ Cannot connect to Crawl4AI Docker API at {base_url}")
        print("\n💡 Make sure Docker container is running:")
        print("   docker ps --filter name=crawl4ai")
        print("\n   If not running, start it with:")
        print("   docker run -d -p 11235:11235 --shm-size=1g unclecode/crawl4ai:latest")
        return None

    print("✅ Docker API is running!")

    # Lidl flyer URL
    lidl_base_url = "https://www.lidl.it/l/it/volantini/offerte-valide-dal-19-01-al-25-01-volantino-settimanale-9e63be/view/flyer/page"

    all_results = []

    # Scrape each page
    for page_num in range(1, max_pages + 1):
        page_url = f"{lidl_base_url}/{page_num}"

        print(f"\n{'='*70}")
        print(f"📄 Scraping Page {page_num}/{max_pages}")
        print(f"🔗 URL: {page_url}")
        print(f"{'='*70}")

        # JavaScript to scroll and load lazy content
        js_code = [
            "window.scrollTo(0, document.body.scrollHeight / 2);",
            "await new Promise(r => setTimeout(r, 1000));",
            "window.scrollTo(0, document.body.scrollHeight);",
            "await new Promise(r => setTimeout(r, 1000));"
        ]

        # Crawl the page
        print("🚀 Sending crawl request to Docker API...")
        result = client.crawl(
            url=page_url,
            wait_time=3,
            js_code=js_code,
            screenshot=True,
            priority=10
        )

        if "error" in result:
            print(f"❌ Error: {result['error']}")
            print(f"   Message: {result['message']}")
            continue

        # Process results
        if result.get("results"):
            page_result = result["results"][0]

            print(f"✅ Successfully crawled page {page_num}")
            print(f"📊 Status: {page_result.get('status', 'unknown')}")

            # Save markdown
            if page_result.get("markdown"):
                markdown_file = output_dir / f"page_{page_num}_markdown.md"
                with open(markdown_file, "w", encoding="utf-8") as f:
                    f.write(f"# Lidl Flyer - Page {page_num}\n\n")
                    f.write(f"**URL:** {page_url}\n")
                    f.write(f"**Scraped:** {datetime.now().isoformat()}\n\n")
                    f.write("---\n\n")
                    f.write(page_result["markdown"])

                print(f"📝 Markdown saved: {markdown_file}")
                print(f"   Length: {len(page_result['markdown'])} characters")

            # Save HTML
            if page_result.get("html"):
                html_file = output_dir / f"page_{page_num}_raw.html"
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(page_result["html"])
                print(f"💾 HTML saved: {html_file}")

            # Save screenshot (if available)
            if page_result.get("screenshot"):
                screenshot_file = output_dir / f"page_{page_num}_screenshot.png"
                # Screenshot is base64 encoded, decode and save
                import base64
                screenshot_data = base64.b64decode(page_result["screenshot"])
                with open(screenshot_file, "wb") as f:
                    f.write(screenshot_data)
                print(f"📸 Screenshot saved: {screenshot_file}")

            # Show preview
            if page_result.get("markdown"):
                preview = page_result["markdown"][:500]
                print(f"\n📝 Content Preview:")
                print("-" * 70)
                print(preview)
                if len(page_result["markdown"]) > 500:
                    print(f"\n... (truncated, total: {len(page_result['markdown'])} chars)")
                print("-" * 70)

            all_results.append({
                "page": page_num,
                "url": page_url,
                "scraped_at": datetime.now().isoformat(),
                "markdown_length": len(page_result.get("markdown", "")),
                "html_length": len(page_result.get("html", ""))
            })

        else:
            print(f"⚠️  No results returned for page {page_num}")

        # Be nice to the server
        if page_num < max_pages:
            print(f"\n⏳ Waiting 2 seconds before next page...")
            time.sleep(2)

    # Save summary
    print(f"\n{'='*70}")
    print("💾 Saving Summary")
    print(f"{'='*70}")

    summary_file = output_dir / f"scrape_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "scrape_date": datetime.now().isoformat(),
            "total_pages": len(all_results),
            "pages": all_results
        }, f, indent=2)

    print(f"✅ Summary saved: {summary_file}")

    # Final summary
    print(f"\n{'='*70}")
    print("📊 Scraping Summary")
    print(f"{'='*70}")
    print(f"✅ Total pages scraped: {len(all_results)}")
    print(f"💾 Output directory: {output_dir}")
    print(f"\nFiles created:")
    for result in all_results:
        print(f"  Page {result['page']}: Markdown ({result['markdown_length']} chars), HTML ({result['html_length']} chars)")

    return all_results


def test_docker_connection(base_url="http://localhost:11235"):
    """
    Test connection to Crawl4AI Docker API and show available endpoints.
    """
    print("=" * 70)
    print("🔍 Crawl4AI Docker API Connection Test")
    print("=" * 70)

    client = Crawl4AIDockerClient(base_url)

    print(f"\n📍 Testing connection to: {base_url}")

    # Test health endpoint
    print("\n1. Testing /health endpoint...")
    if client.check_health():
        print("   ✅ Health check passed!")
    else:
        print("   ❌ Health check failed!")
        print("\n💡 Troubleshooting:")
        print("   1. Check if container is running:")
        print("      docker ps --filter name=crawl4ai")
        print("   2. Check if port 11235 is accessible")
        print("   3. Try: curl http://localhost:11235/health")
        return False

    # Test crawl with simple URL
    print("\n2. Testing /crawl endpoint with example.com...")
    result = client.crawl(
        url="https://example.com",
        wait_time=2,
        screenshot=False,
        priority=10
    )

    if "error" in result:
        print(f"   ❌ Crawl test failed: {result['error']}")
        return False

    if result.get("results"):
        page = result["results"][0]
        print(f"   ✅ Crawl successful!")
        print(f"   📄 Retrieved {len(page.get('markdown', ''))} chars of Markdown")
        print(f"   📝 Preview:")
        preview = page.get("markdown", "")[:200]
        print(f"      {preview}...")
    else:
        print("   ⚠️  Crawl returned no results")
        return False

    # Show available endpoints
    print(f"\n{'='*70}")
    print("🎯 Available Endpoints")
    print(f"{'='*70}")
    print(f"API Endpoint:  {base_url}/crawl")
    print(f"Dashboard:     {base_url}/dashboard")
    print(f"Playground:    {base_url}/playground")
    print(f"Health Check:  {base_url}/health")

    print(f"\n{'='*70}")
    print("✨ Connection test completed successfully!")
    print(f"{'='*70}")

    return True


def main():
    """Main function."""
    import sys

    # Check if we should just test connection
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("\n🔧 Crawl4AI Docker API - Connection Test\n")
        success = test_docker_connection()
        sys.exit(0 if success else 1)

    # Run full Lidl scraper
    print("\n🛒 Crawl4AI Docker API - Lidl Flyer Scraper")
    print("   Using Docker container instead of local browser\n")

    # Test connection first
    client = Crawl4AIDockerClient()
    if not client.check_health():
        print("❌ Cannot connect to Docker API. Please ensure container is running.")
        print("\n💡 Start the container with:")
        print("   docker run -d -p 11235:11235 --shm-size=1g unclecode/crawl4ai:latest")
        print("\n   Then verify it's running:")
        print("   docker ps --filter name=crawl4ai")
        sys.exit(1)

    # Scrape Lidl flyer
    max_pages = 2
    if len(sys.argv) > 1:
        try:
            max_pages = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Invalid page count, using default: {max_pages}")

    results = scrape_lidl_with_docker(max_pages=max_pages)

    if results:
        print("\n✨ Scraping completed successfully!")
    else:
        print("\n❌ Scraping failed or returned no results")
        sys.exit(1)


if __name__ == "__main__":
    main()
