# 🚀 Bug Bounty TUI - Tactical Reconnaissance Framework

A **cyberpunk-themed terminal user interface** that integrates all bug bounty reconnaissance and scanning tools into one powerful, easy-to-use interface!

```
██████╗ ██╗   ██╗ ██████╗ ██████╗  ██████╗ ██╗   ██╗███╗   ██╗
██╔══██╗██║   ██║██╔════╝ ██╔══██╗██╔═══██╗██║   ██║████╗  ██║
██████╔╝██║   ██║██║  ███╗██████╔╝██║   ██║██║   ██║██╔██╗ ██║
██╔══██╗██║   ██║██║   ██║██╔══██╗██║   ██║██║   ██║██║╚██╗██║
██████╔╝╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║
╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
```

## ✨ Features

- 🎨 **Sci-Fi Terminal Interface** - Cyberpunk-themed, beautiful UI
- ⚡ **One-Click Scanning** - Enter target URL and click START
- 📊 **Real-Time Output** - Watch scans execute live
- 🔧 **10+ Integrated Tools** - All essential bug bounty tools in one place
- 📁 **Auto-Organization** - Results automatically saved with timestamps
- 🎯 **Modular Scans** - Enable/disable specific scan types
- ⌨️ **Keyboard Shortcuts** - Efficient workflow
- 📈 **Progress Tracking** - Visual progress bars and status updates

## 🛠️ Integrated Tools

### Reconnaissance
- **Subfinder** - Subdomain enumeration
- **Amass** - Advanced subdomain discovery
- **Waybackurls** - Historical URL discovery
- **Gospider** - Web crawler

### Scanning
- **Nmap** - Port scanning
- **Gobuster** - Directory/file bruteforce
- **Nikto** - Web vulnerability scanner
- **Whatweb** - Technology detection
- **Wafw00f** - WAF detection
- **SSLScan** - SSL/TLS analysis

### Exploitation
- **SQLmap** - SQL injection testing
- **Dalfox** - XSS vulnerability scanner

## 🚀 Quick Start

### Option 1: One-Click Launch (Recommended)

```bash
cd /home/claude/gocardless-pentest
./launch.sh
```

That's it! The launcher will:
1. Check dependencies
2. Install missing Python libraries
3. Launch the TUI

### Option 2: Manual Launch

```bash
# Install Python dependencies
pip3 install rich textual --break-system-packages

# Run the TUI
python3 bugbounty-tui.py
```

## 📋 Installation

### Step 1: Install Tools (First Time Only)

```bash
cd /home/claude/gocardless-pentest
./install-tools.sh
```

This will check for missing tools and install them automatically.

### Step 2: Launch

```bash
./launch.sh
```

## 🎮 How to Use

### 1. Launch the Application
```bash
./launch.sh
```

### 2. Enter Target URL
In the **TARGET ACQUISITION** section, enter your target:
```
https://manage-sandbox.gocardless.com
```

### 3. Select Scan Types
Check the boxes for scans you want to run:
- ✅ Subdomain Enumeration
- ✅ Port Scanning  
- ✅ Directory Bruteforce
- ✅ Technology Detection
- etc.

### 4. Start Scanning
Click **⚡ START SCAN** button or press `R` key

### 5. Watch Real-Time Output
Monitor scan progress in the output window with:
- Live command execution
- Real-time results
- Progress bar
- Color-coded status messages

### 6. View Results
- Results are saved automatically to `./scans/TARGET_TIMESTAMP/`
- Click **📊 RESULTS** button to view summary
- All scan outputs are saved as separate files

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `R` | Run/Start scan |
| `S` | Stop current scan |
| `C` | Clear output window |
| `Q` | Quit application |
| `ESC` | Go back / Close screen |

## 📁 Output Structure

Scans are organized like this:

```
scans/
└── target.com_20251027_143022/
    ├── subdomains.txt
    ├── nmap-scan.txt
    ├── gobuster.txt
    ├── nikto.txt
    ├── wayback-urls.txt
    └── ... (other scan results)
```

