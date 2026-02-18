"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   ██████╗ ██╗███╗   ██╗████████╗    ███████╗████████╗██╗   ██╗██████╗    ║
║   ██╔══██╗██║████╗  ██║╚══██╔══╝    ██╔════╝╚══██╔══╝██║   ██║██╔══██╗   ║
║   ██████╔╝██║██╔██╗ ██║   ██║       ███████╗   ██║   ██║   ██║██║  ██║   ║
║   ██╔══██╗██║██║╚██╗██║   ██║       ╚════██║   ██║   ██║   ██║██║  ██║   ║
║   ██║  ██║██║██║ ╚████║   ██║       ███████║   ██║   ╚██████╔╝██████╔╝   ║
║   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝       ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝    ║
║                                                                          ║
║   RINT Studio  ·  v6.0  ·  Professional IDE                              ║
║   by Léandro BOFFY                                                       ║
╚══════════════════════════════════════════════════════════════════════════╝

  pip install customtkinter psutil
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
import re, os, sys, json, time, threading, subprocess, webbrowser, tempfile
from datetime import datetime
from pathlib import Path
from collections import defaultdict

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ══════════════════════════════════════════════════════════════════════════════
#   DESIGN SYSTEM — THEMES
# ══════════════════════════════════════════════════════════════════════════════

THEMES = {
    "noir": {
        "name": "Noir",
        "bg": "#0d0d0d", "bg1": "#111111", "bg2": "#161616", "bg3": "#1a1a1a",
        "bg4": "#1f1f1f", "bg5": "#252525",
        "fg": "#d4d4d4", "fg2": "#888888", "fg3": "#555555",
        "accent": "#c792ea", "accent2": "#89ddff", "accent3": "#82aaff",
        "green": "#c3e88d", "yellow": "#ffcb6b", "red": "#f07178",
        "orange": "#f78c6c", "cyan": "#89ddff", "pink": "#ff869a",
        "border": "#2a2a2a", "sel": "#264f78", "line_hi": "#1a1a2e",
        "gutter": "#1a1a1a", "gutter_fg": "#3d3d3d",
        "tab_active": "#1e1e1e", "tab_idle": "#111111",
        "status": "#6a0dad", "token_kw": "#c792ea", "token_type": "#82aaff",
        "token_fn": "#82aaff", "token_str": "#c3e88d", "token_num": "#f78c6c",
        "token_cm": "#546e7a", "token_op": "#89ddff", "token_builtin": "#ffcb6b",
    },
    "void": {
        "name": "Void",
        "bg": "#060606", "bg1": "#0a0a0a", "bg2": "#0f0f0f", "bg3": "#141414",
        "bg4": "#1a1a1a", "bg5": "#1f1f1f",
        "fg": "#cccccc", "fg2": "#707070", "fg3": "#404040",
        "accent": "#00d9ff", "accent2": "#00ff9d", "accent3": "#4b7bec",
        "green": "#00ff9d", "yellow": "#ffb800", "red": "#ff4757",
        "orange": "#ffa502", "cyan": "#00d9ff", "pink": "#ff6b81",
        "border": "#1f1f1f", "sel": "#0d3040", "line_hi": "#101820",
        "gutter": "#0a0a0a", "gutter_fg": "#303030",
        "tab_active": "#141414", "tab_idle": "#0a0a0a",
        "status": "#007a99", "token_kw": "#ff79c6", "token_type": "#8be9fd",
        "token_fn": "#50fa7b", "token_str": "#f1fa8c", "token_num": "#bd93f9",
        "token_cm": "#6272a4", "token_op": "#ff79c6", "token_builtin": "#ffb86c",
    },
    "midnight": {
        "name": "Midnight",
        "bg": "#0c1222", "bg1": "#111827", "bg2": "#1a2438", "bg3": "#1e2d45",
        "bg4": "#243250", "bg5": "#2a3a5e",
        "fg": "#e2e8f0", "fg2": "#64748b", "fg3": "#334155",
        "accent": "#5890ff", "accent2": "#2dd4bf", "accent3": "#818cf8",
        "green": "#4ade80", "yellow": "#fbbf24", "red": "#f87171",
        "orange": "#fb923c", "cyan": "#38bdf8", "pink": "#f472b6",
        "border": "#1e293b", "sel": "#1e3a5f", "line_hi": "#111f35",
        "gutter": "#0e1628", "gutter_fg": "#2d4a6e",
        "tab_active": "#1a2538", "tab_idle": "#111827",
        "status": "#1d4ed8", "token_kw": "#c084fc", "token_type": "#38bdf8",
        "token_fn": "#34d399", "token_str": "#a3e635", "token_num": "#fb923c",
        "token_cm": "#475569", "token_op": "#38bdf8", "token_builtin": "#fbbf24",
    },
    "forest": {
        "name": "Forest",
        "bg": "#0a110d", "bg1": "#0f1a13", "bg2": "#142118", "bg3": "#1a291e",
        "bg4": "#203224", "bg5": "#263d2a",
        "fg": "#d4f5e1", "fg2": "#52796f", "fg3": "#344e41",
        "accent": "#40c97a", "accent2": "#64d8cb", "accent3": "#84cc16",
        "green": "#40c97a", "yellow": "#f59e0b", "red": "#ef4444",
        "orange": "#f97316", "cyan": "#06b6d4", "pink": "#a78bfa",
        "border": "#1a2e23", "sel": "#1a3a28", "line_hi": "#0f1f15",
        "gutter": "#0c1510", "gutter_fg": "#2d5038",
        "tab_active": "#16241a", "tab_idle": "#0f1a13",
        "status": "#166534", "token_kw": "#7c3aed", "token_type": "#06b6d4",
        "token_fn": "#40c97a", "token_str": "#84cc16", "token_num": "#f59e0b",
        "token_cm": "#4b6351", "token_op": "#64d8cb", "token_builtin": "#f59e0b",
    },
    "ember": {
        "name": "Ember",
        "bg": "#110a06", "bg1": "#1a1009", "bg2": "#22160c", "bg3": "#2a1d12",
        "bg4": "#332518", "bg5": "#3d2e1f",
        "fg": "#f5e6d0", "fg2": "#8b5a35", "fg3": "#5c3820",
        "accent": "#ff6b35", "accent2": "#f7931e", "accent3": "#ffc107",
        "green": "#a8d08d", "yellow": "#ffd54f", "red": "#ef5350",
        "orange": "#ff6b35", "cyan": "#4fc3f7", "pink": "#f06292",
        "border": "#2d1e14", "sel": "#4a2c18", "line_hi": "#1f1208",
        "gutter": "#140d07", "gutter_fg": "#4d3020",
        "tab_active": "#241810", "tab_idle": "#1a1009",
        "status": "#8b3a0f", "token_kw": "#f06292", "token_type": "#4fc3f7",
        "token_fn": "#ffd54f", "token_str": "#a8d08d", "token_num": "#ff6b35",
        "token_cm": "#6d4c41", "token_op": "#f7931e", "token_builtin": "#ffc107",
    },
}

_T = "noir"  # current theme key

def t(k): return THEMES[_T].get(k, "#ff00ff")

# ══════════════════════════════════════════════════════════════════════════════
#   FONTS
# ══════════════════════════════════════════════════════════════════════════════

def mk_fonts():
    global F_CODE, F_CODES, F_UI, F_UIS, F_UIB, F_TITLE, F_MONO
    F_CODE  = ("JetBrains Mono", 11)
    F_CODES = ("JetBrains Mono", 9)
    F_UI    = ("Segoe UI", 10)
    F_UIS   = ("Segoe UI", 9)
    F_UIB   = ("Segoe UI", 10, "bold")
    F_TITLE = ("Segoe UI", 11, "bold")
    F_MONO  = ("Consolas", 10)

mk_fonts()

# ══════════════════════════════════════════════════════════════════════════════
#   RINT LANGUAGE DEFINITION
# ══════════════════════════════════════════════════════════════════════════════

KEYWORDS = {"if","else","elif","while","when","repeat","return","func","class",
            "true","false","null","and","or","not","in","to","use","as","break",
            "continue","import","alloc","memcpy","memmove","realloc","memset",
            "forward","backward","left","right","down","up","all","time","new"}

TYPES    = {"int","string","bool","float","list","dict","wave","unit","sys",
            "byte","char","void","auto","const"}

BUILTINS = {"console","Audio","System","Voltige","hardware","Turtle","JSON",
            "hard","Math","File","Net","Thread","Event","DB","Cache"}

FUNCS    = {"print","log","ask","read","write","del","play","load","add","remove",
            "set","get","save","run","pick","drop","limit","reduce","error","crash",
            "info","debug","virtual","config","speed","port","autodetect","pen",
            "track","context","push","pop","len","keys","values","range","sorted",
            "map","filter","join","split","format","parse","stringify","now","sleep"}

COMPLETIONS = sorted(KEYWORDS | TYPES | BUILTINS | FUNCS) + [
    "console.print(", "console.log(", "console.ask(", "console.error(",
    "Audio.play(", "Audio.load(", "Turtle.move(", "Turtle.pen(",
    "System.virtual.new(", "hardware.new(", "hardware.config(",
    "hardware.port.autodetect()",
]

DOCS_MAP = {
    "console.print": "Affiche un message dans la sortie standard.\nUsage: console.print(message)",
    "console.log":   "Log vers le panneau dédié.\nUsage: console.log(message)",
    "console.ask":   "Demande une entrée à l'utilisateur.\nUsage: string result = console.ask(prompt)",
    "Audio.play":    "Joue un fichier audio.\nUsage: Audio.play(path, loop=false)",
    "Turtle.move":   "Déplace la tortue.\nUsage: Turtle.move(distance)",
    "alloc":         "Alloue de la mémoire manuellement.\nUsage: alloc(type=\"stack\", name=\"x\", size=\"bit:32\")",
    "memcpy":        "Copie une zone mémoire.\nUsage: memcpy(src to dst)",
    "when":          "Surveille une condition (event-driven).\nUsage: when condition { ... }",
    "repeat":        "Répète un bloc N fois.\nUsage: repeat time(N) { ... }",
    "func":          "Déclare une fonction.\nUsage: func nom(args) { ... }",
}

SNIPPETS = {
    "if":     "if {cond} {\n    \n}",
    "else":   "else {\n    \n}",
    "elif":   "elif {cond} {\n    \n}",
    "while":  "while {cond} {\n    \n}",
    "when":   "when {cond} {\n    \n}",
    "func":   "func {name}({args}) {\n    return \n}",
    "class":  "class {Name} {\n    \n}",
    "repeat": "repeat time({n}) {\n    \n}",
    "alloc":  'alloc(type="stack", name="{var}", size="bit:32") {type} {var} = ',
    "for":    "repeat time({n}) {\n    \n}",
    "try":    "if not {cond} {\n    console.error(\"Error\")\n}",
}

SYNTAX_PATTERNS = [
    ("cm",  r"//[^\n]*"),
    ("str", r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''),
    ("fst", r'f"[^"]*"'),
    ("num", r'\b\d+(?:\.\d+)?\b'),
    ("kw",  r'\b(?:' + '|'.join(sorted(KEYWORDS, key=len, reverse=True)) + r')\b'),
    ("typ", r'\b(?:' + '|'.join(sorted(TYPES,    key=len, reverse=True)) + r')\b'),
    ("blt", r'\b(?:' + '|'.join(sorted(BUILTINS, key=len, reverse=True)) + r')\b'),
    ("fn",  r'\b(?:' + '|'.join(sorted(FUNCS,    key=len, reverse=True)) + r')\b'),
    ("op",  r'[=<>!+\-\*/%&|^~]+|[(){}\[\].,;:]'),
]

TOKEN_TAG_MAP = {
    "cm":  "token_cm",  "str": "token_str", "fst": "token_str",
    "num": "token_num", "kw":  "token_kw",  "typ": "token_type",
    "blt": "token_builtin", "fn": "token_fn", "op": "token_op",
}

# ══════════════════════════════════════════════════════════════════════════════
#   RINT INTERPRETER (Enhanced)
# ══════════════════════════════════════════════════════════════════════════════

