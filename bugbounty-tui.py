#!/usr/bin/env python3
"""
██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗
██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝
██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝ 
██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝  
██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║   
╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝   
                                                                                      
         ADVANCED RECONNAISSANCE & EXPLOITATION FRAMEWORK v2.0
                    [ CLASSIFIED - AUTHORIZED PERSONNEL ONLY ]
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Button, Static, Input, 
    Label, TextLog, ProgressBar, TabbedContent, TabPane,
    DataTable, Tree, RadioSet, RadioButton, Checkbox
)
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Console
import subprocess
import threading
import time
import os
import json
from datetime import datetime
from pathlib import Path

console = Console()

class ScanConfig:
    """Store scan configuration"""
    def __init__(self):
        self.target = ""
        self.output_dir = ""
        self.scan_types = []
        self.running = False
        self.results = {}
        
    def set_target(self, target):
        self.target = target
        # Clean target for directory name
        clean_target = target.replace("https://", "").replace("http://", "").replace("/", "_")
        self.output_dir = f"./scans/{clean_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
config = ScanConfig()

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
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
            """, id="ascii-art")
            
            yield Static("""
[bold cyan]SYSTEM STATUS:[/] [bold green]ONLINE[/]
[bold cyan]SECURITY CLEARANCE:[/] [bold yellow]LEVEL 5[/]
[bold cyan]AUTHORIZATION:[/] [bold green]GRANTED[/]

[dim]Initializing reconnaissance modules...[/]
[dim]Loading exploitation frameworks...[/]
[dim]Establishing secure connection...[/]

[bold green]✓[/] All systems operational
[bold green]✓[/] Ready for engagement

[bold red]WARNING:[/] Use only on authorized targets!
            """, id="welcome-text")
            
            yield Button("⚡ INITIALIZE MISSION ⚡", variant="success", id="start-button")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

class ResultsScreen(Screen):
    """Screen to display scan results"""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]
    
    CSS = """
    ResultsScreen {
        background: $surface;
    }
    
    #results-container {
        height: 100%;
        background: $panel;
        border: heavy $primary;
        padding: 1;
    }
    
    #results-title {
        color: $accent;
        text-style: bold;
        text-align: center;
        padding: 1;
    }
    """
    
    def __init__(self, results: dict):
        super().__init__()
        self.results = results
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with ScrollableContainer(id="results-container"):
            yield Static("[bold cyan]═══════════════════════════════════════════[/]\n[bold green]MISSION RESULTS - OPERATION COMPLETE[/]\n[bold cyan]═══════════════════════════════════════════[/]", id="results-title")
            
            for scan_type, output in self.results.items():
                yield Static(f"\n[bold yellow]▶ {scan_type.upper()}[/]")
                yield Static(f"[dim]{output[:500]}...[/]" if len(output) > 500 else f"[dim]{output}[/]")
            
            yield Static(f"\n[bold green]✓ Results saved to:[/] [cyan]{config.output_dir}[/]")
        
        yield Footer()

