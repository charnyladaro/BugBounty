
# 🎯 QUICK START GUIDE - Bug Bounty TUI

## 📦 Files You Received

```
📁 Your Files:
├── 📄 bugbounty-tui.py          - Main TUI application (Python)
├── 🚀 launch.sh                  - One-click launcher
├── 🔧 install-tools.sh           - Tool installer/checker
├── 📖 README-TUI.md              - Complete documentation
└── 📋 GoCardless-BugBounty-Guide.md - Full testing guide
```

## ⚡ FASTEST WAY TO START (3 Commands)

```bash
# 1. Go to your Kali terminal and navigate to where you saved the files
cd /path/to/downloaded/files

# 2. Make scripts executable
chmod +x launch.sh install-tools.sh bugbounty-tui.py

# 3. Launch!
./launch.sh
```

**That's it!** The TUI will open and you can start scanning!

---

## 🎮 STEP-BY-STEP USAGE

### Step 1: Open Your Kali Linux Terminal (WSL)

```bash
# In Windows, open PowerShell or Command Prompt and type:
wsl
```

### Step 2: Copy Files to Kali

Option A: If files are in Windows
```bash
# Copy from Windows to Kali
cp /mnt/c/Users/YourName/Downloads/bugbounty-tui.py ~/
cp /mnt/c/Users/YourName/Downloads/launch.sh ~/
cp /mnt/c/Users/YourName/Downloads/install-tools.sh ~/
```

Option B: Download directly in Kali (if you have them online)
```bash
cd ~
# Or just paste the files using your text editor
```

### Step 3: Make Executable

```bash
chmod +x launch.sh install-tools.sh bugbounty-tui.py
```

### Step 4: (Optional) Install Tools

First time only - check if tools are installed:
```bash
./install-tools.sh
```

This will show you what's installed and what's missing.

### Step 5: Launch the TUI

```bash
./launch.sh
```

### Step 6: Use the Interface

Once the TUI opens, you'll see:

```
┌─────────────────────────────────────────┐
│  TARGET ACQUISITION                     │
└─────────────────────────────────────────┘
[                                          ] ← Enter URL here

┌─────────────────────────────────────────┐
│  SCAN CONFIGURATION                     │
└─────────────────────────────────────────┘
☑ Subdomain Enumeration
☑ Port Scanning
☑ Directory Bruteforce
☐ SQL Injection
☐ XSS Detection

[⚡ START SCAN] [⏸️ STOP] [🗑️ CLEAR] [📊 RESULTS]

═══════════════════════════════════════════
SYSTEM OUTPUT - REAL-TIME MONITORING
═══════════════════════════════════════════
>>> SYSTEM INITIALIZED
>>> Awaiting target input...
```

1. **Enter target URL:** Type `https://manage-sandbox.gocardless.com`
2. **Select scans:** Check boxes for scans you want
3. **Click START SCAN:** Press Tab to move to button, Enter to click
   - Or just press `R` key
4. **Watch it work:** See real-time output as scans execute!

---

## 🎨 WHAT IT LOOKS LIKE

### Welcome Screen
```
╔═══════════════════════════════════════════════╗
║   ██████╗ ██╗   ██╗ ██████╗                  ║
║   ██╔══██╗██║   ██║██╔════╝                  ║
║   ██████╔╝██║   ██║██║  ███╗                 ║
║   ██╔══██╗██║   ██║██║   ██║                 ║
║   ██████╔╝╚██████╔╝╚██████╔╝                 ║
╚═══════════════════════════════════════════════╝

      ⚡ INITIALIZE MISSION ⚡
```

### Scanning Screen
```
▶▶▶ EXECUTING: SUBDOMAINS
$ subfinder -d gocardless.com -o subdomains.txt
api-sandbox.gocardless.com
manage-sandbox.gocardless.com
connect-sandbox.gocardless.com
✓ SUBDOMAINS COMPLETE

▶▶▶ EXECUTING: PORTS
$ nmap -sV -sC -p 80,443,8080,8443 manage-sandbox...
PORT    STATE SERVICE
443/tcp open  ssl/http
✓ PORTS COMPLETE

[███████████░░░░░░░░░] 60% Complete
```

---

## ⌨️ KEYBOARD SHORTCUTS

| Key | What it does |
|-----|-------------|
| `R` | Run scan (same as clicking START SCAN) |
| `S` | Stop current scan |
| `C` | Clear output window |
| `Q` | Quit application |
| `Tab` | Move between elements |
| `Enter` | Click button / check box |
| `ESC` | Go back |

---

## 🔥 COOL FEATURES

### 1. Real-Time Output
Watch commands execute live - you see exactly what's happening!

### 2. Progress Bar
Visual progress tracking shows how far through the scans you are.

### 3. Auto-Save Results
Everything is automatically saved to:
```
scans/target.com_20251027_143022/
├── subdomains.txt
├── nmap-scan.txt
├── gobuster.txt
└── ...
```

### 4. Color-Coded Output
- 🟢 Green = Success
- 🔴 Red = Error
- 🟡 Yellow = Warning
- 🔵 Cyan = Info

