"""
Roon v1.0
Professional PDF viewer with book-style page flip animation.
Multi-language: English, Hindi, Urdu, Arabic, French, Spanish, Chinese
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz
from PIL import Image, ImageTk, ImageDraw
import threading
import os, sys, math, json

APP_TITLE   = "Roon"
APP_VERSION = "1.0.0"
APP_W, APP_H = 1150, 760

# ── Colors (Windows 11 style) ────────────────────────────────────
BG_TITLE   = "#1f1f1f"
BG_TOOLBAR = "#ffffff"
BG_SIDEBAR = "#f5f5f5"
BG_CANVAS  = "#d0d0d0"
ACCENT     = "#0078d4"
ACCENT_H   = "#106ebe"
TEXT_D     = "#1a1a1a"
TEXT_M     = "#555555"
TEXT_L     = "#999999"
BORDER     = "#e0e0e0"
BTN_BG     = "#f0f0f0"
BTN_H      = "#e0e0e0"
SHADOW     = "#b0b0b0"

FLIP_STEPS  = 14
FLIP_MS     = 14
CACHE_SIZE  = 14

# ── Translations ─────────────────────────────────────────────────
LANGS = {
    "English": {
        "open":       "Open",
        "open_pdf":   "Open PDF...",
        "exit":       "Exit",
        "file":       "File",
        "view":       "View",
        "language":   "Language",
        "help":       "Help",
        "about":      "About",
        "zoom_in":    "Zoom In",
        "zoom_out":   "Zoom Out",
        "fit_page":   "Fit Page",
        "fit_width":  "Fit Width",
        "sidebar":    "Sidebar",
        "first":      "First",
        "prev":       "Prev",
        "next":       "Next",
        "last":       "Last",
        "pages":      "Pages",
        "no_pdf":     "No PDF open",
        "choose_pdf": "Choose a PDF file",
        "welcome1":   "Open a PDF and start reading",
        "welcome2":   "File → Open PDF  or  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nA professional PDF viewer\nwith book-style page flip animation.\n\nKeyboard Shortcuts:\n  Ctrl+O   Open PDF\n  ← →      Navigate pages\n  Ctrl++   Zoom In\n  Ctrl+-   Zoom Out\n  F        Fit Page\n  W        Fit Width\n  Esc      Quit",
        "page_of":    "of",
        "error_open": "Could not open PDF",
        "width":      "Width",
        "fit":        "Fit",
    },
    "हिंदी": {
        "open":       "खोलें",
        "open_pdf":   "PDF खोलें...",
        "exit":       "बंद करें",
        "file":       "फ़ाइल",
        "view":       "दृश्य",
        "language":   "भाषा",
        "help":       "सहायता",
        "about":      "जानकारी",
        "zoom_in":    "बड़ा करें",
        "zoom_out":   "छोटा करें",
        "fit_page":   "पेज फिट",
        "fit_width":  "चौड़ाई फिट",
        "sidebar":    "साइडबार",
        "first":      "पहला",
        "prev":       "पिछला",
        "next":       "अगला",
        "last":       "आखिरी",
        "pages":      "पेज",
        "no_pdf":     "कोई PDF नहीं खुली",
        "choose_pdf": "PDF फ़ाइल चुनें",
        "welcome1":   "PDF खोलें और पढ़ें",
        "welcome2":   "फ़ाइल → PDF खोलें  या  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nपेशेवर PDF व्यूअर\nकिताब जैसी पेज पलटने की सुविधा के साथ।\n\nकीबोर्ड शॉर्टकट:\n  Ctrl+O   PDF खोलें\n  ← →      पेज बदलें\n  Ctrl++   बड़ा करें\n  Ctrl+-   छोटा करें\n  F        पेज फिट\n  W        चौड़ाई फिट",
        "page_of":    "में से",
        "error_open": "PDF नहीं खुल सकी",
        "width":      "चौड़ाई",
        "fit":        "फिट",
    },
    "اردو": {
        "open":       "کھولیں",
        "open_pdf":   "PDF کھولیں...",
        "exit":       "بند کریں",
        "file":       "فائل",
        "view":       "منظر",
        "language":   "زبان",
        "help":       "مدد",
        "about":      "معلومات",
        "zoom_in":    "بڑا کریں",
        "zoom_out":   "چھوٹا کریں",
        "fit_page":   "صفحہ فٹ",
        "fit_width":  "چوڑائی فٹ",
        "sidebar":    "سائیڈبار",
        "first":      "پہلا",
        "prev":       "پچھلا",
        "next":       "اگلا",
        "last":       "آخری",
        "pages":      "صفحات",
        "no_pdf":     "کوئی PDF نہیں کھلی",
        "choose_pdf": "PDF فائل منتخب کریں",
        "welcome1":   "PDF کھولیں اور پڑھیں",
        "welcome2":   "فائل ← PDF کھولیں  یا  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nپیشہ ور PDF ویور\nکتاب جیسی صفحہ پلٹنے کی سہولت کے ساتھ۔",
        "page_of":    "میں سے",
        "error_open": "PDF نہیں کھل سکی",
        "width":      "چوڑائی",
        "fit":        "فٹ",
    },
    "العربية": {
        "open":       "فتح",
        "open_pdf":   "فتح PDF...",
        "exit":       "خروج",
        "file":       "ملف",
        "view":       "عرض",
        "language":   "اللغة",
        "help":       "مساعدة",
        "about":      "حول",
        "zoom_in":    "تكبير",
        "zoom_out":   "تصغير",
        "fit_page":   "احتواء الصفحة",
        "fit_width":  "احتواء العرض",
        "sidebar":    "الشريط الجانبي",
        "first":      "أول",
        "prev":       "السابق",
        "next":       "التالي",
        "last":       "آخر",
        "pages":      "الصفحات",
        "no_pdf":     "لم يتم فتح أي PDF",
        "choose_pdf": "اختر ملف PDF",
        "welcome1":   "افتح ملف PDF وابدأ القراءة",
        "welcome2":   "ملف ← فتح PDF  أو  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nعارض PDF احترافي\nمع تأثير تقليب الصفحات.",
        "page_of":    "من",
        "error_open": "تعذّر فتح الملف",
        "width":      "عرض",
        "fit":        "احتواء",
    },
    "Français": {
        "open":       "Ouvrir",
        "open_pdf":   "Ouvrir PDF...",
        "exit":       "Quitter",
        "file":       "Fichier",
        "view":       "Affichage",
        "language":   "Langue",
        "help":       "Aide",
        "about":      "À propos",
        "zoom_in":    "Zoom avant",
        "zoom_out":   "Zoom arrière",
        "fit_page":   "Ajuster la page",
        "fit_width":  "Ajuster la largeur",
        "sidebar":    "Panneau latéral",
        "first":      "Premier",
        "prev":       "Précédent",
        "next":       "Suivant",
        "last":       "Dernier",
        "pages":      "Pages",
        "no_pdf":     "Aucun PDF ouvert",
        "choose_pdf": "Choisir un fichier PDF",
        "welcome1":   "Ouvrez un PDF et commencez à lire",
        "welcome2":   "Fichier → Ouvrir PDF  ou  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nVisionneuse PDF professionnelle\navec animation de tournage de pages.",
        "page_of":    "sur",
        "error_open": "Impossible d'ouvrir le PDF",
        "width":      "Largeur",
        "fit":        "Ajuster",
    },
    "Español": {
        "open":       "Abrir",
        "open_pdf":   "Abrir PDF...",
        "exit":       "Salir",
        "file":       "Archivo",
        "view":       "Vista",
        "language":   "Idioma",
        "help":       "Ayuda",
        "about":      "Acerca de",
        "zoom_in":    "Acercar",
        "zoom_out":   "Alejar",
        "fit_page":   "Ajustar página",
        "fit_width":  "Ajustar ancho",
        "sidebar":    "Panel lateral",
        "first":      "Primero",
        "prev":       "Anterior",
        "next":       "Siguiente",
        "last":       "Último",
        "pages":      "Páginas",
        "no_pdf":     "No hay PDF abierto",
        "choose_pdf": "Elegir archivo PDF",
        "welcome1":   "Abra un PDF y comience a leer",
        "welcome2":   "Archivo → Abrir PDF  o  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nVisor de PDF profesional\ncon animación de paso de páginas.",
        "page_of":    "de",
        "error_open": "No se pudo abrir el PDF",
        "width":      "Ancho",
        "fit":        "Ajustar",
    },
    "中文": {
        "open":       "打开",
        "open_pdf":   "打开 PDF...",
        "exit":       "退出",
        "file":       "文件",
        "view":       "视图",
        "language":   "语言",
        "help":       "帮助",
        "about":      "关于",
        "zoom_in":    "放大",
        "zoom_out":   "缩小",
        "fit_page":   "适合页面",
        "fit_width":  "适合宽度",
        "sidebar":    "侧边栏",
        "first":      "第一页",
        "prev":       "上一页",
        "next":       "下一页",
        "last":       "最后一页",
        "pages":      "页面",
        "no_pdf":     "未打开 PDF",
        "choose_pdf": "选择 PDF 文件",
        "welcome1":   "打开 PDF 开始阅读",
        "welcome2":   "文件 → 打开 PDF  或  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\n专业 PDF 阅读器\n带有书页翻转动画效果。",
        "page_of":    "共",
        "error_open": "无法打开 PDF",
        "width":      "宽度",
        "fit":        "适合",
    },
    "Deutsch": {
        "open":       "Öffnen",
        "open_pdf":   "PDF öffnen...",
        "exit":       "Beenden",
        "file":       "Datei",
        "view":       "Ansicht",
        "language":   "Sprache",
        "help":       "Hilfe",
        "about":      "Über",
        "zoom_in":    "Vergrößern",
        "zoom_out":   "Verkleinern",
        "fit_page":   "Seite einpassen",
        "fit_width":  "Breite einpassen",
        "sidebar":    "Seitenleiste",
        "first":      "Erste",
        "prev":       "Zurück",
        "next":       "Weiter",
        "last":       "Letzte",
        "pages":      "Seiten",
        "no_pdf":     "Keine PDF geöffnet",
        "choose_pdf": "PDF-Datei auswählen",
        "welcome1":   "PDF öffnen und lesen",
        "welcome2":   "Datei → PDF öffnen  oder  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nProfessioneller PDF-Betrachter\nmit Buchseiten-Umblätteranimation.",
        "page_of":    "von",
        "error_open": "PDF konnte nicht geöffnet werden",
        "width":      "Breite",
        "fit":        "Einpassen",
    },
    "Português": {
        "open":       "Abrir",
        "open_pdf":   "Abrir PDF...",
        "exit":       "Sair",
        "file":       "Arquivo",
        "view":       "Visualizar",
        "language":   "Idioma",
        "help":       "Ajuda",
        "about":      "Sobre",
        "zoom_in":    "Aumentar zoom",
        "zoom_out":   "Diminuir zoom",
        "fit_page":   "Ajustar página",
        "fit_width":  "Ajustar largura",
        "sidebar":    "Painel lateral",
        "first":      "Primeiro",
        "prev":       "Anterior",
        "next":       "Próximo",
        "last":       "Último",
        "pages":      "Páginas",
        "no_pdf":     "Nenhum PDF aberto",
        "choose_pdf": "Escolher arquivo PDF",
        "welcome1":   "Abra um PDF e comece a ler",
        "welcome2":   "Arquivo → Abrir PDF  ou  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nVisualizador de PDF profissional\ncom animação de virar páginas.",
        "page_of":    "de",
        "error_open": "Não foi possível abrir o PDF",
        "width":      "Largura",
        "fit":        "Ajustar",
    },
    "Italiano": {
        "open":       "Apri",
        "open_pdf":   "Apri PDF...",
        "exit":       "Esci",
        "file":       "File",
        "view":       "Visualizza",
        "language":   "Lingua",
        "help":       "Aiuto",
        "about":      "Informazioni",
        "zoom_in":    "Ingrandisci",
        "zoom_out":   "Rimpicciolisci",
        "fit_page":   "Adatta pagina",
        "fit_width":  "Adatta larghezza",
        "sidebar":    "Pannello laterale",
        "first":      "Prima",
        "prev":       "Precedente",
        "next":       "Successivo",
        "last":       "Ultima",
        "pages":      "Pagine",
        "no_pdf":     "Nessun PDF aperto",
        "choose_pdf": "Scegli file PDF",
        "welcome1":   "Apri un PDF e inizia a leggere",
        "welcome2":   "File → Apri PDF  o  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nVisualizzatore PDF professionale\ncon animazione sfoglia pagina.",
        "page_of":    "di",
        "error_open": "Impossibile aprire il PDF",
        "width":      "Larghezza",
        "fit":        "Adatta",
    },
    "日本語": {
        "open":       "開く",
        "open_pdf":   "PDFを開く...",
        "exit":       "終了",
        "file":       "ファイル",
        "view":       "表示",
        "language":   "言語",
        "help":       "ヘルプ",
        "about":      "バージョン情報",
        "zoom_in":    "拡大",
        "zoom_out":   "縮小",
        "fit_page":   "ページに合わせる",
        "fit_width":  "幅に合わせる",
        "sidebar":    "サイドバー",
        "first":      "最初",
        "prev":       "前へ",
        "next":       "次へ",
        "last":       "最後",
        "pages":      "ページ",
        "no_pdf":     "PDFが開かれていません",
        "choose_pdf": "PDFファイルを選択",
        "welcome1":   "PDFを開いて読み始めましょう",
        "welcome2":   "ファイル → PDFを開く  または  Ctrl+O",
        "about_txt":  f"Roon v{APP_VERSION}\n\nプロフェッショナルPDFビューア\n本のようなページめくりアニメーション付き。",
        "page_of":    "/",
        "error_open": "PDFを開けませんでした",
        "width":      "幅",
        "fit":        "合わせる",
    },
}

# Settings file path
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".roon_settings.json")


def load_settings():
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except:
        return {"language": "English"}


def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass


# ── LRU Cache ────────────────────────────────────────────────────
class PageCache:
    def __init__(self, maxsize=CACHE_SIZE):
        self._d, self._order, self._max = {}, [], maxsize
        self._lock = threading.Lock()

    def get(self, k):
        with self._lock: return self._d.get(k)

    def put(self, k, v):
        with self._lock:
            if k in self._d: self._order.remove(k)
            self._d[k] = v; self._order.append(k)
            if len(self._order) > self._max:
                del self._d[self._order.pop(0)]

    def clear(self):
        with self._lock: self._d.clear(); self._order.clear()


# ── Flat Button ──────────────────────────────────────────────────
class Btn(tk.Label):
    def __init__(self, parent, text, cmd=None, accent=False, w=None, **kw):
        cfg = dict(font=("Segoe UI", 9), cursor="hand2", relief="flat",
                   padx=9, pady=5, bg=ACCENT if accent else BTN_BG,
                   fg="white" if accent else TEXT_D, bd=0)
        if w: cfg["width"] = w
        cfg.update(kw)
        super().__init__(parent, text=text, **cfg)
        self._cmd  = cmd
        self._base = cfg["bg"]
        self._acc  = accent
        self.bind("<Enter>",           lambda e: self.config(bg=ACCENT_H if accent else BTN_H))
        self.bind("<Leave>",           lambda e: self.config(bg=self._base))
        self.bind("<ButtonRelease-1>", lambda e: self._cmd() if self._cmd else None)


# ── Thumbnail Sidebar ─────────────────────────────────────────────
class SideBar(tk.Frame):
    def __init__(self, parent, on_select, lang_key="Pages", **kw):
        super().__init__(parent, bg=BG_SIDEBAR, width=145, **kw)
        self.pack_propagate(False)
        self.on_select = on_select
        self._frames, self._photos, self._sel = [], [], -1
        self._header_lbl = None
        self._build(lang_key)

    def _build(self, lang_key):
        self._header_lbl = tk.Label(self, text=lang_key,
                                     font=("Segoe UI", 9, "bold"),
                                     bg=BG_SIDEBAR, fg=TEXT_M)
        self._header_lbl.pack(pady=(8, 4))
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        wrap = tk.Frame(self, bg=BG_SIDEBAR); wrap.pack(fill="both", expand=True)
        self.cv = tk.Canvas(wrap, bg=BG_SIDEBAR, bd=0, highlightthickness=0, width=130)
        sb = tk.Scrollbar(wrap, orient="vertical", command=self.cv.yview)
        self.cv.config(yscrollcommand=sb.set)
        self.cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.inner = tk.Frame(self.cv, bg=BG_SIDEBAR)
        win = self.cv.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.cv.config(scrollregion=self.cv.bbox("all")))
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfig(win, width=e.width))
        self.cv.bind("<MouseWheel>", lambda e: self.cv.yview_scroll(int(-e.delta/120), "units"))

    def update_label(self, text):
        if self._header_lbl:
            self._header_lbl.config(text=text)

    def clear(self):
        for w in self.inner.winfo_children(): w.destroy()
        self._frames.clear(); self._photos.clear(); self._sel = -1

    def add(self, img, n):
        W = 110; r = W / img.width
        ph = ImageTk.PhotoImage(img.resize((W, int(img.height*r)), Image.LANCZOS))
        self._photos.append(ph)
        idx = n - 1
        fr = tk.Frame(self.inner, bg=BG_SIDEBAR, pady=3, cursor="hand2")
        fr.pack(fill="x", padx=4)
        il = tk.Label(fr, image=ph, bg="white", bd=1, relief="solid")
        il.pack()
        nl = tk.Label(fr, text=str(n), font=("Segoe UI", 8), bg=BG_SIDEBAR, fg=TEXT_M)
        nl.pack()
        self._frames.append((fr, il, nl))
        for w in (fr, il, nl):
            w.bind("<Button-1>", lambda e, i=idx: self.select(i, fire=True))

    def select(self, idx, fire=False):
        if 0 <= self._sel < len(self._frames):
            f, il, nl = self._frames[self._sel]
            f.config(bg=BG_SIDEBAR); il.config(bg="white"); nl.config(bg=BG_SIDEBAR)
        self._sel = idx
        if 0 <= idx < len(self._frames):
            f, il, nl = self._frames[idx]
            f.config(bg="#ddeeff"); il.config(bg="#c8e0ff"); nl.config(bg="#ddeeff")
            self.cv.yview_moveto(max(0, idx/max(len(self._frames), 1) - 0.1))
        if fire: self.on_select(idx)


# ── Page Flip Animator ────────────────────────────────────────────
class FlipAnimator:
    def __init__(self, canvas, old_img, new_img, direction, on_done, pw, ph, cx, cy):
        self.cv      = canvas
        self.old     = old_img
        self.new     = new_img
        self.dir     = direction
        self.done_cb = on_done
        self.pw, self.ph = pw, ph
        self.cx, self.cy = cx, cy
        self.step    = 0
        self._refs   = []
        self._run()

    def _shadow_overlay(self, w, h, alpha_max, reverse=False):
        shade = Image.new("RGBA", (w, h), (0,0,0,0))
        draw  = ImageDraw.Draw(shade)
        steps = min(40, w)
        for i in range(steps):
            a = int(alpha_max * (1 - i/steps))
            x = (w-1-i) if not reverse else i
            draw.line([(x,0),(x,h)], fill=(0,0,0,a))
        return shade

    def _run(self):
        if self.step > FLIP_STEPS:
            self.done_cb(); return

        t    = self.step / FLIP_STEPS
        ease = t * t * (3 - 2*t)

        self.cv.delete("all")
        self._refs.clear()
        pw, ph, cx, cy = self.pw, self.ph, self.cx, self.cy
        x0, y0 = cx-pw//2, cy-ph//2
        x1, y1 = cx+pw//2, cy+ph//2

        # Shadow under page
        self.cv.create_rectangle(x0+5,y0+5,x1+5,y1+5, fill=SHADOW, outline="")

        if self.dir == "left":
            fold_x = int(pw * (1 - ease))

            # New page revealed (right portion)
            if pw - fold_x > 0:
                new_strip = self.new.crop((fold_x, 0, pw, ph))
                ph_new = ImageTk.PhotoImage(new_strip)
                self._refs.append(ph_new)
                nx = x0 + fold_x + (pw-fold_x)//2
                self.cv.create_image(nx, cy, image=ph_new)

            # Old page compressing left with shadow
            if fold_x > 2:
                comp = self.old.resize((fold_x, ph), Image.LANCZOS)
                shade = self._shadow_overlay(fold_x, ph,
                                             int(160 * math.sin(ease * math.pi)))
                comp_rgba = comp.convert("RGBA")
                comp_rgba = Image.alpha_composite(comp_rgba, shade)
                ph_old = ImageTk.PhotoImage(comp_rgba.convert("RGB"))
                self._refs.append(ph_old)
                self.cv.create_image(x0 + fold_x//2, cy, image=ph_old)

        else:  # right = prev page
            fold_x = int(pw * ease)

            # New page growing from left
            if fold_x > 0:
                new_strip = self.new.crop((0, 0, fold_x, ph))
                ph_new = ImageTk.PhotoImage(new_strip)
                self._refs.append(ph_new)
                self.cv.create_image(x0 + fold_x//2, cy, image=ph_new)

            # Old page compressing to right
            old_w = pw - fold_x
            if old_w > 2:
                comp = self.old.resize((old_w, ph), Image.LANCZOS)
                shade = self._shadow_overlay(old_w, ph,
                                             int(160 * math.sin((1-ease) * math.pi)),
                                             reverse=True)
                comp_rgba = comp.convert("RGBA")
                comp_rgba = Image.alpha_composite(comp_rgba, shade)
                ph_old = ImageTk.PhotoImage(comp_rgba.convert("RGB"))
                self._refs.append(ph_old)
                self.cv.create_image(x0 + fold_x + old_w//2, cy, image=ph_old)

        self.cv.create_rectangle(x0, y0, x1, y1, outline=BORDER, width=1)
        self.step += 1
        self.cv.after(FLIP_MS, self._run)


# ── Main Application ──────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings   = load_settings()
        self._lang_name = self.settings.get("language", "English")
        self.T          = LANGS[self._lang_name]   # translation dict

        self.title(APP_TITLE)
        self.geometry(f"{APP_W}x{APP_H}")
        self.minsize(800, 560)
        self.config(bg="#f3f3f3")

        # Try to set icon
        icon_path = self._asset("app.ico")
        if os.path.exists(icon_path):
            try: self.iconbitmap(icon_path)
            except: pass

        self.pdf        = None
        self.total      = 0
        self.cur        = 0
        self.zoom       = 1.0
        self.fit        = "page"
        self.cache      = PageCache()
        self._animating = False
        self._cur_pil   = None
        self._refs      = []
        self._maximized = False
        self._side_on   = True
        self._render_id = None

        self._build()
        self._keys()
        self._welcome()

    def _asset(self, name):
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "assets", name)

    def T_(self, key):
        return self.T.get(key, LANGS["English"].get(key, key))

    # ── Build ──────────────────────────────────────────────────────
    def _build(self):
        self._titlebar()
        self._menubar()
        self._toolbar()
        self._body()
        self._statusbar()

    def _titlebar(self):
        self._tbar = tk.Frame(self, bg=BG_TITLE, height=32)
        self._tbar.pack(fill="x"); self._tbar.pack_propagate(False)
        self._title_lbl = tk.Label(self._tbar, text="  📄 "+APP_TITLE,
                                    font=("Segoe UI", 9), bg=BG_TITLE, fg="white")
        self._title_lbl.pack(side="left")
        ctrl = tk.Frame(self._tbar, bg=BG_TITLE); ctrl.pack(side="right")
        for sym, cmd, hov in [("─", self.iconify, "#3a3a3a"),
                               ("□", self._maxim,  "#3a3a3a"),
                               ("✕", self.destroy, "#c42b1c")]:
            b = tk.Label(ctrl, text=sym, font=("Segoe UI", 10), bg=BG_TITLE,
                         fg="white", width=4, cursor="hand2", pady=6)
            b.pack(side="left")
            b.bind("<Enter>",    lambda e, h=hov, w=b: w.config(bg=h))
            b.bind("<Leave>",    lambda e, w=b: w.config(bg=BG_TITLE))
            b.bind("<Button-1>", lambda e, c=cmd: c())
        self._tbar.bind("<Button-1>",  self._drag0)
        self._tbar.bind("<B1-Motion>", self._drag1)
        self._title_lbl.bind("<Button-1>",  self._drag0)
        self._title_lbl.bind("<B1-Motion>", self._drag1)

    def _drag0(self, e): self._ox=e.x_root-self.winfo_x(); self._oy=e.y_root-self.winfo_y()
    def _drag1(self, e):
        if not self._maximized: self.geometry(f"+{e.x_root-self._ox}+{e.y_root-self._oy}")
    def _maxim(self):
        self.wm_state("normal" if self._maximized else "zoomed")
        self._maximized = not self._maximized

    def _menubar(self):
        self._menu = tk.Menu(self, bg=BG_TOOLBAR, fg=TEXT_D,
                              activebackground=ACCENT, activeforeground="white",
                              relief="flat", font=("Segoe UI", 9))
        self.config(menu=self._menu)
        self._rebuild_menu()

    def _rebuild_menu(self):
        self._menu.delete(0, "end")

        fm = tk.Menu(self._menu, tearoff=0, bg=BG_TOOLBAR, fg=TEXT_D,
                     activebackground=ACCENT, activeforeground="white",
                     font=("Segoe UI", 9))
        fm.add_command(label="📂  "+self.T_("open_pdf"), command=self.open_pdf, accelerator="Ctrl+O")
        fm.add_separator()
        fm.add_command(label=self.T_("exit"), command=self.destroy)
        self._menu.add_cascade(label=self.T_("file"), menu=fm)

        vm = tk.Menu(self._menu, tearoff=0, bg=BG_TOOLBAR, fg=TEXT_D,
                     activebackground=ACCENT, activeforeground="white",
                     font=("Segoe UI", 9))
        vm.add_command(label=self.T_("zoom_in")+"  (+)",  command=self.zoom_in,  accelerator="Ctrl++")
        vm.add_command(label=self.T_("zoom_out")+" (-)",  command=self.zoom_out, accelerator="Ctrl+-")
        vm.add_separator()
        vm.add_command(label=self.T_("fit_page")+"  (F)", command=self.fit_page)
        vm.add_command(label=self.T_("fit_width")+" (W)", command=self.fit_width)
        vm.add_separator()
        vm.add_command(label=self.T_("sidebar"),           command=self.toggle_side)
        self._menu.add_cascade(label=self.T_("view"), menu=vm)

        lm = tk.Menu(self._menu, tearoff=0, bg=BG_TOOLBAR, fg=TEXT_D,
                     activebackground=ACCENT, activeforeground="white",
                     font=("Segoe UI", 9))
        for lang in LANGS:
            lm.add_command(label=lang, command=lambda l=lang: self._set_lang(l))
        self._menu.add_cascade(label=self.T_("language"), menu=lm)

        hm = tk.Menu(self._menu, tearoff=0, bg=BG_TOOLBAR, fg=TEXT_D,
                     activebackground=ACCENT, activeforeground="white",
                     font=("Segoe UI", 9))
        hm.add_command(label=self.T_("about"), command=self._show_about)
        self._menu.add_cascade(label=self.T_("help"), menu=hm)

    def _set_lang(self, lang):
        self._lang_name = lang
        self.T = LANGS[lang]
        self.settings["language"] = lang
        save_settings(self.settings)
        self._rebuild_menu()
        self._rebuild_toolbar()
        if hasattr(self, "sidebar"):
            self.sidebar.update_label(self.T_("pages"))
        if hasattr(self, "st_lbl") and not self.pdf:
            self.st_lbl.config(text=self.T_("no_pdf"))
        self._refresh_ui_labels()

    def _refresh_ui_labels(self):
        if self.pdf:
            pg = self.cur + 1
            self.tot_lbl.config(text=f"/ {self.total}")
        else:
            self.tot_lbl.config(text="/ —")

    def _show_about(self):
        messagebox.showinfo(APP_TITLE + " v"+APP_VERSION, self.T_("about_txt"))

    def _toolbar(self):
        self._tb_frame = tk.Frame(self, bg=BG_TOOLBAR, height=44)
        self._tb_frame.pack(fill="x"); self._tb_frame.pack_propagate(False)
        self._tb_sep = tk.Frame(self, bg=BORDER, height=1)
        self._tb_sep.pack(fill="x")
        self._rebuild_toolbar()

    def _rebuild_toolbar(self):
        for w in self._tb_frame.winfo_children(): w.destroy()
        T = self.T

        Btn(self._tb_frame, "📂  "+self.T_("open"), self.open_pdf).pack(
            side="left", padx=(8,4), pady=6)
        tk.Frame(self._tb_frame, bg=BORDER, width=1, height=28).pack(
            side="left", padx=6, pady=8)
        Btn(self._tb_frame, "☰", self.toggle_side).pack(side="left", padx=2)
        tk.Frame(self._tb_frame, bg=BORDER, width=1, height=28).pack(
            side="left", padx=6, pady=8)

        nav = tk.Frame(self._tb_frame, bg=BG_TOOLBAR)
        nav.pack(side="left", expand=True)
        Btn(nav, "⏮", self.go_first).pack(side="left", padx=1)
        Btn(nav, "◀  "+self.T_("prev"), self.go_prev).pack(side="left", padx=2)

        self.pg_var = tk.StringVar(value="—")
        tk.Entry(nav, textvariable=self.pg_var, width=4,
                 font=("Segoe UI",9), justify="center",
                 relief="solid", bd=1, bg="white", fg=TEXT_D
                 ).pack(side="left", padx=4)
        self.tot_lbl = tk.Label(nav, text="/ —", font=("Segoe UI",9),
                                bg=BG_TOOLBAR, fg=TEXT_M)
        self.tot_lbl.pack(side="left", padx=2)
        Btn(nav, self.T_("next")+"  ▶", self.go_next).pack(side="left", padx=2)
        Btn(nav, "⏭", self.go_last).pack(side="left", padx=1)

        zf = tk.Frame(self._tb_frame, bg=BG_TOOLBAR)
        zf.pack(side="right", padx=8)
        Btn(zf, "A-", self.zoom_out).pack(side="left", padx=1)
        self.zlbl = tk.Label(zf, text="100%", font=("Segoe UI",9),
                             bg=BG_TOOLBAR, fg=TEXT_D, width=5)
        self.zlbl.pack(side="left", padx=4)
        Btn(zf, "A+", self.zoom_in).pack(side="left", padx=1)
        tk.Frame(zf, bg=BORDER, width=1, height=28).pack(
            side="left", padx=6, pady=8)
        Btn(zf, self.T_("fit"),   self.fit_page).pack(side="left", padx=1)
        Btn(zf, self.T_("width"), self.fit_width).pack(side="left", padx=2)

    def _body(self):
        self.body = tk.Frame(self, bg="#f3f3f3")
        self.body.pack(fill="both", expand=True)
        self.sidebar = SideBar(self.body, on_select=self._thumb_sel,
                               lang_key=self.T_("pages"))
        self.sidebar.pack(side="left", fill="y")
        tk.Frame(self.body, bg=BORDER, width=1).pack(side="left", fill="y")
        cf = tk.Frame(self.body, bg=BG_CANVAS)
        cf.pack(side="left", fill="both", expand=True)
        self.cv = tk.Canvas(cf, bg=BG_CANVAS, bd=0, highlightthickness=0)
        vb = tk.Scrollbar(cf, orient="vertical",   command=self.cv.yview)
        hb = tk.Scrollbar(cf, orient="horizontal", command=self.cv.xview)
        vb.pack(side="right", fill="y")
        hb.pack(side="bottom", fill="x")
        self.cv.pack(fill="both", expand=True)
        self.cv.config(yscrollcommand=vb.set, xscrollcommand=hb.set)
        self.cv.bind("<Configure>", self._on_resize)
        self.cv.bind("<MouseWheel>",
            lambda e: self.zoom_in()  if (e.state & 4 and e.delta > 0)
            else self.zoom_out() if (e.state & 4)
            else self.cv.yview_scroll(int(-e.delta/120), "units"))

    def _statusbar(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", side="bottom")
        bar = tk.Frame(self, bg=BG_TOOLBAR, height=24)
        bar.pack(fill="x", side="bottom"); bar.pack_propagate(False)
        self.st_lbl = tk.Label(bar, text=self.T_("no_pdf"),
                               font=("Segoe UI",8), bg=BG_TOOLBAR,
                               fg=TEXT_M, anchor="w")
        self.st_lbl.pack(side="left", padx=10)
        self.st_r = tk.Label(bar, text="", font=("Segoe UI",8),
                             bg=BG_TOOLBAR, fg=TEXT_M, anchor="e")
        self.st_r.pack(side="right", padx=10)
        # Version label
        tk.Label(bar, text=f"v{APP_VERSION}", font=("Segoe UI",8),
                 bg=BG_TOOLBAR, fg=TEXT_L).pack(side="right", padx=4)

    # ── Welcome ────────────────────────────────────────────────────
    def _welcome(self):
        def draw(*_):
            w = self.cv.winfo_width() or 600
            h = self.cv.winfo_height() or 400
            self.cv.delete("all")
            self.cv.create_text(w//2, h//2-45, text="📄",
                                font=("Segoe UI Emoji",56), fill="#c0c0c0")
            self.cv.create_text(w//2, h//2+15, fill="#aaa",
                                text=self.T_("welcome1"),
                                font=("Segoe UI",16))
            self.cv.create_text(w//2, h//2+44, fill="#bbb",
                                text=self.T_("welcome2"),
                                font=("Segoe UI",10))
        self.cv.bind("<Configure>", lambda e: draw())
        draw()

    # ── Open / Load ───────────────────────────────────────────────
    def open_pdf(self):
        p = filedialog.askopenfilename(title=self.T_("choose_pdf"),
            filetypes=[("PDF","*.pdf"),("All","*.*")])
        if p: self._load(p)

    def _load(self, path):
        try:
            if self.pdf: self.pdf.close()
            self.pdf   = fitz.open(path)
            self.total = len(self.pdf)
            self.cur   = 0
            self.zoom  = 1.0
            self.fit   = "page"
            self.cache.clear()
            self._cur_pil = None
            fname = os.path.basename(path)
            self.title(f"{fname} — {APP_TITLE}")
            self.st_lbl.config(text=f"  {fname}  •  {self.total} {self.T_('pages')}")
            self.tot_lbl.config(text=f"/ {self.total}")
            self.sidebar.clear()
            self.cv.unbind("<Configure>")
            self.cv.bind("<Configure>", self._on_resize)
            threading.Thread(target=self._load_thumbs, daemon=True).start()
            threading.Thread(target=self._precache, args=(0,), daemon=True).start()
            self._show_page(0, animate=False)
        except Exception as ex:
            messagebox.showerror(self.T_("error_open"), str(ex))

    def _load_thumbs(self):
        for i in range(self.total):
            try:
                px  = self.pdf[i].get_pixmap(matrix=fitz.Matrix(0.15, 0.15))
                img = Image.frombytes("RGB", [px.width, px.height], px.samples)
                self.after(0, self.sidebar.add, img, i+1)
            except: pass

    def _precache(self, idx):
        for i in range(idx, min(idx+4, self.total)):
            key = (i, self.fit, round(self.zoom, 2))
            if not self.cache.get(key):
                r = self._render_pil(i)
                if r: self.cache.put(key, r)

    # ── Render ─────────────────────────────────────────────────────
    def _render_pil(self, idx):
        if not self.pdf or idx < 0 or idx >= self.total: return None
        try:
            page = self.pdf[idx]
            cw   = max(self.cv.winfo_width()-40, 300)
            ch   = max(self.cv.winfo_height()-40, 400)
            r    = page.rect
            if self.fit == "page":
                z = min(cw/r.width, ch/r.height, 3.0)
            elif self.fit == "width":
                z = min(cw/r.width, 3.0)
            else:
                z = self.zoom
            px  = page.get_pixmap(matrix=fitz.Matrix(z, z))
            img = Image.frombytes("RGB", [px.width, px.height], px.samples)
            return img, z
        except: return None

    def _get_img(self, idx):
        key = (idx, self.fit, round(self.zoom, 2))
        hit = self.cache.get(key)
        if hit: return hit
        r = self._render_pil(idx)
        if r: self.cache.put(key, r)
        return r

    def _show_page(self, idx, animate=True, direction="left"):
        if self._animating: return
        old_pil = self._cur_pil

        def worker():
            result = self._get_img(idx)
            if result:
                self.after(0, self._display, idx, result[0], result[1],
                           animate, direction, old_pil)
                threading.Thread(target=self._precache, args=(idx,), daemon=True).start()

        threading.Thread(target=worker, daemon=True).start()

    def _display(self, idx, img, z, animate, direction, old_pil):
        self.cur = idx; self._cur_pil = img; self.zoom = z
        cw = self.cv.winfo_width()  or APP_W-200
        ch = self.cv.winfo_height() or APP_H-120
        pw, ph = img.size
        cx = max(cw//2, pw//2+20)
        cy = max(ch//2, ph//2+20)
        self.pg_var.set(str(idx+1))
        self.zlbl.config(text=f"{int(z*100)}%")
        self.st_r.config(text=f"  {self.T_('pages')} {idx+1} {self.T_('page_of')} {self.total}  |  {int(z*100)}%  ")
        self.sidebar.select(idx)
        self.cv.config(scrollregion=(0,0,max(cw,pw+40),max(ch,ph+40)))
        self.cv.xview_moveto(0); self.cv.yview_moveto(0)
        if animate and old_pil and not self._animating:
            self._animating = True
            resized = old_pil.resize(img.size, Image.LANCZOS) if old_pil.size != img.size else old_pil
            FlipAnimator(self.cv, resized, img, direction, self._anim_done, pw, ph, cx, cy)
        else:
            self._draw_static(img, pw, ph, cx, cy)

    def _draw_static(self, img, pw, ph, cx, cy):
        self.cv.delete("all")
        self.cv.create_rectangle(cx-pw//2+5, cy-ph//2+5,
                                  cx+pw//2+5, cy+ph//2+5,
                                  fill=SHADOW, outline="")
        photo = ImageTk.PhotoImage(img)
        self._refs = [photo]
        self.cv.create_image(cx, cy, image=photo)
        self.cv.create_rectangle(cx-pw//2, cy-ph//2,
                                  cx+pw//2, cy+ph//2,
                                  outline=BORDER, width=1)

    def _anim_done(self):
        self._animating = False
        img = self._cur_pil
        cw  = self.cv.winfo_width()  or APP_W-200
        ch  = self.cv.winfo_height() or APP_H-120
        pw, ph = img.size
        self._draw_static(img, pw, ph, max(cw//2,pw//2+20), max(ch//2,ph//2+20))

    # ── Navigation ─────────────────────────────────────────────────
    def go_to(self, n):
        if not self.pdf or self._animating: return
        n = max(0, min(n, self.total-1))
        if n == self.cur: return
        d = "left" if n > self.cur else "right"
        self._show_page(n, animate=True, direction=d)

    def go_next(self):  self.go_to(self.cur+1)
    def go_prev(self):  self.go_to(self.cur-1)
    def go_first(self): self.go_to(0)
    def go_last(self):  self.go_to(self.total-1)
    def _thumb_sel(self, idx): self.go_to(idx)
    def _pg_jump(self, _=None):
        try: self.go_to(int(self.pg_var.get())-1)
        except: self.pg_var.set(str(self.cur+1))

    # ── Zoom ───────────────────────────────────────────────────────
    def _rerender(self):
        if self.pdf:
            self.cache.clear(); self._cur_pil = None
            self._show_page(self.cur, animate=False)

    def zoom_in(self):
        self.fit="custom"; self.zoom=min(self.zoom*1.25,5.0); self._rerender()
    def zoom_out(self):
        self.fit="custom"; self.zoom=max(self.zoom/1.25,0.1); self._rerender()
    def fit_page(self):  self.fit="page";  self._rerender()
    def fit_width(self): self.fit="width"; self._rerender()

    # ── Sidebar ────────────────────────────────────────────────────
    def toggle_side(self):
        if self._side_on:
            self.sidebar.pack_forget(); self._side_on = False
        else:
            self.sidebar.pack(side="left", fill="y",
                              before=self.body.winfo_children()[0])
            self._side_on = True
        self.after(60, self._rerender)

    # ── Events ─────────────────────────────────────────────────────
    def _on_resize(self, _):
        if self.pdf:
            if self._render_id: self.after_cancel(self._render_id)
            self._render_id = self.after(120, self._rerender)
        else:
            self._welcome()

    def _keys(self):
        self.bind("<Control-o>",     lambda _: self.open_pdf())
        self.bind("<Right>",         lambda _: self.go_next())
        self.bind("<Left>",          lambda _: self.go_prev())
        self.bind("<Next>",          lambda _: self.go_next())
        self.bind("<Prior>",         lambda _: self.go_prev())
        self.bind("<Home>",          lambda _: self.go_first())
        self.bind("<End>",           lambda _: self.go_last())
        self.bind("<Up>",            lambda _: self.cv.yview_scroll(-3,"units"))
        self.bind("<Down>",          lambda _: self.cv.yview_scroll(3,"units"))
        self.bind("<Control-equal>", lambda _: self.zoom_in())
        self.bind("<Control-minus>", lambda _: self.zoom_out())
        self.bind("<f>",             lambda _: self.fit_page())
        self.bind("<w>",             lambda _: self.fit_width())
        self.bind("<Return>",        self._pg_jump)
        self.bind("<Escape>",        lambda _: self.destroy())


if __name__ == "__main__":
    app = App()
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        app.after(300, lambda: app._load(sys.argv[1]))
    app.mainloop()