class RintInterpreter:
    def __init__(self, out_cb, log_cb, err_cb, var_cb=None, turtle_cb=None):
        self.out  = out_cb
        self.log  = log_cb
        self.err  = err_cb
        self.var  = var_cb  or (lambda *a: None)
        self.turt = turtle_cb or (lambda *a: None)
        self.vars = {}
        self.vtypes = {}
        self.funcs = {}
        self.running = False
        self.call_stack = []

    def run(self, code):
        self.running = True
        self.vars = {}
        self.vtypes = {}
        self.funcs = {}
        lines = code.split("\n")
        # First pass: collect function definitions
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            m = re.match(r'^func\s+(\w+)\s*\(([^)]*)\)\s*\{?', line)
            if m:
                fname, params = m.group(1), m.group(2)
                body_lines = []
                if not line.endswith("{"):
                    i += 1
                    continue
                depth = 1
                i += 1
                while i < len(lines) and depth > 0:
                    bl = lines[i]
                    depth += bl.count("{") - bl.count("}")
                    if depth > 0:
                        body_lines.append(bl)
                    i += 1
                self.funcs[fname] = {"params": [p.strip() for p in params.split(",") if p.strip()], "body": body_lines}
                continue
            i += 1
        # Second pass: execute
        try:
            self._exec_block(lines, 0)
        except StopIteration:
            pass
        except Exception as e:
            self.err(f"Runtime Error: {e}")
        finally:
            self.running = False

    def _exec_block(self, lines, start=0):
        i = start
        while i < len(lines) and self.running:
            line = lines[i]
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                i += 1; continue
            result = self._exec_line(stripped, lines, i)
            if isinstance(result, int):
                i = result
            else:
                i += 1

    def _exec_line(self, line, all_lines, lineno):
        # Skip func definitions (already collected)
        if re.match(r'^func\s+\w+', line): 
            return self._skip_block(all_lines, lineno)

        # Use/import
        if line.startswith("use ") or line.startswith("import "):
            self.log(f"import: {line}")
            return None

        # alloc declaration
        m = re.match(r'^alloc\(.*?\)\s+(int|string|bool|float|wave|unit|sys|list)\s+(\w+)\s*=\s*(.+)$', line)
        if m:
            t_, name, expr = m.groups()
            val = self._eval(expr)
            self.vars[name] = val; self.vtypes[name] = t_
            self.log(f"[ALLOC] {t_} {name} = {repr(val)}")
            self.var(name, val, f"alloc:{t_}")
            return None

        # Typed variable declaration
        m = re.match(r'^(int|string|bool|float|wave|unit|sys|list|auto)\s+(\w+)\s*=\s*(.+)$', line)
        if m:
            t_, name, expr = m.groups()
            val = self._eval(expr)
            self.vars[name] = val; self.vtypes[name] = t_
            self.var(name, val, t_)
            return None

        # Variable assignment
        m = re.match(r'^(\w+)\s*([+\-*/]?=)\s*(.+)$', line)
        if m:
            name, op, expr = m.groups()
            if op == "=":
                val = self._eval(expr)
            elif op == "+=":
                val = self._eval(f"{name} + {expr}")
            elif op == "-=":
                val = self._eval(f"{name} - {expr}")
            elif op == "*=":
                val = self._eval(f"{name} * {expr}")
            elif op == "/=":
                val = self._eval(f"{name} / {expr}")
            else:
                val = self._eval(expr)
            if name in self.vars or op == "=":
                self.vars[name] = val
                self.var(name, val, self.vtypes.get(name, "var"))
            return None

        # if block
        m = re.match(r'^if\s+(.+?)\s*\{?$', line)
        if m:
            cond = m.group(1).rstrip("{").strip()
            if self._eval_bool(cond):
                body, after = self._extract_block(all_lines, lineno)
                self._exec_block(body)
                return after
            else:
                after = self._skip_block(all_lines, lineno)
                # check for else
                if after < len(all_lines):
                    nl = all_lines[after].strip()
                    if nl.startswith("else") or nl.startswith("elif"):
                        return self._exec_line(nl, all_lines, after)
                return after

        # else
        m = re.match(r'^else\s*\{?$', line)
        if m:
            body, after = self._extract_block(all_lines, lineno)
            self._exec_block(body)
            return after

        # while
        m = re.match(r'^while\s+(.+?)\s*\{?$', line)
        if m:
            cond = m.group(1).rstrip("{").strip()
            body, after = self._extract_block(all_lines, lineno)
            safety = 0
            while self._eval_bool(cond) and self.running and safety < 10000:
                self._exec_block(body)
                safety += 1
            if safety >= 10000:
                self.err("Boucle infinie détectée — arrêt après 10 000 itérations")
            return after

        # repeat time(N)
        m = re.match(r'^repeat\s+time\((.+?)\)\s*\{?$', line)
        if m:
            n = int(self._eval(m.group(1)))
            body, after = self._extract_block(all_lines, lineno)
            for _ in range(min(n, 10000)):
                if not self.running: break
                self._exec_block(body)
            return after

        # when (one-time condition check)
        m = re.match(r'^when\s+(.+?)\s*\{?$', line)
        if m:
            cond = m.group(1).rstrip("{").strip()
            body, after = self._extract_block(all_lines, lineno)
            if self._eval_bool(cond):
                self._exec_block(body)
            return after

        # return
        m = re.match(r'^return\s*(.*)', line)
        if m:
            val = self._eval(m.group(1)) if m.group(1) else None
            self.vars["__return__"] = val
            raise StopIteration(val)

        # console.print
        m = re.match(r'^console\.print\((.+)\)$', line)
        if m:
            self.out(self._eval_str(m.group(1).strip()))
            return None

        # console.log
        m = re.match(r'^console\.log\((.+)\)$', line)
        if m:
            self.log(self._eval_str(m.group(1).strip()))
            return None

        # console.error
        m = re.match(r'^console\.error\((.+)\)$', line)
        if m:
            self.err(self._eval_str(m.group(1).strip()))
            return None

        # Turtle commands
        m = re.match(r'^Turtle\.(\w+)\(([^)]*)\)$', line)
        if m:
            cmd, args = m.group(1), m.group(2)
            self.turt(cmd, args)
            return None

        # memcpy / memmove
        m = re.match(r'^mem(?:cpy|move)\((\w+)\s+to\s+(\w+)\)$', line)
        if m:
            src, dst = m.group(1), m.group(2)
            if src in self.vars:
                self.vars[dst] = self.vars[src]
                self.log(f"[MEM] {src} → {dst} = {repr(self.vars[dst])}")
            return None

        # realloc
        m = re.match(r'^realloc\(', line)
        if m:
            self.log(f"[MEM] realloc: {line}")
            return None

        # Function call
        m = re.match(r'^(\w+)\(([^)]*)\)$', line)
        if m:
            fname, args_str = m.group(1), m.group(2)
            if fname in self.funcs:
                fdef = self.funcs[fname]
                arg_vals = [self._eval(a.strip()) for a in args_str.split(",") if a.strip()]
                old_vars = dict(self.vars)
                for pname, pval in zip(fdef["params"], arg_vals):
                    self.vars[pname] = pval
                try:
                    self._exec_block(fdef["body"])
                except StopIteration:
                    pass
                result = self.vars.get("__return__")
                self.vars = {k: v for k, v in old_vars.items()}
                if result is not None:
                    self.out(f"→ {fname}() = {result}")
            return None

        return None

    def _extract_block(self, lines, start):
        """Extract the body of a { } block starting at lines[start]"""
        if "{" in lines[start]:
            depth = lines[start].count("{") - lines[start].count("}")
        else:
            depth = 0
        body, i = [], start + 1
        if depth == 0 and i < len(lines) and "{" in lines[i]:
            depth = 1; i += 1
        while i < len(lines) and depth > 0:
            depth += lines[i].count("{") - lines[i].count("}")
            if depth > 0:
                body.append(lines[i])
            i += 1
        return body, i

    def _skip_block(self, lines, start):
        _, after = self._extract_block(lines, start)
        return after

    def _eval(self, expr):
        expr = expr.strip().rstrip(";").strip()
        if not expr: return None
        if expr == "true": return True
        if expr == "false": return False
        if expr == "null": return None
        if expr.startswith('"') and expr.endswith('"'): return expr[1:-1]
        if expr.startswith("'") and expr.endswith("'"): return expr[1:-1]
        if expr.startswith('f"'): return self._eval_fstring(expr)
        if expr.startswith('[') and expr.endswith(']'):
            items = expr[1:-1].split(",")
            return [self._eval(i) for i in items if i.strip()]
        try:
            return int(expr)
        except ValueError:
            pass
        try:
            return float(expr)
        except ValueError:
            pass
        # Variable lookup
        if re.match(r'^\w+$', expr) and expr in self.vars:
            return self.vars[expr]
        # Binary ops
        for op in ["==","!=","<=",">=","<",">"]:
            if op in expr:
                parts = expr.split(op, 1)
                l, r = self._eval(parts[0]), self._eval(parts[1])
                if op == "==": return l == r
                if op == "!=": return l != r
                if op == "<=": return l <= r
                if op == ">=": return l >= r
                if op == "<":  return l < r
                if op == ">":  return l > r
        for op in ["+", "-", "*", "/"]:
            if op in expr:
                parts = expr.split(op, 1)
                l, r = self._eval(parts[0]), self._eval(parts[1])
                try:
                    if op == "+": return l + r
                    if op == "-": return l - r
                    if op == "*": return l * r
                    if op == "/": return l / r if r != 0 else 0
                except:
                    return f"{l}{r}" if op == "+" else expr
        return expr

    def _eval_bool(self, expr):
        val = self._eval(expr)
        if isinstance(val, bool): return val
        if isinstance(val, (int, float)): return val != 0
        if isinstance(val, str): return len(val) > 0
        return bool(val)

    def _eval_str(self, expr):
        val = self._eval(expr)
        return str(val) if val is not None else ""

    def _eval_fstring(self, expr):
        content = expr[2:-1]
        def repl(m):
            return str(self.vars.get(m.group(1), f"{{{m.group(1)}}}"))
        return re.sub(r'\{(\w+)\}', repl, content)

# ══════════════════════════════════════════════════════════════════════════════
#   MEMORY MONITOR
# ══════════════════════════════════════════════════════════════════════════════

class MemoryMonitor:
    def __init__(self):
        self.enabled = HAS_PSUTIL
        self.history = []   # (ts, code_mb, total_mb)

    def reset(self):
        self.history.clear()

    def sample(self):
        if not self.enabled: return
        try:
            proc = psutil.Process()
            total = proc.memory_info().rss / (1024*1024)
            code  = max(0, total - 160)  # estimate IDE baseline at 160MB
            self.history.append((time.time(), code, total))
        except:
            pass

    def get_stats(self):
        if not self.history: return {}
        codes  = [h[1] for h in self.history]
        totals = [h[2] for h in self.history]
        return {
            "peak_code": round(max(codes), 1),
            "avg_code":  round(sum(codes)/len(codes), 1),
            "peak_total": round(max(totals), 1),
            "samples": len(self.history),
        }

# ══════════════════════════════════════════════════════════════════════════════
#   SYNTAX HIGHLIGHTER
# ══════════════════════════════════════════════════════════════════════════════

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text = text_widget
        self._after_id = None
        self._setup_tags()

    def _setup_tags(self):
        tw = self.text
        for tag, color_key in TOKEN_TAG_MAP.items():
            tw.tag_configure(tag, foreground=t(color_key))
        tw.tag_configure("current_line", background=t("line_hi"))
        tw.tag_configure("sel_highlight", background=t("sel"))
        tw.tag_configure("error_line", underline=True, foreground=t("red"))
        tw.tag_configure("warning_line", underline=True, foreground=t("yellow"))
        tw.tag_configure("bp_line",
                         background=t("red"), foreground=t("fg"))
        tw.tag_configure("bookmark_line",
                         background=t("bg5"), foreground=t("cyan"))

    def refresh_tags(self):
        self._setup_tags()

    def highlight(self, event=None):
        if self._after_id:
            self.text.after_cancel(self._after_id)
        self._after_id = self.text.after(80, self._do_highlight)

    def _do_highlight(self):
        tw = self.text
        try:
            code = tw.get("1.0", "end-1c")
        except:
            return
        # Remove all token tags
        for tag in TOKEN_TAG_MAP:
            tw.tag_remove(tag, "1.0", "end")

        for tag, pattern in SYNTAX_PATTERNS:
            for m in re.finditer(pattern, code, re.MULTILINE):
                start = f"1.0 + {m.start()} chars"
                end   = f"1.0 + {m.end()} chars"
                tw.tag_add(tag, start, end)

        # Re-highlight current line
        self._highlight_current_line()

    def _highlight_current_line(self):
        tw = self.text
        tw.tag_remove("current_line", "1.0", "end")
        line = tw.index("insert").split(".")[0]
        tw.tag_add("current_line", f"{line}.0", f"{line}.end+1c")

# ══════════════════════════════════════════════════════════════════════════════
#   LINE NUMBERS (with breakpoints + bookmarks)
# ══════════════════════════════════════════════════════════════════════════════

class LineNumbers(tk.Canvas):
    def __init__(self, parent, text_widget):
        super().__init__(parent, bg=t("gutter"), highlightthickness=0, width=54)
        self.text = text_widget
        self.bps   = set()   # breakpoints
        self.marks = set()   # bookmarks
        self.bind("<Button-1>", self._toggle_bp)
        self.bind("<Button-3>", self._toggle_bookmark)

    def _toggle_bp(self, event):
        line = int(self.text.index(f"@0,{event.y}").split(".")[0])
        if line in self.bps: self.bps.remove(line)
        else: self.bps.add(line)
        self.redraw()

    def _toggle_bookmark(self, event):
        line = int(self.text.index(f"@0,{event.y}").split(".")[0])
        if line in self.marks: self.marks.remove(line)
        else: self.marks.add(line)
        self.redraw()

    def redraw(self, *_):
        self.delete("all")
        self.configure(bg=t("gutter"))
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if not dline: break
            y  = dline[1]
            ln = int(str(i).split(".")[0])
            is_bp   = ln in self.bps
            is_mark = ln in self.marks
            if is_bp:
                self.create_oval(4, y+3, 14, y+13, fill=t("red"), outline="")
            elif is_mark:
                self.create_rectangle(2, y+4, 6, y+14, fill=t("cyan"), outline="")
            fg = t("red") if is_bp else (t("cyan") if is_mark else t("gutter_fg"))
            self.create_text(49, y+8, anchor="e", text=str(ln), fill=fg, font=F_CODES)
            ni = self.text.index(f"{i}+1line")
            if ni == i: break
            i = ni

# ══════════════════════════════════════════════════════════════════════════════
#   MINIMAP
# ══════════════════════════════════════════════════════════════════════════════

class Minimap(tk.Canvas):
    SCALE_X = 1.0   # chars → pixels
    SCALE_Y = 2.0   # lines → pixels

    def __init__(self, parent, text_widget):
        super().__init__(parent, bg=t("bg"), highlightthickness=0, width=80, cursor="hand2")
        self.text = text_widget
        self.bind("<Button-1>", self._jump)
        self._after_id = None

    def schedule_redraw(self, *_):
        if self._after_id: self.after_cancel(self._after_id)
        self._after_id = self.after(300, self.redraw)

    def redraw(self):
        try:
            code = self.text.get("1.0", "end-1c")
        except:
            return
        lines = code.split("\n")
        self.delete("all")
        self.configure(bg=t("bg"))
        W = 80
        for li, line in enumerate(lines[:300]):
            y = li * self.SCALE_Y
            # Color based on content
            stripped = line.strip()
            if stripped.startswith("//"):
                color = t("token_cm")
            elif re.match(r'\s*(func|class)\b', line):
                color = t("accent")
            elif re.match(r'\s*(if|else|while|when|repeat)\b', line):
                color = t("token_kw")
            elif stripped:
                color = t("fg3")
            else:
                continue
            # Indent indicator
            indent = len(line) - len(line.lstrip())
            x_start = max(2, int(indent * 0.4))
            x_end   = min(W - 2, int(len(stripped) * 0.5) + x_start)
            if x_end > x_start:
                self.create_line(x_start, y, x_end, y, fill=color, width=1)

        # Viewport indicator
        try:
            first = int(self.text.index("@0,0").split(".")[0])
            last  = int(self.text.index(f"@0,{self.winfo_height()}").split(".")[0])
            y1, y2 = first * self.SCALE_Y, last * self.SCALE_Y
            self.create_rectangle(0, y1, W, y2, outline=t("accent"), fill=t("bg3"),
                                  stipple="gray25", width=1)
        except:
            pass

    def _jump(self, event):
        total_lines = int(self.text.index("end-1c").split(".")[0])
        frac = event.y / max(1, self.winfo_height())
        target = int(frac * total_lines)
        self.text.see(f"{target}.0")

