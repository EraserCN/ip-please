"""证件和纸张。每种证件知道自己的尺寸、怎么画、各栏位的相对坐标（给检查模式连红线用）。"""
import random
from functools import lru_cache

from PIL import Image

from .base import (DESK_D, GOLD, GREY, INK, NAVY, NAVY_L, PAPER, PAPER_D, PAPER_LINE, PINK, PINK_D, RED_D, SAGE,
                   SAGE_D, SEAL, TEXT, TEXT_L, WHITE, draw, pattern, spark, speckle, tw, txt, wrap)
from .people import photo

SLOT_PASSPORT = (446, 172)


class Doc:
    w = h = 0
    grab = (20, 12)
    icon = ("card", PINK)

    def draw(self, img, d, x, y):
        raise NotImplementedError

    def field(self, name):
        return self.fields[name]

    def image(self):
        """单独渲染成一张 RGBA（打印纸条等需要裁切时用）。"""
        im = Image.new("RGBA", (self.w + 2, self.h + 2), (0, 0, 0, 0))
        self.draw(im, draw(im), 0, 0, shadow=False)
        return im


def _shadow(d, x, y, w, h):
    d.rectangle([x + 2, y + 2, x + w + 1, y + h + 1], fill=DESK_D)


class Passport(Doc):
    w, h = 176, 116
    grab = (24, 14)

    def __init__(self, country, name, rows, person, cover=NAVY, band=NAVY_L, mrz=""):
        self.country, self.name, self.rows = country, name, rows
        self.person, self.cover, self.band, self.mrz = person, cover, band, mrz
        self.icon = ("book", cover)
        self.fields = {"header": (3, 3, 172, 16), "name": (56, 20, 172, 34), "photo": (9, 22, 50, 73)}
        for i, (k, _) in enumerate(rows):
            self.fields[k] = (56, 40 + i * 12, 150, 51 + i * 12)

    def draw(self, img, d, x, y, shadow=True):
        w, h = self.w, self.h
        if shadow:
            _shadow(d, x, y, w, h)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=self.cover)
        d.rectangle([x + 3, y + 3, x + w - 4, y + h - 4], fill=PAPER)
        for yy in range(y + 22, y + h - 22, 4):
            d.line([x + 56, yy, x + w - 8, yy], fill=PAPER_LINE)
        d.rectangle([x + 3, y + 3, x + w - 4, y + 16], fill=self.band)
        txt(d, (x + w // 2, y + 6), self.country, 8, PAPER, anchor="ma")
        d.rectangle([x + 9, y + 22, x + 50, y + 73], fill=PAPER_D)
        img.paste(_photo(self.person), (x + 10, y + 23))
        txt(d, (x + 58, y + 22), self.name, 12, TEXT)
        for i, (k, v) in enumerate(self.rows):
            txt(d, (x + 58, y + 42 + i * 12), k, 8, TEXT_L)
            txt(d, (x + 80, y + 41 + i * 12), v, 10, TEXT)
        d.ellipse([x + 18, y + 78, x + 40, y + 98], outline=GOLD)
        spark(d, x + 29, y + 88, GOLD, big=False)
        if self.mrz:
            txt(d, (x + 8, y + h - 15), self.mrz, 8, TEXT_L)


@lru_cache(maxsize=64)
def _photo(person):
    return photo(person.sprite())


CHICKEN = [
    "....RR....",
    "...RRR....",
    "..WWWW....",
    ".WWOWWW...",
    "YYWWWWWW..",
    "..WWWWWWWW",
    "..WWWWWWW.",
    "...WWWWW..",
    "....Y.Y...",
    "....Y.Y...",
]


class CrayonPassport(Doc):
    """乔治老哥用蜡笔画的“美国护照”。"""
    w, h = 176, 116
    grab = (24, 14)
    icon = ("book", (70, 90, 170))

    def __init__(self):
        self.fields = {"header": (3, 3, 172, 18), "photo": (9, 22, 50, 73), "eagle": (120, 70, 160, 104)}

    def draw(self, img, d, x, y, shadow=True):
        w, h = self.w, self.h
        rng = random.Random(4)
        if shadow:
            _shadow(d, x, y, w, h)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(238, 230, 210))
        blue, red, yellow = (70, 90, 170), (196, 60, 52), (220, 180, 60)
        for i in range(0, w, 3):     # 蜡笔歪歪扭扭的边框
            d.point((x + i, y + 1 + rng.randint(0, 2)), fill=blue)
            d.point((x + i, y + h - 3 + rng.randint(0, 2)), fill=blue)
        for j in range(0, h, 3):
            d.point((x + 1 + rng.randint(0, 2), y + j), fill=blue)
            d.point((x + w - 3 + rng.randint(0, 2), y + j), fill=blue)
        cx = x + 8
        for i, ch in enumerate("UNITED STATES OF AMERCIA"):
            txt(d, (cx, y + 6 + rng.randint(-1, 1)), ch, 8, red if i % 2 else blue)
            cx += tw(ch, 8) + 1
        d.rectangle([x + 9, y + 22, x + 50, y + 73], outline=blue)
        d.ellipse([x + 22, y + 28, x + 38, y + 44], outline=INK)        # 火柴人照片
        d.line([x + 26, y + 39, x + 34, y + 39], fill=INK, width=2)     # 胡子
        d.line([x + 30, y + 44, x + 30, y + 60], fill=INK)
        d.line([x + 22, y + 50, x + 38, y + 50], fill=INK)
        d.line([x + 30, y + 60, x + 24, y + 70], fill=INK)
        d.line([x + 30, y + 60, x + 36, y + 70], fill=INK)
        for i, (k, v) in enumerate((("NAME", "GEORGE"), ("FROM", "USA!!"), ("REAL", "100%"))):
            txt(d, (x + 58, y + 26 + i * 14 + rng.randint(-1, 1)), k, 8, TEXT_L)
            txt(d, (x + 86, y + 25 + i * 14 + rng.randint(-1, 1)), v, 10, red if i == 2 else TEXT)
        pattern(d, CHICKEN, x + 124, y + 72, {"R": red, "W": WHITE, "O": INK, "Y": yellow}, 3)
        d.rectangle([x + 121, y + 69, x + 156, y + 103], outline=blue)
        txt(d, (x + 139, y + 105), "EAGLE", 8, blue, anchor="ma")
        for k in range(5):
            spark(d, x + 66 + k * 10, y + 92, yellow, big=False)


class Card(Doc):
    """设备入境卡 / 账户卡：标题 + 若干行 label/value。"""
    w = 152
    grab = (20, 12)

    def __init__(self, rows, title="设备入境卡", sub="DEVICE ENTRY", color=PINK, color_d=PINK_D, seal=None,
                 value_x=38):
        self.rows, self.title, self.sub = rows, title, sub
        self.color, self.color_d, self.value_x = color, color_d, value_x
        self.seal = len(rows) >= 4 if seal is None else seal
        self.h = 20 + 14 * len(rows) + (14 if self.seal else 6)
        self.icon = ("card", color)
        self.fields = {k: (4, 18 + 14 * i, self.w - 5, 31 + 14 * i) for i, (k, _) in enumerate(rows)}

    def draw(self, img, d, x, y, shadow=True):
        w, h = self.w, self.h
        if shadow:
            _shadow(d, x, y, w, h)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=self.color_d)
        d.rectangle([x + 1, y + 1, x + w - 2, y + h - 2], fill=self.color)
        d.rectangle([x + 1, y + 1, x + w - 2, y + 14], fill=self.color_d)
        txt(d, (x + 6, y + 4), self.title, 10, TEXT)
        txt(d, (x + w - 6, y + 6), self.sub, 8, TEXT_L, anchor="ra")
        for i, (k, v) in enumerate(self.rows):
            yy = y + 20 + i * 14
            txt(d, (x + 8, yy), k, 10, TEXT_L)
            txt(d, (x + self.value_x, yy), v, 10, TEXT)
            for sx in range(x + 6, x + w - 6, 2):
                d.point((sx, yy + 11), fill=self.color_d)
        if self.seal:
            sx, sy = x + w - 40, y + h - 38
            d.ellipse([sx, sy, sx + 33, sy + 33], outline=SEAL, width=2)
            txt(d, (sx + 17, sy + 8), "M.O.A.", 8, SEAL, anchor="ma")
            txt(d, (sx + 17, sy + 19), "对齐部", 8, SEAL, anchor="ma")


