"""
╔══════════════════════════════════════════════════════════════╗
║       RINT IDE v3.6 - Professional Edition                   ║
║       Atlas Studio · 40+ Premium Features                    ║
║       VS Code + JetBrains Rider Inspired                     ║
╚══════════════════════════════════════════════════════════════╝

Features:
• Multiple Themes (Violet, Onyx, Midnight, etc.)
• Full Syntax Highlighting & Linting
• Intelligent Autocomplete with Docs
• Command Palette (Ctrl+P)
• Spotlight Search (Ctrl+Shift+F)
• Git Integration UI
• Project Management
• Terminal Integration
• Debugger with Breakpoints
• Variable Watch & Memory Monitor
• Find & Replace with Regex
• Multi-cursor Editing
• Code Folding
• Minimap
• Split View Editor
• File History & Recovery
• Plugin System
• Snippet Manager
• Color Picker
• Markdown Preview
• Task Runner
• Performance Profiler
• Code Metrics
• TODO Tracker
• Bookmarks
• Live Share (UI)
• Code Generation
• Refactoring Tools
• Smart Imports
• Path Autocomplete
• Symbol Navigation
• Go to Definition
• Find References
• Rename Symbol
• Quick Fix Suggestions
• Documentation Generator
• Export to HTML/PDF
• Keyboard Shortcut Recorder
• Session Management
• Workspace Settings
• Extension Marketplace (UI)
• Collaborative Editing (UI)

Installation:
pip install customtkinter
pip install psutil  (optional - for RAM monitor)
pip install Pillow  (optional - for logo support)
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import re, os, sys, json, time, threading, math, traceback, webbrowser
from datetime import datetime
from pathlib import Path

# Optional dependencies
try:
    import psutil
    HAS_PSUTIL = True
except:
    HAS_PSUTIL = False

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except:
    HAS_PIL = False

# ─── THEMES SYSTEM ────────────────────────────────────────────────────────────

THEMES = {
    "violet": {
        "name": "Violet Dream",
        "bg_root": "#0b0c1a", "bg_panel": "#131427", "bg_editor": "#0d0e1e",
        "bg_sidebar": "#0f1020", "bg_tab_active": "#1a1b2f", "bg_tab_idle": "#0f1020",
        "bg_input": "#181929", "bg_hover": "#1e2038", "bg_select": "#2a2b48",
        "accent": "#7b6cf6", "accent2": "#4ecdc4", "accent_glow": "#9d8ff8",
        "accent_dark": "#5a4fd4", "warn": "#f6a623", "error": "#ff5757",
        "success": "#69e89c", "info": "#60a5fa", "text": "#dce0f5",
        "text_muted": "#5a6080", "text_dim": "#3d4060", "line_num": "#404060",
        "border": "#1e2040", "cursor": "#7b6cf6", "selection": "#2a2b5a",
    },
    "onyx": {
        "name": "Onyx Black",
        "bg_root": "#0a0a0a", "bg_panel": "#121212", "bg_editor": "#0d0d0d",
        "bg_sidebar": "#0f0f0f", "bg_tab_active": "#1a1a1a", "bg_tab_idle": "#0f0f0f",
        "bg_input": "#151515", "bg_hover": "#1c1c1c", "bg_select": "#252525",
        "accent": "#00d9ff", "accent2": "#00ff9d", "accent_glow": "#33e0ff",
        "accent_dark": "#008fb3", "warn": "#ffb800", "error": "#ff4757",
        "success": "#26de81", "info": "#4b7bec", "text": "#e0e0e0",
        "text_muted": "#707070", "text_dim": "#404040", "line_num": "#505050",
        "border": "#1a1a1a", "cursor": "#00d9ff", "selection": "#2a2a3a",
    },
    "midnight": {
        "name": "Midnight Blue",
        "bg_root": "#0c1222", "bg_panel": "#131b2e", "bg_editor": "#0e1628",
        "bg_sidebar": "#101829", "bg_tab_active": "#1a2540", "bg_tab_idle": "#101829",
        "bg_input": "#16213a", "bg_hover": "#1c2a48", "bg_select": "#253556",
        "accent": "#5890ff", "accent2": "#2dd4bf", "accent_glow": "#7ba7ff",
        "accent_dark": "#3a6ed8", "warn": "#fbbf24", "error": "#f87171",
        "success": "#4ade80", "info": "#60a5fa", "text": "#e2e8f0",
        "text_muted": "#64748b", "text_dim": "#475569", "line_num": "#475569",
        "border": "#1e293b", "cursor": "#5890ff", "selection": "#2a3f5f",
    },
    "forest": {
        "name": "Forest Green",
        "bg_root": "#0a120e", "bg_panel": "#0f1912", "bg_editor": "#0b140f",
        "bg_sidebar": "#0d1610", "bg_tab_active": "#152620", "bg_tab_idle": "#0d1610",
        "bg_input": "#111d16", "bg_hover": "#1a2822", "bg_select": "#1f3329",
        "accent": "#10b981", "accent2": "#34d399", "accent_glow": "#6ee7b7",
        "accent_dark": "#059669", "warn": "#f59e0b", "error": "#ef4444",
        "success": "#22c55e", "info": "#3b82f6", "text": "#d1fae5",
        "text_muted": "#6b8e7f", "text_dim": "#475569", "line_num": "#52796f",
        "border": "#1a2e23", "cursor": "#10b981", "selection": "#1f3d2f",
    },
    "sunset": {
        "name": "Sunset Orange",
        "bg_root": "#1a0f0a", "bg_panel": "#221510", "bg_editor": "#1c110c",
        "bg_sidebar": "#1e1310", "bg_tab_active": "#2d1f18", "bg_tab_idle": "#1e1310",
        "bg_input": "#251a14", "bg_hover": "#332520", "bg_select": "#3d2f28",
        "accent": "#ff6b35", "accent2": "#f7931e", "accent_glow": "#ff8c5a",
        "accent_dark": "#cc4b1a", "warn": "#fbbf24", "error": "#dc2626",
        "success": "#10b981", "info": "#3b82f6", "text": "#fef3c7",
        "text_muted": "#a8836b", "text_dim": "#6b5446", "line_num": "#7a5d47",
        "border": "#2d1f16", "cursor": "#ff6b35", "selection": "#3d2820",
    },
}

CURRENT_THEME = "violet"
IDE_INSTANCE = None  # Global reference pour mise à jour live

def get_color(key):
    return THEMES[CURRENT_THEME].get(key, "#ffffff")

def update_theme_live(widget, key, attribute="fg_color"):
    """Met à jour dynamiquement la couleur d'un widget"""
    try:
        color = get_color(key)
        if attribute in ["fg_color", "bg_color"]:
            setattr(widget, f"_{attribute}", color)
        else:
            widget.configure(**{attribute: color})
    except:
        pass

# ─── FONTS ────────────────────────────────────────────────────────────────────

FONT_CODE   = ("JetBrains Mono", 11)
FONT_CODE_S = ("JetBrains Mono", 9)
FONT_UI     = ("Segoe UI", 10)
FONT_UI_S   = ("Segoe UI", 9)
FONT_UI_B   = ("Segoe UI", 10, "bold")
FONT_TITLE  = ("Segoe UI", 12, "bold")

# ─── RINT LANGUAGE DEFINITION ────────────────────────────────────────────────

RINT_KEYWORDS = {
    "if","else","while","when","repeat","return","func","true","false",
    "and","or","not","in","to","time","class","use","as","alloc",
    "memcpy","memmove","realloc","memset","forward","backward",
    "left","right","down","up","all",
}

RINT_TYPES = {"int","string","bool","float","list","wave","unit","sys"}

RINT_BUILTINS = {
    "console","Audio","System","Voltige","hardware","Turtle",
    "JSON","hard","js","PC",
}

RINT_FUNCS = {
    "print","log","ask","read","del","play","load","add","new","config",
    "move","set","get","save","run","pick","drop","return","limit",
    "reduce","error","crash","info","changed","name","debug","virtual",
    "alt","speed","port","autodetect","bass","pen","write","track","context",
}

SYNTAX_PATTERNS = [
    ("comment",   r"//.*?$"),
    ("fstring",   r'f"[^"]*"'),
    ("string",    r'"[^"]*"|\'[^\']*\''),
    ("number",    r'\b\d+(\.\d+)?\b'),
    ("keyword",   r'\b(' + '|'.join(sorted(RINT_KEYWORDS)) + r')\b'),
    ("type_kw",   r'\b(' + '|'.join(sorted(RINT_TYPES)) + r')\b'),
    ("builtin",   r'\b(' + '|'.join(sorted(RINT_BUILTINS)) + r')\b'),
    ("func_call", r'\b(' + '|'.join(sorted(RINT_FUNCS)) + r')\b'),
    ("operator",  r'[=<>!+\-\*/%&|^~]+|[\[\]{}()]'),
]

ALL_COMPLETIONS = sorted(list(RINT_KEYWORDS | RINT_TYPES | RINT_BUILTINS | RINT_FUNCS) + [
    "console.print(","console.log(","console.ask(","Audio.play(","Turtle.move(",
])

SNIPPETS = {
    "if": 'if {cond} {\n    \n}',
    "else": 'else {\n    \n}',
    "while": 'while true {\n    \n}',
    "when": 'when {cond} {\n    \n}',
    "func": 'func {name}({args}) {\n    return \n}',
    "class": 'class {Name}\n{\n    \n}',
    "repeat": 'repeat time({n}) {\n    \n}',
}

DOCS = {
    "console.print": "Affiche un message dans la console.",
    "console.log": "Log vers l'espace dédié.",
    "when": "Surveille une condition.",
    "repeat": "Répète N fois.",
}

# ─── MEMORY MONITORING SYSTEM ────────────────────────────────────────────────

class MemoryMonitor:
    """Tracks memory usage of code execution vs IDE"""
    
    def __init__(self):
        self.enabled = HAS_PSUTIL
        self.history = []  # List of (timestamp, ide_mb, code_mb, total_mb)
        self.max_ide_mb = 0
        self.max_code_mb = 0
        self.max_total_mb = 0
        self.avg_code_mb = 0
        self.peak_time = 0
        self.memory_auto_mgmt = False  # Detected from code
        self.manual_allocs = 0
        self.memory_params = {}
        
    def start_monitoring(self):
        """Reset monitoring for new execution"""
        self.history.clear()
        self.max_ide_mb = 0
        self.max_code_mb = 0
        self.max_total_mb = 0
        self.avg_code_mb = 0
        self.peak_time = 0
        
    def sample_memory(self):
        """Capture memory snapshot"""
        if not self.enabled:
            return None
        try:
            process = psutil.Process()
            total_mb = process.memory_info().rss / (1024*1024)
            # Estimate: ~150-200 MB baseline for IDE + Python
            ide_estimate = 180  # Base IDE memory
            code_mb = max(0, total_mb - ide_estimate)
            
            self.history.append((time.time(), ide_estimate, code_mb, total_mb))
            
            # Update peaks
            if code_mb > self.max_code_mb:
                self.max_code_mb = code_mb
                self.peak_time = time.time()
            if total_mb > self.max_total_mb:
                self.max_total_mb = total_mb
                
            return {"ide": ide_estimate, "code": code_mb, "total": total_mb}
        except:
            return None
    
    def detect_memory_params(self, code):
        """Detect memory management parameters in code"""
        self.memory_auto_mgmt = False
        self.memory_params = {}
        self.manual_allocs = 0
        
        # Check for memory management keywords
        if "alloc" in code.lower():
            self.memory_params["alloc"] = True
            self.manual_allocs += code.lower().count("alloc")
        if "memcpy" in code.lower():
            self.memory_params["memcpy"] = True
        if "realloc" in code.lower():
            self.memory_params["realloc"] = True
        if "memset" in code.lower():
            self.memory_params["memset"] = True
        if re.search(r'\bwhen\s+', code):  # when condition for memory monitoring
            self.memory_params["when"] = True
        if "memory" in code.lower() or "mem" in code.lower():
            self.memory_params["explicit"] = True
        if "Audio" in code:  # Audio often uses large buffers
            self.memory_params["audio_buffers"] = True
        
        # Set auto-management flag if found
        self.memory_auto_mgmt = bool(self.memory_params)
    
    def get_stats(self):
        """Get memory statistics"""
        if not self.history:
            return {}
        
        code_values = [h[2] for h in self.history]
        if code_values:
            self.avg_code_mb = sum(code_values) / len(code_values)
        
        return {
            "peak_code_mb": round(self.max_code_mb, 2),
            "avg_code_mb": round(self.avg_code_mb, 2),
            "peak_total_mb": round(self.max_total_mb, 2),
            "samples": len(self.history),
            "manual_allocs": self.manual_allocs,
            "has_auto_mgmt": self.memory_auto_mgmt,
            "memory_params": self.memory_params,
        }