### 5. Modular Scanning
Pick exactly which tools you want to run - don't waste time on scans you don't need!

### 6. One-Click Launch
No need to remember commands - just run `./launch.sh`

---

## 🎯 EXAMPLE: Full Scan on GoCardless

```bash
# 1. Launch
./launch.sh

# 2. In the TUI:
Target: https://manage-sandbox.gocardless.com

# 3. Check these boxes:
✅ Subdomain Enumeration
✅ Port Scanning
✅ Directory Bruteforce
✅ Technology Detection
✅ Historical URLs

# 4. Press 'R' or click START SCAN

# 5. Watch it go!
>>> INITIATING SCAN SEQUENCE
>>> TARGET: https://manage-sandbox.gocardless.com
>>> OUTPUT: ./scans/manage-sandbox.gocardless.com_20251027_143022
>>> MODULES: 5

▶▶▶ EXECUTING: SUBDOMAINS
Found: api-sandbox.gocardless.com
Found: connect-sandbox.gocardless.com
...
✓ SUBDOMAINS COMPLETE

▶▶▶ EXECUTING: PORTS
PORT    STATE
443/tcp open
...
✓ PORTS COMPLETE

... (continues for all selected scans)

>>> ALL SCANS COMPLETED
>>> Results saved to: ./scans/...
```

---

## 🛠️ TROUBLESHOOTING

### Problem: "Command not found: python3"
**Solution:**
```bash
# Try python instead
python bugbounty-tui.py

# Or install python3
sudo apt update && sudo apt install python3
```

### Problem: "Module not found: rich"
**Solution:**
```bash
pip3 install rich textual --break-system-packages
```

### Problem: "Permission denied"
**Solution:**
```bash
chmod +x launch.sh install-tools.sh bugbounty-tui.py
```

### Problem: TUI looks broken/weird
**Solution:**
```bash
# Your terminal might not support colors
# Try a different terminal or:
export TERM=xterm-256color
./launch.sh
```

### Problem: "Tool not found: subfinder"
**Solution:**
```bash
# Run installer
./install-tools.sh

# Or install manually
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

---

## 🚀 ADVANCED TIPS

### Tip 1: Run Specific Tools Only
Uncheck boxes you don't need to save time!

### Tip 2: Check Results While Scanning
Results are saved immediately - you can open the files while scans are running:
```bash
# In another terminal
tail -f scans/target_*/subdomains.txt
```

### Tip 3: Resume After Stopping
Stopped a scan? Just run it again - results are in separate timestamped folders.

### Tip 4: Multiple Targets
Want to scan multiple targets? Just run the TUI multiple times in different terminals!

### Tip 5: Custom Wordlists
Edit `bugbounty-tui.py` line 396 to use your own wordlists:
```python
"directories": f"gobuster dir -u {target} -w /path/to/your/wordlist.txt ..."
```

---

## 📊 UNDERSTANDING OUTPUT

### Subdomain Scan Output
```
api-sandbox.gocardless.com
connect-sandbox.gocardless.com
manage-sandbox.gocardless.com
```
= Found 3 subdomains to test!

### Port Scan Output
```
PORT    STATE SERVICE
443/tcp open  ssl/http
```
= HTTPS port is open

### Directory Scan Output
```
/admin (Status: 403)
/api (Status: 200)
/login (Status: 200)
```
= Found 3 endpoints!

---

## 🎓 WHAT TO DO NEXT

After TUI scan completes:

1. **Review Results**
   ```bash
   cd scans/target_TIMESTAMP/
   ls -la
   cat subdomains.txt
   ```

2. **Manual Testing**
   - Use Burp Suite for deeper testing
   - Test found endpoints manually
   - Verify automated findings

3. **Test Business Logic**
   - TUI handles reconnaissance
   - You handle exploitation! 🎯

4. **Document Findings**
   - Take screenshots
   - Save requests/responses
   - Write PoC

---

## 🎉 SUCCESS CHECKLIST

- ✅ TUI launches without errors
- ✅ Can enter target URL
- ✅ Can check/uncheck scan options
- ✅ Scans run and show output
- ✅ Results saved to files
- ✅ Can view results in TUI
- ✅ Can find output files on disk

If all checked = YOU'RE READY TO HACK! 🚀

---

## 📞 NEED HELP?

1. Read `README-TUI.md` - Full documentation
2. Read `GoCardless-BugBounty-Guide.md` - Bug bounty guide
3. Test tools individually to see if they work:
   ```bash
   subfinder -version
   nmap --version
   gobuster version
   ```

---

## 🔥 ONE-LINE INSTALL & RUN

For the impatient hacker:

```bash
chmod +x launch.sh install-tools.sh bugbounty-tui.py && ./install-tools.sh && ./launch.sh
```

This will:
1. Make everything executable
2. Install missing tools
3. Launch the TUI

---

**You're all set! Happy hacking! 🎯💻🔥**

---

*Remember: Only test targets you have permission to test!*
*Use for educational purposes and authorized bug bounty programs only.*
