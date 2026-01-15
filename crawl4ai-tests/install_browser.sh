#!/bin/bash
# Crawl4AI Browser Installation Helper Script
# This script tries multiple methods to install Chromium for Playwright

set -e

echo "=========================================="
echo "Crawl4AI Browser Installation Helper"
echo "=========================================="
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Run from crawl4ai-tests directory."
    exit 1
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Function to check if browser is installed
check_browser() {
    echo ""
    echo "🔍 Checking browser installation..."
    python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.chromium.launch(); print('✅ Browser is installed and working!')" 2>/dev/null
    return $?
}

# Method 1: Try with extended timeout
echo ""
echo "=========================================="
echo "Method 1: Install with Extended Timeout"
echo "=========================================="
echo "Setting connection timeout to 120 seconds..."
export PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000

echo "Running: python -m playwright install chromium"
if python -m playwright install chromium 2>&1 | tee /tmp/playwright_install.log; then
    echo "✅ Installation succeeded!"
    if check_browser; then
        exit 0
    fi
else
    echo "⚠️  Method 1 failed. Trying next method..."
fi

# Method 2: Try with proxy if available
if [ ! -z "$HTTP_PROXY" ] || [ ! -z "$HTTPS_PROXY" ]; then
    echo ""
    echo "=========================================="
    echo "Method 2: Install via Proxy"
    echo "=========================================="
    echo "Proxy detected:"
    echo "  HTTP_PROXY: $HTTP_PROXY"
    echo "  HTTPS_PROXY: $HTTPS_PROXY"

    echo "Running: python -m playwright install chromium"
    if python -m playwright install chromium 2>&1 | tee /tmp/playwright_install.log; then
        echo "✅ Installation succeeded!"
        if check_browser; then
            exit 0
        fi
    else
        echo "⚠️  Method 2 failed. Trying next method..."
    fi
fi

# Method 3: Try with custom browser path
echo ""
echo "=========================================="
echo "Method 3: Custom Browser Storage Location"
echo "=========================================="
CUSTOM_BROWSER_PATH="$HOME/.crawl4ai-browsers"
mkdir -p "$CUSTOM_BROWSER_PATH"
echo "Using custom path: $CUSTOM_BROWSER_PATH"
export PLAYWRIGHT_BROWSERS_PATH="$CUSTOM_BROWSER_PATH"

echo "Running: python -m playwright install chromium"
if python -m playwright install chromium 2>&1 | tee /tmp/playwright_install.log; then
    echo "✅ Installation succeeded!"
    if check_browser; then
        exit 0
    fi
else
    echo "⚠️  Method 3 failed. Trying next method..."
fi

# Method 4: Try crawl4ai-setup
echo ""
echo "=========================================="
echo "Method 4: Using crawl4ai-setup"
echo "=========================================="
unset PLAYWRIGHT_BROWSERS_PATH
export PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000

echo "Running: crawl4ai-setup"
if crawl4ai-setup 2>&1 | tee /tmp/crawl4ai_setup.log; then
    echo "✅ Setup completed!"
    if check_browser; then
        exit 0
    fi
else
    echo "⚠️  Method 4 failed."
fi

# All methods failed
echo ""
echo "=========================================="
echo "❌ All automatic installation methods failed"
echo "=========================================="
echo ""
echo "📋 Diagnosis:"
echo ""
grep -i "error\|403\|forbidden\|failed" /tmp/playwright_install.log 2>/dev/null | head -5 || echo "No error log available"
echo ""
echo "🔧 Manual Solutions:"
echo ""
echo "1. Whitelist these domains in your firewall/proxy:"
echo "   - playwright.azureedge.net"
echo "   - cdn.playwright.dev"
echo "   - playwright.download.prss.microsoft.com"
echo ""
echo "2. Manual offline installation:"
echo "   Download from: https://playwright.azureedge.net/builds/chromium/1200/chromium-linux.zip"
echo "   Extract to: ~/.cache/ms-playwright/chromium-1200/"
echo "   Run: ./manual_browser_install.sh <path-to-zip>"
echo ""
echo "3. Use Docker (recommended):"
echo "   docker pull unclecode/crawl4ai:latest"
echo "   docker run -d -p 11235:11235 --shm-size=1g unclecode/crawl4ai:latest"
echo ""
echo "4. Configure proxy (if behind corporate firewall):"
echo "   export HTTPS_PROXY=https://your-proxy:port"
echo "   export HTTP_PROXY=http://your-proxy:port"
echo "   Then rerun this script"
echo ""
echo "See SETUP_NOTES.md for detailed instructions."
echo ""

exit 1