# ─── SPLASH SCREEN ────────────────────────────────────────────────────────────


class SplashScreen(tk.Toplevel):
    """Professional splash screen with logo support and fade animations"""

    def __init__(self, parent, logo_path=None):
        super().__init__(parent)
        self.configure(bg=get_color("bg_root"))
        self.overrideredirect(True)
        self.attributes('-alpha', 0.0)  # Start invisible for fade-in

        # Center on screen
        w, h = 600, 400
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Canvas - no borders, no gradients, clean
        canvas = tk.Canvas(self, bg=get_color("bg_root"), highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Try to load logo
        logo_loaded = False
        if logo_path and HAS_PIL and os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                # Resize to fit
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                # Change color from white to violet
                img = img.convert("RGBA")
                pixels = img.load()
                violet_rgb = (157, 78, 221)  # #9d4edd
                for i in range(img.width):
                    for j in range(img.height):
                        r, g, b, a = pixels[i, j]
                        if a > 0:  # If not transparent
                            pixels[i, j] = (*violet_rgb, a)

                self.logo_img = ImageTk.PhotoImage(img)
                canvas.create_image(w//2, 120, image=self.logo_img)
                logo_loaded = True
            except Exception as e:
                print(f"Logo load error: {e}")

        # Fallback: text logo
        if not logo_loaded:
            canvas.create_text(w//2, 120, text="✦", 
                             font=("Segoe UI", 80),
                             fill="#9d4edd")

        # Title
        canvas.create_text(w//2, 220, text="RINT IDE", 
                          font=("Segoe UI", 32, "bold"),
                          fill=get_color("text"))

        canvas.create_text(w//2, 260, text="Professional Edition v3.5", 
                          font=("Segoe UI", 12),
                          fill=get_color("text_muted"))

        # Progress bar
        self.progress_bar = canvas.create_rectangle(
            100, 310, 100, 320,
            fill=get_color("accent"), outline=""
        )
        self.canvas = canvas
        self.w = w

        # Status text
        self.status_text = canvas.create_text(w//2, 350, text="Initializing...", 
                                              font=("Segoe UI", 9),
                                              fill=get_color("text_dim"))

        # Animate
        self.progress = 0
        self.after(50, self._fade_in)
        self.after(300, self._animate)

    def _animate(self):
        if self.progress < 100:
            self.progress += 0.7  # ~3-4 second load time
            self.canvas.coords(self.progress_bar, 
                              100, 310, 
                              100 + (400 * self.progress / 100), 320)

            # Update status
            statuses = [
                "Loading core modules...",
                "Initializing syntax engine...",
                "Loading plugins...",
                "Preparing workspace...",
                "Ready!"
            ]
            idx = min(int(self.progress) // 20, len(statuses) - 1)
            self.canvas.itemconfig(self.status_text, text=statuses[idx])

            self.after(35, self._animate)
        else:
            self.after(400, self._fade_out)

    def _fade_in(self):
        """Smooth fade-in effect"""
        alpha = self.attributes('-alpha')
        if alpha < 1.0:
            alpha = min(1.0, alpha + 0.1)
            self.attributes('-alpha', alpha)
            self.after(30, self._fade_in)

    def _fade_out(self):
        """Smooth fade-out effect before closing"""
        alpha = self.attributes('-alpha')
        if alpha > 0:
            alpha = max(0, alpha - 0.1)
            self.attributes('-alpha', alpha)
            self.after(30, self._fade_out)
        else:
            self.destroy()

# ─── SYNTAX HIGHLIGHTER ───────────────────────────────────────────────────────

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.w = text_widget
        self._patterns = [(n, re.compile(p, re.MULTILINE)) for n, p in SYNTAX_PATTERNS]
        self._configure_tags()
    
    def _configure_tags(self):
        w = self.w
        w.tag_configure("comment", foreground="#6a7485", font=(*FONT_CODE, "italic"))
        w.tag_configure("fstring", foreground="#c8e6c9")
        w.tag_configure("string", foreground="#a8e063")
        w.tag_configure("number", foreground="#ff9d6c")
        w.tag_configure("keyword", foreground="#c792ea", font=(*FONT_CODE, "bold"))
        w.tag_configure("type_kw", foreground="#f9c74f", font=(*FONT_CODE, "bold"))
        w.tag_configure("builtin", foreground="#ffcb6b")
        w.tag_configure("func_call", foreground="#79b8ff")
        w.tag_configure("operator", foreground="#89ddff")
        w.tag_configure("current_line", background=get_color("bg_select"))
        w.tag_configure("find_match", background=get_color("warn"), foreground="#000")
    
    def highlight(self):
        content = self.w.get("1.0", "end-1c")
        for tag, _ in self._patterns:
            self.w.tag_remove(tag, "1.0", "end")
        for tag, pat in self._patterns:
            for m in pat.finditer(content):
                s = self._off(content, m.start())
                e = self._off(content, m.end())
                self.w.tag_add(tag, s, e)
    
    def _off(self, content, offset):
        line = content[:offset].count("\n") + 1
        col = offset - (content[:offset].rfind("\n") + 1)
        return f"{line}.{col}"

# ─── FIND & REPLACE PANEL ─────────────────────────────────────────────────────

class FindReplacePanel(ctk.CTkFrame):
    """Panel Find & Replace collapsible avec recherche en temps réel"""
    def __init__(self, parent, editor_text, **kwargs):
        super().__init__(parent, corner_radius=0, fg_color=get_color("bg_panel"), height=100, **kwargs)
        self.editor = editor_text
        self.find_matches = []
        self.current_match = 0
        
        # Header
        hdr = ctk.CTkFrame(self, height=32, fg_color=get_color("bg_sidebar"), corner_radius=0)
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="🔍 Find & Replace", font=FONT_UI_S, text_color=get_color("accent")).pack(side="left", padx=8)
        ctk.CTkButton(hdr, text="✕", width=24, height=24, fg_color="transparent", command=self._close).pack(side="right", padx=4)
        
        # Find frame
        find_frame = ctk.CTkFrame(self, fg_color="transparent")
        find_frame.pack(fill="x", padx=8, pady=4)
        ctk.CTkLabel(find_frame, text="Find:", font=FONT_UI_S, text_color=get_color("text_muted")).pack(side="left", padx=4, padx_=0)
        self.find_entry = ctk.CTkEntry(find_frame, placeholder_text="Search...", width=200, height=24, font=FONT_CODE_S)
        self.find_entry.pack(side="left", fill="x", expand=True, padx=4)
        self.find_entry.bind("<KeyRelease>", self._on_find_change)
        self.find_entry.bind("<Return>", lambda e: self._find_next())
        
        ctk.CTkButton(find_frame, text="↑", width=28, height=24, command=self._find_prev).pack(side="left", padx=1)
        ctk.CTkButton(find_frame, text="↓", width=28, height=24, command=self._find_next).pack(side="left", padx=1)
        self.find_count = ctk.CTkLabel(find_frame, text="0/0", font=FONT_UI_S, text_color=get_color("text_muted"))
        self.find_count.pack(side="left", padx=4)
        
        # Replace frame
        replace_frame = ctk.CTkFrame(self, fg_color="transparent")
        replace_frame.pack(fill="x", padx=8, pady=4)
        ctk.CTkLabel(replace_frame, text="Replace:", font=FONT_UI_S, text_color=get_color("text_muted")).pack(side="left", padx=4)
        self.replace_entry = ctk.CTkEntry(replace_frame, placeholder_text="Replace with...", width=200, height=24, font=FONT_CODE_S)
        self.replace_entry.pack(side="left", fill="x", expand=True, padx=4)
        
        ctk.CTkButton(replace_frame, text="Replace", width=70, height=24, command=self._replace_one).pack(side="left", padx=1)
        ctk.CTkButton(replace_frame, text="Replace All", width=80, height=24, command=self._replace_all).pack(side="left", padx=1)
        ctk.CTkButton(replace_frame, text="Match Case", width=80, height=24, fg_color=get_color("bg_input")).pack(side="left", padx=1)
    
    def _on_find_change(self, event=None):
        """Highlight matches en temps réel"""
        if not self.editor: return
        pattern = self.find_entry.get()
        self.editor.tag_remove("find_match", "1.0", "end")
        self.find_matches = []
        self.current_match = 0
        
        if not pattern: 
            self.find_count.configure(text="0/0")
            return
        
        content = self.editor.get("1.0", "end-1c")
        try:
            for m in re.finditer(re.escape(pattern), content):
                start = content[:m.start()].count("\n") + 1
                col = m.start() - (content[:m.start()].rfind("\n") + 1)
                end_col = col + len(pattern)
                self.find_matches.append((f"{start}.{col}", f"{start}.{end_col}"))
            
            if self.find_matches:
                for s, e in self.find_matches:
                    self.editor.tag_add("find_match", s, e)
                self.find_count.configure(text=f"1/{len(self.find_matches)}")
                self.editor.see(self.find_matches[0][0])
            else:
                self.find_count.configure(text="0/0")
        except: pass
    
    def _find_next(self):
        if not self.find_matches: return
        self.current_match = (self.current_match + 1) % len(self.find_matches)
        start, end = self.find_matches[self.current_match]
        self.editor.see(start)
        self.editor.mark_set("insert", end)
        self.find_count.configure(text=f"{self.current_match+1}/{len(self.find_matches)}")
    
    def _find_prev(self):
        if not self.find_matches: return
        self.current_match = (self.current_match - 1) % len(self.find_matches)
        start, end = self.find_matches[self.current_match]
        self.editor.see(start)
        self.editor.mark_set("insert", start)
        self.find_count.configure(text=f"{self.current_match+1}/{len(self.find_matches)}")
    
    def _replace_one(self):
        if not self.find_matches: return
        start, end = self.find_matches[self.current_match]
        replacement = self.replace_entry.get()
        self.editor.delete(start, end)
        self.editor.insert(start, replacement)
        self._on_find_change()
    
    def _replace_all(self):
        pattern = self.find_entry.get()
        replacement = self.replace_entry.get()
        if pattern:
            content = self.editor.get("1.0", "end")
            new_content = content.replace(pattern, replacement)
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", new_content)
            self._on_find_change()
    
    def _close(self):
        if self.editor:
            self.editor.tag_remove("find_match", "1.0", "end")
        self.pack_forget()

# ─── AUTOCOMPLETE ─────────────────────────────────────────────────────────────

class AutoComplete(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.overrideredirect(True)
        self.withdraw()
        self.configure(bg=get_color("accent"))
        self.wm_attributes("-topmost", True)
        
        inner = tk.Frame(self, bg=get_color("bg_panel"))
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.listbox = tk.Listbox(
            inner, bg=get_color("bg_panel"), fg=get_color("text"),
            selectbackground=get_color("accent"), selectforeground="#fff",
            font=FONT_CODE_S, borderwidth=0, highlightthickness=0,
            height=8, width=35,
        )
        self.listbox.pack(fill="both", expand=True, padx=2, pady=2)
        self.listbox.bind("<Double-Button-1>", lambda e: self._select())
        self.listbox.bind("<Return>", lambda e: self._select())
    
    def show(self, x, y, items):
        self.listbox.delete(0, "end")
        if not items: self.withdraw(); return
        for item in items[:12]:
            self.listbox.insert("end", item)
        self.deiconify()
        self.geometry(f"+{x}+{y}")
        self.listbox.selection_set(0)
    
    def hide(self):
        self.withdraw()
    
    def _select(self):
        sel = self.listbox.curselection()
        if sel: self.callback(self.listbox.get(sel[0]))
    
    def navigate(self, delta):
        if not self.winfo_viewable(): return
        sel = self.listbox.curselection()
        idx = sel[0] if sel else -1
        new = max(0, min(self.listbox.size()-1, idx+delta))
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(new)
        self.listbox.see(new)

# ─── LINE NUMBERS ─────────────────────────────────────────────────────────────

class LineNumbers(tk.Canvas):
    def __init__(self, parent, text_widget):
        super().__init__(parent, bg=get_color("bg_sidebar"), 
                        highlightthickness=0, width=50)
        self.text = text_widget
        self.breakpoints = set()
        self.bind("<Button-1>", self._toggle_bp)
    
    def _toggle_bp(self, event):
        line = int(self.text.index(f"@0,{event.y}").split(".")[0])
        if line in self.breakpoints:
            self.breakpoints.remove(line)
        else:
            self.breakpoints.add(line)
        self.redraw()
    
    def redraw(self, *_):
        self.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if not dline: break
            y = dline[1]
            ln = int(str(i).split(".")[0])
            is_bp = ln in self.breakpoints
            if is_bp:
                self.create_oval(3, y+2, 13, y+12, fill=get_color("error"), outline="")
            self.create_text(46, y+8, anchor="e", text=str(ln),
                           fill=get_color("error") if is_bp else get_color("line_num"),
                           font=FONT_CODE_S)
            ni = self.text.index(f"{i}+1line")
            if ni == i: break
            i = ni

# ─── INTERPRETER ──────────────────────────────────────────────────────────────

class RintInterpreter:
    def __init__(self, output_cb, log_cb, error_cb, var_update_cb=None):
        self.output = output_cb
        self.log = log_cb
        self.error = error_cb
        self.var_update = var_update_cb or (lambda *a: None)
        self.variables = {}
        self.variable_types = {}
        self.running = False
    
    def run(self, code):
        self.running = True
        self.variables = {}
        self.variable_types = {}
        try:
            lines = code.split("\n")
            for i, line in enumerate(lines, 1):
                if not self.running: break
                line = line.strip()
                if not line or line.startswith("//"): continue
                self._exec_line(line, i)
        except Exception as e:
            self.error(f"Runtime error: {e}")
        finally:
            self.running = False
    
    def _exec_line(self, line, lineno):
        # Variable declaration avec types
        m = re.match(r'^(int|string|bool|float)\s+(\w+)\s*=\s*(.+)$', line)
        if m:
            t, name, expr = m.groups()
            value = self._eval(expr)
            self.variables[name] = value
            self.variable_types[name] = t
            self.var_update(name, value, t)
            return
        
        # Variable assignment
        m = re.match(r'^(\w+)\s*=\s*(.+)$', line)
        if m:
            name, expr = m.groups()
            value = self._eval(expr)
            self.variables[name] = value
            t = self.variable_types.get(name, "var")
            self.var_update(name, value, t)
            return
        
        # console.print
        m = re.match(r'^console\.print\((.+)\)$', line)
        if m:
            val = self._eval_str(m.group(1).strip())
            self.output(val)
            return
        
        # console.log
        m = re.match(r'^console\.log\((.+)\)$', line)
        if m:
            val = self._eval_str(m.group(1).strip())
            self.log(val)
            return
        
        # Turtle.move
        m = re.match(r'^Turtle\.move\((\d+)\)$', line)
        if m:
            dist = int(m.group(1))
            self.log(f"Turtle moving forward {dist} units")
            return
    
    def _eval(self, expr):
        expr = expr.strip().rstrip(",")
        if expr == "true": return True
        if expr == "false": return False
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        if re.match(r'^\d+$', expr):
            return int(expr)
        if re.match(r'^\d+\.\d+$', expr):
            return float(expr)
        return expr
    
    def _eval_str(self, expr):
        expr = expr.strip()
        if expr.startswith('f"') and expr.endswith('"'):
            content = expr[2:-1]
            def repl(m):
                var = m.group(1)
                return str(self.variables.get(var, f"{{{var}}}"))
            return re.sub(r'\{([^}]+)\}', repl, content)
        if expr.startswith('"'): return expr.strip('"')
        return expr

# ─── COMMAND PALETTE ──────────────────────────────────────────────────────────

class CommandPalette(tk.Toplevel):
    COMMANDS = [
        ("Run Code", "Ctrl+R", "run"),
        ("Save File", "Ctrl+S", "save"),
        ("Open File", "Ctrl+O", "open"),
        ("New File", "Ctrl+N", "new"),
        ("Find", "Ctrl+F", "find"),
        ("Go to Line", "Ctrl+G", "goto"),
        ("Change Theme", "", "theme"),
        ("Toggle Sidebar", "Ctrl+B", "sidebar"),
        ("Terminal", "Ctrl+`", "terminal"),
        ("Git Status", "", "git"),
    ]
    
    def __init__(self, parent, ide):
        super().__init__(parent)
        self.ide = ide
        self.overrideredirect(True)
        self.configure(bg=get_color("accent"))
        w, h = 520, 380
        sw = self.winfo_screenwidth()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{100}")
        
        inner = tk.Frame(self, bg=get_color("bg_panel"))
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.search_var = tk.StringVar()
        self.entry = tk.Entry(inner, textvariable=self.search_var,
                             bg=get_color("bg_input"), fg=get_color("text"),
                             font=("JetBrains Mono", 12), borderwidth=0,
                             insertbackground=get_color("cursor"))
        self.entry.pack(fill="x", padx=12, pady=10, ipady=6)
        
        self.listbox = tk.Listbox(inner, bg=get_color("bg_panel"), 
                                  fg=get_color("text"),
                                  selectbackground=get_color("accent"),
                                  font=FONT_UI, borderwidth=0, 
                                  highlightthickness=0, height=14)
        self.listbox.pack(fill="both", expand=True, padx=2)
        
        self.search_var.trace("w", self._filter)
        self.entry.bind("<Return>", self._run)
        self.entry.bind("<Escape>", lambda e: self.destroy())
        self.entry.bind("<Up>", lambda e: self._nav(-1))
        self.entry.bind("<Down>", lambda e: self._nav(1))
        
        self._filtered = self.COMMANDS[:]
        self._populate()
        self.entry.focus()
    
    def _filter(self, *_):
        q = self.search_var.get().lower()
        self._filtered = [(n,s,c) for n,s,c in self.COMMANDS if q in n.lower()]
        self._populate()
    
    def _populate(self):
        self.listbox.delete(0, "end")
        for name, shortcut, _ in self._filtered:
            line = f"  {name}"
            if shortcut: line += f"  ({shortcut})"
            self.listbox.insert("end", line)
        if self._filtered: self.listbox.selection_set(0)
    
    def _nav(self, delta):
        sel = self.listbox.curselection()
        idx = sel[0] if sel else -1
        new = max(0, min(self.listbox.size()-1, idx+delta))
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(new)
    
    def _run(self, event=None):
        sel = self.listbox.curselection()
        if not sel or sel[0] >= len(self._filtered): return
        cmd = self._filtered[sel[0]][2]
        self.destroy()
        self.ide._exec_command(cmd)

# ─── MAIN IDE CLASS ───────────────────────────────────────────────────────────

class RintIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RINT IDE v3.5 — Professional Edition")
        self.geometry("1480x920")
        self.minsize(1200, 700)
        self.configure(fg_color=get_color("bg_root"))
        
        # State
        self.tabs = []
        self.active_tab = -1
        self.current_file = None
        self._running = False
        self.sidebar_visible = True
        self.right_panel_visible = True
        self.find_panel_visible = False
        self.vm_mode = False  # Isolated VM mode
        self.toolbar = None
        self.right_panel = None
        
        # Memory monitoring
        self.memory_monitor = MemoryMonitor()
        self.monitoring_thread = None
        
        # Show splash
        logo_path = r"C:\Users\leandro.boffy\Downloads\PROGRAME LANGUAGE, I wanna know that!\logo.png"
        splash = SplashScreen(self, logo_path if os.path.exists(logo_path) else None)
        self.wait_window(splash)
        
        # Build UI
        self._build_menu_bar()
        self._build_ui()
        self._bind_shortcuts()
        
        # Interpreter
        self.interpreter = RintInterpreter(
            output_cb=lambda m: self._ui_call(self._add_output, m),
            log_cb=lambda m: self._ui_call(self._add_log, m),
            error_cb=lambda m: self._ui_call(self._add_error, m),
        )
        
        # Global reference
        global IDE_INSTANCE
        IDE_INSTANCE = self
        
        # Create first tab
        self.new_file()
        
        # Initialize left panel (explorer)
        self._switch_left_panel("explorer")
        
        # Initialize right panel (stats)
        self._switch_right_panel("stats")
        
        # Demo: Show some initial content
        self._add_output("✓ RINT IDE v3.5 initialized")
        self._add_log("Ready to code!")
    
    def _ui_call(self, fn, *args):
        try: self.after(0, fn, *args)
        except: pass
    
    def _build_menu_bar(self):
        """Create menu bar with File, Edit, View menus - Dark themed"""
        menubar = tk.Menu(self, bg=get_color("bg_sidebar"), fg=get_color("text"),
                         activebackground=get_color("bg_hover"), 
                         activeforeground=get_color("accent"),
                         borderwidth=0)
        self.config(menu=menubar)
        self.menubar = menubar
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=get_color("bg_sidebar"), 
                           fg=get_color("text"),
                           activebackground=get_color("bg_hover"),
                           activeforeground=get_color("accent"),
                           borderwidth=0)
        menubar.add_cascade(label="Fichier", menu=file_menu, background=get_color("bg_sidebar"), foreground=get_color("text"))
        file_menu.add_command(label="Nouveau", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Ouvrir", command=self._open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Enregistrer", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Enregistrer sous...", command=self._save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Paramètres", command=self._show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0, bg=get_color("bg_sidebar"), 
                           fg=get_color("text"),
                           activebackground=get_color("bg_hover"),
                           activeforeground=get_color("accent"),
                           borderwidth=0)
        menubar.add_cascade(label="Édition", menu=edit_menu)
        edit_menu.add_command(label="Annuler", accelerator="Ctrl+Z")
        edit_menu.add_command(label="Refaire", accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Couper", accelerator="Ctrl+X")
        edit_menu.add_command(label="Copier", accelerator="Ctrl+C")
        edit_menu.add_command(label="Coller", accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Chercher", command=self._toggle_find_replace, accelerator="Ctrl+F")
        edit_menu.add_command(label="Remplacer", accelerator="Ctrl+H")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=get_color("bg_sidebar"), 
                           fg=get_color("text"),
                           activebackground=get_color("bg_hover"),
                           activeforeground=get_color("accent"),
                           borderwidth=0)
        menubar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Barre latérale", command=self._toggle_sidebar, accelerator="Ctrl+B")
        view_menu.add_separator()
        view_menu.add_command(label="Terminal", command=lambda: self._switch_console("Terminal"))
        view_menu.add_command(label="Variables", command=lambda: self._switch_console("Variables"))
        view_menu.add_command(label="Tortue", command=lambda: self._switch_console("Turtle"))
        view_menu.add_separator()
        
        # Themes submenu
        theme_menu = tk.Menu(view_menu, tearoff=0, bg=get_color("bg_sidebar"), 
                            fg=get_color("text"),
                            activebackground=get_color("bg_hover"),
                            activeforeground=get_color("accent"),
                            borderwidth=0)
        view_menu.add_cascade(label="Thème", menu=theme_menu)
        for theme_key in THEMES.keys():
            theme_menu.add_command(label=THEMES[theme_key]["name"], 
                                  command=lambda t=theme_key: self._change_theme(t))
        
        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0, bg=get_color("bg_sidebar"), 
                          fg=get_color("text"),
                          activebackground=get_color("bg_hover"),
                          activeforeground=get_color("accent"),
                          borderwidth=0)
        menubar.add_cascade(label="Exécution", menu=run_menu)
        run_menu.add_command(label="Exécuter", command=self._run_code, accelerator="Ctrl+R")
        run_menu.add_command(label="Arrêter", command=self._stop_code)
        run_menu.add_separator()
        run_menu.add_command(label="Mode VM isolé", command=self._toggle_vm_mode)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=get_color("bg_sidebar"), 
                           fg=get_color("text"),
                           activebackground=get_color("bg_hover"),
                           activeforeground=get_color("accent"),
                           borderwidth=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=lambda: messagebox.showinfo("À propos", "RINT IDE v3.5\nAtlas Studio"))
        help_menu.add_command(label="Documentation", command=lambda: webbrowser.open("https://rint.dev/docs"))
    
    def _build_ui(self):
        # ─── TOP TOOLBAR ──────────────────────────────────────────────────
        toolbar = ctk.CTkFrame(self, height=44, corner_radius=0,
                               fg_color=get_color("bg_sidebar"))
        toolbar.pack(fill="x", side="top")
        
        # Left section
        left_section = ctk.CTkFrame(toolbar, fg_color="transparent")
        left_section.pack(side="left", padx=8)
        
        # Plugins button
        ctk.CTkButton(left_section, text="📦", width=36, height=32,
                     fg_color="transparent", hover_color=get_color("bg_hover"),
                     font=("Segoe UI", 14), command=self._toggle_sidebar
                     ).pack(side="left", padx=2)
        
        tk.Frame(toolbar, bg=get_color("border"), width=1, height=28
                ).pack(side="left", padx=8)
        
        # Logo + Title
        ctk.CTkLabel(toolbar, text="✦ RINT", font=("Segoe UI", 11, "bold"),
                    text_color=get_color("accent")).pack(side="left", padx=4)
        
        tk.Frame(toolbar, bg=get_color("border"), width=1, height=28
                ).pack(side="left", padx=8)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(side="left")
        
        for icon, text, cmd, color in [
            ("▶", "Run", self._run_code, "success"),
            ("⏹", "Stop", self._stop_code, "error"),
            ("💾", "Save", self._save_file, "accent"),
            ("📂", "Open", self._open_file, "accent"),
            ("🔍", "Search", self._spotlight_search, "accent2"),
        ]:
            ctk.CTkButton(btn_frame, text=f"{icon} {text}", width=80, height=32,
                         fg_color=get_color(color), 
                         hover_color=get_color("bg_hover"),
                         text_color="#000" if color == "success" else "#fff",
                         font=FONT_UI_S, corner_radius=6,
                         command=cmd).pack(side="left", padx=2)
        
        # Right section - Search
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.pack(side="right", padx=12)
        
        self.quick_search = ctk.CTkEntry(
            search_frame, placeholder_text="Quick search (Ctrl+P)...",
            width=200, height=32, corner_radius=6,
            fg_color=get_color("bg_input"),
            border_color=get_color("border"),
            text_color=get_color("text"), font=FONT_UI_S,
        )
        self.quick_search.pack(side="left")
        self.quick_search.bind("<Return>", lambda e: self._open_palette())
        
        ctk.CTkButton(toolbar, text="⚙", width=36, height=32,
                     fg_color="transparent", hover_color=get_color("bg_hover"),
                     font=("Segoe UI", 14), command=self._show_settings
                     ).pack(side="right", padx=4)
        
        # ─── MAIN BODY ────────────────────────────────────────────────────
        body = tk.Frame(self, bg=get_color("bg_root"))
        body.pack(fill="both", expand=True)
        
        # ─── LEFT SIDEBAR (Plugins Panel) ────────────────────────────────
        self.left_sidebar = ctk.CTkFrame(body, width=240, corner_radius=0,
                                         fg_color=get_color("bg_sidebar"))
        self.left_sidebar.pack(fill="y", side="left")
        self.left_sidebar.pack_propagate(False)
        
        # Tab selector
        tab_selector = ctk.CTkFrame(self.left_sidebar, height=36, 
                                    corner_radius=0,
                                    fg_color=get_color("bg_panel"))
        tab_selector.pack(fill="x")
        
        self.left_sidebar_tabs = {}
        for icon, tab_name in [("📁", "explorer"), ("🔍", "search"), 
                              ("📦", "plugins"), ("🎯", "debug")]:
            btn = ctk.CTkButton(tab_selector, text=icon, width=40, height=32,
                         fg_color="transparent", 
                         hover_color=get_color("bg_hover"),
                         font=("Segoe UI", 12), corner_radius=0,
                         command=lambda t=tab_name: self._switch_left_panel(t)
                         )
            btn.pack(side="left", padx=2)
            self.left_sidebar_tabs[tab_name] = btn
        
        # Explorer section
        self.explorer_frame = ctk.CTkFrame(self.left_sidebar, corner_radius=0,
                                          fg_color=get_color("bg_sidebar"))
        self.explorer_frame.pack(fill="both", expand=True)
        
        explorer_hdr = ctk.CTkFrame(self.explorer_frame, height=32, 
                                    corner_radius=0,
                                    fg_color=get_color("bg_panel"))
        explorer_hdr.pack(fill="x", pady=(8,0))
        
        ctk.CTkLabel(explorer_hdr, text="EXPLORER", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        ctk.CTkButton(explorer_hdr, text="⊕", width=24, height=24,
                     fg_color="transparent", hover_color=get_color("bg_hover"),
                     text_color=get_color("accent"), font=("Segoe UI", 12),
                     command=self.new_file).pack(side="right", padx=4)
        
        ctk.CTkButton(explorer_hdr, text="🔄", width=24, height=24,
                     fg_color="transparent", hover_color=get_color("bg_hover"),
                     text_color=get_color("accent"), font=("Segoe UI", 12),
                     command=self._refresh_file_tree).pack(side="right", padx=2)
        
        # File tree
        self.file_tree = tk.Listbox(
            self.explorer_frame, bg=get_color("bg_sidebar"),
            fg=get_color("text_muted"), font=FONT_UI_S,
            borderwidth=0, highlightthickness=0,
            selectbackground=get_color("bg_select"),
        )
        self.file_tree.pack(fill="both", expand=True, padx=4, pady=4)
        self.file_tree.bind("<Double-Button-1>", self._tree_double_click)
        self.file_tree.bind("<Button-3>", self._tree_right_click)
        self._refresh_file_tree()
        
        # Search section
        self.search_frame = ctk.CTkFrame(self.left_sidebar, corner_radius=0,
                                        fg_color=get_color("bg_sidebar"))
        self.search_frame.pack(fill="both", expand=True)
        self.search_frame.pack_forget()
        
        search_hdr = ctk.CTkFrame(self.search_frame, height=32, 
                                 corner_radius=0,
                                 fg_color=get_color("bg_panel"))
        search_hdr.pack(fill="x", pady=(8,0))
        
        ctk.CTkLabel(search_hdr, text="SEARCH", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search files...",
                                         height=32, fg_color=get_color("bg_input"),
                                         border_color=get_color("border"))
        self.search_entry.pack(fill="x", padx=4, pady=4)
        self.search_entry.bind("<Return>", lambda e: self._do_search())
        
        self.search_results = tk.Listbox(
            self.search_frame, bg=get_color("bg_sidebar"),
            fg=get_color("text_dim"), font=FONT_UI_S,
            borderwidth=0, highlightthickness=0,
        )
        self.search_results.pack(fill="both", expand=True, padx=4, pady=4)
        self.search_results.bind("<Double-Button-1>", lambda e: self._open_search_result())
        
        # Plugins section
        self.plugins_frame = ctk.CTkFrame(self.left_sidebar, corner_radius=0,
                                         fg_color=get_color("bg_sidebar"))
        self.plugins_frame.pack(fill="both", expand=True)
        self.plugins_frame.pack_forget()
        
        plugins_hdr = ctk.CTkFrame(self.plugins_frame, height=32, 
                                   corner_radius=0,
                                   fg_color=get_color("bg_panel"))
        plugins_hdr.pack(fill="x", pady=(8,0))
        
        ctk.CTkLabel(plugins_hdr, text="PLUGINS", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        ctk.CTkButton(plugins_hdr, text="⊕", width=24, height=24,
                     fg_color="transparent", hover_color=get_color("bg_hover"),
                     text_color=get_color("accent"), font=("Segoe UI", 12),
                     command=self._install_plugin).pack(side="right", padx=4)
        
        self.plugins_list = tk.Listbox(
            self.plugins_frame, bg=get_color("bg_sidebar"),
            fg=get_color("text_dim"), font=FONT_UI_S,
            borderwidth=0, highlightthickness=0,
        )
        self.plugins_list.pack(fill="both", expand=True, padx=4, pady=4)
        self.plugins_list.insert(0, "✓ Syntax Highlighter", "✓ Auto Format", 
                           "✓ Git Integration", "○ Live Share")
        
        # Debug section
        self.debug_frame = ctk.CTkFrame(self.left_sidebar, corner_radius=0,
                                       fg_color=get_color("bg_sidebar"))
        self.debug_frame.pack(fill="both", expand=True)
        self.debug_frame.pack_forget()
        
        debug_hdr = ctk.CTkFrame(self.debug_frame, height=32, 
                                corner_radius=0,
                                fg_color=get_color("bg_panel"))
        debug_hdr.pack(fill="x", pady=(8,0))
        
        ctk.CTkLabel(debug_hdr, text="DEBUGGER", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        self.breakpoints_list = tk.Listbox(
            self.debug_frame, bg=get_color("bg_sidebar"),
            fg=get_color("text_dim"), font=FONT_UI_S,
            borderwidth=0, highlightthickness=0,
        )
        self.breakpoints_list.pack(fill="both", expand=True, padx=4, pady=4)
        self.breakpoints_list.insert(0, "No breakpoints set")
        
        # ─── CENTER EDITOR ────────────────────────────────────────────────
        center = ctk.CTkFrame(body, corner_radius=0,
                             fg_color=get_color("bg_editor"))
        center.pack(fill="both", expand=True, side="left", padx=(4,0))
        
        # Tab bar
        self.tab_bar = ctk.CTkFrame(center, height=36, corner_radius=0,
                                    fg_color=get_color("bg_panel"))
        self.tab_bar.pack(fill="x")
        
        self.tab_btn_frame = ctk.CTkFrame(self.tab_bar, 
                                          fg_color="transparent")
        self.tab_btn_frame.pack(side="left", fill="y", padx=4)
        
        # Find button in tab bar
        ctk.CTkButton(self.tab_bar, text="🔍", width=32, height=32,
                     fg_color="transparent", hover_color=get_color("bg_hover"),
                     font=("Segoe UI", 12), corner_radius=4,
                     command=self._toggle_find_replace).pack(side="right", padx=2)
        
        # Editor container
        editor_container = ctk.CTkFrame(center, corner_radius=0,
                                        fg_color=get_color("bg_editor"))
        editor_container.pack(fill="both", expand=True)
        self.editor_container = editor_container
        
        # Find/Replace panel - initialized when first used
        self.find_panel = None
        self.find_panel_visible = False
        
        # Bottom panel (Console/Terminal)
        self.bottom_panel = ctk.CTkFrame(center, height=200, corner_radius=0,
                                         fg_color=get_color("bg_panel"))
        self.bottom_panel.pack(fill="x", side="bottom")
        self.bottom_panel.pack_propagate(False)
        
        # Console tabs
        console_tabs = ctk.CTkFrame(self.bottom_panel, height=32, 
                                    corner_radius=0,
                                    fg_color=get_color("bg_sidebar"))
        console_tabs.pack(fill="x")
        
        self.console_tabs = {}
        for i, name in enumerate(["Output", "Terminal", "Variables", "Turtle"]):
            btn = ctk.CTkButton(console_tabs, text=name, width=80, height=28,
                         fg_color=get_color("accent") if i==0 else "transparent",
                         hover_color=get_color("bg_hover"),
                         text_color=get_color("text_muted"),
                         font=FONT_UI_S, corner_radius=4,
                         command=lambda n=name: self._switch_console(n)
                         )
            btn.pack(side="left", padx=2, pady=2)
            self.console_tabs[name] = {"btn": btn, "panel": None}
        
        # Output/Console panels
        self.output_text = tk.Text(
            self.bottom_panel, bg=get_color("bg_editor"),
            fg=get_color("text"), font=FONT_CODE_S,
            borderwidth=0, highlightthickness=0,
            state="disabled", wrap="word", padx=12, pady=8,
        )
        self.output_text.pack(fill="both", expand=True)
        self.output_text.tag_configure("log", foreground=get_color("accent2"))
        self.output_text.tag_configure("error", foreground=get_color("error"))
        self.console_tabs["Output"]["panel"] = self.output_text
        
        # Terminal panel
        self.terminal_text = tk.Text(
            self.bottom_panel, bg=get_color("bg_editor"),
            fg=get_color("success"), font=FONT_CODE_S,
            borderwidth=0, highlightthickness=0, wrap="word", padx=12, pady=8,
        )
        self.terminal_text.pack_forget()  # Hidden by default
        self.terminal_text.insert("1.0", "$ Terminal Ready\n>>> ")
        self.console_tabs["Terminal"]["panel"] = self.terminal_text
        
        # Variables panel
        self.variables_text = tk.Text(
            self.bottom_panel, bg=get_color("bg_editor"),
            fg=get_color("accent"), font=FONT_CODE_S,
            borderwidth=0, highlightthickness=0, 
            state="disabled", wrap="word", padx=12, pady=8,
        )
        self.variables_text.pack_forget()
        self.console_tabs["Variables"]["panel"] = self.variables_text
        
        # Turtle panel (Canvas)
        turtle_frame = ctk.CTkFrame(self.bottom_panel, fg_color=get_color("bg_editor"))
        self.turtle_canvas = tk.Canvas(
            turtle_frame, bg=get_color("bg_editor"),
            highlightthickness=0, cursor="crosshair"
        )
        self.turtle_canvas.pack(fill="both", expand=True)
        turtle_frame.pack_forget()
        self.turtle_x, self.turtle_y = 400, 100
        self.turtle_angle = 0
        self.console_tabs["Turtle"]["panel"] = turtle_frame
        self._init_turtle()
        
        # ─── RIGHT PANEL ──────────────────────────────────────────────────
        self.right_panel = ctk.CTkFrame(body, width=260, corner_radius=0,
                                        fg_color=get_color("bg_sidebar"))
        self.right_panel.pack(fill="y", side="right", padx=(4,0))
        self.right_panel.pack_propagate(False)
        
        # Tools tabs
        tools_tabs = ctk.CTkFrame(self.right_panel, height=36, 
                                  corner_radius=0,
                                  fg_color=get_color("bg_panel"))
        tools_tabs.pack(fill="x")
        
        self.right_panel_tabs = {}
        for icon, tab_name in [("📊", "stats"), ("🐛", "debug"), ("📝", "outline"), ("⚡", "performance")]:
            btn = ctk.CTkButton(tools_tabs, text=icon, width=40, height=32,
                         fg_color="transparent", 
                         hover_color=get_color("bg_hover"),
                         font=("Segoe UI", 12), corner_radius=0,
                         command=lambda t=tab_name: self._switch_right_panel(t)
                         )
            btn.pack(side="left", padx=2)
            self.right_panel_tabs[tab_name] = btn
        
        # Variables section
        self.stats_frame = ctk.CTkFrame(self.right_panel, corner_radius=0,
                                       fg_color=get_color("bg_sidebar"))
        self.stats_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        vars_hdr = ctk.CTkFrame(self.stats_frame, height=32, 
                               corner_radius=0,
                               fg_color=get_color("bg_panel"))
        vars_hdr.pack(fill="x", pady=(4,0))
        
        ctk.CTkLabel(vars_hdr, text="VARIABLES", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        self.vars_text = tk.Text(
            self.stats_frame, bg=get_color("bg_editor"),
            fg=get_color("text_muted"), font=FONT_CODE_S,
            borderwidth=0, highlightthickness=0,
            state="disabled", wrap="word", padx=8, pady=8,
        )
        self.vars_text.pack(fill="x", padx=4, pady=4)
        
        # RAM Monitor
        if HAS_PSUTIL:
            ram_hdr = ctk.CTkFrame(self.stats_frame, height=32, 
                                  corner_radius=0,
                                  fg_color=get_color("bg_panel"))
            ram_hdr.pack(fill="x", pady=(8,0))
            
            ctk.CTkLabel(ram_hdr, text="MEMORY", 
                        font=("Segoe UI", 8, "bold"),
                        text_color=get_color("text_muted")).pack(side="left", padx=12)
            
            self.ram_canvas = tk.Canvas(
                self.stats_frame, bg=get_color("bg_editor"),
                highlightthickness=0, height=80, cursor="arrow",
            )
            self.ram_canvas.pack(fill="x", padx=4, pady=4)
            self._update_ram()
        
        # Debug frame
        self.debug_panel_frame = ctk.CTkFrame(self.right_panel, corner_radius=0,
                                             fg_color=get_color("bg_sidebar"))
        self.debug_panel_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.debug_panel_frame.pack_forget()
        
        debug_hdr = ctk.CTkFrame(self.debug_panel_frame, height=32, 
                                corner_radius=0,
                                fg_color=get_color("bg_panel"))
        debug_hdr.pack(fill="x", pady=(4,0))
        
        ctk.CTkLabel(debug_hdr, text="BREAKPOINTS", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        self.debug_list = tk.Listbox(
            self.debug_panel_frame, bg=get_color("bg_editor"),
            fg=get_color("text_dim"), font=FONT_UI_S,
            borderwidth=0, highlightthickness=0,
        )
        self.debug_list.pack(fill="both", expand=True, padx=4, pady=4)
        self.debug_list.insert(0, "No breakpoints set")
        
        # Outline frame
        self.outline_frame = ctk.CTkFrame(self.right_panel, corner_radius=0,
                                         fg_color=get_color("bg_sidebar"))
        self.outline_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.outline_frame.pack_forget()
        
        outline_hdr = ctk.CTkFrame(self.outline_frame, height=32, 
                                   corner_radius=0,
                                   fg_color=get_color("bg_panel"))
        outline_hdr.pack(fill="x", pady=(4,0))
        
        ctk.CTkLabel(outline_hdr, text="OUTLINE", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        self.outline_tree = tk.Listbox(
            self.outline_frame, bg=get_color("bg_editor"),
            fg=get_color("text_dim"), font=FONT_UI_S,
            borderwidth=0, highlightthickness=0,
        )
        self.outline_tree.pack(fill="both", expand=True, padx=4, pady=4)
        self.outline_tree.insert(0, "📌 class Program", "  📌 func main()")
        
        # Performance frame
        self.perf_frame = ctk.CTkFrame(self.right_panel, corner_radius=0,
                                      fg_color=get_color("bg_sidebar"))
        self.perf_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.perf_frame.pack_forget()
        
        perf_hdr = ctk.CTkFrame(self.perf_frame, height=32, 
                               corner_radius=0,
                               fg_color=get_color("bg_panel"))
        perf_hdr.pack(fill="x", pady=(4,0))
        
        ctk.CTkLabel(perf_hdr, text="PERFORMANCE & MEMORY", 
                    font=("Segoe UI", 8, "bold"),
                    text_color=get_color("text_muted")).pack(side="left", padx=12)
        
        # Memory graph canvas
        self.perf_canvas = tk.Canvas(
            self.perf_frame, bg=get_color("bg_editor"), 
            borderwidth=0, highlightthickness=0, height=120
        )
        self.perf_canvas.pack(fill="x", padx=4, pady=(4,0))
        
        # Stats text
        self.perf_text = tk.Text(
            self.perf_frame, bg=get_color("bg_editor"),
            fg=get_color("text_dim"), font=FONT_CODE_S,
            borderwidth=0, highlightthickness=0,
            state="disabled", wrap="word", padx=8, pady=8,
        )
        self.perf_text.pack(fill="both", expand=True, padx=4, pady=4)
        
        # ─── STATUS BAR ───────────────────────────────────────────────────
        self.status_bar = ctk.CTkFrame(self, height=24, corner_radius=0,
                             fg_color=get_color("accent_dark"))
        self.status_bar.pack(fill="x", side="bottom")
        
        self.status_left = ctk.CTkLabel(self.status_bar, text="✓ Ready", 
                                        font=FONT_UI_S,
                                        text_color="#ccc")
        self.status_left.pack(side="left", padx=12)
        
        self.status_center = ctk.CTkLabel(self.status_bar, text="Normal Mode", 
                                         font=FONT_UI_S,
                                         text_color=get_color("text_muted"))
        self.status_center.pack(side="left", padx=12)
        
        self.status_right = ctk.CTkLabel(self.status_bar, 
                                         text=f"Theme: {THEMES[CURRENT_THEME]['name']}", 
                                         font=FONT_UI_S,
                                         text_color=get_color("text_muted"))
        self.status_right.pack(side="right", padx=12)
    
    def _update_ram(self):
        if not HAS_PSUTIL: return
        try:
            process = psutil.Process()
            percent = process.memory_percent()
            mem_mb = process.memory_info().rss / (1024*1024)
            
            w = self.ram_canvas.winfo_width()
            h = 80
            
            self.ram_canvas.delete("all")
            
            # Bar
            bar_h = 20
            bar_y = 30
            self.ram_canvas.create_rectangle(10, bar_y, w-10, bar_y+bar_h,
                                            outline=get_color("border"))
            
            color = (get_color("success") if percent < 50 else
                    get_color("warn") if percent < 80 else
                    get_color("error"))
            
            self.ram_canvas.create_rectangle(
                10, bar_y, 10 + ((w-20) * percent / 100), bar_y+bar_h,
                fill=color, outline=""
            )
            
            # Text
            self.ram_canvas.create_text(w/2, 15, 
                                        text=f"Memory: {percent:.1f}% ({mem_mb:.0f} MB)",
                                        fill=get_color("text_muted"), 
                                        font=FONT_UI_S)
        except: pass
        
        self.after(2000, self._update_ram)
    
    def _draw_memory_graph(self):
        """Draw memory usage graph in performance panel"""
        if not hasattr(self, 'perf_canvas') or not self.memory_monitor.history:
            return
        
        try:
            w = self.perf_canvas.winfo_width()
            h = self.perf_canvas.winfo_height()
            if w < 50 or h < 50:
                w, h = 400, 120
            
            self.perf_canvas.delete("all")
            
            history = self.memory_monitor.history
            if len(history) < 2:
                self._update_perf_text()
                return
            
            # Setup
            margin_l, margin_r = 30, 10
            margin_t, margin_b = 10, 25
            graph_w = w - margin_l - margin_r
            graph_h = h - margin_t - margin_b
            
            # Get data
            code_vals = [h[2] for h in history]  # Code memory
            total_vals = [h[3] for h in history]  # Total memory
            
            max_val = max(max(code_vals), max(total_vals)) if code_vals and total_vals else 1
            if max_val == 0: max_val = 1
            
            # Draw background
            self.perf_canvas.create_rectangle(
                margin_l, margin_t, w - margin_r, h - margin_b,
                outline=get_color("border"), fill=get_color("bg_editor"), width=1
            )
            
            # Draw grid
            for i in range(5):
                y = margin_t + (i * graph_h / 4)
                val = max_val * (1 - i/4)
                self.perf_canvas.create_line(margin_l, y, w - margin_r, y,
                                            fill=get_color("text_dim"), dash=(2,2), width=1)
                self.perf_canvas.create_text(margin_l - 5, y,
                                            text=f"{val:.0f}M",
                                            fill=get_color("text_muted"), anchor="e",
                                            font=FONT_UI_S)
            
            # Draw lines for total and code memory
            points_total = []
            points_code = []
            
            for idx, (_, _, code_mb, total_mb) in enumerate(history):
                x = margin_l + (idx / max(1, len(history)-1)) * graph_w
                y_code = margin_t + graph_h - (code_mb / max_val) * graph_h
                y_total = margin_t + graph_h - (total_mb / max_val) * graph_h
                
                points_code.append((x, y_code))
                points_total.append((x, y_total))
            
            # Draw lines
            if len(points_total) > 1:
                self.perf_canvas.create_line(*[coord for p in points_total for coord in p],
                                            fill=get_color("warn"), width=2, smooth=True)
            
            if len(points_code) > 1:
                self.perf_canvas.create_line(*[coord for p in points_code for coord in p],
                                            fill=get_color("success"), width=2, smooth=True)
            
            # Draw legend
            self.perf_canvas.create_rectangle(w - 140, margin_t, w - margin_r, margin_t + 40,
                                             fill=get_color("bg_sidebar"), outline=get_color("border"))
            self.perf_canvas.create_line(w - 130, margin_t + 10, w - 110, margin_t + 10,
                                        fill=get_color("warn"), width=2)
            self.perf_canvas.create_text(w - 100, margin_t + 10,
                                        text="Total", fill=get_color("text"),
                                        anchor="w", font=FONT_UI_S)
            
            self.perf_canvas.create_line(w - 130, margin_t + 25, w - 110, margin_t + 25,
                                        fill=get_color("success"), width=2)
            self.perf_canvas.create_text(w - 100, margin_t + 25,
                                        text="Code", fill=get_color("text"),
                                        anchor="w", font=FONT_UI_S)
            
            # X-axis label
            self.perf_canvas.create_text(w/2, h - 5,
                                        text="Time (samples)", fill=get_color("text_muted"),
                                        font=FONT_UI_S)
            
            self._update_perf_text()
        except:
            self._update_perf_text()
    
    def _update_perf_text(self):
        """Update performance statistics text"""
        if not hasattr(self, 'perf_text'):
            return
        
        self.perf_text.configure(state="normal")
        self.perf_text.delete("1.0", "end")
        
        stats = self.memory_monitor.get_stats()
        if not stats:
            self.perf_text.insert("end", "No execution data yet.\nRun code to see statistics.")
        else:
            text_content = f"""╔═══════════════════════════════╗
║      MEMORY STATISTICS        ║
╚═══════════════════════════════╝

📊 Code Memory (Execution)
  Peak:    {stats['peak_code_mb']:>8.2f} MB
  Average: {stats['avg_code_mb']:>8.2f} MB
  Samples: {stats['samples']:>8} samples

📊 Total Memory (IDE + Code)
  Peak:    {stats['peak_total_mb']:>8.2f} MB

⚙️  Memory Management
  Manual Allocations: {stats['manual_allocs']}
  Auto Management:    {'YES' if stats['has_auto_mgmt'] else 'NO'}
"""
            if stats['memory_params']:
                text_content += "\n  Active Parameters:\n"
                for param in stats['memory_params']:
                    text_content += f"    • {param}\n"
        
            self.perf_text.insert("end", text_content)
        
        self.perf_text.configure(state="disabled")
    
    
    def new_file(self):
        """Create new editor tab"""
        idx = len(self.tabs)
        
        # Create editor frame
        editor_frame = ctk.CTkFrame(self.editor_container, corner_radius=0,
                                    fg_color=get_color("bg_editor"))
        
        # Editor with line numbers
        text_container = tk.Frame(editor_frame, bg=get_color("bg_editor"))
        text_container.pack(fill="both", expand=True)
        
        text = tk.Text(
            text_container, bg=get_color("bg_editor"),
            fg=get_color("text"), font=FONT_CODE,
            insertbackground=get_color("cursor"),
            selectbackground=get_color("selection"),
            borderwidth=0, highlightthickness=0,
            wrap="none", padx=12, pady=8,
            undo=True, tabs=("28",),
        )
        
        line_nums = LineNumbers(text_container, text)
        line_nums.pack(side="left", fill="y")
        
        scroll_y = ctk.CTkScrollbar(text_container, orientation="vertical",
                                    command=text.yview,
                                    button_color=get_color("accent"))
        scroll_y.pack(side="right", fill="y")
        text.configure(yscrollcommand=scroll_y.set)
        
        text.pack(side="left", fill="both", expand=True)
        
        # Syntax highlighter
        highlighter = SyntaxHighlighter(text)
        
        # Autocomplete
        ac = AutoComplete(self, lambda s: self._insert_completion(text, s))
        
        # Bindings
        text.bind("<KeyRelease>", lambda e: self._on_key_release(text, highlighter, line_nums, e))
        text.bind("<Control-space>", lambda e: self._trigger_ac(text, ac))
        text.bind("<Return>", lambda e: self._on_enter(text))
        text.bind("<Tab>", lambda e: self._on_tab(text))
        
        # Tab info
        tab_info = {
            "frame": editor_frame,
            "text": text,
            "line_nums": line_nums,
            "highlighter": highlighter,
            "ac": ac,
            "file_path": None,
            "modified": False,
        }
        self.tabs.append(tab_info)
        
        # Tab button with close
        tab_frame = ctk.CTkFrame(self.tab_btn_frame, fg_color="transparent", height=32)
        tab_frame.pack(side="left", padx=2, pady=2)
        
        tab_btn = ctk.CTkButton(
            tab_frame, text=f"untitled{idx+1}.rint",
            width=100, height=32,
            fg_color=get_color("bg_tab_active"),
            hover_color=get_color("bg_hover"),
            text_color=get_color("accent"), font=FONT_UI_S,
            corner_radius=6,
            command=lambda i=idx: self._select_tab(i),
        )
        tab_btn.pack(side="left")
        
        close_btn = ctk.CTkButton(
            tab_frame, text="✕", width=24, height=32,
            fg_color="transparent", hover_color=get_color("bg_hover"),
            text_color=get_color("text_muted"), font=("Segoe UI", 10),
            corner_radius=4,
            command=lambda i=idx: self._close_tab(i),
        )
        close_btn.pack(side="left", padx=(2,0))
        tab_info["btn"] = tab_btn
        tab_info["close_btn"] = close_btn
        tab_info["tab_frame"] = tab_frame
        
        # Insert starter code
        text.insert("1.0", "// RINT IDE v3.5\n\nconsole.print(\"Hello, World!\")\n")
        highlighter.highlight()
        line_nums.redraw()
        
        self._select_tab(idx)
    
    def _select_tab(self, idx):
        """Select a tab"""
        if idx < 0 or idx >= len(self.tabs): return
        
        # Hide all
        for t in self.tabs:
            t["frame"].pack_forget()
            t["btn"].configure(fg_color=get_color("bg_tab_idle"),
                              text_color=get_color("text_muted"))
        
        # Show selected
        self.active_tab = idx
        self.tabs[idx]["frame"].pack(fill="both", expand=True)
        self.tabs[idx]["btn"].configure(fg_color=get_color("bg_tab_active"),
                                       text_color=get_color("accent"))
    
    def _on_key_release(self, text, highlighter, line_nums, event):
        highlighter.highlight()
        line_nums.redraw()
    
    def _on_enter(self, text):
        line = text.get("insert linestart", "insert")
        indent = len(line) - len(line.lstrip())
        if line.rstrip().endswith("{"):
            indent += 4
        text.insert("insert", "\n" + " " * indent)
        return "break"
    
    def _on_tab(self, text):
        text.insert("insert", "    ")
        return "break"
    
    def _trigger_ac(self, text, ac):
        word = self._current_word(text)
        if not word: return "break"
        sugg = [c for c in ALL_COMPLETIONS if c.startswith(word)]
        if sugg:
            bbox = text.bbox("insert")
            if bbox:
                x = text.winfo_rootx() + bbox[0]
                y = text.winfo_rooty() + bbox[1] + bbox[3]
                ac.show(x, y, sugg)
        return "break"
    
    def _current_word(self, text):
        pos = text.index("insert")
        line = text.get(f"{pos} linestart", pos)
        m = re.search(r'[\w.]+$', line)
        return m.group() if m else ""
    
    def _insert_completion(self, text, item):
        word = self._current_word(text)
        tail = item[len(word):] if item.startswith(word) else item
        text.insert("insert", tail)
    
    # ─── ACTIONS ──────────────────────────────────────────────────────────
    
    def _run_code(self):
        """Run current code"""
        if self.active_tab < 0: return
        code = self.tabs[self.active_tab]["text"].get("1.0", "end-1c")
        
        # Detect memory management in code
        self.memory_monitor.detect_memory_params(code)
        
        # Auto-detect VM mode
        self._detect_vm_mode()
        
        # Update status bar color
        if self.vm_mode:
            self.status_bar.configure(fg_color="#c84b31")  # Orange/Red for VM
            self.status_center.configure(text="Mode VM isolé")
            self._add_output("⚙ Exécution en mode VM isolé")
        else:
            self.status_bar.configure(fg_color=get_color("accent_dark"))  # Normal
            self.status_center.configure(text="Mode normal")
        
        self.status_left.configure(text="▶ Running...")
        self._add_output("=" * 50)
        exec_info = f"Execution started ({('VM isolé' if self.vm_mode else 'Normal')})"
        
        # Add memory management info if detected
        if self.memory_monitor.memory_auto_mgmt:
            mem_info = ", ".join(self.memory_monitor.memory_params.keys())
            self._add_output(f"Memory Management: {mem_info} ({self.memory_monitor.manual_allocs} allocs)")
            exec_info += " [Memory Managed]"
        
        self._add_output(exec_info)
        self._add_output("=" * 50)
        
        # Clear variables display
        self.variables_text.configure(state="normal")
        self.variables_text.delete("1.0", "end")
        self.variables_text.configure(state="disabled")
        
        # Clear turtle
        self._init_turtle()
        
        # Start memory monitoring
        self.memory_monitor.start_monitoring()
        
        def run_thread():
            # Monitor memory while code runs
            start_time = time.time()
            monitoring = True
            
            def sample_monitor():
                """Background thread to sample memory every 100ms"""
                while monitoring and (time.time() - start_time) < 60:  # Max 60s
                    try:
                        self.memory_monitor.sample_memory()
                        time.sleep(0.1)  # Sample every 100ms
                    except:
                        pass
            
            # Start memory sampling in background
            sample_thread = threading.Thread(target=sample_monitor, daemon=True)
            sample_thread.start()
            
            try:
                self.interpreter.run(code)
            except:
                pass
            finally:
                monitoring = False
            
            # Final sample
            self.memory_monitor.sample_memory()
            
            # Collect final stats
            stats = self.memory_monitor.get_stats()
            if stats:
                duration = time.time() - start_time
                self._ui_call(self._add_output, f"\n{'─'*50}")
                self._ui_call(self._add_output, f"📊 MEMORY REPORT")
                self._ui_call(self._add_output, f"{'─'*50}")
                self._ui_call(self._add_output, 
                    f"Code Peak:  {stats['peak_code_mb']:>8.2f} MB  |  "
                    f"Avg: {stats['avg_code_mb']:>8.2f} MB")
                self._ui_call(self._add_output, 
                    f"Total Peak: {stats['peak_total_mb']:>8.2f} MB  |  "
                    f"Samples: {stats['samples']:>3} | Time: {duration:.2f}s")
                
                if self.memory_monitor.memory_auto_mgmt:
                    params_str = ", ".join(self.memory_monitor.memory_params.keys())
                    self._ui_call(self._add_output,
                        f"⚙️  Managed Memory Detected: {params_str}")
                    self._ui_call(self._add_output,
                        f"    Manual Allocations: {stats['manual_allocs']}")
                else:
                    self._ui_call(self._add_output, "⚙️  No manual memory management detected")
            
            self._ui_call(self.status_left.configure, text="✓ Ready")
            self._ui_call(self._switch_console, "Output")
            
            # Refresh memory graph
            self._ui_call(self._draw_memory_graph)
        
        self.monitoring_thread = threading.Thread(target=run_thread, daemon=True)
        self.monitoring_thread.start()
    
    def _stop_code(self):
        """Stop execution"""
        self.interpreter.running = False
        self.status_left.configure(text="⏹ Stopped")
    
    def _save_file(self):
        """Save current file"""
        if self.active_tab < 0: return
        tab = self.tabs[self.active_tab]
        path = tab["file_path"]
        
        if not path:
            path = filedialog.asksaveasfilename(
                defaultextension=".rint",
                filetypes=[("RINT files", "*.rint"), ("All", "*.*")]
            )
        
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(tab["text"].get("1.0", "end-1c"))
            tab["file_path"] = path
            tab["btn"].configure(text=Path(path).name)
            self.status_left.configure(text=f"💾 Saved: {Path(path).name}")
    
    def _open_file(self):
        """Open file"""
        path = filedialog.askopenfilename(
            filetypes=[("RINT files", "*.rint"), ("All", "*.*")]
        )
        if not path: return
        
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        
        self.new_file()
        tab = self.tabs[self.active_tab]
        tab["text"].delete("1.0", "end")
        tab["text"].insert("1.0", code)
        tab["file_path"] = path
        tab["btn"].configure(text=Path(path).name)
        tab["highlighter"].highlight()
    
    def _spotlight_search(self):
        """Open spotlight search"""
        messagebox.showinfo("Spotlight", "Search across workspace\n(Feature coming soon)")
    
    def _open_palette(self):
        """Open command palette"""
        CommandPalette(self, self)
    
    def _switch_console(self, name):
        """Switch between console panels"""
        # Hide all
        for panel in self.console_tabs.values():
            if panel["panel"]:
                if isinstance(panel["panel"], tk.Text):
                    panel["panel"].pack_forget()
                else:
                    panel["panel"].pack_forget()
        
        # Show selected
        panel = self.console_tabs[name]["panel"]
        if panel:
            if isinstance(panel, tk.Text):
                panel.pack(fill="both", expand=True)
            else:
                panel.pack(fill="both", expand=True)
        
        # Update buttons
        for btn_name, data in self.console_tabs.items():
            color = get_color("accent") if btn_name == name else "transparent"
            data["btn"].configure(fg_color=color)
    
    def _add_output(self, msg):
        """Add message to output panel"""
        self.output_text.configure(state="normal")
        self.output_text.insert("end", msg + "\n", "log")
        self.output_text.configure(state="disabled")
        self.output_text.see("end")
    
    def _add_log(self, msg):
        """Add log message"""
        self._add_output(f"[LOG] {msg}")
    
    def _add_error(self, msg):
        """Add error message"""
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"[ERROR] {msg}\n", "error")
        self.output_text.configure(state="disabled")
        self.output_text.see("end")
    
    def _add_variable(self, name, value, type_=""):
        """Add variable to Variables panel"""
        self.variables_text.configure(state="normal")
        if type_:
            self.variables_text.insert("end", f"📍 {name}: {type_}\n   = {value}\n")
        else:
            self.variables_text.insert("end", f"📍 {name} = {value}\n")
        self.variables_text.configure(state="disabled")
        self.variables_text.see("end")
    
    def update_variables(self, variables_dict):
        """Update all variables in the panel"""
        self.variables_text.configure(state="normal")
        self.variables_text.delete("1.0", "end")
        for name, (value, type_) in variables_dict.items():
            self.variables_text.insert("end", f"📍 {name}: {type_}\n   = {repr(value)}\n\n")
        self.variables_text.configure(state="disabled")
    
    def _init_turtle(self):
        """Initialize turtle canvas"""
        try:
            self.turtle_canvas.delete("all")
            w = self.turtle_canvas.winfo_width() or 800
            h = self.turtle_canvas.winfo_height() or 150
            if w <= 1: w = 800
            if h <= 1: h = 150
            # Background
            self.turtle_canvas.create_rectangle(0, 0, w, h, fill=get_color("bg_editor"), outline=get_color("border"), width=1)
            # Grid
            self.turtle_canvas.create_line(0, h//2, w, h//2, fill=get_color("line_num"), dash=(4,4), width=1)
            self.turtle_canvas.create_line(w//2, 0, w//2, h, fill=get_color("line_num"), dash=(4,4), width=1)
            # Center marker
            self.turtle_canvas.create_oval(w//2-3, h//2-3, w//2+3, h//2+3, fill=get_color("accent_dark"), outline="")
            # Reset turtle position to center
            self.turtle_x = w//2
            self.turtle_y = h//2
            self.turtle_angle = 0
            self._draw_turtle()
        except Exception as e:
            print(f"Turtle init error: {e}")
    
    def _draw_turtle(self, x=None, y=None, angle=None):
        """Draw turtle at position"""
        if x is not None: self.turtle_x = x
        if y is not None: self.turtle_y = y
        if angle is not None: self.turtle_angle = angle
        
        try:
            self.turtle_canvas.delete("turtle")
            import math
            size = 15
            angle_rad = math.radians(self.turtle_angle)
            x1 = self.turtle_x + size * math.cos(angle_rad)
            y1 = self.turtle_y + size * math.sin(angle_rad)
            x2 = self.turtle_x + size * math.cos(angle_rad + 2.4)
            y2 = self.turtle_y + size * math.sin(angle_rad + 2.4)
            x3 = self.turtle_x + size * math.cos(angle_rad - 2.4)
            y3 = self.turtle_y + size * math.sin(angle_rad - 2.4)
            self.turtle_canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=get_color("accent"), tags="turtle")
            self.turtle_canvas.create_oval(self.turtle_x-5, self.turtle_y-5, self.turtle_x+5, self.turtle_y+5, fill=get_color("accent2"), tags="turtle")
        except: pass
    
    def _show_settings(self):
        """Show settings dialog"""
        settings = tk.Toplevel(self)
        settings.title("Settings")
        settings.geometry("500x400")
        settings.configure(bg=get_color("bg_panel"))
        
        ctk.CTkLabel(settings, text="⚙ Settings", font=FONT_TITLE,
                    text_color=get_color("text")).pack(pady=20)
        
        # Theme selector
        theme_frame = ctk.CTkFrame(settings, fg_color=get_color("bg_sidebar"))
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(theme_frame, text="Theme:", font=FONT_UI,
                    text_color=get_color("text_muted")).pack(side="left", padx=10)
        
        for theme_key in THEMES.keys():
            ctk.CTkButton(
                theme_frame, text=THEMES[theme_key]["name"],
                width=100, height=28,
                fg_color=get_color("accent") if theme_key == CURRENT_THEME else get_color("bg_input"),
                command=lambda t=theme_key: self._change_theme(t)
            ).pack(side="left", padx=4, pady=8)
    
    def _change_theme(self, theme_key):
        """Change IDE theme in real-time"""
        global CURRENT_THEME
        CURRENT_THEME = theme_key
        self._apply_theme()
        self.status_left.configure(text=f"✓ Theme: {THEMES[theme_key]['name']}")
    
    def _apply_theme(self):
        """Apply theme to ALL UI elements comprehensively"""
        try:
            # Main window
            self.configure(fg_color=get_color("bg_root"))
            
            # Panels
            if hasattr(self, 'left_sidebar'):
                self.left_sidebar.configure(fg_color=get_color("bg_sidebar"))
            if hasattr(self, 'explorer_frame'):
                self.explorer_frame.configure(fg_color=get_color("bg_sidebar"))
            if hasattr(self, 'search_frame'):
                self.search_frame.configure(fg_color=get_color("bg_sidebar"))
            if hasattr(self, 'plugins_frame'):
                self.plugins_frame.configure(fg_color=get_color("bg_sidebar"))
            if hasattr(self, 'debug_frame'):
                self.debug_frame.configure(fg_color=get_color("bg_sidebar"))
            
            if hasattr(self, 'tab_bar'):
                self.tab_bar.configure(fg_color=get_color("bg_panel"))
            if hasattr(self, 'bottom_panel'):
                self.bottom_panel.configure(fg_color=get_color("bg_panel"))
            if hasattr(self, 'right_panel'):
                self.right_panel.configure(fg_color=get_color("bg_sidebar"))
            
            if hasattr(self, 'stats_frame'):
                self.stats_frame.configure(fg_color=get_color("bg_sidebar"))
            if hasattr(self, 'debug_panel_frame'):
                self.debug_panel_frame.configure(fg_color=get_color("bg_sidebar"))
            if hasattr(self, 'outline_frame'):
                self.outline_frame.configure(fg_color=get_color("bg_sidebar"))
            if hasattr(self, 'perf_frame'):
                self.perf_frame.configure(fg_color=get_color("bg_sidebar"))
            
            if hasattr(self, 'editor_container'):
                self.editor_container.configure(fg_color=get_color("bg_editor"))
            
            # Status bar
            if hasattr(self, 'status_bar'):
                status_color = "#c84b31" if self.vm_mode else get_color("accent_dark")
                self.status_bar.configure(fg_color=status_color)
            if hasattr(self, 'status_left'):
                self.status_left.configure(text_color="#ccc")
            if hasattr(self, 'status_center'):
                self.status_center.configure(text_color=get_color("text_muted"))
            
            # Text widgets
            if hasattr(self, 'output_text'):
                self.output_text.configure(bg=get_color("bg_editor"), fg=get_color("text"))
                self.output_text.tag_configure("log", foreground=get_color("accent2"))
                self.output_text.tag_configure("error", foreground=get_color("error"))
            if hasattr(self, 'terminal_text'):
                self.terminal_text.configure(bg=get_color("bg_editor"), fg=get_color("success"))
            if hasattr(self, 'variables_text'):
                self.variables_text.configure(bg=get_color("bg_editor"), fg=get_color("accent"))
            if hasattr(self, 'vars_text'):
                self.vars_text.configure(bg=get_color("bg_editor"), fg=get_color("accent"))
            if hasattr(self, 'perf_text'):
                self.perf_text.configure(bg=get_color("bg_editor"), fg=get_color("text_dim"))
            
            # Canvas widgets
            if hasattr(self, 'turtle_canvas'):
                self.turtle_canvas.configure(bg=get_color("bg_editor"))
            if hasattr(self, 'ram_canvas'):
                self.ram_canvas.configure(bg=get_color("bg_editor"))
            if hasattr(self, 'perf_canvas'):
                self.perf_canvas.configure(bg=get_color("bg_editor"))
            
            # Listbox widgets
            if hasattr(self, 'file_tree'):
                self.file_tree.configure(bg=get_color("bg_sidebar"), fg=get_color("text_muted"), selectbackground=get_color("bg_select"))
            if hasattr(self, 'search_results'):
                self.search_results.configure(bg=get_color("bg_editor"), fg=get_color("text_dim"))
            if hasattr(self, 'plugins_list'):
                self.plugins_list.configure(bg=get_color("bg_editor"), fg=get_color("text_dim"))
            if hasattr(self, 'breakpoints_list'):
                self.breakpoints_list.configure(bg=get_color("bg_editor"), fg=get_color("text_dim"))
            if hasattr(self, 'debug_list'):
                self.debug_list.configure(bg=get_color("bg_editor"), fg=get_color("text_dim"))
            if hasattr(self, 'outline_tree'):
                self.outline_tree.configure(bg=get_color("bg_editor"), fg=get_color("text_dim"))
            
            # All tabs
            for tab in self.tabs:
                tab["text"].configure(bg=get_color("bg_editor"), fg=get_color("text"), 
                                    insertbackground=get_color("cursor"), 
                                    selectbackground=get_color("selection"))
                tab["btn"].configure(fg_color=get_color("bg_tab_active"),
                                   text_color=get_color("accent"))
                if "close_btn" in tab:
                    tab["close_btn"].configure(text_color=get_color("text_muted"))
                tab["highlighter"]._configure_tags()
                tab["highlighter"].highlight()
                if "line_nums" in tab:
                    tab["line_nums"].redraw()
            
            # Redraw graphics
            self._init_turtle()
            self._update_ram()
            self._draw_memory_graph()
            
            # Status text
            if hasattr(self, 'status_right'):
                self.status_right.configure(text=f"Theme: {THEMES[CURRENT_THEME]['name']}")
            
            # Update menu bar colors
            if hasattr(self, 'menubar'):
                self.menubar.configure(bg=get_color("bg_sidebar"), 
                                      fg=get_color("text"),
                                      activebackground=get_color("bg_hover"),
                                      activeforeground=get_color("accent"))
        except Exception as e:
            print(f"Theme error: {e}")
    
    def _toggle_sidebar(self):
        """Toggle left sidebar"""
        if self.sidebar_visible:
            self.left_sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.left_sidebar.pack(fill="y", side="left", before=self.editor_container.master)
            self.sidebar_visible = True
    
    def _toggle_find_replace(self):
        """Toggle Find & Replace panel"""
        if self.active_tab < 0: return
        
        if self.find_panel is None:
            # Create find panel with current editor
            self.find_panel = FindReplacePanel(self.editor_container, self.tabs[self.active_tab]["text"])
            self.find_panel.pack(fill="x", side="top")
            self.find_panel_visible = True
            self.find_panel.find_entry.focus()
        elif self.find_panel_visible:
            self.find_panel.pack_forget()
            self.find_panel_visible = False
        else:
            self.find_panel.editor = self.tabs[self.active_tab]["text"]
            self.find_panel.pack(fill="x", side="top")
            self.find_panel_visible = True
            self.find_panel.find_entry.focus()
    
    def _tree_double_click(self, event):
        """Handle file tree double click"""
        sel = self.file_tree.curselection()
        if not sel: return
        item = self.file_tree.get(sel[0])
        if item.startswith("📄"):
            # Open file
            filename = item[2:].strip()
            path = filedialog.askopenfilename(initialfile=filename,
                filetypes=[("RINT files", "*.rint"), ("All", "*.*")])
            if path:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
                self.new_file()
                tab = self.tabs[self.active_tab]
                tab["text"].delete("1.0", "end")
                tab["text"].insert("1.0", code)
                tab["file_path"] = path
                tab["btn"].configure(text=Path(path).name)
                tab["highlighter"].highlight()
    
    def _tree_right_click(self, event):
        """Handle file tree right click"""
        sel = self.file_tree.curselection()
        if not sel: return
        item = self.file_tree.get(sel[0])
        menu = tk.Menu(self.file_tree, tearoff=0, bg=get_color("bg_panel"))
        menu.add_command(label="Open", command=self._tree_double_click)
        menu.add_command(label="Delete", command=lambda: self._delete_file(item))
        menu.add_command(label="Rename", command=lambda: self._rename_file(item))
        menu.post(event.x_root, event.y_root)
    
    def _delete_file(self, item):
        """Delete file from explorer"""
        messagebox.showinfo("Delete", f"Delete: {item}")
    
    def _rename_file(self, item):
        """Rename file"""
        messagebox.showinfo("Rename", f"Rename: {item}")
    
    def _refresh_file_tree(self):
        """Refresh file tree from current directory"""
        self.file_tree.delete(0, "end")
        try:
            cwd = Path.cwd()
            # Add project files
            for file in cwd.glob("*.rint"):
                self.file_tree.insert("end", f"📄 {file.name}")
            for folder in cwd.glob("*/"):
                if not folder.name.startswith("."):
                    self.file_tree.insert("end", f"📂 {folder.name}/")
        except:
            self.file_tree.insert("end", "📄 main.rint", "📂 lib/", "📂 data/")
    
    def _switch_left_panel(self, panel_name):
        """Switch left sidebar panels"""
        # Hide all
        self.explorer_frame.pack_forget()
        self.search_frame.pack_forget()
        self.plugins_frame.pack_forget()
        self.debug_frame.pack_forget()
        
        # Show selected
        if panel_name == "explorer":
            self.explorer_frame.pack(fill="both", expand=True)
        elif panel_name == "search":
            self.search_frame.pack(fill="both", expand=True)
        elif panel_name == "plugins":
            self.plugins_frame.pack(fill="both", expand=True)
        elif panel_name == "debug":
            self.debug_frame.pack(fill="both", expand=True)
        
        # Update button colors
        for name, btn in self.left_sidebar_tabs.items():
            color = get_color("accent") if name == panel_name else "transparent"
            btn.configure(fg_color=color)
    
    def _do_search(self):
        """Search in files"""
        query = self.search_entry.get()
        if not query: return
        
        self.search_results.delete(0, "end")
        try:
            cwd = Path.cwd()
            for file in cwd.rglob("*.rint"):
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, 1):
                            if query.lower() in line.lower():
                                self.search_results.insert("end", f"{file.name}:{i}: {line.strip()[:50]}")
                except:
                    pass
        except:
            self.search_results.insert("end", "No results found")
    
    def _open_search_result(self):
        """Open file from search results"""
        sel = self.search_results.curselection()
        if not sel: return
        item = self.search_results.get(sel[0])
        messagebox.showinfo("Open", f"Opening: {item}")
    
    def _install_plugin(self):
        """Install plugin"""
        messagebox.showinfo("Plugins", "Plugin marketplace coming soon!")
    
    def _switch_right_panel(self, panel_name):
        """Switch right sidebar panels"""
        # Hide all
        self.stats_frame.pack_forget()
        self.debug_panel_frame.pack_forget()
        self.outline_frame.pack_forget()
        self.perf_frame.pack_forget()
        
        # Show selected
        if panel_name == "stats":
            self.stats_frame.pack(fill="both", expand=True, padx=0, pady=0)
        elif panel_name == "debug":
            self.debug_panel_frame.pack(fill="both", expand=True, padx=0, pady=0)
        elif panel_name == "outline":
            self.outline_frame.pack(fill="both", expand=True, padx=0, pady=0)
        elif panel_name == "performance":
            self.perf_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Update button colors
        for name, btn in self.right_panel_tabs.items():
            color = get_color("accent") if name == panel_name else "transparent"
            btn.configure(fg_color=color)
    
    def _exec_command(self, cmd):
        """Execute command from palette"""
        commands = {
            "run": self._run_code,
            "save": self._save_file,
            "open": self._open_file,
            "new": self.new_file,
            "find": lambda: messagebox.showinfo("Find", "Find in files (Ctrl+F)"),
            "goto": lambda: messagebox.showinfo("Go to", "Go to line (Ctrl+G)"),
            "theme": self._show_settings,
            "sidebar": self._toggle_sidebar,
            "terminal": lambda: messagebox.showinfo("Terminal", "Terminal integration coming soon"),
            "git": lambda: messagebox.showinfo("Git", "Git status (Feature preview)"),
        }
        fn = commands.get(cmd)
        if fn: fn()
    
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.bind("<Control-r>", lambda e: self._run_code())
        self.bind("<Control-s>", lambda e: self._save_file())
        self.bind("<Control-o>", lambda e: self._open_file())
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-p>", lambda e: self._open_palette())
        self.bind("<Control-b>", lambda e: self._toggle_sidebar())
        self.bind("<Control-q>", lambda e: self.quit())
        self.bind("<F5>", lambda e: self._run_code())
    
    def _close_tab(self, idx):
        """Close a tab"""
        if idx < 0 or idx >= len(self.tabs): return
        if len(self.tabs) == 1:
            messagebox.showwarning("Attention", "Impossible de fermer le dernier onglet")
            return
        
        # Ask to save if modified
        if self.tabs[idx]["modified"]:
            result = messagebox.askyesnocancel("Enregistrer", "Enregistrer avant de fermer?")
            if result is None:
                return
            if result:
                self._save_file()
        
        # Remove tab
        tab = self.tabs[idx]
        tab["tab_frame"].pack_forget()
        tab["frame"].pack_forget()
        self.tabs.pop(idx)
        
        # Select previous or next
        if self.active_tab >= len(self.tabs):
            self._select_tab(len(self.tabs) - 1)
        elif self.active_tab != idx:
            self._select_tab(self.active_tab)
        else:
            if self.tabs:
                self._select_tab(max(0, idx - 1))
    
    def _save_as_file(self):
        """Save file as"""
        if self.active_tab < 0: return
        path = filedialog.asksaveasfilename(
            defaultextension=".rint",
            filetypes=[("RINT files", "*.rint"), ("All", "*.*")]
        )
        if path:
            tab = self.tabs[self.active_tab]
            with open(path, "w", encoding="utf-8") as f:
                f.write(tab["text"].get("1.0", "end-1c"))
            tab["file_path"] = path
            tab["btn"].configure(text=Path(path).name)
            self.status_left.configure(text=f"💾 Saved: {Path(path).name}")
    
    def _toggle_vm_mode(self):
        """Toggle isolated VM mode"""
        self.vm_mode = not self.vm_mode
        if self.vm_mode:
            self._add_output("⚙ Mode VM isolé activé")
            self.status_bar.configure(fg_color="#c84b31")  # Orange/Red
        else:
            self._add_output("⚙ Mode VM isolé désactivé")
            self.status_bar.configure(fg_color=get_color("accent_dark"))  # Normal color
    
    def _detect_vm_mode(self):
        """Auto-detect if code is using VM mode"""
        if self.active_tab < 0: return
        code = self.tabs[self.active_tab]["text"].get("1.0", "end-1c")
        # Check for VM keywords
        vm_keywords = ["alloc(", "PC = System.new()", "memcpy(", "when ", "Audio."]
        self.vm_mode = any(kw in code for kw in vm_keywords)
        if self.vm_mode:
            self.status_bar.configure(fg_color="#c84b31")
        else:
            self.status_bar.configure(fg_color=get_color("accent_dark"))

# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

def main():
    ctk.set_appearance_mode("dark")
    app = RintIDE()
    app.mainloop()

if __name__ == "__main__":
    main()