Each scan session creates a new timestamped directory.

## 🎯 Scan Types Explained

### 🔍 Subdomain Enumeration
**Tool:** Subfinder  
**What it does:** Discovers subdomains of target domain  
**Output:** List of found subdomains  
**Use case:** Find additional attack surface

### 🌐 Port Scanning
**Tool:** Nmap  
**What it does:** Scans for open ports and services  
**Ports scanned:** 80, 443, 8080, 8443  
**Use case:** Identify running services

### 📁 Directory Bruteforce
**Tool:** Gobuster  
**What it does:** Discovers hidden directories and files  
**Wordlist:** `/usr/share/wordlists/dirb/common.txt`  
**Use case:** Find admin panels, backup files, etc.

### 🔧 Technology Detection
**Tool:** Whatweb  
**What it does:** Identifies web technologies in use  
**Detects:** Framework, CMS, server, JavaScript libraries  
**Use case:** Find known vulnerabilities in detected tech

### 🔒 SSL/TLS Analysis
**Tool:** SSLScan  
**What it does:** Tests SSL/TLS configuration  
**Checks:** Certificate, ciphers, protocols  
**Use case:** Find SSL/TLS misconfigurations

### 🐛 Web Vulnerability Scan
**Tool:** Nikto  
**What it does:** Comprehensive web server scanner  
**Tests:** 6700+ vulnerabilities  
**Use case:** Automated vulnerability discovery

### 💉 SQL Injection
**Tool:** SQLmap  
**What it does:** Automated SQL injection testing  
**Note:** ⚠️ Requires authenticated session (manual setup)  
**Use case:** Test database security

### ⚡ XSS Detection
**Tool:** Dalfox  
**What it does:** Cross-site scripting vulnerability scanner  
**Note:** ⚠️ Requires authenticated session (manual setup)  
**Use case:** Find XSS vulnerabilities

### 🕷️ Web Crawling
**Tool:** Gospider  
**What it does:** Crawls website to discover endpoints  
**Depth:** 2 levels  
**Use case:** Map all URLs and endpoints

### 🔗 Historical URLs
**Tool:** Waybackurls  
**What it does:** Fetches historical URLs from Wayback Machine  
**Use case:** Find old/forgotten endpoints

## 🎨 UI Elements

### Color Coding
- 🟢 **Green** - Success, completed tasks
- 🟡 **Yellow** - Warnings, important info
- 🔵 **Cyan** - Information, headers
- 🔴 **Red** - Errors, failures
- ⚪ **Dim** - Command output, logs

### Status Messages
```
>>> SYSTEM INITIALIZED         - Ready to scan
▶▶▶ EXECUTING: SUBDOMAINS     - Running scan
✓ SUBDOMAINS COMPLETE         - Scan finished
✗ SUBDOMAINS FAILED           - Scan error
>>> ALL SCANS COMPLETED       - All done
```

## 🔧 Advanced Usage

### Running Manual Scans After TUI

The TUI shows you the commands it's running. You can run them manually:

```bash
# Example commands from TUI output
subfinder -d target.com -o subdomains.txt
nmap -sV -sC -p 80,443 target.com -oN nmap.txt
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt
```

### Customizing Scans

Edit the `bugbounty-tui.py` file to customize:

1. **Wordlists** - Change directory bruteforce wordlists
2. **Ports** - Add more ports to Nmap scan
3. **Timeout** - Adjust scan timeouts
4. **Threads** - Change concurrency settings

Example (line 396):
```python
"ports": f"nmap -sV -sC -p 80,443,8080,8443,3000,5000 {domain}",
```

### Authenticated Scans (SQLmap/XSS)

For tools requiring authentication:

1. Run TUI scan to get command template
2. Manually add authentication:

