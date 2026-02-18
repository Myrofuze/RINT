"""
╔══════════════════════════════════════════════════════════════╗
║          RINT IDE  v2.2  —  Atlas Studio                     ║
║          Built with customtkinter · Python 3.10+             ║
║          Modern VS Code + JetBrains Rider Interface          ║
║          Native Plugin System · RAM Manager · Collapsible UI ║
╚══════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import re, os, sys, json, time, threading, math
from datetime import datetime
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# ─── THEME ──────────────────────────────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PALETTE = {
    "bg_root"       : "#0b0c1a",
    "bg_panel"      : "#131427",
    "bg_editor"     : "#0d0e1e",
    "bg_sidebar"    : "#0f1020",
    "bg_tab_active" : "#1a1b2f",
    "bg_tab_idle"   : "#0f1020",
    "bg_input"      : "#181929",
    "bg_hover"      : "#1e2038",
    "bg_select"     : "#2a2b48",
    "accent"        : "#7b6cf6",
    "accent2"       : "#4ecdc4",
    "accent_glow"   : "#9d8ff8",
    "accent_dark"   : "#5a4fd4",
    "warn"          : "#f6a623",
    "error"         : "#ff5757",
    "success"       : "#69e89c",
    "info"          : "#60a5fa",
    "text"          : "#dce0f5",
    "text_muted"    : "#5a6080",
    "text_dim"      : "#3d4060",
    "line_num"      : "#404060",
    "border"        : "#1e2040",
    "border_light"  : "#2a2c50",
    "cursor"        : "#7b6cf6",
    "selection"     : "#2a2b5a",
    "syn_keyword"   : "#c792ea",
    "syn_type"      : "#f9c74f",
    "syn_string"    : "#a8e063",
    "syn_comment"   : "#485070",
    "syn_number"    : "#ff9d6c",
    "syn_func"      : "#79b8ff",
    "syn_operator"  : "#89ddff",
    "syn_builtin"   : "#ffcb6b",
    "syn_param"     : "#eefbff",
    "syn_fstring"   : "#c8e6c9",
    "syn_error"     : "#ff5757",
    "syn_warning"   : "#f6a623",
}

FONT_CODE   = ("JetBrains Mono", 12)
FONT_CODE_S = ("JetBrains Mono", 10)
FONT_UI     = ("Segoe UI", 12)
FONT_UI_S   = ("Segoe UI", 10)
FONT_UI_B   = ("Segoe UI", 11, "bold")

# ─── RINT GRAMMAR ─────────────────────────────────────────────────────────────

RINT_KEYWORDS = {
    "if","else","while","when","repeat","return","func",
    "true","false","and","or","not","in","to","time",
    "class","use","as","alloc","memcpy","memmove","realloc","memset",
    "forward","backward","left","right","down","up","all",
}
RINT_TYPES    = {"int","string","bool","float","list","wave","unit","sys"}
RINT_BUILTINS = {
    "console","Audio","System","Voltige","hardware","Turtle","JSON","hard","js","PC",
}
RINT_FUNCS    = {
    "print","log","ask","read","del","play","load","add",
    "new","config","move","set","get","save","run","pick",
    "drop","return","limit","reduce","error","crash","info",
    "changed","name","debug","virtual","alt","speed","port",
    "autodetect","bass","pen","write","track","context",
}

SYNTAX_PATTERNS = [
    ("comment",   r"//.*?$"),
    ("fstring",   r'f"[^"]*"'),
    ("string",    r'"[^"]*"|\'[^\']*\''),
    ("number",    r'\b\d+(\.\d+)?\b'),
    ("keyword",   r'\b(' + '|'.join(sorted(RINT_KEYWORDS))  + r')\b'),
    ("type_kw",   r'\b(' + '|'.join(sorted(RINT_TYPES))     + r')\b'),
    ("builtin",   r'\b(' + '|'.join(sorted(RINT_BUILTINS))  + r')\b'),
    ("func_call", r'\b(' + '|'.join(sorted(RINT_FUNCS))     + r')\b'),
    ("operator",  r'[=<>!+\-\*/%&|^~]+|[\[\]{}()]'),
    ("param_key", r'\b\w+='),
]

ALL_COMPLETIONS = sorted(list(RINT_KEYWORDS | RINT_TYPES | RINT_BUILTINS | RINT_FUNCS) + [
    "console.print(","console.log(","console.ask(","console.read(","console.del(",
    "Audio.load(","Audio.play(","Audio.add.kick(","Audio.add.snare(","Audio.add.piano(",
    "Audio.new.track(","Audio.bass.return(","Audio.bass.reduce(",
    "System.virtual.new(","System.virtual.config(","System.virtual.error(",
    "Voltige.move.forward(","Voltige.move.backward(","Voltige.alt.set(",
    "Voltige.speed.limit(","hardware.new(","hardware.config(","hardware.read(",
    "hardware.set(","hardware.port.autodetect()",
    "Turtle.new(","Turtle.config(","Turtle.move(","Turtle.pen(","Turtle.pick()","Turtle.drop()",
    "alloc(","memcpy(","memmove(","realloc(","memset(",
    "repeat time(","when ","while true {","func ","class ",
])

SNIPPETS = {
    "if":    'if {cond} {\n    \n}',
    "else":  'else {\n    \n}',
    "while": 'while true {\n    \n}',
    "when":  'when {cond} {\n    \n}',
    "func":  'func {name}({args}) {\n    return \n}',
    "class": 'class {Name}\n{\n    \n}',
    "repeat":'repeat time({n}) {\n    \n}',
    "console":'console.print("")',
    "log":   'console.log("")',
    "alloc": 'alloc(type="stack", name="{name}", size="bit:32") string {name} = ""',
}

DOCS = {
    "console.print":  "Affiche un message dans la console.",
    "console.log":    "Log vers l'espace dédié ou la console.",
    "console.ask":    "Demande une saisie à l'utilisateur.",
    "console.read":   "Lit la console. ln=N, all, ln='N:M'",
    "when":           "Surveille une condition, exécute le bloc une fois si vrai.",
    "repeat":         "Répète N fois. Ex: repeat time(3) { }",
    "while":          "Boucle tant que la condition est vraie.",
    "alloc":          "Alloue de la mémoire. alloc(type='stack', name='x', size='bit:32')",
    "memcpy":         "Copie un bloc mémoire. memcpy(src to dst)",
    "Audio.play":     "Joue une track. Audio.play(name='ma musique')",
    "Turtle.move":    "Déplace la tortue. Turtle.move(forward) ou Turtle.move(repeat=3, forward)",
    "func":           "Définit une fonction. func nom(a, b) { return a + b }",
    "class":          "Bloc programme. class MonProgramme { }",
}


# ─── INTERPRETER ──────────────────────────────────────────────────────────────

class RintError(Exception): pass

class RintInterpreter:
    def __init__(self, output_cb, log_cb, error_cb, ask_cb, vars_cb=None, turtle_cb=None):
        self.output   = output_cb
        self.log_out  = log_cb
        self.error    = error_cb
        self.ask_cb   = ask_cb
        self.vars_cb  = vars_cb
        self.turtle_cb = turtle_cb
        self.variables = {}
        self.functions = {}
        self.running   = False

    def run(self, code):
        self.running = True
        self.variables = {}
        self.functions = {}
        lines = code.split("\n")
        try:
            self._first_pass(lines)
            self._exec_block(lines, 0, len(lines))
        except RintError as e:
            self.error(str(e))
        except Exception as e:
            self.error(f"[Runtime] {type(e).__name__}: {e}")
        finally:
            self.running = False
            if self.vars_cb:
                self.vars_cb(self.variables)

    def _first_pass(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            m = re.match(r'^func\s+(\w+)\s*\(([^)]*)\)\s*\{', line)
            if m:
                fname, params_str = m.groups()
                params = [p.strip() for p in params_str.split(",") if p.strip()]
                be, _ = self._find_block_end(lines, i)
                self.functions[fname] = {"params": params, "body_start": i+1, "body_end": be, "lines": lines}
            i += 1

    def _exec_block(self, lines, start, end):
        i = start
        while i < end and self.running:
            line = lines[i].strip()
            if not line or line.startswith("//"):
                i += 1; continue
            try:
                i = self._exec_line(lines, i, end)
            except RintError:
                raise
            except Exception as e:
                self.log_out(f"[warn] Line {i+1}: {e}")
                i += 1

    def _exec_line(self, lines, idx, end):
        line = lines[idx].strip()
        if not line or line.startswith("//") or line == "}":
            return idx + 1

        # Variable declaration (with optional alloc prefix)
        m = re.match(r'^(?:alloc\([^)]*\)\s*)?(int|string|bool|float|list|wave|unit|sys)\s+(\w+)\s*=\s*(.+)$', line)
        if m:
            t, name, expr = m.groups()
            self.variables[name] = self._eval(expr.rstrip())
            if self.vars_cb: self.vars_cb(dict(self.variables))
            return idx + 1

        # Assignment
        m = re.match(r'^(\w+)\s*=\s*(.+)$', line)
        if m and m.group(1) not in (RINT_KEYWORDS | RINT_BUILTINS):
            name, expr = m.groups()
            self.variables[name] = self._eval(expr.rstrip())
            if self.vars_cb: self.vars_cb(dict(self.variables))
            return idx + 1

        # console.print / console.log / console.ask
        m = re.match(r'^console\.print\((.+)\)$', line)
        if m:
            self.output(self._eval_str(m.group(1).strip()))
            return idx + 1

        m = re.match(r'^console\.log\((.+)\)$', line)
        if m:
            self.log_out(self._eval_str(m.group(1).strip()))
            return idx + 1

        m = re.match(r'^(?:\w+\s+)?(\w+)\s*=\s*console\.ask\((.+)\)$', line)
        if m:
            varname, prompt = m.groups()
            self.ask_cb(self._eval_str(prompt.strip()), varname)
            return idx + 1

        m = re.match(r'^console\.ask\((.+)\)$', line)
        if m:
            self.ask_cb(self._eval_str(m.group(1).strip()))
            return idx + 1

        # if / else if / else
        m = re.match(r'^if\s+(.+?)\s*\{$', line)
        if m:
            cond = m.group(1)
            be, _ = self._find_block_end(lines, idx)
            result = self._eval_cond(cond)
            if result:
                self._exec_block(lines, idx+1, be)
            next_i = be + 1
            while next_i < end:
                nl = lines[next_i].strip()
                if nl.startswith("else if ") and nl.endswith("{"):
                    eb2, _ = self._find_block_end(lines, next_i)
                    if not result:
                        ec = re.match(r'^else if\s+(.+?)\s*\{$', nl)
                        if ec and self._eval_cond(ec.group(1)):
                            self._exec_block(lines, next_i+1, eb2)
                            result = True
                    next_i = eb2 + 1
                elif nl in ("else {", "else{") or nl.startswith("else {"):
                    eb2, _ = self._find_block_end(lines, next_i)
                    if not result:
                        self._exec_block(lines, next_i+1, eb2)
                    next_i = eb2 + 1
                    break
                else:
                    break
            return next_i

        # while
        m = re.match(r'^while\s+(.+?)\s*\{$', line)
        if m:
            cond = m.group(1)
            be, _ = self._find_block_end(lines, idx)
            it = 0
            while self._eval_cond(cond) and self.running:
                self._exec_block(lines, idx+1, be)
                it += 1
                if it > 1000:
                    self.log_out("[while] Limit reached (1000)")
                    break
            return be + 1

        # repeat time(n)
        m = re.match(r'^repeat\s+time\((\d+)\)\s*\{$', line)
        if m:
            n  = int(m.group(1))
            be, _ = self._find_block_end(lines, idx)
            for _ in range(n):
                if not self.running: break
                self._exec_block(lines, idx+1, be)
            return be + 1

        # when
        m = re.match(r'^when\s+(.+?)\s*\{$', line)
        if m:
            cond = m.group(1)
            be, _ = self._find_block_end(lines, idx)
            if self._eval_cond(cond):
                self._exec_block(lines, idx+1, be)
            return be + 1

        # func definition (skip body, already pre-registered)
        m = re.match(r'^func\s+\w+\s*\([^)]*\)\s*\{$', line)
        if m:
            be, _ = self._find_block_end(lines, idx)
            return be + 1

        # func call
        m = re.match(r'^(\w+)\s*\(([^)]*)\)$', line)
        if m and m.group(1) in self.functions:
            self._call_func(m.group(1), m.group(2))
            return idx + 1

        # class
        m = re.match(r'^class\s+\w+\s*$', line)
        if m:
            if idx+1 < len(lines) and lines[idx+1].strip() == "{":
                be, _ = self._find_block_end(lines, idx+1)
                self.log_out(f"[Class] Executing block")
                self._exec_block(lines, idx+2, be)
                return be + 1
            return idx + 1

        # use
        m = re.match(r'^use\s+(\w+)', line)
        if m:
            self.log_out(f"[Import] '{m.group(1)}' loaded")
            return idx + 1

        # Turtle
        if line.startswith("Turtle.move("):
            m = re.match(r'^Turtle\.move\((.*)\)$', line)
            if m and self.turtle_cb:
                args  = m.group(1)
                steps = 1
                rm    = re.search(r'repeat=(\d+)', args)
                if rm: steps = int(rm.group(1))
                for d in ["forward","backward","left","right"]:
                    if d in args:
                        self.turtle_cb(d, steps); break
            return idx + 1

        if line.startswith("Turtle.pen("):
            m = re.match(r'^Turtle\.pen\((\w+)\)$', line)
            if m and self.turtle_cb:
                self.turtle_cb("pen_" + m.group(1), 0)
            return idx + 1

        # Memory ops
        if any(line.startswith(x) for x in ["memset(","memcpy(","memmove(","realloc("]):
            self.log_out(f"[Memory] {line}")
            return idx + 1

        # Audio (log)
        if line.startswith("Audio."):
            self.log_out(f"[Audio] {line}")
            return idx + 1

        return idx + 1

    def _call_func(self, fname, args_str):
        fn = self.functions[fname]
        arg_vals = [a.strip() for a in args_str.split(",") if a.strip()]
        local = dict(self.variables)
        for param, val in zip(fn["params"], arg_vals):
            local[param] = self._eval(val)
        saved = self.variables
        self.variables = local
        self._exec_block(fn["lines"], fn["body_start"], fn["body_end"])
        ret = self.variables.get("__return__")
        self.variables = saved
        return ret

    def _find_block_end(self, lines, start):
        depth = 0
        for i in range(start, len(lines)):
            s = lines[i].strip()
            if s.endswith("{"): depth += 1
            if s == "}":
                depth -= 1
                if depth == 0: return i, i
        return len(lines)-1, len(lines)-1

    def _eval_cond(self, cond):
        cond = cond.strip()
        cond = re.sub(r'\bor\b',  ' or ',  cond)
        cond = re.sub(r'\band\b', ' and ', cond)
        cond = cond.replace("true","True").replace("false","False")
        for name, val in self.variables.items():
            if isinstance(val, str):
                cond = re.sub(r'\b'+re.escape(name)+r'\b', f'"{val}"', cond)
            else:
                cond = re.sub(r'\b'+re.escape(name)+r'\b', str(val), cond)
        try:
            return bool(eval(cond))
        except:
            return False

    def _eval(self, expr):
        expr = expr.strip().rstrip(",")
        if expr in ("true","True"):   return True
        if expr in ("false","False"): return False
        if (expr.startswith('"') and expr.endswith('"')) or \
           (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        if re.match(r'^\d+$', expr):       return int(expr)
        if re.match(r'^\d+\.\d+$', expr):  return float(expr)
        if expr.startswith("["):
            inner = expr[1:-1]
            return [p.strip().strip('"\'') for p in inner.split(",") if p.strip()]
        if expr in self.variables: return self.variables[expr]
        return expr

    def _eval_str(self, expr):
        expr = expr.strip()
        if expr.startswith('f"') and expr.endswith('"'):
            content = expr[2:-1]
            def repl(m):
                inner = m.group(1)
                if inner.endswith(".name()"):
                    return inner.replace(".name()", "")
                v = inner.split(".")[0]
                return str(self.variables.get(v, "{"+inner+"}"))
            return re.sub(r'\{([^}]+)\}', repl, content)
        if "+" in expr:
            return "".join(self._eval_str(p.strip()) for p in self._split_concat(expr))
        if expr in self.variables: return str(self.variables[expr])
        if expr.startswith('"') and expr.endswith('"'): return expr[1:-1]
        if expr.startswith("'") and expr.endswith("'"): return expr[1:-1]
        return expr

    def _split_concat(self, expr):
        parts, cur, in_str = [], "", False
        for ch in expr:
            if ch == '"': in_str = not in_str
            if ch == '+' and not in_str:
                parts.append(cur); cur = ""
            else:
                cur += ch
        if cur: parts.append(cur)
        return parts


# ─── LINTER ───────────────────────────────────────────────────────────────────

class RintLinter:
    def lint(self, code):
        issues = []
        lines  = code.split("\n")
        depth  = 0
        for i, raw in enumerate(lines, 1):
            line = raw.strip()
            if not line or line.startswith("//"): continue
            depth += line.count("{") - line.count("}")
            if line.endswith(";"):
                issues.append((i, "warn", "RINT n'utilise pas de point-virgule"))
            quotes = line.count('"') - line.count('\\"')
            if quotes % 2 != 0 and not line.startswith("//"):
                issues.append((i, "error", "Guillemet non ferme"))
        if depth != 0:
            issues.append((len(lines), "error", f"Accolades non equilibrees (delta: {depth:+d})"))
        return issues


# ─── SYNTAX HIGHLIGHTER ───────────────────────────────────────────────────────

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.w = text_widget
        self._compiled = [(n, re.compile(p, re.MULTILINE)) for n, p in SYNTAX_PATTERNS]
        self._configure_tags()

    def _configure_tags(self):
        w = self.w
        w.tag_configure("comment",      foreground=PALETTE["syn_comment"], font=(*FONT_CODE,"italic"))
        w.tag_configure("fstring",      foreground=PALETTE["syn_fstring"])
        w.tag_configure("string",       foreground=PALETTE["syn_string"])
        w.tag_configure("number",       foreground=PALETTE["syn_number"])
        w.tag_configure("keyword",      foreground=PALETTE["syn_keyword"], font=(*FONT_CODE,"bold"))
        w.tag_configure("type_kw",      foreground=PALETTE["syn_type"],    font=(*FONT_CODE,"bold"))
        w.tag_configure("builtin",      foreground=PALETTE["syn_builtin"])
        w.tag_configure("func_call",    foreground=PALETTE["syn_func"])
        w.tag_configure("operator",     foreground=PALETTE["syn_operator"])
        w.tag_configure("param_key",    foreground=PALETTE["syn_param"])
        w.tag_configure("error_hl",     underline=True, foreground=PALETTE["syn_error"])
        w.tag_configure("warn_hl",      underline=True, foreground=PALETTE["syn_warning"])
        w.tag_configure("find_match",   background=PALETTE["warn"], foreground="#000000")
        w.tag_configure("current_line", background="#161830")
        w.tag_configure("bracket_match",background=PALETTE["bg_select"])

    def highlight(self):
        w = self.w
        content = w.get("1.0","end-1c")
        for tag, _ in self._compiled:
            w.tag_remove(tag,"1.0","end")
        for tag, pat in self._compiled:
            for m in pat.finditer(content):
                s = self._off(content, m.start())
                e = self._off(content, m.end())
                w.tag_add(tag, s, e)

    def _off(self, content, offset):
        line = content[:offset].count("\n") + 1
        col  = offset - (content[:offset].rfind("\n") + 1)
        return f"{line}.{col}"

    def mark_issues(self, issues):
        w = self.w
        w.tag_remove("error_hl","1.0","end")
        w.tag_remove("warn_hl", "1.0","end")
        for lineno, severity, _ in issues:
            tag = "error_hl" if severity == "error" else "warn_hl"
            w.tag_add(tag, f"{lineno}.0", f"{lineno}.end")


# ─── LINE NUMBERS ─────────────────────────────────────────────────────────────

class LineNumbers(tk.Canvas):
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = text_widget
        self.breakpoints = set()
        self.configure(bg=PALETTE["bg_sidebar"], highlightthickness=0, width=54)
        self.bind("<Button-1>", self._toggle_bp)

    def _toggle_bp(self, event):
        line = int(self.text.index(f"@0,{event.y}").split(".")[0])
        if line in self.breakpoints: self.breakpoints.remove(line)
        else: self.breakpoints.add(line)
        self.redraw()

    def redraw(self, *_):
        self.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None: break
            y  = dline[1]
            ln = int(str(i).split(".")[0])
            bp = ln in self.breakpoints
            if bp:
                self.create_oval(3, y+2, 15, y+14, fill=PALETTE["error"], outline="")
            self.create_text(
                50, y+8, anchor="e",
                text=str(ln),
                fill=PALETTE["error"] if bp else PALETTE["line_num"],
                font=FONT_CODE_S,
            )
            ni = self.text.index(f"{i}+1line")
            if ni == i: break
            i = ni


# ─── AUTOCOMPLETE ─────────────────────────────────────────────────────────────

class AutoComplete(tk.Toplevel):
    def __init__(self, parent, on_select):
        super().__init__(parent)
        self.on_select = on_select
        self.overrideredirect(True)
        self.withdraw()
        self.configure(bg=PALETTE["accent"])
        self.wm_attributes("-topmost", True)

        inner = tk.Frame(self, bg=PALETTE["bg_panel"])
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.listbox = tk.Listbox(
            inner, bg=PALETTE["bg_panel"], fg=PALETTE["text"],
            selectbackground=PALETTE["accent"], selectforeground="#ffffff",
            font=FONT_CODE_S, borderwidth=0, highlightthickness=0,
            relief="flat", height=9, width=38, activestyle="none",
        )
        self.listbox.pack(fill="both", expand=True, padx=2, pady=2)

        self.doc_lbl = tk.Label(
            inner, bg=PALETTE["bg_input"], fg=PALETTE["text_muted"],
            font=FONT_UI_S, anchor="w", wraplength=280, justify="left",
            padx=6, pady=3,
        )
        self.doc_lbl.pack(fill="x")

        self.listbox.bind("<Double-Button-1>", lambda e: self._select())
        self.listbox.bind("<<ListboxSelect>>", self._update_doc)

    def show(self, x, y, items):
        self.listbox.delete(0, "end")
        if not items: self.withdraw(); return
        for item in items[:14]:
            self.listbox.insert("end", item)
        self.deiconify()
        self.geometry(f"+{x}+{y}")
        self.listbox.selection_set(0)
        self._update_doc()

    def hide(self): self.withdraw()

    def _update_doc(self, event=None):
        sel = self.listbox.curselection()
        if sel:
            key = self.listbox.get(sel[0]).rstrip("(")
            self.doc_lbl.configure(text=DOCS.get(key, ""))

    def _select(self):
        sel = self.listbox.curselection()
        if sel: self.on_select(self.listbox.get(sel[0]))

    def navigate(self, delta):
        if not self.winfo_viewable(): return
        sel = self.listbox.curselection()
        idx = sel[0] if sel else -1
        new = max(0, min(self.listbox.size()-1, idx+delta))
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(new)
        self.listbox.see(new)
        self._update_doc()

    def accept(self): self._select()


# ─── FIND & REPLACE ───────────────────────────────────────────────────────────

class FindReplaceBar(ctk.CTkFrame):
    def __init__(self, parent, editor, **kwargs):
        super().__init__(parent, height=76, corner_radius=0,
                         fg_color=PALETTE["bg_panel"], **kwargs)
        self.editor   = editor
        self._matches = []
        self._cur     = 0
        self._build()
        self.pack_forget()

    def _build(self):
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(fill="x", padx=8, pady=(4,2))
        ctk.CTkLabel(row1, text="Find:", font=FONT_UI_S,
                     text_color=PALETTE["text_muted"], width=50).pack(side="left")
        self.find_var = tk.StringVar()
        fe = ctk.CTkEntry(row1, textvariable=self.find_var, height=26, width=200, corner_radius=4,
                           fg_color=PALETTE["bg_input"], border_color=PALETTE["border"],
                           text_color=PALETTE["text"], font=FONT_CODE_S)
        fe.pack(side="left", padx=4)
        fe.bind("<KeyRelease>", lambda e: self._do_find())
        fe.bind("<Return>",     lambda e: self._next())
        self.find_entry = fe

        for lbl, cmd in [("↑",self._prev),("↓",self._next)]:
            ctk.CTkButton(row1, text=lbl, width=28, height=26,
                           fg_color="transparent", hover_color=PALETTE["bg_hover"],
                           text_color=PALETTE["accent"], font=("Segoe UI",13),
                           command=cmd).pack(side="left", padx=2)

        self.count_lbl = ctk.CTkLabel(row1, text="", font=FONT_UI_S,
                                       text_color=PALETTE["text_muted"])
        self.count_lbl.pack(side="left", padx=6)

        self.case_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(row1, text="Aa", variable=self.case_var, font=FONT_UI_S,
                         text_color=PALETTE["text_muted"], fg_color=PALETTE["accent"],
                         hover_color=PALETTE["accent_glow"],
                         command=self._do_find).pack(side="left", padx=4)

        self.regex_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(row1, text=".*", variable=self.regex_var, font=FONT_UI_S,
                         text_color=PALETTE["text_muted"], fg_color=PALETTE["accent"],
                         hover_color=PALETTE["accent_glow"],
                         command=self._do_find).pack(side="left", padx=4)

        ctk.CTkButton(row1, text="✕", width=26, height=26,
                       fg_color="transparent", hover_color=PALETTE["error"],
                       text_color=PALETTE["text_muted"], font=("Segoe UI",12),
                       command=self.hide).pack(side="right", padx=4)

        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(fill="x", padx=8, pady=(0,4))
        ctk.CTkLabel(row2, text="Replace:", font=FONT_UI_S,
                     text_color=PALETTE["text_muted"], width=50).pack(side="left")
        self.repl_var = tk.StringVar()
        re_e = ctk.CTkEntry(row2, textvariable=self.repl_var, height=26, width=200, corner_radius=4,
                             fg_color=PALETTE["bg_input"], border_color=PALETTE["border"],
                             text_color=PALETTE["text"], font=FONT_CODE_S)
        re_e.pack(side="left", padx=4)
        re_e.bind("<Return>", lambda e: self._replace_one())
        for lbl, cmd in [("Replace",self._replace_one),("All",self._replace_all)]:
            ctk.CTkButton(row2, text=lbl, width=70, height=26,
                           fg_color=PALETTE["accent"], hover_color=PALETTE["accent_glow"],
                           text_color="#ffffff", font=FONT_UI_S, corner_radius=4,
                           command=cmd).pack(side="left", padx=3)

    def show(self):
        self.pack(fill="x", before=self.editor.editor_container)
        self.find_entry.focus()

    def hide(self):
        self.editor.text.tag_remove("find_match","1.0","end")
        self._matches = []
        self.pack_forget()

    def _off(self, content, offset):
        line = content[:offset].count("\n") + 1
        col  = offset - (content[:offset].rfind("\n") + 1)
        return f"{line}.{col}"

    def _do_find(self):
        t = self.editor.text
        t.tag_remove("find_match","1.0","end")
        query = self.find_var.get()
        if not query:
            self.count_lbl.configure(text="")
            self._matches = []
            return
        self._matches = []
        content = t.get("1.0","end-1c")
        flags = 0 if self.case_var.get() else re.IGNORECASE
        try:
            pat = query if self.regex_var.get() else re.escape(query)
            for m in re.finditer(pat, content, flags):
                s = self._off(content, m.start())
                e = self._off(content, m.end())
                t.tag_add("find_match", s, e)
                self._matches.append((s, e))
        except:
            pass
        n = len(self._matches)
        self.count_lbl.configure(text=f"{n} match{'es' if n!=1 else ''}")
        if self._matches:
            self._cur = 0
            t.see(self._matches[0][0])

    def _next(self):
        if not self._matches: return
        self._cur = (self._cur + 1) % len(self._matches)
        self.editor.text.see(self._matches[self._cur][0])

    def _prev(self):
        if not self._matches: return
        self._cur = (self._cur - 1) % len(self._matches)
        self.editor.text.see(self._matches[self._cur][0])

    def _replace_one(self):
        if not self._matches: return
        s, e = self._matches[self._cur]
        self.editor.text.delete(s, e)
        self.editor.text.insert(s, self.repl_var.get())
        self._do_find()

    def _replace_all(self):
        query = self.find_var.get()
        repl  = self.repl_var.get()
        if not query: return
        t = self.editor.text
        content = t.get("1.0","end-1c")
        flags = 0 if self.case_var.get() else re.IGNORECASE
        try:
            pat = query if self.regex_var.get() else re.escape(query)
            new_content = re.sub(pat, repl, content, flags=flags)
            t.delete("1.0","end")
            t.insert("1.0", new_content)
            self._do_find()
        except:
            pass


# ─── CODE EDITOR ─────────────────────────────────────────────────────────────

class CodeEditor(ctk.CTkFrame):
    def __init__(self, parent, ide, **kwargs):
        super().__init__(parent, corner_radius=0, fg_color=PALETTE["bg_root"], **kwargs)
        self.ide               = ide
        self.modified_since_save = False
        self.font_size         = 13
        self.linter            = RintLinter()
        self._lint_job         = None
        self._build()
        self._bind_keys()

    def _build(self):
        # Breadcrumb
        self.breadcrumb = ctk.CTkFrame(self, height=26, corner_radius=0,
                                        fg_color=PALETTE["bg_panel"])
        self.breadcrumb.pack(fill="x", side="top")
        self.bc_label = ctk.CTkLabel(
            self.breadcrumb, text="  ✦  rint  ›  untitled.rint",
            text_color=PALETTE["text_muted"], font=FONT_UI_S, anchor="w"
        )
        self.bc_label.pack(side="left", padx=8, fill="x")

        # Find & Replace bar
        self.find_bar = FindReplaceBar(self, self)

        # Editor container
        self.editor_container = ctk.CTkFrame(self, fg_color=PALETTE["bg_editor"], corner_radius=0)
        self.editor_container.pack(fill="both", expand=True)

        self.text = tk.Text(
            self.editor_container,
            bg=PALETTE["bg_editor"], fg=PALETTE["text"],
            insertbackground=PALETTE["cursor"],
            selectbackground=PALETTE["selection"],
            selectforeground=PALETTE["text"],
            font=("JetBrains Mono", self.font_size),
            borderwidth=0, highlightthickness=0, relief="flat",
            wrap="none", padx=14, pady=10,
            undo=True, autoseparators=True,
            tabs=("28",), spacing1=2, spacing3=2,
        )
        self.line_nums = LineNumbers(self.editor_container, self.text)
        self.line_nums.pack(side="left", fill="y")

        self.scroll_y = ctk.CTkScrollbar(
            self.editor_container, orientation="vertical",
            command=self._yscroll_cmd,
            button_color=PALETTE["accent"],
            button_hover_color=PALETTE["accent_glow"],
        )
        self.scroll_y.pack(side="right", fill="y")

        self.scroll_x = ctk.CTkScrollbar(
            self, orientation="horizontal",
            command=self.text.xview,
            button_color=PALETTE["accent"],
            button_hover_color=PALETTE["accent_glow"],
            height=10,
        )
        self.scroll_x.pack(side="bottom", fill="x")

        self.text.configure(
            yscrollcommand=self._yscroll,
            xscrollcommand=self.scroll_x.set,
        )
        self.text.pack(side="left", fill="both", expand=True)

        self.highlighter = SyntaxHighlighter(self.text)
        self.ac          = AutoComplete(self.ide, self._insert_completion)

        # Issue bar
        self.issue_bar = ctk.CTkFrame(self, height=22, corner_radius=0,
                                       fg_color=PALETTE["bg_sidebar"])
        self.issue_bar.pack(fill="x", side="bottom")
        self.issue_label = ctk.CTkLabel(
            self.issue_bar, text="  ✓  No issues",
            font=FONT_UI_S, text_color=PALETTE["success"], anchor="w"
        )
        self.issue_label.pack(side="left", padx=8)
        self.cursor_label = ctk.CTkLabel(
            self.issue_bar, text="Ln 1, Col 1",
            font=FONT_UI_S, text_color=PALETTE["text_muted"], anchor="e"
        )
        self.cursor_label.pack(side="right", padx=8)

        self._insert_starter_code()

    def _yscroll_cmd(self, *args):
        self.text.yview(*args)
        self.line_nums.redraw()

    def _yscroll(self, *args):
        self.scroll_y.set(*args)
        self.line_nums.redraw()

    def _insert_starter_code(self):
        code = '''// ✦ RINT IDE — Atlas Studio
// Ctrl+R = Run · Ctrl+F = Find/Replace · Ctrl+Space = Autocomplete · Ctrl+P = Command Palette

use System(*)
use Audio(*)

string nom = "Atlas"
int age = 25
bool actif = true

class Program
{
    console.print(f"Bonjour, {nom}!")
    console.log(f"Age: {age}")

    repeat time(3) {
        console.print(".")
    }

    when actif == true {
        console.print("Systeme actif.")
    }

    if age > 20 {
        console.log("Utilisateur majeur")
    }
    else {
        console.log("Utilisateur mineur")
    }
}
'''
        self.text.insert("1.0", code)
        self.highlighter.highlight()
        self.line_nums.redraw()

    def _bind_keys(self):
        t = self.text
        t.bind("<KeyRelease>",     self._on_key_release)
        t.bind("<Return>",         self._on_enter)
        t.bind("<Tab>",            self._on_tab)
        t.bind("<BackSpace>",      self._on_backspace, add="+")
        t.bind("<Control-space>",  self._trigger_ac)
        t.bind("<Escape>",         lambda e: self.ac.hide())
        t.bind("<Up>",             self._ac_up)
        t.bind("<Down>",           self._ac_down)
        t.bind("<Control-z>",      lambda e: (t.edit_undo(), "break"))
        t.bind("<Control-y>",      lambda e: (t.edit_redo(), "break"))
        t.bind("<Control-a>",      lambda e: (t.tag_add("sel","1.0","end"), "break"))
        t.bind("<Control-d>",      self._duplicate_line)
        t.bind("<Control-slash>",  self._toggle_comment)
        t.bind("<Control-b>",      self._toggle_bp_current)
        t.bind("<Control-equal>",  lambda e: self._zoom(+1))
        t.bind("<Control-minus>",  lambda e: self._zoom(-1))
        t.bind("<Control-f>",      lambda e: self.ide.show_find())
        t.bind("<Control-h>",      lambda e: self.ide.show_find())
        t.bind("<Control-Return>", lambda e: self.ide.run_code())
        t.bind("<ButtonRelease>",  self._on_cursor)
        t.bind("<KeyRelease>",     self._on_cursor, add="+")

    def _on_key_release(self, event):
        self.highlighter.highlight()
        self.line_nums.redraw()
        self._update_ac(event)
        self.modified_since_save = True
        self.ide.update_title()
        if self._lint_job: self.after_cancel(self._lint_job)
        self._lint_job = self.after(700, self._run_lint)

    def _run_lint(self):
        code   = self.get_code()
        issues = self.linter.lint(code)
        self.highlighter.mark_issues(issues)
        errors = [i for i in issues if i[1]=="error"]
        warns  = [i for i in issues if i[1]=="warn"]
        if errors:
            self.issue_label.configure(
                text=f"  ⛔ {len(errors)} error(s)  ⚠ {len(warns)} warning(s)",
                text_color=PALETTE["error"])
        elif warns:
            self.issue_label.configure(
                text=f"  ⚠ {len(warns)} warning(s)",
                text_color=PALETTE["warn"])
        else:
            self.issue_label.configure(text="  ✓  No issues", text_color=PALETTE["success"])
        self.ide.update_issues(issues)

    def _on_cursor(self, event=None):
        self.text.tag_remove("current_line","1.0","end")
        line = self.text.index("insert").split(".")[0]
        self.text.tag_add("current_line", f"{line}.0", f"{line}.end+1c")
        pos = self.text.index("insert")
        l, c = pos.split(".")
        self.cursor_label.configure(text=f"Ln {l}, Col {int(c)+1}")
        self.ide.update_cursor_pos()

    def _on_enter(self, event):
        line   = self.text.get("insert linestart","insert")
        indent = len(line) - len(line.lstrip())
        extra  = 4 if line.rstrip().endswith("{") else 0
        self.text.insert("insert", "\n" + " "*(indent+extra))
        if line.rstrip().endswith("{"):
            cur = self.text.index("insert")
            self.text.insert("insert", "\n" + " "*indent + "}")
            self.text.mark_set("insert", cur)
        return "break"

    def _on_tab(self, event):
        try:
            s = self.text.index("sel.first linestart")
            e = self.text.index("sel.last lineend")
            lines = self.text.get(s, e).split("\n")
            self.text.delete(s, e)
            self.text.insert(s, "\n".join("    "+l for l in lines))
            return "break"
        except:
            pass
        self.text.insert("insert","    ")
        return "break"

    def _on_backspace(self, event):
        line = self.text.get("insert linestart","insert")
        if line.endswith("    "):
            self.text.delete("insert-4c","insert")
            return "break"

    def _trigger_ac(self, event=None):
        word = self._current_word()
        sugg = self._get_suggestions(word)
        if sugg:
            bbox = self.text.bbox("insert")
            if bbox:
                x = self.text.winfo_rootx() + bbox[0]
                y = self.text.winfo_rooty() + bbox[1] + bbox[3] + 2
                self.ac.show(x, y, sugg)
        return "break"

    def _update_ac(self, event):
        if event.keysym in ("Escape","Return","Tab","BackSpace"):
            self.ac.hide(); return
        if event.char and (event.char.isalnum() or event.char in "._"):
            word = self._current_word()
            if len(word) >= 2:
                sugg = self._get_suggestions(word)
                if sugg:
                    bbox = self.text.bbox("insert")
                    if bbox:
                        x = self.text.winfo_rootx() + bbox[0]
                        y = self.text.winfo_rooty() + bbox[1] + bbox[3] + 2
                        self.ac.show(x, y, sugg)
                    return
        if not self.ac.listbox.curselection():
            self.ac.hide()

    def _ac_up(self, event):
        if self.ac.winfo_viewable():
            self.ac.navigate(-1); return "break"

    def _ac_down(self, event):
        if self.ac.winfo_viewable():
            self.ac.navigate(1); return "break"

    def _get_suggestions(self, word):
        if not word: return []
        lower = word.lower()
        return [c for c in ALL_COMPLETIONS if c.lower().startswith(lower)][:14]

    def _current_word(self):
        pos  = self.text.index("insert")
        line = self.text.get(f"{pos} linestart", pos)
        m    = re.search(r'[\w.]+$', line)
        return m.group() if m else ""

    def _insert_completion(self, full):
        word = self._current_word()
        tail = full[len(word):] if full.startswith(word) else full
        self.text.insert("insert", tail)
        self.ac.hide()
        self.highlighter.highlight()

    def _duplicate_line(self, event=None):
        line = self.text.index("insert").split(".")[0]
        content = self.text.get(f"{line}.0", f"{line}.end")
        self.text.insert(f"{line}.end", f"\n{content}")
        return "break"

    def _toggle_comment(self, event=None):
        try:
            s = self.text.index("sel.first linestart")
            e = self.text.index("sel.last lineend")
        except:
            s = self.text.index("insert linestart")
            e = self.text.index("insert lineend")
        lines = self.text.get(s, e).split("\n")
        toggled = []
        for l in lines:
            toggled.append(re.sub(r'^//', '', l, count=1) if l.strip().startswith("//") else "//"+l)
        self.text.delete(s, e)
        self.text.insert(s, "\n".join(toggled))
        self.highlighter.highlight()
        return "break"

    def _toggle_bp_current(self, event=None):
        line = int(self.text.index("insert").split(".")[0])
        if line in self.line_nums.breakpoints:
            self.line_nums.breakpoints.remove(line)
        else:
            self.line_nums.breakpoints.add(line)
            self.ide.console_panel.add_msg(f"[Breakpoint] Line {line}", "warn")
        self.line_nums.redraw()
        return "break"

    def _zoom(self, delta):
        self.font_size = max(9, min(28, self.font_size + delta))
        self.text.configure(font=("JetBrains Mono", self.font_size))
        self.ide.status_bar.update_zoom(self.font_size)

    def get_code(self):
        return self.text.get("1.0","end-1c")

    def set_code(self, code):
        self.text.delete("1.0","end")
        self.text.insert("1.0", code)
        self.highlighter.highlight()
        self.line_nums.redraw()

    def goto_line(self, lineno):
        self.text.mark_set("insert", f"{lineno}.0")
        self.text.see(f"{lineno}.0")
        self.text.focus()


# ─── CONSOLE PANEL ────────────────────────────────────────────────────────────

class ConsolePanel(ctk.CTkFrame):
    def __init__(self, parent, ide, **kwargs):
        super().__init__(parent, corner_radius=0, fg_color=PALETTE["bg_panel"], **kwargs)
        self.ide = ide
        self._pending_ask = None
        self._all_messages = []
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, height=36, corner_radius=0,
                            fg_color=PALETTE["bg_sidebar"])
        top.pack(fill="x")
        self._tabs = {}
        for name in ["Output","Log","Debug","Problems"]:
            btn = ctk.CTkButton(
                top, text=name, width=82, height=28,
                fg_color="transparent", hover_color=PALETTE["bg_hover"],
                text_color=PALETTE["text_muted"],
                font=FONT_UI_S, corner_radius=6,
                command=lambda n=name: self._tab(n),
            )
            btn.pack(side="left", padx=3, pady=4)
            self._tabs[name] = btn

        self.filter_var = tk.StringVar()
        fe = ctk.CTkEntry(top, textvariable=self.filter_var,
                           placeholder_text="Filter...",
                           height=24, width=130, corner_radius=4,
                           fg_color=PALETTE["bg_input"], border_color=PALETTE["border"],
                           text_color=PALETTE["text"], font=FONT_UI_S)
        fe.pack(side="right", padx=8, pady=6)
        fe.bind("<KeyRelease>", self._apply_filter)

        ctk.CTkButton(top, text="⌫", width=30, height=28,
                       fg_color="transparent", hover_color=PALETTE["bg_hover"],
                       text_color=PALETTE["text_muted"], font=("Segoe UI",13),
                       command=self.clear).pack(side="right", padx=2)

        self.output = tk.Text(
            self, bg=PALETTE["bg_editor"], fg=PALETTE["text"],
            font=FONT_CODE_S, borderwidth=0, highlightthickness=0,
            state="disabled", wrap="word", padx=12, pady=6,
        )
        self.output.pack(fill="both", expand=True)

        irow = ctk.CTkFrame(self, height=38, corner_radius=0,
                             fg_color=PALETTE["bg_sidebar"])
        irow.pack(fill="x", side="bottom")
        ctk.CTkLabel(irow, text=" › ", text_color=PALETTE["accent"],
                     font=("JetBrains Mono",14,"bold")).pack(side="left")
        self.input_var = tk.StringVar()
        self.input_entry = ctk.CTkEntry(
            irow, textvariable=self.input_var,
            placeholder_text="User input...",
            height=28, corner_radius=6,
            fg_color=PALETTE["bg_input"], border_color=PALETTE["border"],
            text_color=PALETTE["text"], font=FONT_CODE_S,
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=4, pady=5)
        self.input_entry.bind("<Return>", lambda e: self._send())
        ctk.CTkButton(irow, text="Send", width=60, height=28,
                       fg_color=PALETTE["accent"], hover_color=PALETTE["accent_glow"],
                       text_color="#ffffff", font=FONT_UI_S, corner_radius=6,
                       command=self._send).pack(side="right", padx=8)

        self._configure_tags()
        self._tab("Output")

    def _configure_tags(self):
        o = self.output
        o.tag_configure("info",      foreground=PALETTE["text"])
        o.tag_configure("log",       foreground=PALETTE["accent2"])
        o.tag_configure("warn",      foreground=PALETTE["warn"])
        o.tag_configure("error",     foreground=PALETTE["error"])
        o.tag_configure("success",   foreground=PALETTE["success"])
        o.tag_configure("prompt",    foreground=PALETTE["syn_builtin"])
        o.tag_configure("input",     foreground=PALETTE["syn_string"])
        o.tag_configure("ts",        foreground=PALETTE["text_dim"])
        o.tag_configure("problem_e", foreground=PALETTE["error"])
        o.tag_configure("problem_w", foreground=PALETTE["warn"])

    def _tab(self, name):
        for n, btn in self._tabs.items():
            btn.configure(
                fg_color=PALETTE["accent"] if n == name else "transparent",
                text_color="#ffffff"        if n == name else PALETTE["text_muted"],
            )
        self._current_tab = name

    def _send(self):
        val = self.input_var.get()
        if not val: return
        self.add_msg(f">>> {val}", "input")
        if self._pending_ask:
            self.ide.interpreter.variables[self._pending_ask] = val
            self._pending_ask = None
        self.input_var.set("")

    def add_msg(self, msg, tag="info"):
        self._all_messages.append((msg, tag))
        ts = datetime.now().strftime("%H:%M:%S")
        self.output.configure(state="normal")
        self.output.insert("end", f"[{ts}] ", "ts")
        self.output.insert("end", msg+"\n", tag)
        self.output.configure(state="disabled")
        self.output.see("end")

    def add_output(self, msg):       self.add_msg(msg, "info")
    def add_log(self, msg, t="log"): self.add_msg(msg, t)
    def add_error(self, msg):        self.add_msg(f"⛔ {msg}", "error")
    def add_warn(self, msg):         self.add_msg(f"⚠  {msg}", "warn")
    def add_success(self, msg):      self.add_msg(msg, "success")

    def ask_user(self, prompt, var_name="__response__"):
        self.add_msg(prompt, "prompt")
        self._pending_ask = var_name
        self.input_entry.focus()

    def show_problems(self, issues):
        self.output.configure(state="normal")
        # Only update if Problems tab is active
        self.output.configure(state="disabled")

    def clear(self):
        self._all_messages.clear()
        self.output.configure(state="normal")
        self.output.delete("1.0","end")
        self.output.configure(state="disabled")

    def _apply_filter(self, event=None):
        query = self.filter_var.get().lower()
        self.output.configure(state="normal")
        self.output.delete("1.0","end")
        for msg, tag in self._all_messages:
            if not query or query in msg.lower():
                self.output.insert("end", msg+"\n", tag)
        self.output.configure(state="disabled")
        self.output.see("end")


# ─── FILE EXPLORER ────────────────────────────────────────────────────────────

class FileExplorer(ctk.CTkFrame):
    def __init__(self, parent, ide, **kwargs):
        super().__init__(parent, corner_radius=0, fg_color=PALETTE["bg_sidebar"], **kwargs)
        self.ide          = ide
        self.current_path = os.path.expanduser("~")
        self._expanded    = set()
        self._items       = []
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, height=38, corner_radius=0,
                            fg_color=PALETTE["bg_panel"])
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="  EXPLORER", font=("Segoe UI",10,"bold"),
                     text_color=PALETTE["text_muted"]).pack(side="left", padx=8)
        row = ctk.CTkFrame(hdr, fg_color="transparent")
        row.pack(side="right", padx=4)
        for icon, cmd in [("⊕",self._new_file),("↑",self._go_up),("↻",self._refresh)]:
            ctk.CTkButton(row, text=icon, width=26, height=26,
                           fg_color="transparent", hover_color=PALETTE["bg_hover"],
                           text_color=PALETTE["text_muted"], font=("Segoe UI",13),
                           command=cmd).pack(side="left", padx=1)

        self.path_var = tk.StringVar(value=self.current_path)
        pe = ctk.CTkEntry(self, textvariable=self.path_var, height=24,
                           fg_color=PALETTE["bg_input"], border_color=PALETTE["border"],
                           text_color=PALETTE["text_muted"], font=FONT_UI_S, corner_radius=0)
        pe.pack(fill="x")
        pe.bind("<Return>", self._nav_to_path)

        frame = tk.Frame(self, bg=PALETTE["bg_sidebar"])
        frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(frame, bg=PALETTE["bg_sidebar"], highlightthickness=0)
        sb = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview,
                           bg=PALETTE["bg_sidebar"])
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1*(e.delta//120),"units"))
        self._populate()

    def _populate(self):
        self.canvas.delete("all")
        self._items = []
        self.path_var.set(self.current_path)
        y = [8]
        self._render_dir(self.current_path, 0, y)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _render_dir(self, path, indent, y_counter):
        try:
            entries = sorted(os.listdir(path))
        except:
            return
        dirs  = [e for e in entries if os.path.isdir(os.path.join(path,e)) and not e.startswith(".")]
        files = [e for e in entries if not os.path.isdir(os.path.join(path,e))]
        for name in dirs + files:
            full   = os.path.join(path, name)
            is_dir = os.path.isdir(full)
            is_rint = name.endswith(".rint")
            y   = y_counter[0]
            x   = 10 + indent * 16
            icon  = "📂" if is_dir else ("✦" if is_rint else "📄")
            color = PALETTE["accent"] if is_rint else PALETTE["text"]
            arrow = ("▼ " if full in self._expanded else "▶ ") if is_dir else "  "
            self.canvas.create_text(
                x, y, anchor="w",
                text=f"{arrow}{icon} {name}",
                fill=color, font=FONT_UI_S,
                tags=f"item_{len(self._items)}",
            )
            self._items.append({"path": full, "is_dir": is_dir, "y": y})
            y_counter[0] += 22
            if is_dir and full in self._expanded:
                self._render_dir(full, indent+1, y_counter)

    def _on_click(self, event):
        for item in self._items:
            if abs(item["y"] - event.y) < 11:
                if item["is_dir"]:
                    if item["path"] in self._expanded:
                        self._expanded.discard(item["path"])
                    else:
                        self._expanded.add(item["path"])
                    self._populate()
                else:
                    self.ide.open_file(item["path"])
                break

    def _go_up(self):
        self.current_path = os.path.dirname(self.current_path)
        self._expanded.clear(); self._populate()

    def _refresh(self):
        self._populate()

    def _nav_to_path(self, event=None):
        p = self.path_var.get().strip()
        if os.path.isdir(p):
            self.current_path = p
            self._expanded.clear(); self._populate()

    def _new_file(self):
        self.ide.new_tab()


# ─── VARIABLES WATCH ─────────────────────────────────────────────────────────

class VariablesWatch(ctk.CTkFrame):
    def __init__(self, parent, ide, **kwargs):
        self.ide = ide
        super().__init__(parent, corner_radius=0, fg_color=PALETTE["bg_panel"], **kwargs)
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, height=36, corner_radius=0,
                            fg_color=PALETTE["bg_sidebar"])
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="  VARIABLES", font=("Segoe UI",10,"bold"),
                     text_color=PALETTE["text_muted"]).pack(side="left", padx=8)
        frame = tk.Frame(self, bg=PALETTE["bg_panel"])
        frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(frame, bg=PALETTE["bg_panel"], highlightthickness=0)
        sb = tk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)

    def update_vars(self, variables):
        c = self.canvas
        c.delete("all")
        y = 10
        for col, x in [("Name",8),("Value",100),("Type",195)]:
            c.create_text(x, y, anchor="w", text=col,
                           fill=PALETTE["text_muted"], font=(*FONT_UI_S,"bold"))
        y += 14
        c.create_line(4, y, 245, y, fill=PALETTE["border"])
        y += 14
        if not variables:
            c.create_text(10, y, anchor="w", text="(no variables)",
                           fill=PALETTE["text_dim"], font=FONT_UI_S)
        else:
            for name, val in list(variables.items())[:50]:
                if name.startswith("__"): continue
                tname = type(val).__name__
                vs    = str(val)[:20]
                col   = (PALETTE["syn_string"] if isinstance(val, str) else
                         PALETTE["syn_number"] if isinstance(val, (int,float)) else
                         PALETTE["syn_keyword"] if isinstance(val, bool) else
                         PALETTE["text"])
                c.create_text(8,   y, anchor="w", text=name,  fill=PALETTE["accent"],      font=FONT_CODE_S)
                c.create_text(100, y, anchor="w", text=vs,    fill=col,                    font=FONT_CODE_S)
                c.create_text(195, y, anchor="w", text=tname, fill=PALETTE["text_muted"],  font=FONT_UI_S)
                y += 22
        c.configure(scrollregion=c.bbox("all"))


# ─── TURTLE PREVIEW ──────────────────────────────────────────────────────────

class TurtlePreview(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        self.tx = self.ty = self.angle = 0
        self.pen = True
        super().__init__(parent, corner_radius=0, fg_color=PALETTE["bg_panel"], **kwargs)
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, height=36, corner_radius=0,
                            fg_color=PALETTE["bg_sidebar"])
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="  TURTLE", font=("Segoe UI",10,"bold"),
                     text_color=PALETTE["text_muted"]).pack(side="left", padx=8)
        ctk.CTkButton(hdr, text="Reset", width=54, height=24,
                       fg_color="transparent", hover_color=PALETTE["bg_hover"],
                       text_color=PALETTE["text_muted"], font=FONT_UI_S,
                       command=self.reset).pack(side="right", padx=6)
        self.canvas = tk.Canvas(self, bg="#080916", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=4, pady=4)
        self.canvas.bind("<Configure>", lambda e: self._init_canvas())
        self.after(100, self._init_canvas)

    def _init_canvas(self):
        self.canvas.delete("grid")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 2 or h < 2: return
        step = 20
        for x in range(0, w, step):
            self.canvas.create_line(x,0,x,h, fill=PALETTE["border"], tags="grid")
        for y in range(0, h, step):
            self.canvas.create_line(0,y,w,y, fill=PALETTE["border"], tags="grid")
        cx, cy = w//2, h//2
        self.canvas.create_oval(cx-3,cy-3,cx+3,cy+3,
                                 fill=PALETTE["accent2"], outline="", tags="grid")
        self._draw_turtle()

    def _cx(self): return max(self.canvas.winfo_width()//2, 1)
    def _cy(self): return max(self.canvas.winfo_height()//2, 1)

    def _draw_turtle(self):
        self.canvas.delete("turtle")
        x = self._cx() + self.tx
        y = self._cy() - self.ty
        r = 9
        a = math.radians(self.angle)
        pts = [
            x + r*math.cos(a),      y - r*math.sin(a),
            x + r*math.cos(a+2.3),  y - r*math.sin(a+2.3),
            x + r*math.cos(a-2.3),  y - r*math.sin(a-2.3),
        ]
        self.canvas.create_polygon(pts, fill=PALETTE["success"],
                                    outline=PALETTE["accent2"], width=1, tags="turtle")

    def move(self, direction, steps=1):
        dist = steps * 20
        a    = math.radians(self.angle)
        sx   = self._cx() + self.tx
        sy   = self._cy() - self.ty
        nx, ny = self.tx, self.ty
        if direction == "forward":
            nx = self.tx + dist*math.cos(a)
            ny = self.ty + dist*math.sin(a)
        elif direction == "backward":
            nx = self.tx - dist*math.cos(a)
            ny = self.ty - dist*math.sin(a)
        elif direction == "left":
            self.angle += 90*steps; self._draw_turtle(); return
        elif direction == "right":
            self.angle -= 90*steps; self._draw_turtle(); return
        elif direction == "pen_down":
            self.pen = True; return
        elif direction == "pen_up":
            self.pen = False; return
        if self.pen:
            ex = self._cx() + nx
            ey = self._cy() - ny
            self.canvas.create_line(sx,sy,ex,ey, fill=PALETTE["accent2"], width=2)
        self.tx, self.ty = nx, ny
        self._draw_turtle()

    def reset(self):
        self.canvas.delete("all")
        self.tx = self.ty = self.angle = 0
        self.pen = True
        self._init_canvas()


# ─── AUDIO PREVIEW ───────────────────────────────────────────────────────────

class AudioPreview(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        self.waves    = []
        self._anim    = 0
        self._running = False
        super().__init__(parent, corner_radius=0, fg_color=PALETTE["bg_panel"], **kwargs)
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, height=36, corner_radius=0,
                            fg_color=PALETTE["bg_sidebar"])
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="  AUDIO", font=("Segoe UI",10,"bold"),
                     text_color=PALETTE["text_muted"]).pack(side="left", padx=8)
        ctk.CTkButton(hdr, text="▶", width=30, height=24,
                       fg_color=PALETTE["accent"], hover_color=PALETTE["accent_glow"],
                       text_color="#ffffff", font=("Segoe UI",12),
                       command=self._toggle).pack(side="right", padx=6)
        self.canvas = tk.Canvas(self, bg="#080916", highlightthickness=0, height=100)
        self.canvas.pack(fill="x", padx=4, pady=4)
        self.track_list = tk.Listbox(
            self, bg=PALETTE["bg_panel"], fg=PALETTE["text"],
            selectbackground=PALETTE["accent"], selectforeground="#ffffff",
            font=FONT_CODE_S, borderwidth=0, highlightthickness=0, height=5,
        )
        self.track_list.pack(fill="both", expand=True, padx=4, pady=4)
        self._draw()

    def _draw(self, **kwargs):
        if not hasattr(self, 'canvas'):
            return
        self.canvas.delete("all")
        w = max(self.canvas.winfo_width(), 200)
        h = 100
        mid = h//2
        self.canvas.create_rectangle(0,0,w,h, fill="#080916", outline="")
        self.canvas.create_line(0,mid,w,mid, fill=PALETTE["border"])
        t = self._anim * 0.06
        pts = []
        for x in range(0, w, 2):
            y = mid + int(20 * math.sin(x*0.07+t) * math.sin(x*0.03-t))
            pts.extend([x, y])
        if len(pts) >= 4:
            self.canvas.create_line(pts, fill=PALETTE["accent"], width=2, smooth=True)
        self.canvas.create_rectangle(0,0,w,3, fill=PALETTE["accent"], outline="")

    def _toggle(self):
        self._running = not self._running
        if self._running: self._animate()

    def _animate(self):
        if not self._running: return
        self._anim += 1
        self._draw()
        self.after(30, self._animate)

    def add_wave(self, name, wave_type="sine"):
        self.waves.append(name)
        self.track_list.insert("end", f"  {name}  [{wave_type}]")


# ─── CONSOLE OUTPUT PANEL ────────────────────────────────────────────────────

class ConsoleOutputPanel(ctk.CTkFrame):
    def __init__(self, parent, ide=None, **kwargs):
        super().__init__(parent, corner_radius=0, fg_color=PALETTE["bg_panel"], **kwargs)
        self.messages = []
        self.ide = ide
        self._pending_ask = None
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, height=36, corner_radius=0,
                            fg_color=PALETTE["bg_sidebar"])
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="  CONSOLE", font=("Segoe UI",8,"bold"),
                     text_color=PALETTE["text_muted"]).pack(side="left", padx=8)
        ctk.CTkButton(hdr, text="⌫", width=30, height=28,
                       fg_color="transparent", hover_color=PALETTE["bg_hover"],
                       text_color=PALETTE["text_muted"], font=("Segoe UI",11),
                       command=self.clear).pack(side="right", padx=2)
        
        frame = tk.Frame(self, bg=PALETTE["bg_panel"])
        frame.pack(fill="both", expand=True)
        self.output = tk.Text(
            frame, bg=PALETTE["bg_editor"], fg=PALETTE["text"],
            font=FONT_CODE_S, borderwidth=0, highlightthickness=0,
            state="disabled", wrap="word", padx=10, pady=6,
        )
        self.output.tag_configure("info",    foreground=PALETTE["text"])
        self.output.tag_configure("log",     foreground=PALETTE["accent2"])
        self.output.tag_configure("warn",    foreground=PALETTE["warn"])
        self.output.tag_configure("error",   foreground=PALETTE["error"])
        self.output.tag_configure("success", foreground=PALETTE["success"])
        self.output.tag_configure("prompt",  foreground=PALETTE["syn_builtin"])
        self.output.tag_configure("input",   foreground=PALETTE["syn_string"])
        
        sb = tk.Scrollbar(frame, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.output.pack(fill="both", expand=True)

        irow = ctk.CTkFrame(self, height=38, corner_radius=0,
                             fg_color=PALETTE["bg_sidebar"])
        irow.pack(fill="x", side="bottom")
        ctk.CTkLabel(irow, text=" › ", text_color=PALETTE["accent"],
                     font=("JetBrains Mono",11,"bold")).pack(side="left")
        self.input_var = tk.StringVar()
        self.input_entry = ctk.CTkEntry(
            irow, textvariable=self.input_var,
            placeholder_text="User input...",
            height=28, corner_radius=6,
            fg_color=PALETTE["bg_input"], border_color=PALETTE["border"],
            text_color=PALETTE["text"], font=FONT_CODE_S,
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=4, pady=5)
        self.input_entry.bind("<Return>", lambda e: self._send())
        ctk.CTkButton(irow, text="Send", width=50, height=28,
                       fg_color=PALETTE["accent"], hover_color=PALETTE["accent_glow"],
                       text_color="#ffffff", font=FONT_UI_S, corner_radius=6,
                       command=self._send).pack(side="right", padx=8)

    def add_message(self, msg, tag="info"):
        self.messages.append((msg, tag))
        self.output.configure(state="normal")
        self.output.insert("end", msg + "\n", tag)
        self.output.configure(state="disabled")
        self.output.see("end")

    def _send(self):
        val = self.input_var.get()
        if not val: return
        self.add_message(f">>> {val}", "input")
        if self._pending_ask and self.ide:
            self.ide.interpreter.variables[self._pending_ask] = val
            self._pending_ask = None
        self.input_var.set("")

    def ask_user(self, prompt, var_name="__response__"):
        self.add_message(prompt, "prompt")
        self._pending_ask = var_name
        self.input_entry.focus()

    def clear(self):
        self.messages.clear()
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")


# ─── COMMAND PALETTE ─────────────────────────────────────────────────────────

class CommandPalette(tk.Toplevel):
    COMMANDS = [
        ("Run Code",               "Ctrl+R",  "run"),
        ("Save File",              "Ctrl+S",  "save"),
        ("Open File",              "Ctrl+O",  "open"),
        ("New Tab",                "Ctrl+N",  "new_tab"),
        ("Find & Replace",         "Ctrl+F",  "find"),
        ("Go to Line...",          "Ctrl+G",  "goto_line"),
        ("Toggle Comment",         "Ctrl+/",  "comment"),
        ("Duplicate Line",         "Ctrl+D",  "duplicate"),
        ("Zoom In",                "Ctrl++",  "zoom_in"),
        ("Zoom Out",               "Ctrl+-",  "zoom_out"),
        ("Toggle Bottom Panel",    "",        "toggle_bottom"),
        ("Clear Console",          "",        "clear_console"),
        ("Open Command Palette",   "Ctrl+P",  "palette"),
        ("Insert Snippet: if",     "",        "snippet_if"),
        ("Insert Snippet: func",   "",        "snippet_func"),
        ("Insert Snippet: class",  "",        "snippet_class"),
        ("Insert Snippet: when",   "",        "snippet_when"),
        ("Insert Snippet: repeat", "",        "snippet_repeat"),
        ("Insert Snippet: while",  "",        "snippet_while"),
    ]

    def __init__(self, parent, ide):
        super().__init__(parent)
        self.ide = ide
        self.overrideredirect(True)
        self.configure(bg=PALETTE["accent"])
        self.wm_attributes("-topmost", True)
        w, h = 520, 380
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//6}")

        inner = tk.Frame(self, bg=PALETTE["bg_panel"])
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.search_var = tk.StringVar()
        self.entry = tk.Entry(
            inner, textvariable=self.search_var,
            bg=PALETTE["bg_input"], fg=PALETTE["text"],
            font=("JetBrains Mono",13), borderwidth=0,
            insertbackground=PALETTE["cursor"], relief="flat",
        )
        self.entry.pack(fill="x", padx=12, pady=10, ipady=6)
        tk.Frame(inner, bg=PALETTE["border"], height=1).pack(fill="x")

        self.listbox = tk.Listbox(
            inner, bg=PALETTE["bg_panel"], fg=PALETTE["text"],
            selectbackground=PALETTE["accent"], selectforeground="#ffffff",
            font=FONT_UI_S, borderwidth=0, highlightthickness=0,
            relief="flat", height=14, activestyle="none",
        )
        self.listbox.pack(fill="both", expand=True, padx=2)

        self.search_var.trace("w", self._filter)
        self.entry.bind("<Return>",  self._run_selected)
        self.entry.bind("<Escape>",  lambda e: self.destroy())
        self.entry.bind("<Up>",      lambda e: self._nav(-1))
        self.entry.bind("<Down>",    lambda e: self._nav(1))
        self.listbox.bind("<Double-Button-1>", self._run_selected)
        self.bind("<FocusOut>", lambda e: self.destroy())

        self._filtered = self.COMMANDS[:]
        self._populate(self._filtered)
        self.entry.focus()

    def _filter(self, *_):
        q = self.search_var.get().lower()
        self._filtered = [(n,s,c) for n,s,c in self.COMMANDS if q in n.lower()]
        self._populate(self._filtered)

    def _populate(self, items):
        self.listbox.delete(0, "end")
        for name, shortcut, _ in items:
            line = f"  {name}"
            if shortcut: line += f"  ({shortcut})"
            self.listbox.insert("end", line)
        if items: self.listbox.selection_set(0)

    def _nav(self, delta):
        sel = self.listbox.curselection()
        idx = sel[0] if sel else -1
        new = max(0, min(self.listbox.size()-1, idx+delta))
        self.listbox.selection_clear(0,"end")
        self.listbox.selection_set(new)
        self.listbox.see(new)

    def _run_selected(self, event=None):
        sel = self.listbox.curselection()
        if not sel or sel[0] >= len(self._filtered): return
        cmd = self._filtered[sel[0]][2]
        self.destroy()
        self._execute(cmd)

    def _execute(self, cmd):
        ide = self.ide
        ed  = ide.current_editor()
        dispatch = {
            "run":            ide.run_code,
            "save":           ide.save_file,
            "open":           ide.open_file_dialog,
            "new_tab":        ide.new_tab,
            "find":           ide.show_find,
            "goto_line":      ide.goto_line_dialog,
            "comment":        lambda: ed and ed._toggle_comment(),
            "duplicate":      lambda: ed and ed._duplicate_line(),
            "zoom_in":        lambda: ed and ed._zoom(+1),
            "zoom_out":       lambda: ed and ed._zoom(-1),
            "toggle_bottom":  ide.toggle_bottom,
            "clear_console":  ide.console_panel.clear,
            "palette":        ide.open_palette,
            "snippet_if":     lambda: ide.insert_snippet("if"),
            "snippet_func":   lambda: ide.insert_snippet("func"),
            "snippet_class":  lambda: ide.insert_snippet("class"),
            "snippet_when":   lambda: ide.insert_snippet("when"),
            "snippet_repeat": lambda: ide.insert_snippet("repeat"),
            "snippet_while":  lambda: ide.insert_snippet("while"),
        }
        fn = dispatch.get(cmd)
        if fn: fn()


# ─── TOOLBAR ─────────────────────────────────────────────────────────────────

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, ide, **kwargs):
        super().__init__(parent, height=46, corner_radius=0,
                         fg_color=PALETTE["bg_sidebar"], **kwargs)
        self.ide = ide
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="  ✦ RINT IDE",
                     font=("Segoe UI",14,"bold"),
                     text_color=PALETTE["accent"]).pack(side="left", padx=10)

        tk.Frame(self, bg=PALETTE["border"], width=1, height=28).pack(side="left", padx=8)

        for lbl, cmd in [("🗂 New",self.ide.new_tab),("📂 Open",self.ide.open_file_dialog),("💾 Save",self.ide.save_file)]:
            ctk.CTkButton(self, text=lbl, width=80, height=32,
                           fg_color="transparent", hover_color=PALETTE["bg_hover"],
                           text_color=PALETTE["text_muted"], font=FONT_UI_S, corner_radius=6,
                           command=cmd).pack(side="left", padx=2)

        tk.Frame(self, bg=PALETTE["border"], width=1, height=28).pack(side="left", padx=8)

        self.run_btn = ctk.CTkButton(
            self, text="▶  Run", width=90, height=32,
            fg_color=PALETTE["success"], hover_color="#56d982",
            text_color="#061208", font=("Segoe UI",12,"bold"), corner_radius=8,
            command=self.ide.run_code,
        )
        self.run_btn.pack(side="left", padx=3)

        self.stop_btn = ctk.CTkButton(
            self, text="⏹  Stop", width=90, height=32,
            fg_color=PALETTE["error"], hover_color="#ff7070",
            text_color="#ffffff", font=("Segoe UI",12,"bold"), corner_radius=8,
            command=self.ide.stop_code, state="disabled",
        )
        self.stop_btn.pack(side="left", padx=3)

        tk.Frame(self, bg=PALETTE["border"], width=1, height=28).pack(side="left", padx=8)

        ctk.CTkLabel(self, text="Mode:", font=FONT_UI_S,
                     text_color=PALETTE["text_muted"]).pack(side="left", padx=4)
        self.mode_var = tk.StringVar(value="exec")
        for m in ["exec","compiled"]:
            ctk.CTkRadioButton(
                self, text=m, variable=self.mode_var, value=m,
                fg_color=PALETTE["accent"], hover_color=PALETTE["accent_glow"],
                font=FONT_UI_S, text_color=PALETTE["text_muted"],
            ).pack(side="left", padx=4)

        tk.Frame(self, bg=PALETTE["border"], width=1, height=28).pack(side="left", padx=8)

        ctk.CTkButton(self, text="⌘ Palette", width=90, height=32,
                       fg_color="transparent", hover_color=PALETTE["bg_hover"],
                       text_color=PALETTE["text_muted"], font=FONT_UI_S, corner_radius=6,
                       command=self.ide.open_palette).pack(side="left", padx=2)

        self.search = ctk.CTkEntry(
            self, placeholder_text="Quick search...", width=180, height=32,
            corner_radius=8, fg_color=PALETTE["bg_input"],
            border_color=PALETTE["border"],
            text_color=PALETTE["text"], font=FONT_UI_S,
        )
        self.search.pack(side="right", padx=12)
        self.search.bind("<KeyRelease>", self.ide.search_code)

        self.status_label = ctk.CTkLabel(self, text="Ready", font=FONT_UI_S,
                                          text_color=PALETTE["success"])
        self.status_label.pack(side="right", padx=6)
        self.status_dot = ctk.CTkLabel(self, text="●", font=("Segoe UI",14),
                                        text_color=PALETTE["success"])
        self.status_dot.pack(side="right")

    def set_status(self, text, color=None):
        self.status_label.configure(text=text)
        if color: self.status_dot.configure(text_color=color)

    def set_running(self, running):
        if running:
            self.run_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.set_status("Running...", PALETTE["warn"])
        else:
            self.run_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.set_status("Ready", PALETTE["success"])


# ─── STATUS BAR ──────────────────────────────────────────────────────────────

class StatusBar(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, height=24, corner_radius=0,
                         fg_color=PALETTE["accent_dark"], **kwargs)
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="  RINT IDE · Atlas Studio",
                     font=FONT_UI_S, text_color="#ccc9ff").pack(side="left", padx=8)
        self.zoom_lbl = ctk.CTkLabel(self, text="13px", font=FONT_UI_S,
                                      text_color="#9999cc")
        self.zoom_lbl.pack(side="right", padx=8)
        ctk.CTkLabel(self, text=" · ", font=FONT_UI_S,
                     text_color="#9999cc").pack(side="right")
        ctk.CTkLabel(self, text="UTF-8 · RINT · LF", font=FONT_UI_S,
                     text_color="#9999cc").pack(side="right", padx=8)
        ctk.CTkLabel(self, text=" · ", font=FONT_UI_S,
                     text_color="#9999cc").pack(side="right")
        self.pos_lbl = ctk.CTkLabel(self, text="Ln 1, Col 1", font=FONT_UI_S,
                                     text_color="#ccc9ff")
        self.pos_lbl.pack(side="right", padx=8)
        self.issue_lbl = ctk.CTkLabel(self, text="", font=FONT_UI_S,
                                       text_color=PALETTE["success"])
        self.issue_lbl.pack(side="right", padx=8)

    def update_pos(self, line, col):
        self.pos_lbl.configure(text=f"Ln {line}, Col {col}")

    def update_zoom(self, size):
        self.zoom_lbl.configure(text=f"{size}px")

    def update_issues(self, issues):
        errors = sum(1 for i in issues if i[1]=="error")
        warns  = sum(1 for i in issues if i[1]=="warn")
        if errors:
            self.issue_lbl.configure(text=f"  E:{errors}  W:{warns}",
                                      text_color=PALETTE["error"])
        elif warns:
            self.issue_lbl.configure(text=f"  W:{warns}", text_color=PALETTE["warn"])
        else:
            self.issue_lbl.configure(text="  OK", text_color=PALETTE["success"])


# ─── TAB BUTTON ──────────────────────────────────────────────────────────────

class TabButton(ctk.CTkFrame):
    def __init__(self, parent, title, close_cb, select_cb, **kwargs):
        super().__init__(parent, height=34, corner_radius=7,
                         fg_color=PALETTE["bg_tab_idle"], **kwargs)
        self.title_var = tk.StringVar(value=title)
        self.lbl = ctk.CTkLabel(self, textvariable=self.title_var,
                                 font=FONT_UI_S, text_color=PALETTE["text_muted"],
                                 cursor="hand2")
        self.lbl.pack(side="left", padx=(10,4))
        self.lbl.bind("<Button-1>", lambda e: select_cb())
        dot = ctk.CTkLabel(self, text="✦", font=FONT_UI_S,
                            text_color=PALETTE["text_dim"])
        dot.pack(side="left", padx=(0,2))
        self.dot = dot
        cl = ctk.CTkLabel(self, text="✕", font=FONT_UI_S,
                           text_color=PALETTE["text_muted"], cursor="hand2")
        cl.pack(side="left", padx=(0,8))
        cl.bind("<Button-1>", lambda e: close_cb())
        self.bind("<Button-1>", lambda e: select_cb())

    def set_active(self, active):
        self.configure(fg_color=PALETTE["bg_tab_active"] if active else PALETTE["bg_tab_idle"])
        self.lbl.configure(text_color=PALETTE["text"]       if active else PALETTE["text_muted"])
        self.dot.configure(text_color=PALETTE["accent"]     if active else PALETTE["text_dim"])

    def set_modified(self, modified):
        t = self.title_var.get().rstrip(" *")
        self.title_var.set(t + (" *" if modified else ""))


# ─── MAIN IDE ─────────────────────────────────────────────────────────────────

class RintIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RINT IDE  —  Atlas Studio v2.1")
        self.geometry("1440x880")
        self.minsize(960, 620)
        self.configure(fg_color=PALETTE["bg_root"])

        self.tabs        = []
        self.active_tab  = -1
        self._running    = False

        self._build_ui()
        self._bind_shortcuts()
        self._start_autosave()

        self.interpreter = RintInterpreter(
            output_cb  = lambda m: self._ui(self._console_output, m, "info"),
            log_cb     = lambda m: self._ui(self._console_output, m, "log"),
            error_cb   = lambda m: self._ui(self._on_error, m),
            ask_cb     = lambda p, n="__response__": self._ui(self._console_ask, p, n),
            vars_cb    = lambda v: self._ui(self.vars_panel.update_vars, v),
            turtle_cb  = lambda d, s: self._ui(self.turtle_panel.move, d, s),
        )

    def _console_output(self, msg, tag="info"):
        self.console_panel.add_msg(msg, tag)
        self.console_right.add_message(msg, tag)

    def _console_ask(self, prompt, var_name="__response__"):
        self.console_panel.ask_user(prompt, var_name)
        self.console_right.ask_user(prompt, var_name)

    def _ui(self, fn, *args):
        try: self.after(0, fn, *args)
        except: pass

    # ── Layout ───────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.toolbar = Toolbar(self, self)
        self.toolbar.pack(fill="x", side="top")

        self.body = tk.Frame(self, bg=PALETTE["bg_root"])
        self.body.pack(fill="both", expand=True)

        # Left sidebar
        self.sidebar_left = tk.Frame(self.body, bg=PALETTE["bg_sidebar"], width=210)
        self.sidebar_left.pack(side="left", fill="y")
        self.sidebar_left.pack_propagate(False)
        self.file_explorer = FileExplorer(self.sidebar_left, self)
        self.file_explorer.pack(fill="both", expand=True)

        # Center
        self.center = tk.Frame(self.body, bg=PALETTE["bg_root"])
        self.center.pack(side="left", fill="both", expand=True)

        # Tab bar
        self.tab_bar = tk.Frame(self.center, bg=PALETTE["bg_panel"], height=42)
        self.tab_bar.pack(fill="x")
        self.tab_btn_frame = tk.Frame(self.tab_bar, bg=PALETTE["bg_panel"])
        self.tab_btn_frame.pack(side="left", fill="y", padx=4)
        ctk.CTkButton(self.tab_bar, text="+", width=28, height=28,
                       fg_color="transparent", hover_color=PALETTE["bg_hover"],
                       text_color=PALETTE["text_muted"], font=("Segoe UI",16),
                       command=self.new_tab).pack(side="left", padx=4, pady=7)

        # Editor area
        self.editor_frame = tk.Frame(self.center, bg=PALETTE["bg_root"])
        self.editor_frame.pack(fill="both", expand=True)

        # Bottom panel
        self._bottom_h = 240
        self._bottom_visible = True
        self.bottom_panel = tk.Frame(self.center, bg=PALETTE["bg_root"], height=self._bottom_h)
        self.bottom_panel.pack(fill="x", side="bottom")
        self.bottom_panel.pack_propagate(False)
        self._build_bottom()

        # Right sidebar
        self.sidebar_right = tk.Frame(self.body, bg=PALETTE["bg_sidebar"], width=250)
        self.sidebar_right.pack(side="right", fill="y")
        self.sidebar_right.pack_propagate(False)
        self._build_right()

        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill="x", side="bottom")

        self.new_tab()

    def _build_bottom(self):
        btab = tk.Frame(self.bottom_panel, bg=PALETTE["bg_sidebar"], height=36)
        btab.pack(fill="x")
        btab.pack_propagate(False)
        self._btabs = {}
        self._bframes = {}
        for key in ["Output","Debug"]:
            btn = ctk.CTkButton(btab, text=key, width=82, height=28,
                                 fg_color="transparent", hover_color=PALETTE["bg_hover"],
                                 text_color=PALETTE["text_muted"], font=FONT_UI_S, corner_radius=6,
                                 command=lambda k=key: self._switch_bottom(k))
            btn.pack(side="left", padx=3, pady=4)
            self._btabs[key] = btn

        ctk.CTkButton(btab, text="⌄", width=28, height=24,
                       fg_color="transparent", hover_color=PALETTE["bg_hover"],
                       text_color=PALETTE["text_muted"], font=("Segoe UI",14),
                       command=self.toggle_bottom).pack(side="right", padx=8)

        self._bcontent = tk.Frame(self.bottom_panel, bg=PALETTE["bg_root"])
        self._bcontent.pack(fill="both", expand=True, side="bottom")

        self.console_panel = ConsolePanel(self._bcontent, self)
        self._bframes["Output"] = self.console_panel

        self.debug_text = tk.Text(
            self._bcontent, bg=PALETTE["bg_editor"], fg=PALETTE["text"],
            font=FONT_CODE_S, borderwidth=0, highlightthickness=0,
            state="disabled", wrap="word", padx=10, pady=6,
        )
        self.debug_text.tag_configure("error",   foreground=PALETTE["error"])
        self.debug_text.tag_configure("warn",    foreground=PALETTE["warn"])
        self.debug_text.tag_configure("info",    foreground=PALETTE["accent2"])
        self.debug_text.tag_configure("success", foreground=PALETTE["success"])
        self._bframes["Debug"] = self.debug_text

        self._switch_bottom("Output")

    def _switch_bottom(self, key):
        for k, f in self._bframes.items(): f.pack_forget()
        self._bframes[key].pack(fill="both", expand=True)
        for k, btn in self._btabs.items():
            btn.configure(
                fg_color=PALETTE["accent"] if k == key else "transparent",
                text_color="#ffffff"        if k == key else PALETTE["text_muted"],
            )

    def toggle_bottom(self):
        if self._bottom_visible:
            self._bcontent.pack_forget()
            self.bottom_panel.configure(height=36)
            self._bottom_visible = False
        else:
            self._bcontent.pack(fill="both", expand=True)
            self.bottom_panel.configure(height=self._bottom_h)
            self._bottom_visible = True

    def _build_right(self):
        rtab = tk.Frame(self.sidebar_right, bg=PALETTE["bg_panel"], height=36)
        rtab.pack(fill="x")
        self._rtabs  = {}
        self._rframes = {}
        rc = ctk.CTkFrame(self.sidebar_right, fg_color="transparent")
        rc.pack(fill="both", expand=True)
        
        self.vars_panel   = VariablesWatch(rc, self)
        self.turtle_panel = TurtlePreview(rc)
        self.audio_panel  = AudioPreview(rc)
        self.console_right = ConsoleOutputPanel(rc, self)
        
        self._rframes = {
            "Vars":self.vars_panel, 
            "Turtle":self.turtle_panel, 
            "Audio":self.audio_panel, 
            "Console":self.console_right,
        }
        
        for label in ["Vars","Turtle","Audio","Console"]:
            btn = ctk.CTkButton(rtab, text=label, width=55, height=28,
                                 fg_color="transparent", hover_color=PALETTE["bg_hover"],
                                 text_color=PALETTE["text_muted"], font=FONT_UI_S, corner_radius=6,
                                 command=lambda l=label: self._switch_right(l))
            btn.pack(side="left", padx=2, pady=4)
            self._rtabs[label] = btn
        self._switch_right("Vars")

    def _switch_right(self, key):
        for k, f in self._rframes.items(): f.pack_forget()
        self._rframes[key].pack(fill="both", expand=True)
        for k, btn in self._rtabs.items():
            btn.configure(
                fg_color=PALETTE["accent"] if k == key else "transparent",
                text_color="#ffffff"        if k == key else PALETTE["text_muted"],
            )

    # ── Tabs ─────────────────────────────────────────────────────────────────

    def new_tab(self, title="untitled.rint", code=None, path=None):
        editor = CodeEditor(self.editor_frame, self)
        if code: editor.set_code(code)
        idx    = len(self.tabs)
        info   = {"title": title, "editor": editor, "path": path}
        self.tabs.append(info)
        btn = TabButton(self.tab_btn_frame, title,
                        close_cb=lambda i=idx: self.close_tab(i),
                        select_cb=lambda i=idx: self.select_tab(i))
        btn.pack(side="left", padx=2, pady=5)
        info["btn"] = btn
        self.select_tab(idx)

    def select_tab(self, idx):
        if idx < 0 or idx >= len(self.tabs): return
        for t in self.tabs:
            t["editor"].pack_forget()
            t["btn"].set_active(False)
        self.active_tab = idx
        self.tabs[idx]["editor"].pack(fill="both", expand=True)
        self.tabs[idx]["btn"].set_active(True)
        self.update_title()

    def close_tab(self, idx):
        if len(self.tabs) <= 1: return
        self.tabs[idx]["editor"].destroy()
        self.tabs[idx]["btn"].destroy()
        self.tabs.pop(idx)
        self.active_tab = -1
        self.select_tab(min(idx, len(self.tabs)-1))

    def update_title(self):
        if self.active_tab < 0: return
        t   = self.tabs[self.active_tab]
        mod = t["editor"].modified_since_save
        self.title(f"{'● ' if mod else ''}{t['title']}  —  RINT IDE · Atlas Studio")
        t["btn"].set_modified(mod)

    def current_editor(self):
        if self.active_tab < 0 or not self.tabs: return None
        return self.tabs[self.active_tab]["editor"]

    # ── File ops ─────────────────────────────────────────────────────────────

    def open_file(self, path=None):
        if not path:
            path = filedialog.askopenfilename(
                filetypes=[("RINT files","*.rint"),("All files","*.*")])
        if not path or not os.path.isfile(path): return
        with open(path,"r",encoding="utf-8") as f:
            code = f.read()
        self.new_tab(os.path.basename(path), code=code, path=path)

    def open_file_dialog(self): self.open_file()

    def save_file(self, event=None):
        ed = self.current_editor()
        if not ed: return
        t    = self.tabs[self.active_tab]
        path = t.get("path")
        if not path:
            path = filedialog.asksaveasfilename(
                defaultextension=".rint",
                filetypes=[("RINT files","*.rint"),("All files","*.*")])
        if not path: return
        with open(path,"w",encoding="utf-8") as f:
            f.write(ed.get_code())
        t["path"] = path
        t["title"] = os.path.basename(path)
        t["btn"].title_var.set(t["title"])
        ed.modified_since_save = False
        self.update_title()
        self.console_panel.add_success(f"Saved: {path}")

    # ── Run ───────────────────────────────────────────────────────────────────

    def run_code(self, event=None):
        ed = self.current_editor()
        if not ed or self._running: return
        code = ed.get_code()
        self.console_panel.clear()
        self.console_panel.add_log("Run started", "log")
        self._log_debug("Run started", "info")
        self.toolbar.set_running(True)
        self._running = True
        self.interpreter.running = True
        t = threading.Thread(target=self._run_thread, args=(code,), daemon=True)
        t.start()
        self._poll()

    def _run_thread(self, code):
        try:
            self.interpreter.run(code)
        finally:
            self._running = False

    def _poll(self):
        if self._running:
            self.after(80, self._poll)
        else:
            self.toolbar.set_running(False)
            self.console_panel.add_log("Execution finished", "success")
            self._log_debug("Finished", "success")

    def stop_code(self, event=None):
        self.interpreter.running = False
        self._running = False
        self.toolbar.set_running(False)
        self.console_panel.add_warn("Stopped by user")

    def _on_error(self, msg):
        self.console_panel.add_error(msg)
        self._log_debug(msg, "error")

    def _log_debug(self, msg, tag="info"):
        self.debug_text.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.debug_text.insert("end", f"[{ts}] {msg}\n", tag)
        self.debug_text.configure(state="disabled")
        self.debug_text.see("end")

    # ── Features ─────────────────────────────────────────────────────────────

    def show_find(self, event=None):
        ed = self.current_editor()
        if ed: ed.find_bar.show()

    def open_palette(self, event=None):
        CommandPalette(self, self)

    def goto_line_dialog(self):
        ed = self.current_editor()
        if not ed: return
        val = simpledialog.askstring("Go to Line", "Line number:", parent=self)
        if val and val.isdigit():
            ed.goto_line(int(val))

    def insert_snippet(self, name):
        ed = self.current_editor()
        if not ed: return
        snippet = SNIPPETS.get(name, "")
        ed.text.insert("insert", snippet)
        ed.highlighter.highlight()

    def update_cursor_pos(self):
        ed = self.current_editor()
        if not ed: return
        pos = ed.text.index("insert")
        line, col = pos.split(".")
        self.status_bar.update_pos(line, int(col)+1)

    def update_issues(self, issues):
        self.status_bar.update_issues(issues)

    def search_code(self, event=None):
        query = self.toolbar.search.get().strip()
        ed    = self.current_editor()
        if not ed or not query: return
        ed.text.tag_remove("find_match","1.0","end")
        start = "1.0"
        while True:
            pos = ed.text.search(query, start, stopindex="end", nocase=True)
            if not pos: break
            end = f"{pos}+{len(query)}c"
            ed.text.tag_add("find_match", pos, end)
            start = end

    # ── Shortcuts ─────────────────────────────────────────────────────────────

    def _bind_shortcuts(self):
        self.bind("<Control-n>",   lambda e: self.new_tab())
        self.bind("<Control-o>",   lambda e: self.open_file_dialog())
        self.bind("<Control-s>",   self.save_file)
        self.bind("<Control-r>",   lambda e: self.run_code())
        self.bind("<Control-p>",   lambda e: self.open_palette())
        self.bind("<Control-g>",   lambda e: self.goto_line_dialog())
        self.bind("<Control-f>",   lambda e: self.show_find())
        self.bind("<Control-Tab>", lambda e: self.select_tab((self.active_tab+1) % max(len(self.tabs),1)))
        self.bind("<F5>",          lambda e: self.run_code())

    # ── Autosave ──────────────────────────────────────────────────────────────

    def _start_autosave(self):
        self._autosave()

    def _autosave(self):
        for t in self.tabs:
            if t.get("path") and t["editor"].modified_since_save:
                try:
                    with open(t["path"],"w",encoding="utf-8") as f:
                        f.write(t["editor"].get_code())
                    t["editor"].modified_since_save = False
                    self.update_title()
                except: pass
        self.after(30_000, self._autosave)


# ─── SPLASH ───────────────────────────────────────────────────────────────────

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.overrideredirect(True)
        w, h = 500, 300
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.configure(fg_color=PALETTE["bg_root"])
        self.wm_attributes("-topmost", True)
        self._build()
        self._step(0)

    def _build(self):
        ctk.CTkLabel(self, text="✦", font=("Segoe UI",60),
                     text_color=PALETTE["accent"]).place(relx=0.5, rely=0.22, anchor="center")
        ctk.CTkLabel(self, text="RINT IDE", font=("Segoe UI",30,"bold"),
                     text_color=PALETTE["text"]).place(relx=0.5, rely=0.48, anchor="center")
        ctk.CTkLabel(self, text="Atlas Studio · v2.0",
                     font=FONT_UI_S, text_color=PALETTE["text_muted"]
                     ).place(relx=0.5, rely=0.62, anchor="center")
        self.prog = ctk.CTkProgressBar(self, width=340, height=6, corner_radius=4,
                                        fg_color=PALETTE["border"],
                                        progress_color=PALETTE["accent"])
        self.prog.set(0)
        self.prog.place(relx=0.5, rely=0.80, anchor="center")
        self.status = ctk.CTkLabel(self, text="Initializing...",
                                    font=FONT_UI_S, text_color=PALETTE["text_muted"])
        self.status.place(relx=0.5, rely=0.90, anchor="center")

    def _step(self, n):
        steps = [
            (0.15, "Loading syntax engine..."),
            (0.30, "Building keyword index..."),
            (0.50, "Compiling autocomplete..."),
            (0.70, "Starting interpreter..."),
            (0.88, "Configuring UI panels..."),
            (1.00, "Ready!"),
        ]
        if n < len(steps):
            v, msg = steps[n]
            self.prog.set(v)
            self.status.configure(text=msg)
            self.after(280, self._step, n+1)
        else:
            self.after(350, self.destroy)


# ─── ENTRY ────────────────────────────────────────────────────────────────────

def main():
    root = ctk.CTk()
    root.withdraw()
    splash = SplashScreen(root)
    splash.update()

    def launch():
        try: splash.destroy()
        except: pass
        root.destroy()
        ide = RintIDE()
        ide.mainloop()

    root.after(2200, launch)
    root.mainloop()

if __name__ == "__main__":
    if "--no-splash" in sys.argv:
        RintIDE().mainloop()
    else:
        main()