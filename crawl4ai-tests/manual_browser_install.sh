#!/bin/bash
# Manual Browser Installation Script for Playwright
# Use this when automatic downloads fail due to network restrictions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Manual Playwright Browser Installation"
echo "=========================================="
echo ""

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <path-to-chromium-zip>"
    echo ""
    echo "Example: $0 ~/Downloads/chromium-linux.zip"
    echo ""
    echo "Download URL: https://playwright.azureedge.net/builds/chromium/1200/chromium-linux.zip"
    echo ""
    echo "Note: Version 1200 corresponds to Chromium 143.0.7499.4"
    echo "      Adjust version number based on your Playwright installation"
    exit 1
fi

BROWSER_ZIP="$1"

if [ ! -f "$BROWSER_ZIP" ]; then
    echo "❌ Error: File not found: $BROWSER_ZIP"
    exit 1
fi

echo "📦 Browser archive: $BROWSER_ZIP"
echo ""

# Detect Playwright version and browser build
echo "🔍 Detecting Playwright configuration..."
source "$SCRIPT_DIR/venv/bin/activate"

BROWSER_BUILD=$(python3 - <<EOF
try:
    from playwright._impl._driver import compute_driver_executable, get_driver_env
    import json

    # Get browser registry info
    import subprocess
    result = subprocess.run(
        ["python", "-m", "playwright", "install", "--dry-run", "chromium"],
        capture_output=True,
        text=True
    )

    # Extract build number from output
    for line in result.stderr.split('\n'):
        if 'chromium' in line.lower() and 'build' in line.lower():
            import re
            match = re.search(r'v?(\d+)', line)
            if match:
                print(match.group(1))
                break
    else:
        print("1200")  # Default fallback
except:
    print("1200")  # Default fallback
EOF
)

echo "📋 Browser build version: $BROWSER_BUILD"
echo ""

# Determine installation directory
if [ ! -z "$PLAYWRIGHT_BROWSERS_PATH" ]; then
    INSTALL_BASE="$PLAYWRIGHT_BROWSERS_PATH"
else
    INSTALL_BASE="$HOME/.cache/ms-playwright"
fi

INSTALL_DIR="$INSTALL_BASE/chromium-$BROWSER_BUILD"

echo "📂 Installation directory: $INSTALL_DIR"
echo ""

# Check if already installed
if [ -f "$INSTALL_DIR/INSTALLATION_COMPLETE" ]; then
    echo "⚠️  Browser already installed at $INSTALL_DIR"
    read -p "Reinstall? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled"
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

# Create directory
echo "📁 Creating directory structure..."
mkdir -p "$INSTALL_DIR"

# Extract archive
echo "📦 Extracting browser archive..."
if command -v unzip &> /dev/null; then
    unzip -q "$BROWSER_ZIP" -d "$INSTALL_DIR/"
elif command -v 7z &> /dev/null; then
    7z x "$BROWSER_ZIP" -o"$INSTALL_DIR/" -y > /dev/null
else
    echo "❌ Error: Neither unzip nor 7z found. Please install unzip:"
    echo "   sudo apt-get install unzip"
    exit 1
fi

echo "✅ Extraction complete"
echo ""

# List extracted contents
echo "📋 Extracted contents:"
ls -la "$INSTALL_DIR/" | head -10
echo ""

# Create marker files
echo "🏷️  Creating installation marker files..."
touch "$INSTALL_DIR/INSTALLATION_COMPLETE"
touch "$INSTALL_DIR/DEPENDENCIES_VALIDATED"

echo "✅ Marker files created"
echo ""

# Set executable permissions
echo "🔧 Setting executable permissions..."
find "$INSTALL_DIR" -type f -name "chrome" -o -name "chromium" | while read -r executable; do
    chmod +x "$executable"
    echo "  Made executable: $executable"
done

# Find and set permissions for chrome-wrapper if it exists
find "$INSTALL_DIR" -type f -name "*chrome*" -executable -o -name "chromium*" | head -5 | while read -r file; do
    chmod +x "$file" 2>/dev/null || true
done

echo ""

# Verify installation
echo "🔍 Verifying installation..."
if [ -f "$INSTALL_DIR/INSTALLATION_COMPLETE" ]; then
    echo "✅ Installation markers present"
else
    echo "❌ Installation markers missing"
    exit 1
fi

# Try to find the chrome executable
CHROME_EXEC=$(find "$INSTALL_DIR" -name "chrome" -o -name "chromium" | grep -v ".so" | head -1)
if [ ! -z "$CHROME_EXEC" ]; then
    echo "✅ Chrome executable found: $CHROME_EXEC"

    # Test if executable runs
    if [ -x "$CHROME_EXEC" ]; then
        echo "✅ Executable permissions OK"
    else
        echo "⚠️  Setting executable permissions..."
        chmod +x "$CHROME_EXEC"
    fi
else
    echo "⚠️  Chrome executable not found in expected location"
    echo "   Contents of $INSTALL_DIR:"
    ls -la "$INSTALL_DIR/"
fi

echo ""
echo "=========================================="
echo "✨ Installation Complete!"
echo "=========================================="
echo ""
echo "Installation location: $INSTALL_DIR"
echo ""
echo "🧪 Test the installation:"
echo "   source venv/bin/activate"
echo "   python test_basic.py"
echo ""
echo "Or verify with:"
echo "   python -m playwright install --dry-run chromium"
echo ""
