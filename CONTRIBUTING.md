# Contributing to Bug Bounty TUI

First off, thank you for considering contributing to Bug Bounty TUI! 🎉

The following is a set of guidelines for contributing. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers and help them learn
- ✅ Focus on what is best for the community
- ✅ Show empathy towards other community members

### Not Acceptable

- ❌ Trolling, insulting/derogatory comments
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Unethical or illegal conduct

---

## 🤝 How Can I Contribute?

### Reporting Bugs

**Before creating a bug report:**
- Check the [issues](https://github.com/yourusername/bug-bounty-tui/issues) to see if it's already reported
- Try the latest version from `main` branch

**When creating a bug report, include:**

```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Launch with './launch.sh'
2. Enter target 'https://example.com'
3. Click START
4. See error

**Expected Behavior:**
Scan should start and show output

**Actual Behavior:**
Error message appears

**Environment:**
- OS: Ubuntu 22.04 / Kali Linux / WSL
- Python Version: 3.10.5
- Tool Version: 2.0

**Screenshots:**
(if applicable)

**Additional Context:**
Any other relevant information
```

### Suggesting Enhancements

**Before creating an enhancement suggestion:**
- Check if it's already suggested
- Check the roadmap in README.md

**When suggesting an enhancement, include:**

```markdown
**Feature Description:**
Clear description of the feature

**Use Case:**
Why is this feature useful?

**Proposed Solution:**
How would you implement it?

**Alternatives Considered:**
Other approaches you thought about

**Additional Context:**
Mockups, examples, references
```

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Good for newcomers
- `help wanted` - Need community help
- `documentation` - Documentation improvements

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, test it thoroughly
3. Update documentation as needed
4. Follow the style guidelines
5. Write a clear pull request description

---

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/yourusername/bug-bounty-tui.git
cd bug-bounty-tui
```

### 2. Set Up Development Environment

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install rich textual

# Install development dependencies
pip install pytest black flake8 mypy

# Install security tools (for testing)
./install-tools.sh
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 4. Make Your Changes

```bash
# Edit files
nano bugbounty-tui.py

# Test your changes
python3 bugbounty-tui.py
```

### 5. Test Thoroughly

```bash
# Manual testing
./launch.sh

# Test different scenarios:
# - Different target URLs
# - Different scan combinations
# - Error conditions
# - Edge cases
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update README.md if adding features
   - Update relevant .md files
   - Add code comments for complex logic

2. **Format Your Code**
   ```bash
   # Format with Black
   black bugbounty-tui.py
   
   # Check with flake8
   flake8 bugbounty-tui.py
   ```

3. **Test Everything**
   - Run the application multiple times
   - Test on different targets
   - Verify all scans work
   - Check error handling

4. **Update CHANGELOG** (if exists)
   ```markdown
   ## [Unreleased]
   ### Added
   - Your new feature
   
   ### Changed
   - What you modified
   
   ### Fixed
   - Bugs you fixed
   ```

### Submitting

1. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the template:

   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   - [ ] Tested on Linux
   - [ ] Tested on WSL
   - [ ] All scans work
   - [ ] No errors in output
   
   ## Screenshots
   (if applicable)
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex code
   - [ ] Documentation updated
   - [ ] No new warnings
   ```

3. **Wait for Review**
   - Maintainers will review your PR
   - Address any feedback
   - Make requested changes
   - Push updates to same branch

### After Merge

- Delete your branch (optional)
- Pull latest changes from main
- Celebrate! 🎉

---

## 🎨 Style Guidelines

### Python Code Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```python
# Good
def scan_target(target_url: str, scan_types: list) -> dict:
    """
    Execute scans on target.
    
    Args:
        target_url: The target URL to scan
        scan_types: List of scan types to run
        
    Returns:
        Dictionary of scan results
    """
    results = {}
    for scan_type in scan_types:
        results[scan_type] = execute_scan(scan_type, target_url)
    return results

# Bad
def scan(t,s):
    r={}
    for x in s:
        r[x]=execute_scan(x,t)
    return r
```

### Documentation Style

```python
# Good docstring
def execute_scan(self, scan_type: str) -> str:
    """
    Execute a specific scan type.
    
    Args:
        scan_type: Type of scan ('subdomains', 'ports', etc.)
        
    Returns:
        Output from the scan command
        
    Raises:
        subprocess.TimeoutExpired: If scan takes >5 minutes
        Exception: For other scan failures
    """
    pass

# Bad docstring
def execute_scan(self, scan_type):
    # does a scan
    pass
```

### Variable Naming

```python
# Good
target_url = "https://example.com"
scan_results = {}
is_scanning = False
total_scans = 10

# Bad
url = "https://example.com"
res = {}
flag = False
num = 10
```

### Code Organization

```python
# Good structure
class BugBountyTUI(App):
    """Main application class."""
    
    # Constants
    TITLE = "Bug Bounty TUI"
    
    # Initialization
    def __init__(self):
        super().__init__()
        self.config = ScanConfig()
    
    # UI Methods
    def compose(self) -> ComposeResult:
        pass
    
    # Event Handlers
    def on_button_pressed(self, event):
        pass
    
    # Action Methods
    def action_run_scan(self):
        pass
    
    # Helper Methods
    def _execute_command(self, cmd):
        pass
```

### Comments

```python
# Good comments
# Calculate scan progress as percentage
progress = (completed_scans / total_scans) * 100

# Execute subprocess with 5-minute timeout to prevent hanging
result = subprocess.run(cmd, timeout=300)

# Bad comments
# set progress
progress = (completed_scans / total_scans) * 100

# run command
result = subprocess.run(cmd, timeout=300)
```

---

## 📝 Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

**Good commit messages:**

```bash
feat(scanner): Add Nuclei integration

- Integrate Nuclei vulnerability scanner
- Add checkbox in UI for Nuclei scan
- Update install script to include Nuclei
- Add documentation for Nuclei usage

Closes #42
```

```bash
fix(output): Fix progress bar not updating

The progress bar was stuck at 0% due to incorrect
calculation in the update method. Changed division
to use completed/total instead of total/completed.

Fixes #38
```

```bash
docs(readme): Update installation instructions

- Add Windows WSL section
- Update Python version requirement
- Add troubleshooting section
- Fix broken links
```

**Bad commit messages:**

```bash
# Too vague
update stuff

# No context
fix bug

# Not descriptive
changes
```

---

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting PR, test:

- [ ] Application launches without errors
- [ ] Target input accepts valid URLs
- [ ] All checkboxes work
- [ ] START button initiates scans
- [ ] STOP button halts scans
- [ ] CLEAR button clears output
- [ ] RESULTS button shows results
- [ ] Progress bar updates correctly
- [ ] Scans execute and complete
- [ ] Output displays correctly
- [ ] Results save to files
- [ ] Keyboard shortcuts work
- [ ] Error handling works
- [ ] Multiple scans work
- [ ] Different targets work

### Test Different Scenarios

```bash
# Test valid inputs
https://example.com
http://example.com
example.com

# Test edge cases
https://example.com/path
https://sub.example.com:8080
https://example.com?query=param

# Test error conditions
invalid-url
http://nonexistent-domain-xyz123.com
```

---

## 🏗️ Architecture Overview

Understanding the code structure:

```
bugbounty-tui.py
├── ScanConfig class          # Configuration management
├── WelcomeScreen class       # Welcome screen
├── ResultsScreen class       # Results display
└── BugBountyTUI class        # Main application
    ├── compose()             # UI layout
    ├── on_button_pressed()   # Button handlers
    ├── action_*()            # Keyboard shortcuts
    ├── run_scans()           # Scan orchestration
    └── execute_scan()        # Individual scan execution
```

### Adding a New Scan Type

1. **Add checkbox** (line ~250):
```python
yield Checkbox("🔥 New Scanner (newtool)", value=False, id="scan_newtool")
```

2. **Add to scan selection** (line ~330):
```python
if self.query_one("#scan_newtool", Checkbox).value:
    scans.append("newtool")
```

3. **Add command** (line ~390):
```python
commands = {
    # ... existing commands ...
    "newtool": f"newtool {target} -o {output_dir}/newtool.txt"
}
```

4. **Update documentation**
   - Add to README.md features
   - Add to tool list
   - Update installation instructions if needed

---

## 📚 Additional Resources

### Learn More

- [Textual Documentation](https://textual.textualize.io/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Git Commit Guidelines](https://www.conventionalcommits.org/)

### Project Resources

- [Project Board](https://github.com/yourusername/bug-bounty-tui/projects)
- [Issue Tracker](https://github.com/yourusername/bug-bounty-tui/issues)
- [Discussions](https://github.com/yourusername/bug-bounty-tui/discussions)
- [Wiki](https://github.com/yourusername/bug-bounty-tui/wiki)

---

## 🎓 Learning Path

### For New Contributors

1. **Week 1**: Understand the code
   - Read README.md
   - Run the application
   - Browse the code
   - Understand structure

2. **Week 2**: Make small changes
   - Fix typos
   - Update documentation
   - Add comments

3. **Week 3**: Add features
   - Add a new scan type
   - Improve UI element
   - Add error handling

4. **Week 4+**: Major contributions
   - New features
   - Architecture improvements
   - Performance optimization

---

## 🆘 Getting Help

### Stuck? Here's how to get help:

1. **Read the docs** - Check all .md files
2. **Search issues** - Someone may have had the same problem
3. **Ask in discussions** - Community can help
4. **Open an issue** - For bugs or feature requests

### Questions?

- 💬 [Start a Discussion](https://github.com/yourusername/bug-bounty-tui/discussions)
- 📧 Contact maintainers (see README.md)

---

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<div align="center">

**Thank you for contributing to Bug Bounty TUI! 🙏**

Every contribution, no matter how small, makes a difference!

</div>
