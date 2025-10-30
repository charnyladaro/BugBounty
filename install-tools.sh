#!/bin/bash

# Bug Bounty TUI - Tool Installer
# Checks for required tools and installs missing ones

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         BUG BOUNTY TUI - TOOL INSTALLER v1.0              ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

REQUIRED_TOOLS=(
    "nmap"
    "gobuster"
    "nikto"
    "whatweb"
    "wafw00f"
    "sslscan"
    "curl"
)

GO_TOOLS=(
    "subfinder:github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    "gospider:github.com/jaeles-project/gospider@latest"
    "waybackurls:github.com/tomnomnom/waybackurls@latest"
    "dalfox:github.com/hahwul/dalfox/v2@latest"
    "amass:github.com/owasp-amass/amass/v4/...@master"
)

PYTHON_TOOLS=(
    "sqlmap"
)

echo "[*] Checking system tools..."

missing_tools=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "  [✓] $tool - installed"
    else
        echo "  [✗] $tool - missing"
        missing_tools+=("$tool")
    fi
done

echo ""
echo "[*] Checking Go tools..."

for tool_info in "${GO_TOOLS[@]}"; do
    tool_name="${tool_info%%:*}"
    if command -v "$tool_name" &> /dev/null; then
        echo "  [✓] $tool_name - installed"
    else
        echo "  [✗] $tool_name - missing"
        missing_tools+=("$tool_name")
    fi
done

echo ""
echo "[*] Checking Python tools..."

for tool in "${PYTHON_TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "  [✓] $tool - installed"
    else
        echo "  [✗] $tool - missing"
        missing_tools+=("$tool")
    fi
done

echo ""

if [ ${#missing_tools[@]} -eq 0 ]; then
    echo "[✓] All required tools are installed!"
    echo ""
    echo "Run the TUI with: python3 bugbounty-tui.py"
    exit 0
fi

echo "[!] Missing ${#missing_tools[@]} tool(s): ${missing_tools[*]}"
echo ""
read -p "Do you want to install missing tools? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "[!] Installation cancelled. Some features may not work."
    exit 1
fi

echo ""
echo "[*] Installing missing tools..."
echo ""

# Install system tools
for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        echo "[*] Installing $tool..."
        sudo apt-get install -y "$tool" 2>&1 | tail -5
    fi
done

# Install Go tools
for tool_info in "${GO_TOOLS[@]}"; do
    tool_name="${tool_info%%:*}"
    tool_path="${tool_info#*:}"
    
    if ! command -v "$tool_name" &> /dev/null; then
        echo "[*] Installing $tool_name..."
        go install -v "$tool_path" 2>&1 | tail -5
    fi
done

# Install Python tools
for tool in "${PYTHON_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        echo "[*] Installing $tool..."
        if [ "$tool" = "sqlmap" ]; then
            sudo apt-get install -y sqlmap 2>&1 | tail -5
        fi
    fi
done

echo ""
echo "[✓] Installation complete!"
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         Ready to launch Bug Bounty TUI!                  ║"
echo "║                                                           ║"
echo "║         Run: python3 bugbounty-tui.py                    ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
