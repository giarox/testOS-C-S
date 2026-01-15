# Lidl Flyer Scraper - Real World Example

This is a production-ready web scraper for extracting product information from Lidl Italy's weekly promotional flyers.

## Target Website

**URL:** https://www.lidl.it/l/it/volantini/offerte-valide-dal-19-01-al-25-01-volantino-settimanale-9e63be/view/flyer/page/1

**Description:** Lidl Italy weekly promotional catalog showing discounted products and special offers.

## What It Does

The scraper performs two types of extraction:

### 1. Simple Mode
- Extracts clean Markdown representation of the flyer
- Captures screenshots for verification
- Saves raw HTML for debugging
- Good for initial testing and content preview

### 2. Structured Mode
- Extracts detailed product information:
  - Product name
  - Current price
  - Original price (if available)
  - Product description
  - Image URLs
  - Discount badges/labels
  - Page number
  - Source URL

- Supports multi-page scraping with pagination
- Exports data to JSON format
- Creates individual files per page

## Features Demonstrated

### Advanced Crawl4AI Capabilities
- **Dynamic Content Handling**: Executes JavaScript to load lazy-loaded images and content
- **Structured Data Extraction**: Uses CSS selectors with JsonCssExtractionStrategy
- **Screenshot Capture**: Takes screenshots of each page for verification
- **Pagination**: Automatically crawls multiple pages
- **Smart Delays**: Implements proper waiting times for content to load
- **Markdown Export**: Clean, LLM-ready content extraction

### Technical Features
- Realistic user agent to avoid blocking
- Scroll simulation to trigger lazy loading
- Configurable page timeout
- Rate limiting (2-second delay between pages)
- Comprehensive error handling
- Multiple output formats (JSON, Markdown, HTML, PNG)

## Usage

### Basic Usage

```bash
# Activate environment
source venv/bin/activate

# Run the scraper
python test_lidl_scraper.py
```

Or use the test runner:
```bash
./run_tests.sh lidl
```

### Customization

Edit the script to adjust:

```python
# Change number of pages to scrape
products = await scrape_lidl_flyer(lidl_url, max_pages=5)

# Adjust wait times
delay_before_return_html=5.0  # Wait 5 seconds instead of 3

# Change product extraction schema
product_schema = {
    # Modify CSS selectors to match actual page structure
    "baseSelector": ".your-product-class",
    # ... more fields
}
```

## Output Structure

All results are saved to `output/lidl_scraper/`:

```
output/lidl_scraper/
├── lidl_products_20260115_143052.json    # All products in structured format
├── page_1_raw.html                       # Raw HTML of page 1
├── page_1_markdown.md                    # Clean Markdown of page 1
├── page_1_screenshot.png                 # Screenshot of page 1
├── page_2_raw.html                       # Page 2 files...
├── page_2_markdown.md
├── page_2_screenshot.png
└── ...
```

### JSON Output Format

```json
{
  "scrape_date": "2026-01-15T14:30:52",
  "total_products": 42,
  "pages_scraped": 2,
  "products": [
    {
      "product_name": "Organic Bananas",
      "price": "€1.99",
      "original_price": "€2.49",
      "description": "1 kg pack, imported from Ecuador",
      "image_url": "https://www.lidl.it/...",
      "discount": "-20%",
      "page": 1,
      "url": "https://www.lidl.it/.../page/1"
    },
    {
      "product_name": "Premium Coffee",
      "price": "€4.99",
      ...
    }
  ]
}
```

## Troubleshooting

### CSS Selectors Not Working

The product extraction uses CSS selectors that may need adjustment if Lidl updates their website structure:

1. Run the simple mode first to see the page structure:
   ```python
   await scrape_lidl_flyer_simple(lidl_url)
   ```

2. Check the HTML output file to find actual CSS classes
3. Update the `product_schema` in the script with correct selectors
4. Common Lidl product selectors:
   - `.product-card`
   - `.offer-item`
   - `[data-product]`
   - `article.product`

### No Products Extracted

1. Check screenshots to verify page loaded correctly
2. Review HTML files to see actual page structure
3. Increase `delay_before_return_html` if content loads slowly
4. Check if page requires additional scrolling or interactions

### Browser Not Installed

See main [SETUP_NOTES.md](./SETUP_NOTES.md) for comprehensive browser installation solutions.

Quick fix:
```bash
source venv/bin/activate
python -m playwright install chromium
```

## Extending the Scraper

### Scrape Different Weeks

Update the URL in the script:
```python
lidl_url = "https://www.lidl.it/l/it/volantini/offerte-valide-dal-DD-MM-al-DD-MM-volantino-settimanale-XXXXX/view/flyer/page/1"
```

### Add More Data Fields

Extend the `product_schema`:
```python
{
    "name": "availability",
    "selector": ".stock-status",
    "type": "text"
},
{
    "name": "category",
    "selector": ".product-category",
    "type": "text"
}
```

### Export to CSV

Add this after scraping:
```python
import csv

with open('lidl_products.csv', 'w', newline='', encoding='utf-8') as f:
    if all_products:
        writer = csv.DictWriter(f, fieldnames=all_products[0].keys())
        writer.writeheader()
        writer.writerows(all_products)
```

## Use Cases

1. **Price Monitoring**: Track product prices over time
2. **Competitor Analysis**: Compare prices with other retailers
3. **Inventory Planning**: Identify promotional patterns
4. **Data Analysis**: Analyze discount trends and pricing strategies
5. **Consumer Apps**: Build price comparison tools
6. **Research**: Study retail pricing and promotional strategies

## Legal & Ethical Considerations

- ⚠️ **Terms of Service**: Check Lidl.it's robots.txt and terms of service
- 🚦 **Rate Limiting**: Script includes 2-second delays to be respectful
- 📊 **Personal Use**: Designed for educational and personal use
- 🔒 **No Authentication Bypass**: Only scrapes publicly accessible pages
- 🤝 **Responsible Scraping**: Uses realistic user agents, respects server load

Always ensure your scraping activities comply with:
- Website's Terms of Service
- Local data protection laws (GDPR in EU)
- Responsible scraping best practices

## Performance

- **Speed**: ~5-10 seconds per page (including delays)
- **Memory**: ~100-200 MB during execution
- **Storage**: ~2-5 MB per page scraped (HTML, screenshots, JSON)

## Related Files

- [test_lidl_scraper.py](./test_lidl_scraper.py) - Main scraper script
- [SETUP_NOTES.md](./SETUP_NOTES.md) - Browser installation solutions
- [README.md](./README.md) - Main project documentation

## Support

For issues specific to this scraper:
1. Check screenshots in `output/lidl_scraper/` to verify page loading
2. Review HTML files to confirm page structure
3. Adjust CSS selectors if Lidl has updated their website
4. See main SETUP_NOTES.md for browser installation issues

For Crawl4AI issues:
- GitHub: https://github.com/unclecode/crawl4ai/issues
- Documentation: https://docs.crawl4ai.com
