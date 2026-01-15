#!/bin/bash
# Lidl Flyer Scraper - Docker API Test Script
# Run this on your local machine where Docker is running

echo "=========================================="
echo "🛒 Lidl Flyer Scraper - Docker API Test"
echo "=========================================="
echo ""

# Check if Docker container is running
echo "🔍 Checking if Crawl4AI Docker container is running..."
if ! docker ps --filter name=crawl4ai | grep -q crawl4ai; then
    echo "❌ Crawl4AI container is not running!"
    echo ""
    echo "Starting container..."
    docker run -d -p 11235:11235 --name crawl4ai --shm-size=1g unclecode/crawl4ai:latest
    echo "⏳ Waiting 10 seconds for container to start..."
    sleep 10
fi

echo "✅ Container is running"
echo ""

# Test health endpoint
echo "🔍 Testing API health..."
if curl -s http://localhost:11235/health > /dev/null; then
    echo "✅ API is healthy"
else
    echo "❌ API not responding"
    exit 1
fi
echo ""

# Scrape Lidl page 1
echo "=========================================="
echo "📄 Scraping Lidl Flyer Page 1"
echo "=========================================="
echo ""
echo "URL: https://www.lidl.it/l/it/volantini/offerte-valide-dal-19-01-al-25-01-volantino-settimanale-9e63be/view/flyer/page/1"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://www.lidl.it/l/it/volantini/offerte-valide-dal-19-01-al-25-01-volantino-settimanale-9e63be/view/flyer/page/1"],
    "priority": 10,
    "wait_time": 3,
    "js_code": [
      "window.scrollTo(0, document.body.scrollHeight / 2);",
      "await new Promise(r => setTimeout(r, 1000));",
      "window.scrollTo(0, document.body.scrollHeight);",
      "await new Promise(r => setTimeout(r, 1000));"
    ],
    "screenshot": true
  }')

# Save full response
echo "$RESPONSE" > lidl_response.json
echo "✅ Full response saved to: lidl_response.json"
echo ""

# Extract and display markdown preview
echo "📝 Markdown Content Preview:"
echo "=========================================="
MARKDOWN=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['markdown'][:800] if 'results' in data and data['results'] and 'markdown' in data['results'][0] else 'No markdown found')" 2>/dev/null)

if [ -n "$MARKDOWN" ]; then
    echo "$MARKDOWN"
    echo ""
    echo "... (truncated for preview)"
    echo ""

    # Save markdown to file
    echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['results'][0]['markdown'])" 2>/dev/null > lidl_page1.md
    echo "✅ Full markdown saved to: lidl_page1.md"

    # Count characters
    CHAR_COUNT=$(wc -c < lidl_page1.md)
    echo "📊 Total content: $CHAR_COUNT characters"
else
    echo "⚠️  Could not extract markdown. Check lidl_response.json for details."
fi

echo ""
echo "=========================================="
echo "✨ Scraping Complete!"
echo "=========================================="
echo ""
echo "Files created:"
echo "  - lidl_response.json  (Full API response)"
echo "  - lidl_page1.md       (Extracted markdown content)"
echo ""
echo "💡 To view the content:"
echo "   cat lidl_page1.md"
echo ""
echo "💡 To scrape more pages, modify the URL in this script"
echo "   Change '/page/1' to '/page/2', '/page/3', etc."
echo ""
