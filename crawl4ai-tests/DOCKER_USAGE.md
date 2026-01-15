# Using Crawl4AI Docker Container

You've successfully started the Crawl4AI Docker container! Here's how to use it to scrape the Lidl flyer.

## Quick Start - 3 Simple Commands

Run these commands on your **local machine** where Docker is running:

### 1. Verify Container is Running

```bash
docker ps --filter name=crawl4ai
```

Should show a running container on port 11235.

### 2. Test API Connection

```bash
curl http://localhost:11235/health
```

Should return: `{"status":"healthy"}`

### 3. Scrape Lidl Page (Simple Test)

```bash
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://www.lidl.it/l/it/volantini/offerte-valide-dal-19-01-al-25-01-volantino-settimanale-9e63be/view/flyer/page/1"],
    "priority": 10,
    "wait_time": 3
  }' > lidl_result.json
```

Then view the results:
```bash
cat lidl_result.json
```

---

## Method 1: Simple Curl Command (Recommended)

Copy and paste this into your terminal:

```bash
curl -X POST http://localhost:11235/crawl \
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
  }' | python3 -m json.tool > lidl_page1_full.json
```

This will:
- ✅ Scrape the Lidl flyer page 1
- ✅ Execute JavaScript to load lazy content
- ✅ Capture a screenshot
- ✅ Save everything to `lidl_page1_full.json`

**View the markdown content:**
```bash
python3 -c "import json; data=json.load(open('lidl_page1_full.json')); print(data['results'][0]['markdown'])" > lidl_page1.md
cat lidl_page1.md
```

---

## Method 2: Using the Test Script

Download the test script from this repo:

```bash
# Copy test_lidl_local.sh to your local machine
# Then run:
chmod +x test_lidl_local.sh
./test_lidl_local.sh
```

This script will:
1. Check if Docker container is running
2. Test API health
3. Scrape Lidl page 1
4. Extract and save markdown
5. Show a preview

---

## Method 3: Using Python Script

If you have Python with requests library:

```bash
# Copy test_lidl_docker_api.py to your local machine
pip install requests

# Test connection
python3 test_lidl_docker_api.py test

# Scrape Lidl (default 2 pages)
python3 test_lidl_docker_api.py

# Scrape 5 pages
python3 test_lidl_docker_api.py 5
```

---

## Method 4: Using the Web Interface

Open your browser and visit:

**Dashboard:** http://localhost:11235/dashboard
**Playground:** http://localhost:11235/playground

In the playground, you can:
1. Enter the URL: `https://www.lidl.it/l/it/volantini/offerte-valide-dal-19-01-al-25-01-volantino-settimanale-9e63be/view/flyer/page/1`
2. Configure options (wait time, JavaScript, etc.)
3. Click "Crawl"
4. View results in the browser

---

## Understanding the Response

The API returns a JSON response with this structure:

```json
{
  "task_id": "abc123...",
  "status": "completed",
  "results": [
    {
      "url": "https://www.lidl.it/...",
      "markdown": "# Clean markdown content...",
      "html": "<html>Raw HTML...</html>",
      "screenshot": "base64_encoded_image...",
      "metadata": {
        "title": "Lidl - Volantino...",
        ...
      }
    }
  ]
}
```

**Key fields:**
- `markdown` - Clean, LLM-ready text content
- `html` - Raw HTML source
- `screenshot` - Base64-encoded PNG screenshot
- `metadata` - Page title, description, etc.

---

## Scraping Multiple Pages

To scrape pages 1-3, run these commands:

```bash
# Page 1
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.lidl.it/.../page/1"], "priority": 10, "wait_time": 3}' \
  > page1.json

# Page 2
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.lidl.it/.../page/2"], "priority": 10, "wait_time": 3}' \
  > page2.json

# Page 3
curl -X POST http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.lidl.it/.../page/3"], "priority": 10, "wait_time": 3}' \
  > page3.json
```

---

## Extracting Product Information

The markdown content will contain product information. To extract structured data, you can:

1. **Use the markdown content** - Already clean and formatted
2. **Parse the HTML** - Use BeautifulSoup or similar
3. **Use AI extraction** - Feed the markdown to an LLM

Example - save markdown for AI processing:

```bash
# Extract markdown from page 1
python3 -c "
import json
with open('page1.json') as f:
    data = json.load(f)
    markdown = data['results'][0]['markdown']
    with open('lidl_page1.md', 'w') as out:
        out.write(markdown)
"

# Now feed lidl_page1.md to your LLM or parser
```

---

## Troubleshooting

### Container not responding

```bash
# Check container status
docker ps -a --filter name=crawl4ai

# View logs
docker logs crawl4ai

# Restart container
docker restart crawl4ai

# Or stop and start fresh
docker stop crawl4ai
docker rm crawl4ai
docker run -d -p 11235:11235 --name crawl4ai --shm-size=1g unclecode/crawl4ai:latest
```

### Port already in use

```bash
# Use a different port
docker run -d -p 8080:11235 --name crawl4ai --shm-size=1g unclecode/crawl4ai:latest

# Then use http://localhost:8080 instead
```

### Slow scraping

- Increase `wait_time` in the request (default 3 seconds)
- Reduce `priority` for less important pages
- Check Docker container resources

---

## Advanced Options

### Request Parameters

```json
{
  "urls": ["https://example.com"],
  "priority": 10,                    // 1-10, higher = more important
  "wait_time": 3,                    // Seconds to wait before extracting
  "screenshot": true,                // Capture screenshot
  "js_code": ["console.log('hi')"],  // JavaScript to execute
  "cache_mode": "bypass",            // bypass, read, write
  "page_timeout": 30                 // Max seconds for page load
}
```

### JavaScript Execution

Execute custom JavaScript on the page:

```json
{
  "js_code": [
    "// Click a button",
    "document.querySelector('.button').click();",
    "",
    "// Wait for content to load",
    "await new Promise(r => setTimeout(r, 2000));",
    "",
    "// Scroll to bottom",
    "window.scrollTo(0, document.body.scrollHeight);",
    "",
    "// Extract custom data",
    "const products = Array.from(document.querySelectorAll('.product')).map(p => p.textContent);"
  ]
}
```

---

## Production Tips

1. **Rate Limiting** - Add delays between requests
   ```bash
   for i in {1..5}; do
     curl ... > page${i}.json
     sleep 2  # Wait 2 seconds
   done
   ```

2. **Error Handling** - Check response status
   ```bash
   response=$(curl -s -w "\n%{http_code}" ...)
   http_code=$(echo "$response" | tail -n1)
   if [ "$http_code" -eq 200 ]; then
     echo "Success"
   else
     echo "Failed: $http_code"
   fi
   ```

3. **Batch Processing** - Scrape multiple URLs at once
   ```json
   {
     "urls": [
       "https://example.com/page1",
       "https://example.com/page2",
       "https://example.com/page3"
     ]
   }
   ```

---

## Next Steps

1. ✅ Test basic scraping with the simple curl command
2. ✅ Review the markdown output
3. ✅ Scrape multiple pages
4. ✅ Extract product information
5. ✅ Integrate into your workflow

For more examples and advanced usage, see:
- [test_lidl_docker_api.py](./test_lidl_docker_api.py) - Python implementation
- [LIDL_SCRAPER_README.md](./LIDL_SCRAPER_README.md) - Detailed scraper documentation
- Official docs: https://docs.crawl4ai.com