# ══════════════════════════════════════════════════════════════════════════════
#   AUTOCOMPLETE POPUP
# ══════════════════════════════════════════════════════════════════════════════

class AutocompletePopup(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.overrideredirect(True)
        self.withdraw()
        self.configure(bg=t("accent"))
        self.wm_attributes("-topmost", True)
        inner = tk.Frame(self, bg=t("bg2"))
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        self.lb = tk.Listbox(inner, bg=t("bg2"), fg=t("fg"),
                             selectbackground=t("accent"),
                             selectforeground=t("bg"),
                             font=F_CODES, borderwidth=0,
                             highlightthickness=0, height=9, width=36)
        self.lb.pack(fill="both", expand=True, padx=2, pady=2)
        self.doc = tk.Label(inner, bg=t("bg3"), fg=t("fg2"),
                            font=F_UIS, anchor="w", justify="left",
                            wraplength=220, pady=4, padx=6)
        self.doc.pack(fill="x")
        self.lb.bind("<Double-1>", lambda _: self._select())
        self.lb.bind("<Return>",   lambda _: self._select())
        self.lb.bind("<<ListboxSelect>>", self._show_doc)

    def show(self, x, y, items):
        self.lb.delete(0, "end")
        if not items: self.withdraw(); return
        for it in items[:14]: self.lb.insert("end", it)
        self.deiconify()
        self.geometry(f"+{x}+{y}")
        self.lb.selection_set(0)
        self._show_doc()

    def hide(self): self.withdraw()

    def _show_doc(self, *_):
        sel = self.lb.curselection()
        if not sel: return
        word = self.lb.get(sel[0]).rstrip("(")
        doc  = DOCS_MAP.get(word, "")
        self.doc.configure(text=doc if doc else "")

    def _select(self):
        sel = self.lb.curselection()
        if sel: self.callback(self.lb.get(sel[0]))

    def navigate(self, delta):
        if not self.winfo_viewable(): return
        sel = self.lb.curselection()
        idx = sel[0] if sel else -1
        nw  = max(0, min(self.lb.size()-1, idx+delta))
        self.lb.selection_clear(0, "end")
        self.lb.selection_set(nw)
        self.lb.see(nw)
        self._show_doc()

# ══════════════════════════════════════════════════════════════════════════════
#   FIND & REPLACE PANEL (fully working)
# ══════════════════════════════════════════════════════════════════════════════

class FindReplacePanel(ctk.CTkFrame):
    def __init__(self, parent, get_editor_cb):
        super().__init__(parent, fg_color=t("bg2"), corner_radius=0, height=64)
        self.get_editor = get_editor_cb
        self.matches = []
        self.match_idx = -1
        self._build()

    def _build(self):
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=8, pady=(4,2))

        self.find_var = tk.StringVar()
        self.repl_var = tk.StringVar()

        tk.Label(row1, text="Find:", bg=t("bg2"), fg=t("fg2"), font=F_UIS).pack(side="left")
        self.find_entry = tk.Entry(row1, textvariable=self.find_var,
                                   bg=t("bg4"), fg=t("fg"), font=F_CODE,
                                   insertbackground=t("accent"), relief="flat",
                                   highlightthickness=1, highlightbackground=t("border"),
                                   highlightcolor=t("accent"), width=26)
        self.find_entry.pack(side="left", padx=(4,8))

        self.case_var = tk.BooleanVar(value=False)
        self.regex_var = tk.BooleanVar(value=False)
        self.word_var  = tk.BooleanVar(value=False)

        for text, var in [("Aa", self.case_var), (".*", self.regex_var), ("\\b", self.word_var)]:
            cb = tk.Checkbutton(row1, text=text, variable=var,
                                bg=t("bg2"), fg=t("fg2"), selectcolor=t("bg4"),
                                activebackground=t("bg2"), font=F_UIS)
            cb.pack(side="left", padx=2)

        self.count_lbl = tk.Label(row1, text="", bg=t("bg2"), fg=t("fg2"), font=F_UIS)
        self.count_lbl.pack(side="left", padx=8)

        for text, cmd in [("▲", self._prev), ("▼", self._next), ("All", self._select_all)]:
            tk.Button(row1, text=text, command=cmd,
                      bg=t("bg4"), fg=t("fg"), relief="flat", font=F_UIS,
                      activebackground=t("accent"), activeforeground=t("bg"),
                      padx=6, pady=1).pack(side="left", padx=2)

        # Close button
        tk.Button(row1, text="✕", command=self._close,
                  bg=t("bg2"), fg=t("fg2"), relief="flat", font=F_UIS,
                  activebackground=t("red"), activeforeground=t("fg"),
                  padx=4).pack(side="right")

        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", padx=8, pady=(0,4))

        tk.Label(row2, text="Replace:", bg=t("bg2"), fg=t("fg2"), font=F_UIS).pack(side="left")
        self.repl_entry = tk.Entry(row2, textvariable=self.repl_var,
                                   bg=t("bg4"), fg=t("fg"), font=F_CODE,
                                   insertbackground=t("accent"), relief="flat",
                                   highlightthickness=1, highlightbackground=t("border"),
                                   highlightcolor=t("accent"), width=26)
        self.repl_entry.pack(side="left", padx=(4,8))

        for text, cmd in [("Replace", self._replace_one), ("Replace All", self._replace_all)]:
            tk.Button(row2, text=text, command=cmd,
                      bg=t("accent"), fg=t("bg"), relief="flat", font=F_UIS,
                      activebackground=t("accent2"), activeforeground=t("bg"),
                      padx=8, pady=1).pack(side="left", padx=3)

        self.find_var.trace("w", lambda *_: self._do_find())
        self.find_entry.bind("<Return>", lambda _: self._next())
        self.find_entry.bind("<Shift-Return>", lambda _: self._prev())

    def focus(self):
        self.find_entry.focus_set()
        self.find_entry.select_all()

    def _get_pattern(self):
        query = self.find_var.get()
        if not query: return None
        flags = 0 if self.case_var.get() else re.IGNORECASE
        if not self.regex_var.get():
            query = re.escape(query)
        if self.word_var.get():
            query = r'\b' + query + r'\b'
        try:
            return re.compile(query, flags)
        except re.error:
            return None

    def _do_find(self, *_):
        editor = self.get_editor()
        if not editor: return
        pat = self._get_pattern()
        editor.tag_remove("find_hi", "1.0", "end")
        editor.tag_remove("find_cur", "1.0", "end")
        self.matches = []
        if not pat: self.count_lbl.configure(text=""); return
        code = editor.get("1.0", "end-1c")
        for m in pat.finditer(code):
            start = f"1.0 + {m.start()} chars"
            end   = f"1.0 + {m.end()} chars"
            editor.tag_add("find_hi", start, end)
            self.matches.append((m.start(), m.end()))
        editor.tag_configure("find_hi",  background=t("yellow"),  foreground=t("bg"))
        editor.tag_configure("find_cur", background=t("orange"),  foreground=t("bg"))
        n = len(self.matches)
        self.count_lbl.configure(text=f"{n} match{'es' if n!=1 else ''}")
        self.match_idx = -1
        if self.matches: self._next()

    def _jump_to(self, idx):
        editor = self.get_editor()
        if not editor or not self.matches: return
        editor.tag_remove("find_cur", "1.0", "end")
        start_c, end_c = self.matches[idx]
        start = f"1.0 + {start_c} chars"
        end   = f"1.0 + {end_c} chars"
        editor.tag_add("find_cur", start, end)
        editor.see(start)
        self.count_lbl.configure(text=f"{idx+1} / {len(self.matches)}")

    def _next(self, *_):
        if not self.matches: self._do_find(); return
        self.match_idx = (self.match_idx + 1) % len(self.matches)
        self._jump_to(self.match_idx)

    def _prev(self, *_):
        if not self.matches: return
        self.match_idx = (self.match_idx - 1) % len(self.matches)
        self._jump_to(self.match_idx)

    def _select_all(self):
        editor = self.get_editor()
        if not editor or not self.matches: return
        editor.tag_remove("sel", "1.0", "end")
        for s, e in self.matches:
            editor.tag_add("sel", f"1.0+{s}c", f"1.0+{e}c")

    def _replace_one(self):
        editor = self.get_editor()
        if not editor or self.match_idx < 0 or not self.matches: return
        s, e = self.matches[self.match_idx]
        repl = self.repl_var.get()
        editor.delete(f"1.0+{s}c", f"1.0+{e}c")
        editor.insert(f"1.0+{s}c", repl)
        self._do_find()

    def _replace_all(self):
        editor = self.get_editor()
        if not editor: return
        pat = self._get_pattern()
        if not pat: return
        code = editor.get("1.0", "end-1c")
        new_code = pat.sub(self.repl_var.get(), code)
        editor.delete("1.0", "end")
        editor.insert("1.0", new_code)
        self._do_find()

    def _close(self):
        editor = self.get_editor()
        if editor:
            editor.tag_remove("find_hi",  "1.0", "end")
            editor.tag_remove("find_cur", "1.0", "end")
        self.pack_forget()

# ══════════════════════════════════════════════════════════════════════════════
#   COMMAND PALETTE
# ══════════════════════════════════════════════════════════════════════════════

class CommandPalette(tk.Toplevel):
    COMMANDS = [
        ("▶  Run Code",               "F5 / Ctrl+R",    "run"),
        ("⏹  Stop Execution",          "Ctrl+.",          "stop"),
        ("💾  Save File",               "Ctrl+S",          "save"),
        ("📂  Open File",               "Ctrl+O",          "open"),
        ("📄  New File",                "Ctrl+N",          "new"),
        ("🔍  Find & Replace",          "Ctrl+F",          "find"),
        ("🔎  Spotlight Search",        "Ctrl+Shift+F",    "spotlight"),
        ("⬆  Go to Line",              "Ctrl+G",          "goto"),
        ("📌  Toggle Bookmark",         "Ctrl+F2",         "bookmark"),
        ("🔖  Next Bookmark",           "F2",              "next_bookmark"),
        ("⚙  Rename Symbol",            "",                "rename"),
        ("📊  Code Metrics",            "",                "metrics"),
        ("✅  Show TODOs",              "",                "todos"),
        ("📤  Export to HTML",          "",                "export_html"),
        ("🌿  Git Status",              "",                "git_status"),
        ("🎨  Change Theme",            "",                "theme"),
        ("⊞  Toggle Minimap",          "Ctrl+M",          "minimap"),
        ("◧  Toggle Sidebar",          "Ctrl+B",          "sidebar"),
        ("📐  Format Code",             "Shift+Alt+F",     "format"),
        ("🖥  Terminal",                "Ctrl+`",          "terminal"),
        ("❓  About RINT Studio",       "",                "about"),
    ]

    def __init__(self, parent, ide):
        super().__init__(parent)
        self.ide = ide
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.configure(bg=t("accent"))
        w, h = 560, 420
        sw = self.winfo_screenwidth()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+80")
        inner = tk.Frame(self, bg=t("bg2"))
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        # Header
        hdr = tk.Frame(inner, bg=t("bg1"))
        hdr.pack(fill="x")
        tk.Label(hdr, text="⌘  Command Palette", bg=t("bg1"), fg=t("fg2"),
                 font=F_UIS, pady=6).pack(side="left", padx=12)
        tk.Label(hdr, text="Esc to close", bg=t("bg1"), fg=t("fg3"),
                 font=F_UIS).pack(side="right", padx=12)
        # Search
        self.sv = tk.StringVar()
        entry = tk.Entry(inner, textvariable=self.sv,
                         bg=t("bg3"), fg=t("fg"), font=F_CODE,
                         insertbackground=t("accent"), relief="flat",
                         highlightthickness=1, highlightbackground=t("border"),
                         highlightcolor=t("accent"))
        entry.pack(fill="x", padx=12, pady=8, ipady=7)
        # List
        self.lb = tk.Listbox(inner, bg=t("bg2"), fg=t("fg"),
                             selectbackground=t("accent"), selectforeground=t("bg"),
                             font=F_UI, borderwidth=0, highlightthickness=0, height=14)
        self.lb.pack(fill="both", expand=True, padx=2)
        # Footer
        tk.Label(inner, text="↑↓ navigate  ·  Enter execute  ·  Esc close",
                 bg=t("bg1"), fg=t("fg3"), font=F_UIS).pack(fill="x", padx=12, pady=4)

        self._filtered = self.COMMANDS[:]
        self._populate()
        self.sv.trace("w", self._filter)
        entry.bind("<Return>",  self._run)
        entry.bind("<Escape>",  lambda _: self.destroy())
        entry.bind("<Up>",      lambda _: self._nav(-1))
        entry.bind("<Down>",    lambda _: self._nav(1))
        self.lb.bind("<Double-1>", self._run)
        self.bind("<FocusOut>", lambda _: self.after(100, self._check_focus))
        entry.focus()

    def _check_focus(self):
        try:
            if self.focus_get() is None: self.destroy()
        except: self.destroy()

    def _filter(self, *_):
        q = self.sv.get().lower()
        self._filtered = [(n,s,c) for n,s,c in self.COMMANDS if q in n.lower() or q in c.lower()]
        self._populate()

    def _populate(self):
        self.lb.delete(0, "end")
        for name, shortcut, _ in self._filtered:
            line = f"  {name}"
            if shortcut: line += f"  {shortcut}"
            self.lb.insert("end", line)
        if self._filtered: self.lb.selection_set(0)

    def _nav(self, d):
        sel = self.lb.curselection()
        idx = sel[0] if sel else -1
        nw  = max(0, min(self.lb.size()-1, idx+d))
        self.lb.selection_clear(0, "end")
        self.lb.selection_set(nw)

    def _run(self, *_):
        sel = self.lb.curselection()
        if not sel or sel[0] >= len(self._filtered): return
        cmd = self._filtered[sel[0]][2]
        self.destroy()
        self.ide._exec_command(cmd)