class BugBountyTUI(App):
    """Main Bug Bounty TUI Application"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        height: 100%;
        background: $panel;
    }
    
    #target-container {
        height: auto;
        background: $surface;
        border: heavy $primary;
        padding: 1;
        margin: 1;
    }
    
    #scan-options {
        height: auto;
        background: $surface;
        border: heavy $success;
        padding: 1;
        margin: 1;
    }
    
    #output-container {
        height: 1fr;
        background: black;
        border: heavy $accent;
        padding: 1;
        margin: 1;
    }
    
    #control-panel {
        height: auto;
        background: $surface;
        padding: 1;
        margin: 1;
    }
    
    .section-title {
        color: $accent;
        text-style: bold;
        padding-bottom: 1;
    }
    
    Input {
        border: solid $primary;
        width: 100%;
    }
    
    Button {
        margin: 0 1;
    }
    
    TextLog {
        background: black;
        color: $success;
        border: solid $accent;
    }
    
    ProgressBar {
        margin: 1;
    }
    
    .checkbox-group {
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "run_scan", "Run Scan", show=True),
        Binding("s", "stop_scan", "Stop", show=True),
        Binding("c", "clear_output", "Clear", show=True),
    ]
    
    def __init__(self):
        super().__init__()
        self.title = "BUG BOUNTY TUI v2.0"
        self.sub_title = "Advanced Reconnaissance Framework"
        
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with ScrollableContainer(id="main-container"):
            # Target input section
            with Container(id="target-container"):
                yield Static("[bold cyan]┌─────────────────────────────────────────┐[/]\n[bold cyan]│[/]  [bold green]TARGET ACQUISITION[/]                   [bold cyan]│[/]\n[bold cyan]└─────────────────────────────────────────┘[/]", classes="section-title")
                yield Input(
                    placeholder="https://manage-sandbox.gocardless.com",
                    id="target-input"
                )
                yield Static("[dim]Enter target URL (e.g., https://target.com)[/]", classes="hint")
            
            # Scan options section
            with Container(id="scan-options"):
                yield Static("[bold cyan]┌─────────────────────────────────────────┐[/]\n[bold cyan]│[/]  [bold yellow]SCAN CONFIGURATION[/]                   [bold cyan]│[/]\n[bold cyan]└─────────────────────────────────────────┘[/]", classes="section-title")
                
                yield Checkbox("🔍 Subdomain Enumeration (subfinder, amass)", value=True, id="scan_subdomains")
                yield Checkbox("🌐 Port Scanning (nmap)", value=True, id="scan_ports")
                yield Checkbox("📁 Directory Bruteforce (gobuster)", value=True, id="scan_dirs")
                yield Checkbox("🔧 Technology Detection (whatweb, wafw00f)", value=True, id="scan_tech")
                yield Checkbox("🔒 SSL/TLS Analysis (sslscan)", value=False, id="scan_ssl")
                yield Checkbox("🐛 Web Vulnerability Scan (nikto)", value=False, id="scan_nikto")
                yield Checkbox("💉 SQL Injection (sqlmap) - Manual Auth Required", value=False, id="scan_sql")
                yield Checkbox("⚡ XSS Detection (dalfox) - Manual Auth Required", value=False, id="scan_xss")
                yield Checkbox("🕷️ Web Crawling (gospider)", value=False, id="scan_spider")
                yield Checkbox("🔗 Historical URLs (waybackurls)", value=False, id="scan_wayback")
            
            # Control panel
            with Horizontal(id="control-panel"):
                yield Button("⚡ START SCAN", variant="success", id="start-btn")
                yield Button("⏸️  STOP", variant="warning", id="stop-btn")
                yield Button("🗑️  CLEAR", variant="error", id="clear-btn")
                yield Button("📊 RESULTS", variant="primary", id="results-btn")
            
            # Progress bar
            yield ProgressBar(total=100, show_eta=True, id="progress-bar")
            
            # Output section
            with Container(id="output-container"):
                yield Static("[bold green]═══════════════════════════════════════════[/]\n[bold cyan]SYSTEM OUTPUT - REAL-TIME MONITORING[/]\n[bold green]═══════════════════════════════════════════[/]", classes="section-title")
                yield TextLog(id="output-log", highlight=True, markup=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Show welcome screen on mount"""
        self.push_screen(WelcomeScreen())
        log = self.query_one("#output-log", TextLog)
        log.write("[bold green]>>> SYSTEM INITIALIZED[/]")
        log.write("[bold cyan]>>> Awaiting target input...[/]")
    
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
    
    def action_run_scan(self) -> None:
        """Start the scanning process"""
        target_input = self.query_one("#target-input", Input)
        target = target_input.value.strip()
        
        if not target:
            self.notify("❌ Please enter a target URL!", severity="error")
            return
        
        config.set_target(target)
        
        # Get selected scans
        scans = []
        if self.query_one("#scan_subdomains", Checkbox).value:
            scans.append("subdomains")
        if self.query_one("#scan_ports", Checkbox).value:
            scans.append("ports")
        if self.query_one("#scan_dirs", Checkbox).value:
            scans.append("directories")
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
        
        log = self.query_one("#output-log", TextLog)
        log.write(f"\n[bold yellow]{'='*50}[/]")
        log.write(f"[bold green]>>> INITIATING SCAN SEQUENCE[/]")
        log.write(f"[bold cyan]>>> TARGET:[/] {target}")
        log.write(f"[bold cyan]>>> OUTPUT:[/] {config.output_dir}")
        log.write(f"[bold cyan]>>> MODULES:[/] {len(scans)}")
        log.write(f"[bold yellow]{'='*50}[/]\n")
        
        # Start scanning in background thread
        thread = threading.Thread(target=self.run_scans, daemon=True)
        thread.start()
        
        self.notify("🚀 Scan started!", severity="information")
    
    def action_stop_scan(self) -> None:
        """Stop the scanning process"""
        config.running = False
        log = self.query_one("#output-log", TextLog)
        log.write("\n[bold red]>>> SCAN TERMINATED BY USER[/]\n")
        self.notify("⏸️  Scan stopped", severity="warning")
    
    def action_clear_output(self) -> None:
        """Clear output log"""
        log = self.query_one("#output-log", TextLog)
        log.clear()
        log.write("[bold green]>>> OUTPUT CLEARED[/]")
    
    def show_results(self) -> None:
        """Show results screen"""
        if config.results:
            self.push_screen(ResultsScreen(config.results))
        else:
            self.notify("📊 No results yet. Run a scan first!", severity="information")
    
    def run_scans(self):
        """Execute all selected scans"""
        log = self.query_one("#output-log", TextLog)
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
        log = self.query_one("#output-log", TextLog)
        target = config.target
        output_dir = config.output_dir
        
        # Extract domain from URL
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]
        
        commands = {
            "subdomains": f"subfinder -d {domain} -o {output_dir}/subdomains.txt -silent",
            "ports": f"nmap -sV -sC -p 80,443,8080,8443 {domain} -oN {output_dir}/nmap-scan.txt",
            "directories": f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt -o {output_dir}/gobuster.txt -q -t 50",
            "technology": f"whatweb {target} -v",
            "ssl": f"sslscan {domain}",
            "nikto": f"nikto -h {target} -output {output_dir}/nikto.txt",
            "sqlmap": f"echo 'SQLmap requires authenticated session. Run manually with: sqlmap -u {target}/endpoint --cookie=SESSION'",
            "xss": f"echo 'XSS scanning requires authenticated session. Run manually with: dalfox url {target}/endpoint'",
            "spider": f"gospider -s {target} -d 2 -c 5 -o {output_dir}/spider",
            "wayback": f"waybackurls {domain} | tee {output_dir}/wayback-urls.txt"
        }
        
        cmd = commands.get(scan_type, f"echo 'Unknown scan type: {scan_type}'")
        
        # Log the command being executed
        self.call_from_thread(log.write, f"[dim]$ {cmd}[/]")
        
        try:
            # Execute command
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            output = result.stdout if result.stdout else result.stderr
            
            # Stream output to log
            for line in output.split('\n')[:20]:  # Show first 20 lines
                if line.strip():
                    self.call_from_thread(log.write, f"[dim]{line}[/]")
            
            if len(output.split('\n')) > 20:
                self.call_from_thread(log.write, f"[dim]... ({len(output.split('\\n')) - 20} more lines in file)[/]")
            
            return output
            
        except subprocess.TimeoutExpired:
            return "ERROR: Scan timed out after 5 minutes"
        except Exception as e:
            return f"ERROR: {str(e)}"

if __name__ == "__main__":
    app = BugBountyTUI()
    app.run()
