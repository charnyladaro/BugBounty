# 🪟 Bug Bounty TUI - Windows Installation Guide

## ✅ YES! It Works on Windows!

You have **3 options** to run this on Windows:

---

## 🎯 OPTION 1: WSL (RECOMMENDED - Best Experience)

### What is WSL?
**Windows Subsystem for Linux** - Run Linux directly on Windows!

### ✅ Advantages
- ✅ Full Linux compatibility
- ✅ All security tools work perfectly
- ✅ Native performance
- ✅ Easy installation
- ✅ Best experience overall

### 📦 Installation Steps

#### Step 1: Install WSL (One Command!)

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

This installs Ubuntu by default. Restart your computer when done.

#### Step 2: Install Kali Linux (Optional but Recommended)

```powershell
# List available distros
wsl --list --online

# Install Kali Linux
wsl --install -d kali-linux
```

#### Step 3: Launch WSL

```bash
# In PowerShell or Command Prompt:
wsl

# Or launch "Kali Linux" from Start Menu
```

#### Step 4: Set Up Environment

Inside WSL terminal:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install Go (for some tools)
sudo apt install golang-go -y

# Configure Go path
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
source ~/.bashrc
```

#### Step 5: Transfer Files to WSL

Your Windows drives are mounted at `/mnt/`:
- `C:\` is `/mnt/c/`
- `D:\` is `/mnt/d/`

```bash
# Copy files from Windows Downloads to WSL home
cp /mnt/c/Users/YourName/Downloads/bugbounty-tui.py ~/
cp /mnt/c/Users/YourName/Downloads/launch.sh ~/
cp /mnt/c/Users/YourName/Downloads/install-tools.sh ~/
cp /mnt/c/Users/YourName/Downloads/*.md ~/

# Make executable
chmod +x ~/launch.sh ~/install-tools.sh ~/bugbounty-tui.py

# Install tools
cd ~
./install-tools.sh

# Launch!
./launch.sh
```

#### Step 6: Access Files from Windows

Your WSL files are accessible from Windows at:
```
\\wsl$\Ubuntu\home\your-username\
# or
\\wsl$\kali-linux\home\your-username\
```

You can open this in Windows Explorer!

### 💡 Pro Tips for WSL

```bash
# Open current directory in Windows Explorer from WSL
explorer.exe .

# Open VS Code in WSL directory
code .

# Copy from WSL to Windows clipboard
cat file.txt | clip.exe

# Access Windows programs from WSL
notepad.exe file.txt
```

---

## 🎯 OPTION 2: Native Windows Python (Partial Support)

### What Works
- ✅ The TUI interface itself
- ✅ Python libraries (Rich, Textual)
- ✅ Basic functionality

### What Doesn't Work
- ❌ Most Linux security tools (nmap, nikto, etc.)
- ❌ Bash scripts (launch.sh, install-tools.sh)
- ❌ Tool integration

### Installation Steps

#### Step 1: Install Python

Download from https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation!

#### Step 2: Install Python Libraries

Open **Command Prompt** or **PowerShell**:

```powershell
pip install rich textual
```

#### Step 3: Install Windows Security Tools (Optional)

Some tools have Windows versions:

```powershell
# Install Chocolatey (Windows package manager)
# Run as Administrator in PowerShell:
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install tools
choco install nmap
choco install golang
```

#### Step 4: Run TUI

```powershell
# Navigate to directory
cd C:\path\to\files

# Run directly with Python
python bugbounty-tui.py
```

### ⚠️ Limitations

- Many scans won't work without Linux tools
- You'll need to install Windows versions of each tool manually
- Bash scripts won't work - only the Python TUI

### 🔧 Modified Windows Version

I can create a Windows-specific version that:
- Uses Windows-compatible tools only
- Replaces Bash scripts with Python
- Includes PowerShell alternatives

**Would you like me to create this?**

---

## 🎯 OPTION 3: Docker (Advanced)

### What is Docker?
Run Linux containers on Windows!

### ✅ Advantages
- ✅ Isolated environment
- ✅ All tools included
- ✅ Easy distribution
- ✅ No system changes

### Installation Steps

#### Step 1: Install Docker Desktop

Download from https://www.docker.com/products/docker-desktop/

#### Step 2: Create Dockerfile

Create a file called `Dockerfile`:

```dockerfile
FROM kalilinux/kali-rolling

# Install system packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nmap \
    gobuster \
    nikto \
    whatweb \
    wafw00f \
    sslscan \
    golang-go \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install rich textual --break-system-packages

# Install Go tools
ENV PATH="${PATH}:/root/go/bin"
RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/jaeles-project/gospider@latest && \
    go install github.com/tomnomnom/waybackurls@latest && \
    go install github.com/hahwul/dalfox/v2@latest

# Copy TUI files
WORKDIR /app
COPY bugbounty-tui.py .
COPY launch.sh .
COPY install-tools.sh .
RUN chmod +x *.sh *.py

# Set entrypoint
ENTRYPOINT ["python3", "bugbounty-tui.py"]
```

#### Step 3: Build Docker Image

```powershell
# In PowerShell (same directory as Dockerfile)
docker build -t bugbounty-tui .
```

#### Step 4: Run Container

```powershell
# Run TUI in Docker
docker run -it --rm bugbounty-tui

# Run with volume for results
docker run -it --rm -v ${PWD}/scans:/app/scans bugbounty-tui
```

---

## 📊 Comparison Matrix

| Feature | WSL | Native Windows | Docker |
|---------|-----|----------------|--------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Tool Compatibility** | ✅ 100% | ⚠️ 30% | ✅ 100% |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **File Access** | ✅ Easy | ✅ Direct | ⚠️ Volumes |
| **Learning Curve** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Updates** | ✅ Easy | ⚠️ Manual | ⭐⭐⭐ |
| **Recommended For** | Everyone | Light use | Advanced |

---

## 🏆 RECOMMENDATION

### For You: **USE WSL!** 

**Why?**
1. ✅ You mentioned "WSL Kali Linux" in your question
2. ✅ Best compatibility (100% of tools work)
3. ✅ Easy to use
4. ✅ Already have it installed!
5. ✅ Perfect for security testing

---

## 🚀 Quick Start with WSL (Your Situation)

Since you mentioned WSL Kali, here's your fastest path:

### Step 1: Open Your Kali WSL Terminal

```bash
# In Windows, press Win + R, type:
wsl

# Or open "Kali Linux" from Start Menu
```

### Step 2: Copy Files from Windows to WSL

```bash
# Assuming files are in Downloads folder
cd ~
cp /mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/bugbounty-tui.py .
cp /mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/launch.sh .
cp /mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/install-tools.sh .
cp /mnt/c/Users/YOUR_WINDOWS_USERNAME/Downloads/*.md .

# Make executable
chmod +x launch.sh install-tools.sh bugbounty-tui.py
```

### Step 3: Install Python Libraries

```bash
pip3 install rich textual --break-system-packages
```

### Step 4: Install Security Tools (Optional)

```bash
./install-tools.sh
```

### Step 5: Launch!

```bash
./launch.sh
```

**Done!** 🎉

---

## 🔧 Troubleshooting WSL

### Issue: "wsl command not found"

**Solution:** Install WSL first:
```powershell
# In PowerShell as Administrator
wsl --install
# Restart computer
```

### Issue: "Python3 not found in WSL"

**Solution:**
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### Issue: "Can't access Windows files from WSL"

**Solution:** Windows drives are at `/mnt/`:
```bash
# C:\ is at:
cd /mnt/c

# Your user folder:
cd /mnt/c/Users/YourName
```

### Issue: "Can't access WSL files from Windows"

**Solution:** In Windows Explorer, type:
```
\\wsl$\kali-linux\home\your-username
```

### Issue: "Tools not found"

**Solution:**
```bash
# Run installer
./install-tools.sh

# Or manually install
sudo apt update
sudo apt install nmap gobuster nikto whatweb -y
```

---

## 💡 WSL Pro Tips

### 1. Windows Terminal (Better Experience)

Install **Windows Terminal** from Microsoft Store for:
- ✅ Better colors
- ✅ Multiple tabs
- ✅ Custom themes
- ✅ Better fonts

### 2. Direct File Access

```bash
# From WSL, open Windows Explorer
explorer.exe .

# From WSL, open VS Code
code .

# From WSL, open file in Windows notepad
notepad.exe file.txt
```

### 3. Copy/Paste

```bash
# Copy WSL output to Windows clipboard
cat results.txt | clip.exe

# Use Ctrl+Shift+C/V in terminal
```

### 4. Run Windows Programs from WSL

```bash
# Run any .exe from WSL
notepad.exe
calc.exe
chrome.exe https://google.com
```

### 5. Network Access

WSL shares your Windows network, so:
- Same internet connection
- Can access same targets
- Same IP address

---

## 🎨 Enhanced Setup for Windows Users

### Visual Studio Code Integration

1. Install VS Code on Windows
2. Install "Remote - WSL" extension
3. In WSL terminal:
```bash
code .
```
4. VS Code opens with full WSL integration!

### File Organization

Create a project structure:
```bash
# In WSL
mkdir -p ~/bug-bounty-projects/gocardless
cd ~/bug-bounty-projects/gocardless

# Copy TUI files here
cp ~/bugbounty-tui.py .
cp ~/launch.sh .
# etc.

# Access from Windows at:
# \\wsl$\kali-linux\home\username\bug-bounty-projects\gocardless
```

---

## 📱 Windows Terminal Configuration

Create a beautiful terminal experience:

### Install Windows Terminal

From Microsoft Store or:
```powershell
winget install Microsoft.WindowsTerminal
```

### Configure Kali Profile

1. Open Windows Terminal
2. Settings → Add Profile
3. Choose "Kali Linux"
4. Set as default (optional)

### Custom Theme

In settings.json:
```json
{
    "profiles": {
        "list": [
            {
                "name": "Kali Linux",
                "commandline": "wsl -d kali-linux",
                "icon": "🐉",
                "colorScheme": "One Half Dark",
                "fontFace": "Cascadia Code",
                "fontSize": 12
            }
        ]
    }
}
```

---

## 🔐 Security Considerations

### Windows Defender

Windows Defender may flag security tools:

**Solution 1: Add Exclusion**
1. Windows Security
2. Virus & threat protection
3. Exclusions
4. Add: `\\wsl$\kali-linux\home\your-username\`

**Solution 2: Disable Real-time Protection (Temporarily)**
- Only when running tools
- Re-enable after testing

### Firewall

WSL uses Windows firewall:
- Outbound: Usually works
- Inbound: May need rules
- VPN: Works with WSL

---

## 🎯 Summary: Windows Users

### ✅ RECOMMENDED: WSL
```bash
# 1. Already have it? Use it!
wsl

# 2. Don't have it? Install it!
# In PowerShell as Admin:
wsl --install

# 3. Launch TUI
cd ~
./launch.sh
```

### ⚠️ ALTERNATIVE: Native Windows
- Limited tool support
- Need to install Windows versions
- TUI interface works fine
- Good for learning/testing TUI only

### 🔧 ADVANCED: Docker
- Full tool support
- Isolated environment
- Requires Docker Desktop
- More complex setup

---

## 🎉 Bottom Line

**YES, it works on Windows!**

**Best method: WSL** (which you already have!)

**Time to setup:** 
- With WSL: 5 minutes
- Native Windows: 30+ minutes (limited functionality)
- Docker: 20+ minutes

---

## 🚀 Your Next Steps

Since you have **WSL Kali Linux**:

```bash
# 1. Open Kali WSL
wsl

# 2. Copy files to WSL
cp /mnt/c/Users/YOUR_NAME/Downloads/*.py ~/
cp /mnt/c/Users/YOUR_NAME/Downloads/*.sh ~/
cp /mnt/c/Users/YOUR_NAME/Downloads/*.md ~/

# 3. Make executable
chmod +x ~/*.sh ~/*.py

# 4. Install dependencies
pip3 install rich textual --break-system-packages

# 5. Launch!
cd ~
./launch.sh
```

**That's it! 5 commands and you're hacking! 🎯**

---

## 📞 Need Help?

### Common Windows + WSL Issues

**Q: "Can't find downloaded files in WSL"**  
A: They're at `/mnt/c/Users/YOUR_NAME/Downloads/`

**Q: "How do I transfer files?"**  
A: Use `cp /mnt/c/path/to/file ~/destination/`

**Q: "How do I access WSL files from Windows?"**  
A: Type `\\wsl$\` in Windows Explorer

**Q: "Does this affect my Windows system?"**  
A: No! WSL is isolated and safe

**Q: "Can I run this and use Windows normally?"**  
A: Yes! They run side-by-side

---

**You're ready! Your WSL Kali Linux is perfect for this! 🚀**

**Any questions? Just ask!**