# ══════════════════════════════════════════════════════════════════════════════
#   SPLASH SCREEN
# ══════════════════════════════════════════════════════════════════════════════

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes('-alpha', 0.0)
        w, h = 640, 360
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.configure(bg=t("bg"))

        c = tk.Canvas(self, bg=t("bg"), highlightthickness=0)
        c.pack(fill="both", expand=True)
        self.c = c

        # Decorative grid lines
        for i in range(0, w, 40):
            c.create_line(i, 0, i, h, fill=t("bg3"), width=1)
        for j in range(0, h, 40):
            c.create_line(0, j, w, j, fill=t("bg3"), width=1)

        # Glowing accent rectangle
        c.create_rectangle(0, 0, w, 4, fill=t("accent"), outline="")

        # Logo text
        c.create_text(w//2, 120, text="RINT", font=("JetBrains Mono", 72, "bold"),
                      fill=t("accent"))
        c.create_text(w//2, 185, text="S T U D I O", 
                      font=("Segoe UI", 16), fill=t("fg2"))
        c.create_text(w//2, 215, text="v6.0  ·  Professional Edition",
                      font=F_UIS, fill=t("fg3"))

        # Progress bar background
        c.create_rectangle(80, 280, w-80, 294, fill=t("bg3"), outline="")
        self.prog = c.create_rectangle(80, 280, 80, 294,
                                       fill=t("accent"), outline="")
        self.status = c.create_text(w//2, 312, text="Initializing…",
                                    font=F_UIS, fill=t("fg3"))
        c.create_rectangle(0, h-4, w, h, fill=t("accent"), outline="")

        self.progress = 0
        self.after(40, self._fade_in)
        self.after(200, self._animate)

    STEPS = ["Loading syntax engine…", "Building UI components…",
             "Configuring interpreter…", "Initializing memory monitor…",
             "Starting terminal…", "RINT Studio ready!"]

    def _fade_in(self):
        a = self.attributes('-alpha')
        if a < 1.0:
            self.attributes('-alpha', min(1.0, a + 0.08))
            self.after(25, self._fade_in)

    def _animate(self):
        if self.progress < 100:
            self.progress += 1.4
            W = 640
            self.c.coords(self.prog, 80, 280, 80 + (W-160) * self.progress/100, 294)
            idx = min(int(self.progress) * len(self.STEPS) // 100, len(self.STEPS)-1)
            self.c.itemconfig(self.status, text=self.STEPS[idx])
            self.after(28, self._animate)
        else:
            self.after(600, self._fade_out)

    def _fade_out(self):
        a = self.attributes('-alpha')
        if a > 0.0:
            self.attributes('-alpha', max(0.0, a - 0.07))
            self.after(20, self._fade_out)
        else:
            self.destroy()

# ══════════════════════════════════════════════════════════════════════════════
#   MAIN IDE
# ══════════════════════════════════════════════════════════════════════════════

class RintStudio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RINT Studio  v6.0")
        self.geometry("1520x940")
        self.minsize(1200, 700)
        self.configure(fg_color=t("bg"))

        # State
        self.tabs        = []
        self.active_tab  = -1
        self._running    = False
        self.sidebar_vis = True
        self.minimap_vis = True
        self.find_panel  = None

        # Memory
        self.mem_monitor = MemoryMonitor()

        # Terminal history
        self.term_hist   = []
        self.term_idx    = -1
        self.term_cwd    = str(Path.home())

        # Build
        splash = SplashScreen(self)
        self.update()
        self._build_menu()
        self._build_layout()
        self._bind_keys()

        # Interpreter
        self.interp = RintInterpreter(
            out_cb   = lambda m: self.after(0, self._console_out, m),
            log_cb   = lambda m: self.after(0, self._console_log, m),
            err_cb   = lambda m: self.after(0, self._console_err, m),
            var_cb   = lambda n, v, tp: self.after(0, self._update_var, n, v, tp),
            turtle_cb= lambda cmd, args: self.after(0, self._turtle_cmd, cmd, args),
        )

        self.wait_window(splash)
        self.new_tab()
        self._ram_loop()
        self._console_out("✓  RINT Studio v6.0 initialized")
        self._console_log("Bienvenue ! Écrivez du code RINT et appuyez sur F5 pour l'exécuter.")

    # ── MENU ─────────────────────────────────────────────────────────────────

    def _build_menu(self):
        bg, fg, hbg, hfg = t("bg1"), t("fg"), t("bg4"), t("accent")
        mb = tk.Menu(self, bg=bg, fg=fg, activebackground=hbg,
                     activeforeground=hfg, borderwidth=0, relief="flat")
        self.config(menu=mb)

        def add_menu(label, items):
            m = tk.Menu(mb, tearoff=0, bg=bg, fg=fg,
                        activebackground=hbg, activeforeground=hfg,
                        borderwidth=0, relief="flat")
            mb.add_cascade(label=label, menu=m)
            for item in items:
                if item is None:
                    m.add_separator()
                elif len(item) == 2:
                    m.add_command(label=item[0], command=item[1])
                elif len(item) == 3:
                    m.add_command(label=item[0], command=item[1], accelerator=item[2])
            return m

        add_menu("Fichier", [
            ("Nouveau",           self.new_tab,           "Ctrl+N"),
            ("Ouvrir…",           self._open_file,        "Ctrl+O"),
            ("Enregistrer",       self._save_file,        "Ctrl+S"),
            ("Enregistrer sous…", self._save_file_as,     ""),
            None,
            ("Exporter HTML",     lambda: self._exec_command("export_html"), ""),
            None,
            ("Quitter",           self.quit,              "Ctrl+Q"),
        ])

        add_menu("Édition", [
            ("Annuler",              lambda: self._active_text() and self._active_text().edit_undo(), "Ctrl+Z"),
            ("Refaire",              lambda: self._active_text() and self._active_text().edit_redo(), "Ctrl+Y"),
            None,
            ("Couper",               lambda: self.focus_get() and self.focus_get().event_generate("<<Cut>>"),   "Ctrl+X"),
            ("Copier",               lambda: self.focus_get() and self.focus_get().event_generate("<<Copy>>"),  "Ctrl+C"),
            ("Coller",               lambda: self.focus_get() and self.focus_get().event_generate("<<Paste>>"), "Ctrl+V"),
            None,
            ("Trouver / Remplacer",  self._toggle_find,    "Ctrl+F"),
            ("Spotlight Search",     lambda: self._exec_command("spotlight"), "Ctrl+Shift+F"),
            ("Aller à la ligne…",    lambda: self._exec_command("goto"),      "Ctrl+G"),
            None,
            ("Renommer Symbole",     lambda: self._exec_command("rename"),    ""),
            ("Métriques du Code",    lambda: self._exec_command("metrics"),   ""),
        ])

        vm = add_menu("Affichage", [
            ("Barre latérale",    self._toggle_sidebar, "Ctrl+B"),
            ("Minimap",           self._toggle_minimap, "Ctrl+M"),
            None,
            ("Terminal",          lambda: self._switch_console("Terminal"), ""),
            ("Output",            lambda: self._switch_console("Output"),   ""),
            ("Variables",         lambda: self._switch_console("Variables"),""),
            ("Turtle",            lambda: self._switch_console("Turtle"),   ""),
            None,
        ])
        tm = tk.Menu(vm, tearoff=0, bg=bg, fg=fg,
                     activebackground=hbg, activeforeground=hfg)
        vm.add_cascade(label="Thème", menu=tm)
        for k, td in THEMES.items():
            tm.add_command(label=td["name"], command=lambda key=k: self._set_theme(key))

        add_menu("Exécuter", [
            ("Exécuter",  self._run_code,  "F5 / Ctrl+R"),
            ("Arrêter",   self._stop_code, "Ctrl+."),
            None,
            ("TODOs",     lambda: self._exec_command("todos"),    ""),
            ("Git Status",lambda: self._exec_command("git_status"),""),
        ])

    # ── LAYOUT ───────────────────────────────────────────────────────────────

    def _build_layout(self):
        # Toolbar
        self._build_toolbar()
        # Body: [activity] [sidebar] [editor+bottom] [right panel]
        self.body = tk.Frame(self, bg=t("bg"))
        self.body.pack(fill="both", expand=True)

        self._build_activity_bar()
        self._build_sidebar()
        self._build_center()
        self._build_status_bar()

    def _build_toolbar(self):
        tb = tk.Frame(self, bg=t("bg1"), height=40)
        tb.pack(fill="x")
        tb.pack_propagate(False)

        # Logo
        tk.Label(tb, text=" RINT Studio ", bg=t("bg1"), fg=t("accent"),
                 font=("JetBrains Mono", 11, "bold")).pack(side="left", padx=(12,4))

        sep = tk.Frame(tb, bg=t("border"), width=1)
        sep.pack(side="left", fill="y", pady=8, padx=4)

        # Toolbar buttons
        tools = [
            ("📄", self.new_tab,        "New  Ctrl+N"),
            ("📂", self._open_file,     "Open  Ctrl+O"),
            ("💾", self._save_file,     "Save  Ctrl+S"),
            ("",  None, ""),
            ("▶", self._run_code,      "Run  F5"),
            ("⏹", self._stop_code,     "Stop  Ctrl+."),
            ("",  None, ""),
            ("🔍", self._toggle_find,   "Find  Ctrl+F"),
            ("⌘",  self._open_palette, "Palette  Ctrl+P"),
        ]
        for icon, cmd, tip in tools:
            if not icon:
                tk.Frame(tb, bg=t("border"), width=1).pack(side="left", fill="y", pady=8, padx=4)
                continue
            btn = tk.Button(tb, text=icon, command=cmd,
                            bg=t("bg1"), fg=t("fg"), relief="flat",
                            font=("Segoe UI", 11), padx=8, pady=4,
                            activebackground=t("bg4"), activeforeground=t("accent"),
                            cursor="hand2")
            btn.pack(side="left", padx=1)
            self._tooltip(btn, tip)

        # Theme quick-pick
        tk.Frame(tb, bg=t("border"), width=1).pack(side="right", fill="y", pady=8, padx=4)
        self._theme_label = tk.Label(tb, text=f"⬤  {THEMES[_T]['name']}", bg=t("bg1"),
                                     fg=t("accent"), font=F_UIS, cursor="hand2")
        self._theme_label.pack(side="right", padx=12)
        self._theme_label.bind("<Button-1>", lambda _: self._cycle_theme())

        tk.Frame(tb, bg=t("border"), width=1).pack(side="right", fill="y", pady=8, padx=4)

    def _tooltip(self, widget, text):
        def enter(_):
            tip = tk.Toplevel(self)
            tip.overrideredirect(True)
            tip.wm_attributes("-topmost", True)
            tk.Label(tip, text=text, bg=t("bg4"), fg=t("fg2"),
                     font=F_UIS, padx=6, pady=3).pack()
            x = widget.winfo_rootx() + 4
            y = widget.winfo_rooty() + widget.winfo_height() + 2
            tip.geometry(f"+{x}+{y}")
            widget._tip = tip
        def leave(_):
            if hasattr(widget, "_tip"):
                try: widget._tip.destroy()
                except: pass
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def _build_activity_bar(self):
        self.act = tk.Frame(self.body, bg=t("bg1"), width=44)
        self.act.pack(side="left", fill="y")
        self.act.pack_propagate(False)
        tk.Frame(self.act, bg=t("border"), height=1).pack(fill="x", pady=4)

        self.act_btns = {}
        icons = [("📁","explorer"),("🔍","search"),("🌿","git"),("🐛","debug"),("🧩","plugins")]
        for icon, key in icons:
            btn = tk.Button(self.act, text=icon, command=lambda k=key: self._switch_sidebar(k),
                            bg=t("bg1"), fg=t("fg3"), relief="flat",
                            font=("Segoe UI", 14), padx=0, pady=8, width=3,
                            activebackground=t("bg4"), activeforeground=t("accent"),
                            cursor="hand2")
            btn.pack(fill="x")
            self.act_btns[key] = btn
        self._active_panel = "explorer"
        self.act_btns["explorer"].configure(fg=t("accent"))

    def _build_sidebar(self):
        self.sidebar = tk.Frame(self.body, bg=t("bg1"), width=224)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar panels dict
        self.sb_panels = {}

        # Explorer panel
        ep = tk.Frame(self.sidebar, bg=t("bg1"))
        self.sb_panels["explorer"] = ep
        ep.pack(fill="both", expand=True)
        tk.Label(ep, text="EXPLORER", bg=t("bg1"), fg=t("fg3"),
                 font=F_UIS, pady=6).pack(fill="x", padx=12)

        btn_row = tk.Frame(ep, bg=t("bg1"))
        btn_row.pack(fill="x", padx=6)
        for icon, tip, cmd in [("📄","New File",self.new_tab),
                                ("📂","New Folder",lambda: None),
                                ("⟳","Refresh",self._refresh_tree)]:
            tk.Button(btn_row, text=icon, command=cmd,
                      bg=t("bg1"), fg=t("fg2"), relief="flat", font=F_UIS,
                      padx=4, activebackground=t("bg3")).pack(side="left")

        self.file_tree = tk.Listbox(ep, bg=t("bg1"), fg=t("fg"),
                                    selectbackground=t("sel"),
                                    selectforeground=t("fg"),
                                    font=F_UIS, borderwidth=0,
                                    highlightthickness=0, activestyle="none")
        self.file_tree.pack(fill="both", expand=True, padx=4, pady=4)
        self.file_tree.bind("<Double-1>", self._open_from_tree)
        self._refresh_tree()

        # Search panel
        sp = tk.Frame(self.sidebar, bg=t("bg1"))
        self.sb_panels["search"] = sp
        tk.Label(sp, text="SEARCH", bg=t("bg1"), fg=t("fg3"),
                 font=F_UIS, pady=6).pack(fill="x", padx=12)
        self.search_var = tk.StringVar()
        se = tk.Entry(sp, textvariable=self.search_var, bg=t("bg3"), fg=t("fg"),
                      font=F_CODE, insertbackground=t("accent"), relief="flat",
                      highlightthickness=1, highlightbackground=t("border"),
                      highlightcolor=t("accent"))
        se.pack(fill="x", padx=8, pady=4, ipady=5)
        se.bind("<Return>", lambda _: self._spotlight_do())
        tk.Button(sp, text="🔍 Search", command=self._spotlight_do,
                  bg=t("accent"), fg=t("bg"), relief="flat", font=F_UIB).pack(padx=8, pady=2, fill="x")
        self.search_results = tk.Listbox(sp, bg=t("bg1"), fg=t("fg2"),
                                         selectbackground=t("sel"),
                                         font=F_UIS, borderwidth=0,
                                         highlightthickness=0)
        self.search_results.pack(fill="both", expand=True, padx=4, pady=4)
        self.search_results.bind("<Double-1>", self._goto_search_result)

        # Git panel
        gp = tk.Frame(self.sidebar, bg=t("bg1"))
        self.sb_panels["git"] = gp
        hdr_g = tk.Frame(gp, bg=t("bg1"))
        hdr_g.pack(fill="x", padx=8, pady=6)
        tk.Label(hdr_g, text="GIT", bg=t("bg1"), fg=t("fg3"), font=F_UIS).pack(side="left")
        tk.Button(hdr_g, text="⟳", command=self._git_refresh,
                  bg=t("bg1"), fg=t("fg2"), relief="flat", font=F_UIS).pack(side="right")
        self.git_text = tk.Text(gp, bg=t("bg1"), fg=t("fg"), font=F_UIS,
                                borderwidth=0, highlightthickness=0,
                                state="disabled", wrap="word")
        self.git_text.pack(fill="both", expand=True, padx=4)
        btn_row_g = tk.Frame(gp, bg=t("bg1"))
        btn_row_g.pack(fill="x", padx=6, pady=4)
        for text, cmd in [("Status", self._git_refresh),
                          ("Log", lambda: self._git_cmd("log --oneline -10")),
                          ("Diff", lambda: self._git_cmd("diff"))]:
            tk.Button(btn_row_g, text=text, command=cmd,
                      bg=t("bg3"), fg=t("fg"), relief="flat", font=F_UIS,
                      padx=6, activebackground=t("accent"),
                      activeforeground=t("bg")).pack(side="left", padx=2)

        # Debug panel
        dp = tk.Frame(self.sidebar, bg=t("bg1"))
        self.sb_panels["debug"] = dp
        tk.Label(dp, text="DEBUG", bg=t("bg1"), fg=t("fg3"),
                 font=F_UIS, pady=6).pack(fill="x", padx=12)
        bp_lbl = tk.Label(dp, text="BREAKPOINTS", bg=t("bg1"), fg=t("fg3"), font=F_UIS)
        bp_lbl.pack(fill="x", padx=12)
        self.bp_list = tk.Listbox(dp, bg=t("bg1"), fg=t("red"),
                                   font=F_UIS, borderwidth=0, highlightthickness=0)
        self.bp_list.pack(fill="x", padx=4, pady=4)
        tk.Button(dp, text="Clear Breakpoints", command=self._clear_bps,
                  bg=t("bg3"), fg=t("fg"), relief="flat", font=F_UIS).pack(padx=8, fill="x")
        var_lbl = tk.Label(dp, text="VARIABLES", bg=t("bg1"), fg=t("fg3"), font=F_UIS)
        var_lbl.pack(fill="x", padx=12, pady=(12,0))
        self.watch_list = tk.Listbox(dp, bg=t("bg1"), fg=t("accent2"),
                                     font=F_CODES, borderwidth=0, highlightthickness=0)
        self.watch_list.pack(fill="both", expand=True, padx=4, pady=4)

        # Plugins panel
        pp = tk.Frame(self.sidebar, bg=t("bg1"))
        self.sb_panels["plugins"] = pp
        tk.Label(pp, text="EXTENSIONS", bg=t("bg1"), fg=t("fg3"),
                 font=F_UIS, pady=6).pack(fill="x", padx=12)
        plugins = [
            ("RINT Formatter",    "v1.2", True),
            ("Git Lens",          "v2.0", True),
            ("Bracket Colorizer", "v1.5", True),
            ("RINT Debugger",     "v3.1", True),
            ("Theme Builder",     "v1.0", False),
            ("Live Share",        "v0.9", False),
            ("Linter Pro",        "v2.3", False),
        ]
        for name, ver, installed in plugins:
            row = tk.Frame(pp, bg=t("bg1"))
            row.pack(fill="x", padx=8, pady=3)
            state = "✓" if installed else "↓"
            clr   = t("green") if installed else t("fg3")
            tk.Label(row, text=state, bg=t("bg1"), fg=clr, font=F_UIB).pack(side="left")
            tk.Label(row, text=f"  {name}", bg=t("bg1"), fg=t("fg"), font=F_UIS).pack(side="left")
            tk.Label(row, text=ver, bg=t("bg1"), fg=t("fg3"), font=F_UIS).pack(side="right")

        # Show default panel
        self._switch_sidebar("explorer", init=True)

    def _build_center(self):
        self.center = tk.Frame(self.body, bg=t("bg"))
        self.center.pack(side="left", fill="both", expand=True)

        # Tabs bar
        self.tabs_bar = tk.Frame(self.center, bg=t("bg1"), height=36)
        self.tabs_bar.pack(fill="x")
        self.tabs_bar.pack_propagate(False)

        self.tabs_inner = tk.Frame(self.tabs_bar, bg=t("bg1"))
        self.tabs_inner.pack(side="left", fill="both", expand=True)

        # Editor area (holds the active editor)
        self.editor_area = tk.Frame(self.center, bg=t("bg"))
        self.editor_area.pack(fill="both", expand=True)

        # Bottom panel
        self._build_bottom()

        # Right info panel
        self._build_right_panel()

        # Find panel (hidden by default)
        self.find_panel = FindReplacePanel(self.center, self._active_text)
        # Don't pack yet

    def _build_bottom(self):
        self.bottom = tk.Frame(self.center, bg=t("bg1"), height=220)
        self.bottom.pack(fill="x", side="bottom")
        self.bottom.pack_propagate(False)

        # Console tab bar
        self.con_bar = tk.Frame(self.bottom, bg=t("bg"), height=30)
        self.con_bar.pack(fill="x")
        self.con_bar.pack_propagate(False)

        self.con_btns = {}
        self.con_panels = {}
        for name in ["Output", "Terminal", "Variables", "Turtle", "TODOs"]:
            btn = tk.Button(self.con_bar, text=name, command=lambda n=name: self._switch_console(n),
                            bg=t("bg"), fg=t("fg3"), relief="flat", font=F_UIS,
                            padx=12, pady=4, activebackground=t("bg3"),
                            activeforeground=t("fg"), cursor="hand2")
            btn.pack(side="left", padx=1)
            self.con_btns[name] = btn

        # Resize handle
        sep = tk.Frame(self.con_bar, bg=t("border"), width=1)
        sep.pack(side="right", fill="y")
        tk.Button(self.con_bar, text="✕", command=self._toggle_bottom,
                  bg=t("bg"), fg=t("fg3"), relief="flat", font=F_UIS,
                  activebackground=t("red"), activeforeground=t("fg")).pack(side="right", padx=4)

        # Output panel
        out_frame = tk.Frame(self.bottom, bg=t("bg2"))
        self.output_text = tk.Text(out_frame, bg=t("bg2"), fg=t("fg"),
                                   font=F_CODES, borderwidth=0, highlightthickness=0,
                                   state="disabled", wrap="word", padx=12, pady=8)
        sb = tk.Scrollbar(out_frame, orient="vertical", command=self.output_text.yview,
                          bg=t("bg2"), troughcolor=t("bg2"), width=8)
        self.output_text.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.output_text.pack(fill="both", expand=True)
        self.output_text.tag_configure("out", foreground=t("fg"))
        self.output_text.tag_configure("log", foreground=t("accent2"))
        self.output_text.tag_configure("err", foreground=t("red"))
        self.output_text.tag_configure("hdr", foreground=t("accent"), font=F_UIB)
        btn_row = tk.Frame(out_frame, bg=t("bg1"))
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="Clear", command=self._clear_console,
                  bg=t("bg1"), fg=t("fg3"), relief="flat", font=F_UIS).pack(side="right", padx=4)
        self.con_panels["Output"] = out_frame

        # Terminal panel
        term_frame = tk.Frame(self.bottom, bg=t("bg"))
        self.term_text = tk.Text(term_frame, bg=t("bg"), fg=t("green"),
                                  font=F_CODES, borderwidth=0, highlightthickness=0,
                                  wrap="word", padx=12, pady=8,
                                  insertbackground=t("green"))
        self.term_text.pack(fill="both", expand=True)
        self.term_text.insert("end", f"RINT Studio Terminal  ·  {sys.platform}\n")
        self.term_text.insert("end", f"cwd: {self.term_cwd}\n$ ")
        self.term_text.mark_set("prompt_end", "end-1c")
        self.term_text.bind("<Return>",  self._term_exec)
        self.term_text.bind("<Up>",      self._term_hist_up)
        self.term_text.bind("<Down>",    self._term_hist_down)
        self.term_text.bind("<Control-c>", lambda _: self.term_text.insert("end", "\n$ "))
        self.con_panels["Terminal"] = term_frame

        # Variables panel
        var_frame = tk.Frame(self.bottom, bg=t("bg2"))
        self.var_text = tk.Text(var_frame, bg=t("bg2"), fg=t("accent"),
                                 font=F_CODES, borderwidth=0, highlightthickness=0,
                                 state="disabled", wrap="word", padx=12, pady=8)
        self.var_text.pack(fill="both", expand=True)
        self.var_text.tag_configure("name", foreground=t("accent"), font=("JetBrains Mono",9,"bold"))
        self.var_text.tag_configure("type", foreground=t("yellow"))
        self.var_text.tag_configure("val",  foreground=t("fg"))
        self.con_panels["Variables"] = var_frame

        # Turtle panel
        turtle_frame = tk.Frame(self.bottom, bg=t("bg2"))
        self.turtle_canvas = tk.Canvas(turtle_frame, bg=t("bg"), highlightthickness=0)
        self.turtle_canvas.pack(fill="both", expand=True)
        self.turtle_x, self.turtle_y = 400, 90
        self.turtle_angle = 0
        self.turtle_pen = True
        self._init_turtle()
        self.con_panels["Turtle"] = turtle_frame

        # TODOs panel
        todo_frame = tk.Frame(self.bottom, bg=t("bg2"))
        tk.Label(todo_frame, text="  TODO / FIXME / HACK / NOTE",
                 bg=t("bg2"), fg=t("fg3"), font=F_UIS).pack(fill="x", pady=4)
        self.todo_list = tk.Listbox(todo_frame, bg=t("bg2"), fg=t("yellow"),
                                     selectbackground=t("sel"),
                                     font=F_UIS, borderwidth=0, highlightthickness=0)
        self.todo_list.pack(fill="both", expand=True, padx=4, pady=4)
        self.todo_list.bind("<Double-1>", self._goto_todo)
        tk.Button(todo_frame, text="⟳ Refresh", command=self._refresh_todos,
                  bg=t("bg3"), fg=t("fg"), relief="flat", font=F_UIS).pack(pady=4)
        self.con_panels["TODOs"] = todo_frame

        self._switch_console("Output")

    def _build_right_panel(self):
        self.right = tk.Frame(self.body, bg=t("bg1"), width=230)
        self.right.pack(side="right", fill="y")
        self.right.pack_propagate(False)

        tab_bar = tk.Frame(self.right, bg=t("bg"), height=32)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)
        self.rp_btns = {}
        self.rp_panels = {}

        for icon, key in [("📊","stats"), ("📝","outline"), ("⚡","perf")]:
            btn = tk.Button(tab_bar, text=icon,
                            command=lambda k=key: self._switch_rp(k),
                            bg=t("bg"), fg=t("fg3"), relief="flat",
                            font=("Segoe UI", 12), padx=8, pady=4,
                            activebackground=t("bg3"),
                            activeforeground=t("accent"), cursor="hand2")
            btn.pack(side="left")
            self.rp_btns[key] = btn

        # Stats panel
        sp = tk.Frame(self.right, bg=t("bg1"))
        self.rp_panels["stats"] = sp
        tk.Label(sp, text="MEMORY", bg=t("bg1"), fg=t("fg3"),
                 font=("Segoe UI",8,"bold"), pady=4).pack(fill="x", padx=8)
        self.ram_canvas = tk.Canvas(sp, bg=t("bg"), highlightthickness=0, height=70)
        self.ram_canvas.pack(fill="x", padx=4, pady=4)
        tk.Label(sp, text="CODE METRICS", bg=t("bg1"), fg=t("fg3"),
                 font=("Segoe UI",8,"bold"), pady=4).pack(fill="x", padx=8)
        self.metrics_text = tk.Text(sp, bg=t("bg1"), fg=t("fg2"),
                                     font=F_UIS, height=8, borderwidth=0,
                                     highlightthickness=0, state="disabled", padx=8)
        self.metrics_text.pack(fill="x")

        # Outline panel
        op = tk.Frame(self.right, bg=t("bg1"))
        self.rp_panels["outline"] = op
        hdr_o = tk.Frame(op, bg=t("bg1"))
        hdr_o.pack(fill="x", padx=8, pady=4)
        tk.Label(hdr_o, text="OUTLINE", bg=t("bg1"), fg=t("fg3"),
                 font=("Segoe UI",8,"bold")).pack(side="left")
        tk.Button(hdr_o, text="⟳", command=self._refresh_outline,
                  bg=t("bg1"), fg=t("fg3"), relief="flat", font=F_UIS).pack(side="right")
        self.outline_tree = tk.Listbox(op, bg=t("bg1"), fg=t("fg"),
                                       selectbackground=t("sel"),
                                       font=F_UIS, borderwidth=0, highlightthickness=0)
        self.outline_tree.pack(fill="both", expand=True, padx=4, pady=4)
        self.outline_tree.bind("<Double-1>", self._goto_outline)

        # Performance panel
        pf = tk.Frame(self.right, bg=t("bg1"))
        self.rp_panels["perf"] = pf
        tk.Label(pf, text="PERFORMANCE", bg=t("bg1"), fg=t("fg3"),
                 font=("Segoe UI",8,"bold"), pady=4).pack(fill="x", padx=8)
        self.perf_canvas = tk.Canvas(pf, bg=t("bg"), highlightthickness=0, height=100)
        self.perf_canvas.pack(fill="x", padx=4, pady=4)
        self.perf_text = tk.Text(pf, bg=t("bg1"), fg=t("fg2"),
                                  font=F_UIS, borderwidth=0,
                                  highlightthickness=0, state="disabled",
                                  padx=8, height=8)
        self.perf_text.pack(fill="x")

        self._switch_rp("stats")

    def _build_status_bar(self):
        self.status_bar = tk.Frame(self, bg=t("status"), height=22)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)
        self.st_left  = tk.Label(self.status_bar, text="✓ Ready", bg=t("status"),
                                  fg="#fff", font=F_UIS)
        self.st_left.pack(side="left", padx=12)
        self.st_right = tk.Label(self.status_bar, text="", bg=t("status"),
                                  fg="#FFFFFF", font=F_UIS)
        self.st_right.pack(side="right", padx=12)
        self.st_center = tk.Label(self.status_bar, text="RINT  ·  UTF-8",
                                   bg=t("status"), fg="#ccc", font=F_UIS)
        self.st_center.pack(side="right", padx=12)

    # ── TAB SYSTEM ──────────────────────────────────────────────────────────

    def new_tab(self, content="", filename=None):
        idx = len(self.tabs)
        name = filename or f"untitled_{idx+1}.rint"
        tab_data = {
            "name": name, "path": None, "modified": False,
            "frame": None, "text": None, "highlighter": None,
            "linenums": None, "minimap": None, "tab_btn": None, "close_btn": None,
            "bookmarks": set(), "scroll_pos": "1.0",
        }

        # Tab button frame
        tf = tk.Frame(self.tabs_inner, bg=t("bg1"))
        tf.pack(side="left")
        dot = tk.Label(tf, text="", bg=t("tab_idle"), fg=t("yellow"),
                       font=("Segoe UI",8))
        dot.pack(side="left", padx=(6,0))
        tab_data["dot"] = dot
        btn = tk.Button(tf, text=name, command=lambda i=idx: self._select_tab(i),
                        bg=t("tab_idle"), fg=t("fg2"), relief="flat",
                        font=F_UIS, padx=6, pady=6, cursor="hand2",
                        activebackground=t("tab_active"), activeforeground=t("fg"))
        btn.pack(side="left")
        x_btn = tk.Button(tf, text="×", command=lambda i=idx: self._close_tab(i),
                          bg=t("tab_idle"), fg=t("fg3"), relief="flat",
                          font=F_UIS, padx=4, pady=6, cursor="hand2",
                          activebackground=t("red"), activeforeground="#fff")
        x_btn.pack(side="left", padx=(0,4))
        tab_data["tab_frame"] = tf
        tab_data["tab_btn"]   = btn
        tab_data["close_btn"] = x_btn

        # Editor frame
        ef = tk.Frame(self.editor_area, bg=t("bg"))
        # Find panel placeholder per-tab (shared)
        editor_row = tk.Frame(ef, bg=t("bg"))
        editor_row.pack(fill="both", expand=True)

        # Line numbers
        lf = tk.Frame(editor_row, bg=t("gutter"))
        lf.pack(side="left", fill="y")

        # Text widget
        txt = tk.Text(editor_row, bg=t("bg"), fg=t("fg"),
                      font=F_CODE, borderwidth=0, highlightthickness=0,
                      insertbackground=t("accent"),
                      selectbackground=t("sel"), selectforeground=t("fg"),
                      undo=True, autoseparators=True, maxundo=-1,
                      wrap="none", padx=8, pady=4,
                      tabs=("28p",), spacing1=2, spacing3=2)
        txt_sb = tk.Scrollbar(editor_row, orient="vertical", command=txt.yview,
                               bg=t("bg"), troughcolor=t("bg"), width=8)
        txt_x  = tk.Scrollbar(ef, orient="horizontal",
                      command=txt.xview,
                      bg=t("bg"), troughcolor=t("bg"), width=8)
        txt.configure(yscrollcommand=txt_sb.set, xscrollcommand=txt_x.set)
        txt_x.pack(fill="x", side="bottom")
        txt_sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)

        # Minimap
        mm_frame = tk.Frame(editor_row, bg=t("bg"))
        mm_frame.pack(side="right", fill="y")
        mm = Minimap(mm_frame, txt)
        mm.pack(fill="both", expand=True)

        ln = LineNumbers(lf, txt)
        ln.pack(fill="both", expand=True)

        hi = SyntaxHighlighter(txt)

        tab_data.update({"frame": ef, "text": txt, "highlighter": hi,
                         "linenums": ln, "minimap": mm,
                         "minimap_frame": mm_frame})

        # Bindings
        def on_key(_=None, i=idx):
            self.tabs[i]["modified"] = True
            self.tabs[i]["dot"].configure(text="●")
            hi.highlight()
            ln.redraw()
            mm.schedule_redraw()
            self._update_cursor_pos()
            self._update_metrics()

        def on_click(_=None):
            hi._highlight_current_line()
            ln.redraw()
            self._update_cursor_pos()

        txt.bind("<KeyRelease>", on_key)
        txt.bind("<ButtonRelease>", on_click)
        txt.bind("<Tab>", self._handle_tab)
        txt.bind("<Return>", self._handle_enter)
        txt.bind("<Control-space>", self._trigger_autocomplete)
        txt.bind(".", lambda e, i=idx: self._check_dot_complete(e, i))

        # Insert content
        if content:
            txt.insert("1.0", content)
            hi.highlight()

        self.tabs.append(tab_data)
        self._select_tab(idx)
        return idx

    def _select_tab(self, idx):
        if idx < 0 or idx >= len(self.tabs): return
        # Hide all editor frames
        for i, tab in enumerate(self.tabs):
            tab["frame"].pack_forget()
            tab["tab_btn"].configure(bg=t("tab_idle"), fg=t("fg3"))
            tab["close_btn"].configure(bg=t("tab_idle"))
            tab["tab_frame"].configure(bg=t("tab_idle"))
            tab["dot"].configure(bg=t("tab_idle"))

        self.active_tab = idx
        tab = self.tabs[idx]
        tab["frame"].pack(fill="both", expand=True)
        tab["tab_btn"].configure(bg=t("tab_active"), fg=t("fg"))
        tab["close_btn"].configure(bg=t("tab_active"))
        tab["tab_frame"].configure(bg=t("tab_active"))
        tab["dot"].configure(bg=t("tab_active"))
        tab["text"].focus_set()
        tab["linenums"].redraw()
        tab["minimap"].schedule_redraw()
        self._update_cursor_pos()
        self._update_metrics()

    def _close_tab(self, idx):
        if len(self.tabs) == 1:
            self.tabs[0]["text"].delete("1.0", "end")
            self.tabs[0]["modified"] = False
            self.tabs[0]["dot"].configure(text="")
            return
        tab = self.tabs[idx]
        if tab["modified"]:
            r = messagebox.askyesnocancel("Fermer", f"Enregistrer '{tab['name']}' avant de fermer ?")
            if r is None: return
            if r: self._save_file()
        tab["frame"].pack_forget()
        tab["tab_frame"].pack_forget()
        self.tabs.pop(idx)
        new = max(0, idx - 1)
        self._select_tab(new)

    def _active_text(self):
        if self.active_tab < 0 or self.active_tab >= len(self.tabs): return None
        return self.tabs[self.active_tab]["text"]

    def _active_tab_data(self):
        if self.active_tab < 0 or self.active_tab >= len(self.tabs): return None
        return self.tabs[self.active_tab]

    # ── KEYBOARD SHORTCUTS ──────────────────────────────────────────────────

    def _bind_keys(self):
        self.bind("<Control-r>",         lambda _: self._run_code())
        self.bind("<F5>",                lambda _: self._run_code())
        self.bind("<Control-period>",    lambda _: self._stop_code())
        self.bind("<Control-s>",         lambda _: self._save_file())
        self.bind("<Control-o>",         lambda _: self._open_file())
        self.bind("<Control-n>",         lambda _: self.new_tab())
        self.bind("<Control-p>",         lambda _: self._open_palette())
        self.bind("<Control-b>",         lambda _: self._toggle_sidebar())
        self.bind("<Control-m>",         lambda _: self._toggle_minimap())
        self.bind("<Control-f>",         lambda _: self._toggle_find())
        self.bind("<Control-F>",         lambda _: self._exec_command("spotlight"))
        self.bind("<Control-Shift-f>",   lambda _: self._exec_command("spotlight"))
        self.bind("<Control-g>",         lambda _: self._exec_command("goto"))
        self.bind("<Control-F2>",        lambda _: self._toggle_bookmark())
        self.bind("<F2>",                lambda _: self._next_bookmark())
        self.bind("<Control-q>",         lambda _: self.quit())
        self.bind("<Control-grave>",     lambda _: self._switch_console("Terminal"))
        self.bind("<Control-w>",         lambda _: self._close_tab(self.active_tab))

    # ── EDITOR HELPERS ──────────────────────────────────────────────────────

    def _handle_tab(self, event):
        tw = event.widget
        tw.insert("insert", "    ")
        return "break"

    def _handle_enter(self, event):
        tw = event.widget
        line = tw.get("insert linestart", "insert")
        indent = len(line) - len(line.lstrip())
        if line.rstrip().endswith("{"):
            indent += 4
        tw.insert("insert", "\n" + " " * indent)
        return "break"

    def _trigger_autocomplete(self, event=None):
        tw = self._active_text()
        if not tw: return
        word = self._get_current_word(tw)
        if len(word) < 1: return
        matches = [c for c in COMPLETIONS if c.startswith(word)]
        if not matches: return
        x = tw.winfo_rootx() + int(tw.bbox("insert")[0])
        y = tw.winfo_rooty() + int(tw.bbox("insert")[1]) + 20
        if not hasattr(self, "_ac_popup"):
            self._ac_popup = AutocompletePopup(self, self._insert_completion)
        self._ac_popup.show(x, y, matches)
        tw.bind("<Down>",   lambda _: self._ac_popup.navigate(1), "+")
        tw.bind("<Up>",     lambda _: self._ac_popup.navigate(-1), "+")
        tw.bind("<Escape>", lambda _: self._ac_popup.hide(), "+")
        return "break"

    def _check_dot_complete(self, event, idx):
        """Trigger autocomplete after a dot"""
        self.after(10, self._trigger_autocomplete)

    def _get_current_word(self, tw):
        pos = tw.index("insert")
        line_start = f"{pos.split('.')[0]}.0"
        text_before = tw.get(line_start, pos)
        m = re.search(r'[\w.]+$', text_before)
        return m.group(0) if m else ""

    def _insert_completion(self, item):
        tw = self._active_text()
        if not tw: return
        word = self._get_current_word(tw)
        pos  = tw.index("insert")
        # Remove current word
        start = f"{pos} - {len(word)} chars"
        tw.delete(start, pos)
        tw.insert("insert", item)
        if hasattr(self, "_ac_popup"):
            self._ac_popup.hide()

    # ── FILE OPERATIONS ─────────────────────────────────────────────────────

    def _open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("RINT files","*.rint"),("All files","*.*")])
        if not path: return
        with open(path, encoding="utf-8") as f:
            content = f.read()
        idx = self.new_tab(content, Path(path).name)
        self.tabs[idx]["path"] = path
        self.tabs[idx]["modified"] = False
        self.tabs[idx]["dot"].configure(text="")
        self._refresh_tree()

    def _save_file(self):
        tab = self._active_tab_data()
        if not tab: return
        path = tab["path"]
        if not path:
            path = filedialog.asksaveasfilename(
                defaultextension=".rint",
                filetypes=[("RINT files","*.rint"),("All","*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(tab["text"].get("1.0","end-1c"))
            tab["path"] = path
            tab["name"] = Path(path).name
            tab["modified"] = False
            tab["dot"].configure(text="")
            tab["tab_btn"].configure(text=tab["name"])
            self.st_left.configure(text=f"💾 Saved: {tab['name']}")
            self._refresh_tree()

    def _save_file_as(self):
        tab = self._active_tab_data()
        if not tab: return
        tab["path"] = None
        self._save_file()

    def _open_from_tree(self, event):
        sel = self.file_tree.curselection()
        if not sel: return
        item = self.file_tree.get(sel[0]).strip().lstrip("📄 ").lstrip("📂 ")
        if item.endswith("/"): return
        path = Path(self.term_cwd) / item
        if path.exists():
            with open(path, encoding="utf-8", errors="replace") as f:
                content = f.read()
            idx = self.new_tab(content, item)
            self.tabs[idx]["path"] = str(path)

    def _refresh_tree(self):
        self.file_tree.delete(0, "end")
        try:
            cwd = Path(self.term_cwd)
            entries = sorted(cwd.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
            for p in entries:
                if p.name.startswith("."): continue
                icon = "📄 " if p.is_file() else "📂 "
                self.file_tree.insert("end", f"{icon}{p.name}")
        except Exception as e:
            self.file_tree.insert("end", f"Error: {e}")

    # ── RUN CODE ────────────────────────────────────────────────────────────

    def _run_code(self):
        if self._running:
            self._console_err("Already running!")
            return
        tab = self._active_tab_data()
        if not tab: return
        code = tab["text"].get("1.0", "end-1c")
        self._clear_console()
        self._switch_console("Output")
        self._console_out(f"▶  Running '{tab['name']}'…")

        self.mem_monitor.reset()
        self._running = True
        self.st_left.configure(text="▶ Running…")

        def _thread():
            def sample():
                while self._running:
                    self.mem_monitor.sample()
                    time.sleep(0.15)

            sampler = threading.Thread(target=sample, daemon=True)
            sampler.start()

            try:
                self.interp.run(code)
            except Exception as e:
                self.after(0, self._console_err, str(e))
            finally:
                self._running = False
                self.after(0, self._run_done)

        threading.Thread(target=_thread, daemon=True).start()

    def _run_done(self):
        stats = self.mem_monitor.get_stats()
        if stats:
            self._console_out(f"\n─────────────────────────────────")
            self._console_out(f"  Peak code mem : {stats['peak_code']} MB")
            self._console_out(f"  Samples       : {stats['samples']}")
            self._console_out(f"─────────────────────────────────")
            self._draw_perf_graph()
        self.st_left.configure(text="✓ Done")
        self._refresh_outline()
        self._refresh_todos()

    def _stop_code(self):
        self.interp.running = False
        self._running = False
        self.st_left.configure(text="⏹ Stopped")

    # ── CONSOLE ─────────────────────────────────────────────────────────────

    def _console_out(self, msg):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", msg + "\n", "out")
        self.output_text.configure(state="disabled")
        self.output_text.see("end")

    def _console_log(self, msg):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"  {msg}\n", "log")
        self.output_text.configure(state="disabled")
        self.output_text.see("end")

    def _console_err(self, msg):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"✗  {msg}\n", "err")
        self.output_text.configure(state="disabled")
        self.output_text.see("end")
        self._switch_console("Output")

    def _clear_console(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")

    def _switch_console(self, name):
        for n, p in self.con_panels.items():
            p.pack_forget()
            self.con_btns[n].configure(bg=t("bg"), fg=t("fg3"))
        self.con_panels[name].pack(fill="both", expand=True)
        self.con_btns[name].configure(bg=t("bg3"), fg=t("fg"))

    def _toggle_bottom(self):
        if self.bottom.winfo_viewable():
            self.bottom.pack_forget()
        else:
            self.bottom.pack(fill="x", side="bottom")

    # ── TERMINAL ────────────────────────────────────────────────────────────

    def _term_exec(self, event=None):
        tw = self.term_text
        try:
            cmd_start = tw.search("$ ", "end-1c linestart", backwards=True)
            if not cmd_start: return "break"
            cmd_start = f"{cmd_start} + 2 chars"
            cmd = tw.get(cmd_start, "end-1c").strip()
        except:
            cmd = ""

        if not cmd:
            tw.insert("end", "\n$ ")
            return "break"

        self.term_hist.append(cmd)
        self.term_idx = len(self.term_hist)
        tw.insert("end", "\n")

        # Handle cd
        if cmd.startswith("cd "):
            target = cmd[3:].strip().strip('"').strip("'")
            try:
                if target == "~": target = str(Path.home())
                new_path = (Path(self.term_cwd) / target).resolve()
                if new_path.is_dir():
                    self.term_cwd = str(new_path)
                    tw.insert("end", f"cwd: {self.term_cwd}\n$ ")
                    self._refresh_tree()
                else:
                    tw.insert("end", f"cd: no such directory: {target}\n$ ")
            except Exception as e:
                tw.insert("end", f"cd error: {e}\n$ ")
        elif cmd.strip() == "clear":
            tw.delete("1.0", "end")
            tw.insert("end", f"cwd: {self.term_cwd}\n$ ")
        else:
            def run_cmd():
                try:
                    result = subprocess.run(
                        cmd, shell=True, capture_output=True,
                        text=True, cwd=self.term_cwd, timeout=30,
                        encoding="utf-8", errors="replace"
                    )
                    out = result.stdout + result.stderr
                    self.after(0, self._term_output, out)
                except subprocess.TimeoutExpired:
                    self.after(0, self._term_output, "Command timed out (30s)\n")
                except Exception as e:
                    self.after(0, self._term_output, f"Error: {e}\n")

            threading.Thread(target=run_cmd, daemon=True).start()

        return "break"

    def _term_output(self, text):
        tw = self.term_text
        tw.insert("end", text if text else "(no output)\n")
        tw.insert("end", "$ ")
        tw.see("end")

    def _term_hist_up(self, event):
        if not self.term_hist: return "break"
        self.term_idx = max(0, self.term_idx - 1)
        self._term_set_cmd(self.term_hist[self.term_idx])
        return "break"

    def _term_hist_down(self, event):
        if not self.term_hist: return "break"
        self.term_idx = min(len(self.term_hist), self.term_idx + 1)
        cmd = self.term_hist[self.term_idx] if self.term_idx < len(self.term_hist) else ""
        self._term_set_cmd(cmd)
        return "break"

    def _term_set_cmd(self, cmd):
        tw = self.term_text
        try:
            prompt_pos = tw.search("$ ", "end-1c linestart", backwards=True)
            if prompt_pos:
                tw.delete(f"{prompt_pos} + 2 chars", "end")
                tw.insert("end", cmd)
        except:
            pass

    # ── UPDATE VARIABLE PANEL ────────────────────────────────────────────────

    def _update_var(self, name, value, type_):
        vt = self.var_text
        vt.configure(state="normal")
        # Check if variable already exists in text and update
        content = vt.get("1.0", "end")
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith(f"{name}"):
                vt.delete(f"{i+1}.0", f"{i+2}.0")
                break
        vt.insert("end", f"{name}", "name")
        vt.insert("end", f"  ::{type_}  ", "type")
        vt.insert("end", f"= {repr(value)}\n", "val")
        vt.configure(state="disabled")
        vt.see("end")
        # Also update the watch list in debug panel
        self._refresh_debug_vars()

    def _refresh_debug_vars(self):
        self.watch_list.delete(0, "end")
        for name, val in self.interp.vars.items():
            tp = self.interp.vtypes.get(name, "var")
            self.watch_list.insert("end", f"{tp} {name} = {repr(val)}")

    # ── TURTLE ──────────────────────────────────────────────────────────────

    def _init_turtle(self):
        c = self.turtle_canvas
        c.delete("all")
        c.configure(bg=t("bg"))
        w = 800; h = 160
        c.create_line(w//2, 0, w//2, h, fill=t("bg3"), dash=(4,4))
        c.create_line(0, h//2, w, h//2, fill=t("bg3"), dash=(4,4))
        self.turtle_x, self.turtle_y = w//2, h//2
        self.turtle_angle = 0
        self.turtle_pen = True

    def _turtle_cmd(self, cmd, args):
        c = self.turtle_canvas
        try:
            if cmd == "move":
                dist = float(args) if args else 50
                import math as m_
                nx = self.turtle_x + dist * m_.cos(m_.radians(self.turtle_angle))
                ny = self.turtle_y - dist * m_.sin(m_.radians(self.turtle_angle))
                if self.turtle_pen:
                    c.create_line(self.turtle_x, self.turtle_y, nx, ny,
                                  fill=t("accent"), width=2)
                self.turtle_x, self.turtle_y = nx, ny
            elif cmd == "right":
                self.turtle_angle -= float(args or 90)
            elif cmd == "left":
                self.turtle_angle += float(args or 90)
            elif cmd == "pen":
                self.turtle_pen = "down" in (args or "").lower()
            elif cmd == "clear":
                self._init_turtle()
        except Exception as e:
            self._console_err(f"Turtle error: {e}")

    # ── FIND & REPLACE ──────────────────────────────────────────────────────

    def _toggle_find(self):
        if self.find_panel.winfo_ismapped():
            self.find_panel.pack_forget()
        else:
            self.find_panel.pack(fill="x", before=self.editor_area)
            self.find_panel.focus()

    # ── BOOKMARKS ───────────────────────────────────────────────────────────

    def _toggle_bookmark(self):
        tab = self._active_tab_data()
        if not tab: return
        line = int(tab["text"].index("insert").split(".")[0])
        ln = tab["linenums"]
        if line in ln.marks:
            ln.marks.discard(line)
            tab["text"].tag_remove("bookmark_line", f"{line}.0", f"{line}.end+1c")
        else:
            ln.marks.add(line)
            tab["text"].tag_add("bookmark_line", f"{line}.0", f"{line}.end+1c")
        ln.redraw()
        self.st_left.configure(text=f"{'📌 Bookmark added' if line in ln.marks else '🗑 Bookmark removed'} — Line {line}")

    def _next_bookmark(self):
        tab = self._active_tab_data()
        if not tab: return
        marks = sorted(tab["linenums"].marks)
        if not marks: return
        cur = int(tab["text"].index("insert").split(".")[0])
        after = [m for m in marks if m > cur]
        target = after[0] if after else marks[0]
        tab["text"].see(f"{target}.0")
        tab["text"].mark_set("insert", f"{target}.0")

    # ── SPOTLIGHT SEARCH ────────────────────────────────────────────────────

    def _spotlight_do(self):
        query = self.search_var.get().strip()
        if not query: return
        self.search_results.delete(0, "end")
        found = 0
        try:
            cwd = Path(self.term_cwd)
            for fpath in list(cwd.glob("*.rint")) + list(cwd.rglob("*.rint")):
                try:
                    with open(fpath, encoding="utf-8", errors="replace") as f:
                        for i, line in enumerate(f, 1):
                            if query.lower() in line.lower():
                                self.search_results.insert("end",
                                    f"{fpath.name}:{i}  {line.strip()[:50]}")
                                found += 1
                                if found >= 200: break
                except: pass
        except: pass
        # Also search current editor
        tab = self._active_tab_data()
        if tab:
            code = tab["text"].get("1.0", "end-1c")
            for i, line in enumerate(code.split("\n"), 1):
                if query.lower() in line.lower():
                    self.search_results.insert("end",
                        f"[current]:{i}  {line.strip()[:50]}")
                    found += 1
        if found == 0:
            self.search_results.insert("end", "No results found.")

    def _goto_search_result(self, event):
        sel = self.search_results.curselection()
        if not sel: return
        item = self.search_results.get(sel[0])
        m = re.match(r'^(.+?):(\d+)', item)
        if not m: return
        fname, line = m.group(1), int(m.group(2))
        if fname == "[current]":
            tab = self._active_tab_data()
            if tab:
                tab["text"].see(f"{line}.0")
                tab["text"].mark_set("insert", f"{line}.0")
        else:
            path = Path(self.term_cwd) / fname
            if path.exists():
                with open(path, encoding="utf-8", errors="replace") as f:
                    content = f.read()
                idx = self.new_tab(content, fname)
                self.tabs[idx]["path"] = str(path)
                self.tabs[idx]["text"].see(f"{line}.0")

    # ── OUTLINE ─────────────────────────────────────────────────────────────

    def _refresh_outline(self):
        self.outline_tree.delete(0, "end")
        tab = self._active_tab_data()
        if not tab: return
        code = tab["text"].get("1.0", "end-1c")
        for i, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()
            if stripped.startswith("func "):
                m = re.match(r'^func\s+(\w+)\s*\(([^)]*)\)', stripped)
                if m: self.outline_tree.insert("end", f"  ƒ  {m.group(1)}({m.group(2)})  :{i}")
            elif stripped.startswith("class "):
                m = re.match(r'^class\s+(\w+)', stripped)
                if m: self.outline_tree.insert("end", f"  ◆  {m.group(1)}  :{i}")
            elif re.match(r'^(int|string|bool|float|auto)\s+\w+\s*=', stripped):
                m = re.match(r'^(\w+)\s+(\w+)\s*=', stripped)
                if m: self.outline_tree.insert("end", f"    ·  {m.group(2)}  :{i}")

    def _goto_outline(self, event):
        sel = self.outline_tree.curselection()
        if not sel: return
        item = self.outline_tree.get(sel[0])
        m = re.search(r':(\d+)$', item)
        if not m: return
        line = int(m.group(1))
        tab = self._active_tab_data()
        if tab:
            tab["text"].see(f"{line}.0")
            tab["text"].mark_set("insert", f"{line}.0")

    # ── TODO TRACKER ────────────────────────────────────────────────────────

    def _refresh_todos(self):
        self.todo_list.delete(0, "end")
        tab = self._active_tab_data()
        if not tab: return
        code = tab["text"].get("1.0", "end-1c")
        patterns = ["TODO", "FIXME", "HACK", "NOTE", "XXX", "BUG"]
        for i, line in enumerate(code.split("\n"), 1):
            for p in patterns:
                if p in line.upper():
                    self.todo_list.insert("end", f"  {p}  :{i}  {line.strip()[:55]}")
                    break

    def _goto_todo(self, event):
        sel = self.todo_list.curselection()
        if not sel: return
        item = self.todo_list.get(sel[0])
        m = re.search(r':(\d+)\s', item)
        if not m: return
        line = int(m.group(1))
        tab = self._active_tab_data()
        if tab:
            tab["text"].see(f"{line}.0")
            tab["text"].mark_set("insert", f"{line}.0")
            self._switch_console("TODOs")

    # ── GIT ─────────────────────────────────────────────────────────────────

    def _git_refresh(self):
        self._git_cmd("status")

    def _git_cmd(self, cmd):
        def run():
            try:
                result = subprocess.run(
                    f"git {cmd}", shell=True, capture_output=True,
                    text=True, cwd=self.term_cwd, timeout=10,
                    encoding="utf-8", errors="replace"
                )
                out = result.stdout or result.stderr or "(no output)"
                self.after(0, self._git_display, f"$ git {cmd}\n{out}")
            except Exception as e:
                self.after(0, self._git_display, f"Git error: {e}\n(Not a git repository?)")

        threading.Thread(target=run, daemon=True).start()

    def _git_display(self, text):
        self.git_text.configure(state="normal")
        self.git_text.delete("1.0", "end")
        self.git_text.insert("1.0", text)
        self.git_text.configure(state="disabled")

    # ── CODE METRICS ────────────────────────────────────────────────────────

    def _update_metrics(self):
        tab = self._active_tab_data()
        if not tab: return
        code = tab["text"].get("1.0", "end-1c")
        lines = code.split("\n")
        n_lines  = len(lines)
        n_code   = sum(1 for l in lines if l.strip() and not l.strip().startswith("//"))
        n_cmts   = sum(1 for l in lines if l.strip().startswith("//"))
        n_blank  = sum(1 for l in lines if not l.strip())
        n_funcs  = len(re.findall(r'^\s*func\s+\w+', code, re.MULTILINE))
        n_cls    = len(re.findall(r'^\s*class\s+\w+', code, re.MULTILINE))
        n_vars   = len(re.findall(r'^\s*(int|string|bool|float|auto)\s+\w+\s*=', code, re.MULTILINE))
        n_chars  = len(code)
        complexity = n_funcs + len(re.findall(r'\b(if|while|when|elif)\b', code))

        self.metrics_text.configure(state="normal")
        self.metrics_text.delete("1.0", "end")
        self.metrics_text.insert("end",
            f"Lines      {n_lines:>6}\n"
            f"Code       {n_code:>6}\n"
            f"Comments   {n_cmts:>6}\n"
            f"Blank      {n_blank:>6}\n"
            f"─────────────────\n"
            f"Functions  {n_funcs:>6}\n"
            f"Classes    {n_cls:>6}\n"
            f"Variables  {n_vars:>6}\n"
            f"─────────────────\n"
            f"Chars      {n_chars:>6}\n"
            f"Complexity {complexity:>6}\n"
        )
        self.metrics_text.configure(state="disabled")

    # ── EXPORT HTML ──────────────────────────────────────────────────────────

    def _export_html(self):
        tab = self._active_tab_data()
        if not tab: return
        code = tab["text"].get("1.0", "end-1c")
        path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML","*.html"),("All","*.*")],
            initialfile=tab["name"].replace(".rint", ".html"))
        if not path: return

        # Build highlighted HTML
        html_code = code
        # Escape HTML
        html_code = html_code.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>{tab['name']} — RINT Studio Export</title>
<style>
  body {{ background: {t('bg')}; margin: 0; padding: 40px; }}
  .header {{ color: {t('accent')}; font-family: 'JetBrains Mono', monospace; font-size:11px;
             letter-spacing:0.1em; text-transform:uppercase; margin-bottom:20px; }}
  pre {{ font-family: 'JetBrains Mono', Consolas, monospace; font-size: 13px;
         line-height: 1.7; color: {t('fg')}; background: {t('bg2')};
         padding: 28px; border-radius: 12px; overflow-x: auto;
         border: 1px solid {t('border')}; }}
  .ln {{ color: {t('gutter_fg')}; user-select:none; margin-right:20px; }}
</style>
</head>
<body>
<div class="header">// {tab['name']} — exported from RINT Studio v6.0 — {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
<pre>"""
        for i, line in enumerate(html_code.split("\n"), 1):
            html += f'<span class="ln">{i:>4}</span>{line}\n'
        html += "</pre></body></html>"

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open(f"file://{path}")
        self.st_left.configure(text=f"✓ Exported: {Path(path).name}")

    # ── RENAME SYMBOL ───────────────────────────────────────────────────────

    def _rename_symbol(self):
        tab = self._active_tab_data()
        if not tab: return
        tw = tab["text"]
        # Get word at cursor
        pos = tw.index("insert")
        line_content = tw.get(f"{pos.split('.')[0]}.0", f"{pos.split('.')[0]}.end")
        col = int(pos.split(".")[1])
        # Find word boundaries
        start = col
        while start > 0 and (line_content[start-1].isalnum() or line_content[start-1] == "_"):
            start -= 1
        end = col
        while end < len(line_content) and (line_content[end].isalnum() or line_content[end] == "_"):
            end += 1
        old_name = line_content[start:end]
        if not old_name:
            messagebox.showwarning("Rename", "Aucun symbole sélectionné.")
            return
        new_name = simpledialog.askstring("Rename Symbol",
                                          f"Renommer '{old_name}' en :",
                                          parent=self)
        if new_name and new_name != old_name and re.match(r'^\w+$', new_name):
            code = tw.get("1.0", "end-1c")
            count = len(re.findall(r'\b' + re.escape(old_name) + r'\b', code))
            new_code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
            tw.delete("1.0", "end")
            tw.insert("1.0", new_code)
            tab["highlighter"].highlight()
            self.st_left.configure(text=f"✓ Renamed '{old_name}' → '{new_name}'  ({count} occurrence{'s' if count!=1 else ''})")

    # ── GO TO LINE ──────────────────────────────────────────────────────────

    def _goto_line(self):
        tab = self._active_tab_data()
        if not tab: return
        line = simpledialog.askinteger("Aller à la ligne", "Numéro de ligne :", parent=self, minvalue=1)
        if line:
            total = int(tab["text"].index("end").split(".")[0])
            line  = min(line, total)
            tab["text"].see(f"{line}.0")
            tab["text"].mark_set("insert", f"{line}.0")
            self.st_left.configure(text=f"→ Ligne {line}")

    # ── RAM / PERF ───────────────────────────────────────────────────────────

    def _ram_loop(self):
        if not HAS_PSUTIL:
            self.after(3000, self._ram_loop)
            return
        try:
            proc = psutil.Process()
            pct  = proc.memory_percent()
            mb   = proc.memory_info().rss / (1024*1024)
            cpu  = proc.cpu_percent(interval=None)
            # Draw bar
            c = self.ram_canvas
            c.delete("all")
            W = c.winfo_width() or 210
            c.configure(bg=t("bg"))
            # RAM bar
            bar_color = t("green") if pct < 50 else (t("yellow") if pct < 80 else t("red"))
            c.create_rectangle(8, 12, W-8, 28, fill=t("bg3"), outline="")
            c.create_rectangle(8, 12, 8 + (W-16)*pct/100, 28, fill=bar_color, outline="")
            c.create_text(W//2, 20, text=f"RAM {pct:.1f}%  ({mb:.0f} MB)",
                          fill=t("fg2"), font=F_UIS)
            # CPU bar
            cpu_c = t("green") if cpu < 50 else (t("yellow") if cpu < 80 else t("red"))
            c.create_rectangle(8, 38, W-8, 54, fill=t("bg3"), outline="")
            c.create_rectangle(8, 38, 8 + (W-16)*cpu/100, 54, fill=cpu_c, outline="")
            c.create_text(W//2, 46, text=f"CPU {cpu:.1f}%",
                          fill=t("fg2"), font=F_UIS)
            self.st_right.configure(text=f"RAM {mb:.0f}MB  ·  CPU {cpu:.1f}%")
        except:
            pass
        self.after(2000, self._ram_loop)

    def _draw_perf_graph(self):
        if not self.mem_monitor.history: return
        c = self.perf_canvas
        c.delete("all")
        W = c.winfo_width() or 210
        H = 100
        c.configure(bg=t("bg"))
        history = self.mem_monitor.history
        vals = [h[1] for h in history]  # code memory
        if not vals or max(vals) == 0: return
        mx = max(vals)
        step = W / max(1, len(vals)-1)
        points = [(i*step, H - 8 - (v/mx)*(H-16)) for i, v in enumerate(vals)]
        # Fill
        poly = [0, H] + [coord for p in points for coord in p] + [W, H]
        if len(poly) >= 6:
            c.create_polygon(poly, fill=t("bg4"), outline="")
        # Line
        if len(points) > 1:
            flat = [coord for p in points for coord in p]
            c.create_line(flat, fill=t("accent"), width=2, smooth=True)
        # Labels
        c.create_text(4, 8, anchor="nw", text=f"{mx:.1f}MB", fill=t("fg3"), font=F_UIS)
        c.create_text(4, H-8, anchor="sw", text="0MB", fill=t("fg3"), font=F_UIS)
        # Update text
        stats = self.mem_monitor.get_stats()
        self.perf_text.configure(state="normal")
        self.perf_text.delete("1.0", "end")
        self.perf_text.insert("end",
            f"Peak     {stats.get('peak_code',0):>6.1f} MB\n"
            f"Avg      {stats.get('avg_code',0):>6.1f} MB\n"
            f"Total pk {stats.get('peak_total',0):>6.1f} MB\n"
            f"Samples  {stats.get('samples',0):>6}\n"
        )
        self.perf_text.configure(state="disabled")

    # ── STATUS BAR ──────────────────────────────────────────────────────────

    def _update_cursor_pos(self):
        tab = self._active_tab_data()
        if not tab: return
        pos = tab["text"].index("insert")
        line, col = pos.split(".")
        self.st_center.configure(text=f"RINT  ·  UTF-8  ·  Ln {line}, Col {int(col)+1}")

    # ── SIDEBAR / PANELS ────────────────────────────────────────────────────

    def _switch_sidebar(self, key, init=False):
        for k, p in self.sb_panels.items():
            p.pack_forget()
            self.act_btns[k].configure(fg=t("fg3"))
        self.sb_panels[key].pack(fill="both", expand=True)
        self.act_btns[key].configure(fg=t("accent"))
        self._active_panel = key

    def _toggle_sidebar(self):
        if self.sidebar_vis:
            self.act.pack_forget()
            self.sidebar.pack_forget()
            self.sidebar_vis = False
        else:
            self.act.pack(side="left", fill="y")
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_vis = True

    def _toggle_minimap(self):
        tab = self._active_tab_data()
        if not tab: return
        mf = tab["minimap_frame"]
        if self.minimap_vis:
            mf.pack_forget()
            self.minimap_vis = False
        else:
            mf.pack(side="right", fill="y")
            self.minimap_vis = True

    def _switch_rp(self, key):
        for k, p in self.rp_panels.items():
            p.pack_forget()
            self.rp_btns[k].configure(fg=t("fg3"))
        self.rp_panels[key].pack(fill="both", expand=True)
        self.rp_btns[key].configure(fg=t("accent"))

    # ── BREAKPOINTS ─────────────────────────────────────────────────────────

    def _clear_bps(self):
        tab = self._active_tab_data()
        if not tab: return
        tab["linenums"].bps.clear()
        tab["linenums"].redraw()
        self.bp_list.delete(0, "end")

    # ── THEME ────────────────────────────────────────────────────────────────

    def _set_theme(self, key):
        global _T
        _T = key
        self._theme_label.configure(text=f"⬤  {THEMES[_T]['name']}", fg=t("accent"))
        self.st_left.configure(text=f"🎨 Theme: {THEMES[_T]['name']}")

    def _cycle_theme(self):
        keys = list(THEMES.keys())
        idx  = keys.index(_T)
        self._set_theme(keys[(idx+1) % len(keys)])

    # ── COMMAND DISPATCHER ──────────────────────────────────────────────────

    def _open_palette(self):
        CommandPalette(self, self)

    def _exec_command(self, cmd):
        dispatch = {
            "run":          self._run_code,
            "stop":         self._stop_code,
            "save":         self._save_file,
            "open":         self._open_file,
            "new":          self.new_tab,
            "find":         self._toggle_find,
            "spotlight":    lambda: (self._switch_sidebar("search"), self.search_var.get() or None,
                                     self._spotlight_do()),
            "goto":         self._goto_line,
            "bookmark":     self._toggle_bookmark,
            "next_bookmark":self._next_bookmark,
            "rename":       self._rename_symbol,
            "metrics":      lambda: self._switch_rp("stats"),
            "todos":        lambda: (self._refresh_todos(), self._switch_console("TODOs")),
            "export_html":  self._export_html,
            "git_status":   lambda: (self._switch_sidebar("git"), self._git_refresh()),
            "theme":        lambda: self._cycle_theme(),
            "minimap":      self._toggle_minimap,
            "sidebar":      self._toggle_sidebar,
            "format":       self._format_code,
            "terminal":     lambda: self._switch_console("Terminal"),
            "about":        self._show_about,
        }
        fn = dispatch.get(cmd)
        if fn:
            try: fn()
            except Exception as e: self._console_err(f"Command error: {e}")

    def _format_code(self):
        """Basic RINT code formatter"""
        tab = self._active_tab_data()
        if not tab: return
        tw = tab["text"]
        code = tw.get("1.0", "end-1c")
        lines = code.split("\n")
        formatted = []
        indent = 0
        for line in lines:
            stripped = line.strip()
            if stripped.endswith("}") and not stripped.startswith("//"):
                indent = max(0, indent - 1)
            formatted.append("    " * indent + stripped)
            if stripped.endswith("{") and not stripped.startswith("//"):
                indent += 1
        new_code = "\n".join(formatted)
        tw.delete("1.0", "end")
        tw.insert("1.0", new_code)
        tab["highlighter"].highlight()
        self.st_left.configure(text="✓ Formatted")

    def _show_about(self):
        w = tk.Toplevel(self)
        w.title("About RINT Studio")
        w.configure(bg=t("bg"))
        w.geometry("420x280")
        w.resizable(False, False)
        tk.Frame(w, bg=t("accent"), height=3).pack(fill="x")
        tk.Label(w, text="RINT Studio", bg=t("bg"), fg=t("accent"),
                 font=("JetBrains Mono", 28, "bold")).pack(pady=(24,4))
        tk.Label(w, text="v6.0  ·  Professional Edition", bg=t("bg"),
                 fg=t("fg2"), font=F_UI).pack()
        tk.Frame(w, bg=t("border"), height=1).pack(fill="x", padx=40, pady=16)
        tk.Label(w, text="by Léandro BOFFY", bg=t("bg"), fg=t("fg"),
                 font=F_UIB).pack()
        tk.Label(w, text="An IDE purpose-built for the RINT language.\nMemory management, hardware control,\ndrone telemetry — all in one place.",
                 bg=t("bg"), fg=t("fg2"), font=F_UIS, justify="center").pack(pady=12)
        tk.Button(w, text="Close", command=w.destroy,
                  bg=t("accent"), fg=t("bg"), relief="flat",
                  font=F_UIB, padx=20, pady=6).pack(pady=8)

# ══════════════════════════════════════════════════════════════════════════════
#   DEMO CODE — inserted on first launch
# ══════════════════════════════════════════════════════════════════════════════

DEMO_CODE = """\
// RINT Studio v6.0 — Demo
// Appuyez sur F5 pour exécuter !

use System(*)
use Audio(*)

// ─── Variables ────────────────────────────────────
string nom = "RINT"
int version = 6
float pi = 3.14159
bool actif = true

// ─── Types natifs ────────────────────────────────
wave son = Audio.load(path="demo.wav")
unit vitesse = "km:160"

// ─── Fonctions ───────────────────────────────────
func saluer(name) {
    console.print(f"Bonjour, {name} !")
    return true
}

func fibonacci(n) {
    int a = 0
    int b = 1
    repeat time(n) {
        int tmp = b
        b = a + b
        a = tmp
        console.log(f"fib = {a}")
    }
    return a
}

// ─── Exécution ────────────────────────────────────
saluer(nom)
console.print(f"RINT v{version} — {vitesse}")

int fib = fibonacci(8)
console.print(f"fib(8) = {fib}")

// ─── Mémoire manuelle ─────────────────────────────
alloc(type="stack", name="buffer", size="bit:32") string buffer = "données"
memcpy(buffer to backup)
console.log(f"buffer = {buffer}")

// ─── Hardware ─────────────────────────────────────
// use hardware() as hard()
// hardware.new(board="arduino", model="uno", name="projet")
// when hard.read(pin=9) == true {
//     hard.set(pin=10, digit=true)
//     console.log("Capteur activé !")
// }

// TODO: ajouter la détection de distance via LIDAR
// FIXME: calibrer les valeurs PID
// NOTE: Turtle.move() fonctionne dans l'onglet Turtle
"""

# ══════════════════════════════════════════════════════════════════════════════
#   ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = RintStudio()
    # Insert demo code into first tab
    if app.tabs:
        tab = app.tabs[0]
        tab["text"].insert("1.0", DEMO_CODE)
        tab["highlighter"].highlight()
        tab["linenums"].redraw()
        tab["minimap"].schedule_redraw()
        tab["modified"] = False
        tab["dot"].configure(text="")
    app.mainloop()

if __name__ == "__main__":
    main()