def device(**kw):
    """设备入境卡，按传入顺序排栏：ip / loc / tz / lang / dev。"""
    labels = {"ip": "IP", "loc": "归属", "tz": "时区", "lang": "语言", "dev": "设备"}
    rows = [(labels[k], v) for k, v in kw.items()]
    return Card(rows)


def account(**kw):
    labels = {"pay": "付款", "bill": "账单", "phone": "手机"}
    rows = [(labels[k], v) for k, v in kw.items()]
    return Card(rows, title="账户卡", sub="ACCOUNT", color=SAGE, color_d=SAGE_D, seal=False)


class Note(Doc):
    """夹在护照里的小纸条（地下中转联盟）。"""
    grab = (16, 8)
    icon = ("card", (236, 228, 204))

    def __init__(self, lines):
        self.lines = lines
        self.w = max(tw(s, 10) for s in lines) + 16
        self.h = 12 + 13 * len(lines)
        self.fields = {}

    def draw(self, img, d, x, y, shadow=True):
        if shadow:
            _shadow(d, x, y, self.w, self.h)
        d.rectangle([x, y, x + self.w - 1, y + self.h - 1], fill=(236, 228, 204))
        d.polygon([(x + self.w - 8, y), (x + self.w - 1, y), (x + self.w - 1, y + 7)], fill=DESK_D)
        for i, s in enumerate(self.lines):
            txt(d, (x + 8, y + 7 + i * 13), s, 10, (70, 70, 96))


