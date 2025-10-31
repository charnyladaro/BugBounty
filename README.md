# 🎯 Bug Bounty TUI

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20WSL-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen.svg)

**A cyberpunk-themed Terminal User Interface (TUI) that integrates 10+ security tools into one powerful reconnaissance framework**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📸 Screenshots

```
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                           ║
║   ██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗    ║
║   ██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝    ║
║   ██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝     ║
║   ██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝      ║ 
║   ██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║       ║
║   ╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝       ║
║                                                                                           ║
║                       TACTICAL RECONNAISSANCE FRAMEWORK v2.0                              ║
║                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
```

<div align="center">

**🎨 Beautiful sci-fi interface with real-time output and progress tracking**

</div>

---

## 🌟 Features

### 🎨 **Beautiful Interface**
- Cyberpunk-themed Terminal UI built with [Textual](https://textual.textualize.io/)
- Real-time command output with syntax highlighting
- Progress bars and status indicators
- Color-coded results (Green = Success, Red = Error, Yellow = Warning)

### ⚡ **One-Click Scanning**
- Enter target URL and select scan types
- Click START or press `R` to launch
- Watch all tools execute in real-time
- Results automatically saved with timestamps

### 🔧 **10+ Integrated Tools**
| Category | Tools |
|----------|-------|
| **Subdomain Enum** | Subfinder, Amass |
| **Port Scanning** | Nmap |
| **Directory Brute** | Gobuster |
| **Web Scanning** | Nikto, Whatweb, Wafw00f |
| **SSL/TLS** | SSLScan |
| **Vulnerabilities** | SQLmap, Dalfox |
| **Crawling** | Gospider, Waybackurls |

### 📊 **Smart Organization**
```
scans/
└── target.com_20241027_143022/
    ├── subdomains.txt      # All discovered subdomains
    ├── nmap-scan.txt       # Port scan results
    ├── gobuster.txt        # Found directories/files
    ├── nikto.txt           # Web vulnerabilities
    └── ...                 # All results organized
```

### ⌨️ **Keyboard Shortcuts**
- `R` - Run scan
- `S` - Stop current scan
- `C` - Clear output window
- `Q` - Quit application
- `ESC` - Go back / Close popups

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Linux or WSL (Windows Subsystem for Linux)
- Internet connection

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bug-bounty-tui.git
cd bug-bounty-tui

# Make scripts executable
chmod +x launch.sh install-tools.sh bugbounty-tui.py

# Install security tools (optional - installs nmap, gobuster, etc.)
./install-tools.sh

# Launch the TUI
./launch.sh
```

That's it! The launcher will install Python dependencies automatically.

---

## 📖 Usage

### Basic Workflow

1. **Launch the application**
   ```bash
   ./launch.sh
   ```

2. **Enter your target URL**
   ```
   https://example.com
   ```

3. **Select scan types** (check boxes)
   - ☑ Subdomain Enumeration
   - ☑ Port Scanning
   - ☑ Directory Bruteforce
   - ☑ Technology Detection
   - ... and more

4. **Start scanning** (Click START or press `R`)

5. **Watch real-time output** in the terminal

6. **View results** 
   - Click RESULTS button in TUI
   - Or check `./scans/target_timestamp/` directory

### Example Session

```bash
$ ./launch.sh

# In the TUI:
Target: https://manage-sandbox.gocardless.com
✅ Subdomain Enumeration
✅ Port Scanning  
✅ Directory Bruteforce
✅ Technology Detection

# Press R to run

# Output:
▶▶▶ EXECUTING: SUBDOMAINS
api.example.com
app.example.com
✓ COMPLETE

▶▶▶ EXECUTING: PORTS
443/tcp open ssl/http
✓ COMPLETE

# Results saved to: ./scans/example.com_20241027_143022/
```

---

## 🛠️ Advanced Usage

### Custom Wordlists

Edit `bugbounty-tui.py` line 396 to use your own wordlists:

```python
"directories": f"gobuster dir -u {target} -w /path/to/your/wordlist.txt ..."
```

### Adding New Tools

1. Add tool to `commands` dictionary (line 390-410)
2. Add checkbox in `compose()` method (line 250)
3. Update tool list in installer

Example:
```python
commands = {
    # ... existing tools ...
    "your_tool": f"your-command {target} -o {output_dir}/output.txt"
}
```

### Running Without TUI

Extract commands from the source and run manually:
```bash
subfinder -d target.com -o subdomains.txt
nmap -sV -p 80,443 target.com -oN nmap.txt
```

---

## 📋 Requirements

### System Requirements
- **OS:** Linux (Ubuntu, Kali, Debian, etc.) or WSL
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum
- **Disk:** 500MB for tools + scan results

### Python Dependencies
```
rich>=13.0.0
textual>=0.40.0
```

### Security Tools (Optional)
The TUI works without these, but scans will fail. Run `./install-tools.sh` to install:

- nmap
- gobuster  
- nikto
- whatweb
- wafw00f
- sslscan
- subfinder
- gospider
- waybackurls
- dalfox
- amass
- sqlmap

---

## 🪟 Windows Support

### ✅ Recommended: WSL

**Best experience with full tool support!**

```powershell
# Install WSL (PowerShell as Administrator)
wsl --install

# Restart computer, then:
wsl

# Follow Linux installation steps above
```

### ⚠️ Native Windows (Limited)

Python TUI works, but most security tools don't have Windows versions.

**See [WINDOWS-GUIDE.md](WINDOWS-GUIDE.md) for detailed instructions.**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [README-TUI.md](README-TUI.md) | Complete feature documentation |
| [VISUAL-DEMO.md](VISUAL-DEMO.md) | Interface screenshots and mockups |
| [WINDOWS-GUIDE.md](WINDOWS-GUIDE.md) | Windows/WSL installation guide |
| [GoCardless-BugBounty-Guide.md](GoCardless-BugBounty-Guide.md) | Bug bounty methodology (66 pages) |

---

## 🎯 Use Cases

### Bug Bounty Hunting
Fast reconnaissance on authorized targets:
- Discover subdomains
- Find hidden endpoints  
- Identify technologies
- Detect vulnerabilities

### Penetration Testing
Initial scanning phase:
- Port enumeration
- Service detection
- Web application mapping
- Attack surface analysis

### CTF Competitions
Quick enumeration:
- Fast subdomain discovery
- Directory bruteforcing
- Technology fingerprinting

### Security Research
Automated reconnaissance:
- Historical URL discovery
- SSL/TLS analysis
- WAF detection

---

## ⚠️ Legal Disclaimer

**Important:** This tool is for **authorized security testing only**.

### ✅ Authorized Use
- Your own systems
- Bug bounty programs (with permission)
- Penetration testing engagements (with contract)
- Educational labs (with permission)

### ❌ Unauthorized Use
- Other people's websites without permission
- Production systems without approval
- Malicious purposes
- Illegal activities

**You are responsible for ensuring you have permission to test any target.**

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **Report Bugs** - Open an issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System info (OS, Python version)

2. **Suggest Features** - Open an issue with:
   - Feature description
   - Use case
   - Potential implementation

3. **Submit Pull Requests**
   ```bash
   # Fork the repo
   # Create a feature branch
   git checkout -b feature/amazing-feature
   
   # Make your changes
   # Commit with clear messages
   git commit -m "Add amazing feature"
   
   # Push to your fork
   git push origin feature/amazing-feature
   
   # Open a Pull Request
   ```

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/bug-bounty-tui.git
cd bug-bounty-tui

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install rich textual pytest black flake8

# Make your changes

# Test
python3 bugbounty-tui.py

# Format code
black bugbounty-tui.py

# Lint
flake8 bugbounty-tui.py
```

### Code Style

- Follow PEP 8
- Use meaningful variable names
- Add comments for complex logic
- Update documentation for new features

---

## 🗺️ Roadmap

### Version 2.1 (Upcoming)
- [ ] Custom wordlist selection in UI
- [ ] Scan templates (Quick/Full/Stealth)
- [ ] Export results to PDF/HTML
- [ ] Email notifications

### Version 2.2 (Future)
- [ ] Nuclei integration
- [ ] Screenshot capture (Eyewitness)
- [ ] Shodan API integration
- [ ] Multi-target scanning

### Version 3.0 (Long-term)
- [ ] Web interface option
- [ ] Collaborative scanning
- [ ] Database backend
- [ ] REST API
- [ ] Plugin system

---

## 🐛 Known Issues

- SQLmap and Dalfox require manual authentication setup
- Scan timeout set to 5 minutes (may need adjustment for large targets)
- Some tools may require additional configuration

**See [Issues](https://github.com/yourusername/bug-bounty-tui/issues) for current bugs and workarounds.**

---

## 📊 Project Statistics

- **Lines of Code:** ~450 (Python)
- **Integrated Tools:** 10+
- **Documentation Pages:** 7 files (~132KB)
- **Development Time:** Active
- **Language:** Python 3.8+
- **Framework:** Textual

---

## 🙏 Acknowledgments

### Built With
- [Textual](https://textual.textualize.io/) - Modern TUI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- All the amazing security tools integrated

### Inspired By
- Bug bounty community
- Penetration testing frameworks
- Cyberpunk aesthetics

### Special Thanks
- Security researchers who built the tools
- Textual framework developers
- Bug bounty programs that support ethical hacking

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Bug Bounty TUI Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support & Contact

### Get Help
- 📖 Read the [documentation](QUICKSTART.md)
- 🐛 Report bugs via [Issues](https://github.com/yourusername/bug-bounty-tui/issues)
- 💬 Start a [Discussion](https://github.com/yourusername/bug-bounty-tui/discussions)

### Stay Updated
- ⭐ Star this repo to show support
- 👁️ Watch for updates
- 🔔 Enable notifications for releases

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/bug-bounty-tui?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/bug-bounty-tui?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/bug-bounty-tui?style=social)

---

## 🎉 Show Your Support

If this project helped you, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs or suggesting features
- 📣 Sharing with the security community
- 💰 Sponsoring (if available)

---

<div align="center">

**Built with 💚 by the security community, for the security community**

*"The only way to secure a system is to think like an attacker"*

---

[⬆ Back to Top](#-bug-bounty-tui)

</div>