```bash
# SQLmap with session cookie
sqlmap -u "https://target.com/endpoint?id=1" \
  --cookie="session=YOUR_SESSION_COOKIE" \
  --batch --level=5 --risk=3

# Dalfox with auth header
dalfox url "https://target.com/search?q=FUZZ" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐛 Troubleshooting

### Tool Not Found
```bash
# Install missing tool
./install-tools.sh
```

### Permission Denied
```bash
# Make scripts executable
chmod +x launch.sh install-tools.sh bugbounty-tui.py
```

### Python Import Error
```bash
# Reinstall dependencies
pip3 install --upgrade rich textual --break-system-packages
```

### Network Error During Scan
- Check internet connection
- Verify target URL is accessible
- Check if target blocks automated scanning

### Scan Timeout
- Default timeout is 5 minutes per scan
- Some scans (like Gobuster) may need longer
- Edit `bugbounty-tui.py` line 409 to increase timeout

## ⚠️ Important Notes

### For GoCardless Bug Bounty

1. ✅ **Use sandbox only:** `manage-sandbox.gocardless.com`
2. ✅ **HackerOne alias:** Use your alias for account creation
3. ✅ **Test responsibly:** Don't overload servers
4. ⚠️ **Rate limiting:** Some scans may trigger rate limits
5. ⚠️ **Manual verification:** Always verify automated findings manually

### Ethical Testing

- ✅ Only scan targets you have permission to test
- ✅ Follow bug bounty program rules
- ✅ Don't access other users' data
- ✅ Report vulnerabilities responsibly
- ❌ Never test on production without approval

## 📊 Example Session

```
1. Launch TUI: ./launch.sh
2. Enter target: https://manage-sandbox.gocardless.com
3. Select scans:
   ✅ Subdomain Enumeration
   ✅ Port Scanning
   ✅ Directory Bruteforce
   ✅ Technology Detection
4. Click START SCAN
5. Watch output:
   ▶▶▶ EXECUTING: SUBDOMAINS
   $ subfinder -d manage-sandbox.gocardless.com -o ...
   api-sandbox.gocardless.com
   connect-sandbox.gocardless.com
   ✓ SUBDOMAINS COMPLETE
   
   ▶▶▶ EXECUTING: PORTS
   $ nmap -sV -sC -p 80,443,8080,8443 ...
   PORT    STATE SERVICE
   443/tcp open  ssl/http
   ✓ PORTS COMPLETE
   
6. Click RESULTS to view summary
7. Check ./scans/ directory for full output
```

## 🔄 Updates & Improvements

### Planned Features
- [ ] Custom wordlist selection
- [ ] Scan scheduling
- [ ] Report generation (PDF/HTML)
- [ ] Multiple target support
- [ ] Scan templates (Quick/Full/Custom)
- [ ] Integration with Burp Suite
- [ ] Vulnerability database lookup
- [ ] Collaborative scanning

### Contributing

Want to add features? Edit `bugbounty-tui.py` and add:
- New scan types in `commands` dict (line 390)
- New checkboxes in compose() method (line 250)
- New buttons/features as needed

## 📚 Resources

- [Textual Documentation](https://textual.textualize.io/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Bug Bounty Guide](./GoCardless-BugBounty-Guide.md)

## 🆘 Support

Issues? Questions?

1. Check this README
2. Review bug bounty guide
3. Test tools individually to isolate problems
4. Check tool documentation

## 📜 License

Educational purposes only. Use responsibly and ethically.

---

## 🚀 Quick Commands Reference

```bash
# Launch TUI
./launch.sh

# Install tools
./install-tools.sh

# Direct run
python3 bugbounty-tui.py

# Check tool status
./install-tools.sh

# View previous scans
ls -la scans/

# Quick test
./launch.sh
# Enter: https://example.com
# Select: Technology Detection
# Click: START SCAN
```

---

**Made with 💚 by hackers, for hackers**

*"The only way to secure a system is to think like an attacker"*

---

**Version:** 2.0  
**Last Updated:** October 2025  
**Status:** Production Ready 🚀
