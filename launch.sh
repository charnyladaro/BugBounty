#!/bin/bash

clear

cat << "EOF"
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ██████╗ ██╗   ██╗ ██████╗ ██████╗  ██████╗ ██╗   ██╗███╗   ██╗ ║
║   ██╔══██╗██║   ██║██╔════╝ ██╔══██╗██╔═══██╗██║   ██║████╗  ██║ ║
║   ██████╔╝██║   ██║██║  ███╗██████╔╝██║   ██║██║   ██║██╔██╗ ██║ ║
║   ██╔══██╗██║   ██║██║   ██║██╔══██╗██║   ██║██║   ██║██║╚██╗██║ ║
║   ██████╔╝╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║ ║
║   ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ║
║                                                                   ║
║            TACTICAL RECONNAISSANCE FRAMEWORK v2.0                 ║
║                  AUTOMATED SECURITY TESTING SUITE                 ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

EOF

echo ""
echo "[*] Checking Python dependencies..."

if ! python3 -c "import rich" 2>/dev/null; then
    echo "[!] Installing Rich library..."
    pip3 install rich --break-system-packages -q
fi

if ! python3 -c "import textual" 2>/dev/null; then
    echo "[!] Installing Textual library..."
    pip3 install textual --break-system-packages -q
fi

echo "[✓] Dependencies OK"
echo ""
echo "[*] Launching Bug Bounty TUI..."
echo ""

sleep 1

# Launch the TUI
python3 bugbounty-tui.py