class Citation(Doc):
    """对齐部警告单（原作的罚单）。"""
    w = 168
    grab = (20, 10)
    icon = ("card", (226, 184, 176))

    def __init__(self, lines):
        self.lines = lines
        self.h = 26 + 13 * len(lines) + 6
        self.fields = {}

    def draw(self, img, d, x, y, shadow=True):
        if shadow:
            _shadow(d, x, y, self.w, self.h)
        d.rectangle([x, y, x + self.w - 1, y + self.h - 1], fill=(226, 184, 176))
        d.rectangle([x, y, x + self.w - 1, y + 16], fill=RED_D)
        txt(d, (x + 6, y + 4), "M.O.A. 警告单", 10, WHITE)
        txt(d, (x + self.w - 6, y + 6), "CITATION", 8, (226, 184, 176), anchor="ra")
        for i, s in enumerate(self.lines):
            txt(d, (x + 8, y + 22 + i * 13), s, 10, TEXT)


class PrintStrip(Doc):
    """打印机吐出来的长纸条。"""
    w = 128
    icon = ("card", (232, 230, 222))

    def __init__(self, header, rows):
        self.header, self.rows = header, rows
        self.h = 10 + 13 * len(header) + 6 + 10 * len(rows) + 6
        self.fields = {}

    def draw(self, img, d, x, y, shadow=True):
        w, h = self.w, self.h
        if shadow:
            _shadow(d, x, y, w, h)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 230, 222))
        for yy in range(y + 3, y + h, 6):
            d.point((x + 2, yy), fill=GREY)
            d.point((x + w - 3, yy), fill=GREY)
        yy = y + 6
        for s in self.header:
            txt(d, (x + 8, yy), s, 10, INK)
            yy += 13
        d.line([x + 6, yy, x + w - 7, yy], fill=GREY)
        yy += 5
        for s in self.rows:
            txt(d, (x + 8, yy), s, 8, TEXT)
            yy += 10


class PromptPaper(Doc):
    """结局：旅客递上来的不是护照，是一段 prompt。"""
    w, h = 176, 120
    grab = (24, 14)
    icon = ("card", (236, 234, 226))

    def __init__(self, text):
        self.lines = wrap(text, 10, 158)
        self.fields = {"text": (6, 20, 170, 20 + 13 * len(self.lines)), "header": (3, 3, 172, 16)}

    def draw(self, img, d, x, y, shadow=True):
        if shadow:
            _shadow(d, x, y, self.w, self.h)
        d.rectangle([x, y, x + self.w - 1, y + self.h - 1], fill=(236, 234, 226))
        d.rectangle([x + 3, y + 3, x + self.w - 4, y + 16], fill=(120, 116, 110))
        txt(d, (x + 8, y + 6), "PROMPT · 用户请求", 8, WHITE)
        for i, s in enumerate(self.lines):
            txt(d, (x + 9, y + 22 + i * 13), s, 10, INK)


class MiniPassport(Doc):
    """合上的护照封面（套娃用）。"""

    def __init__(self, w, h, cover, label):
        self.w, self.h, self.cover, self.label = w, h, cover, label
        self.grab = (w // 2, h // 2)
        self.icon = ("book", cover)
        self.fields = {"all": (0, 0, w - 1, h - 1)}

    def draw(self, img, d, x, y, shadow=True):
        w, h = self.w, self.h
        if shadow:
            _shadow(d, x, y, w, h)
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=self.cover)
        if w > 50:
            d.rectangle([x + 3, y + 3, x + w - 4, y + h - 4], outline=GOLD)
            r = min(w, h) // 6
            d.ellipse([x + w // 2 - r, y + h // 2 - r - 6, x + w // 2 + r, y + h // 2 + r - 6], outline=GOLD)
            size = 10 if tw(self.label, 10) < w - 12 else 8
            txt(d, (x + w // 2, y + h - 18), self.label, size, GOLD, anchor="ma")
        else:
            txt(d, (x + w // 2, y + h // 2 - 4), self.label, 8, GOLD, anchor="ma")


class AddressCard(Doc):
    w, h = 96, 34
    icon = ("card", PAPER)
    fields = {}

    def draw(self, img, d, x, y, shadow=True):
        if shadow:
            _shadow(d, x, y, self.w, self.h)
        d.rectangle([x, y, x + self.w - 1, y + self.h - 1], fill=PAPER_D)
        d.rectangle([x + 1, y + 1, x + self.w - 2, y + self.h - 2], fill=PAPER)
        txt(d, (x + 6, y + 6), "123 MAIN ST", 10, TEXT)
        txt(d, (x + 6, y + 20), "PORTLAND, OR", 8, TEXT_L)


def small_icon(d, kind, color, x, y):
    if kind == "book":
        d.rectangle([x, y, x + 18, y + 12], fill=INK)
        d.rectangle([x + 1, y + 1, x + 17, y + 11], fill=color)
        d.point((x + 9, y + 6), fill=GOLD)
    else:
        d.rectangle([x, y, x + 16, y + 10], fill=tuple(int(c * 0.85) for c in color))
        d.rectangle([x + 1, y + 1, x + 15, y + 9], fill=color)
        d.line([x + 3, y + 4, x + 12, y + 4], fill=tuple(int(c * 0.8) for c in color))


@lru_cache(maxsize=8)
def stamp_mark(kind, k=1):
    """拒绝 / 准予入境的章：带随机缺墨的颗粒感。返回 L 蒙版。"""
    w, h = 58, 34
    m = Image.new("L", (w, h), 0)
    dm = draw(m)
    dm.rectangle([0, 0, w - 1, h - 1], outline=255, width=2)
    big, small = ("DENIED", "拒绝入境") if kind == "deny" else ("APPROVED", "准予入境")
    txt(dm, (w // 2, 5), big, 12 if kind == "deny" else 10, 255, anchor="ma")
    txt(dm, (w // 2, 20), small, 10, 255, anchor="ma")
    speckle(m, 0.08, 9 if kind == "deny" else 10)
    if k > 1:
        m = m.resize((w * k, h * k), Image.NEAREST)
    return m.point(lambda v: int(v * 0.95))
