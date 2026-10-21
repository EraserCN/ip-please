"""全屏画面：开场打字机、标题、日期卡、报纸、下班结算、聊天窗口、片尾。"""
import math
import random

from PIL import Image

from . import audio as au
from .base import (CLAUDE, CLAUDE_L, DESK, DESK_D, GOLD, GREEN_L, GREY, GREY_D, H, INK, ORANGE, RED, RED_D, RED_L,
                   TEXT, TEXT_L, W, WHITE, big_text, darken, draw, ease_out, lerp, pattern, seg, spark, tw, txt,
                   wrap)
from .booth import DATES, WEEKDAYS, static_layer


class Scene:
    tag = ""
    amb = 0.0

    def cues(self):
        return []


class TypeScene(Scene):
    """黑屏 + 打字机，逐段出现。"""
    amb = 0.55

    def __init__(self, tag, paras, cps=17, pause=0.6, tail=1.3):
        self.tag, self.paras, self.cps = tag, paras, cps
        self.events = []        # (t, para, line, nchars)
        t = 0.5
        self.lines = []         # (para, text)
        for pi, para in enumerate(paras):
            for s in para:
                self.lines.append((pi, s, t))
                t += len(s) / cps + 0.12
            t += pause
        self.dur = t + tail

    def frame(self, t):
        img = Image.new("RGB", (W, H), INK)
        d = draw(img)
        total = len(self.lines) + len(self.paras) - 1
        y = H // 2 - total * 18 // 2
        last = None
        for pi, s, t0 in self.lines:
            if last is not None and pi != last:
                y += 18
            last = pi
            n = int((t - t0) * self.cps)
            if n > 0:
                txt(d, (W // 2 - tw(s) // 2, y), s[:n], 12, (214, 206, 190))
            y += 18
        return img

    def cues(self):
        out = []
        for pi, s, t0 in self.lines:
            for i, ch in enumerate(s):
                if ch.strip():
                    out.append((t0 + i / self.cps, au.typekey(i % 16), 1.8))
        return out


class TitleScene(Scene):
    def __init__(self, tag="title", dur=8.6, sub=True):
        self.tag, self.dur, self.sub = tag, dur, sub

    def frame(self, t):
        img = darken(static_layer().copy(), 0.88)
        d = draw(img)
        if t < 0.3:
            return img
        d.rectangle([0, 124, W - 1, 214], fill=(92, 28, 26))
        d.rectangle([0, 124, W - 1, 125], fill=RED)
        d.rectangle([0, 213, W - 1, 214], fill=RED)
        d.ellipse([298, 62, 342, 106], fill=(60, 24, 22))
        d.ellipse([298, 62, 342, 106], outline=CLAUDE)
        spark(d, 320, 84, CLAUDE_L, k=2)
        big_text(img, W // 2, 140, "IP, PLEASE", 12, 5, WHITE, shadow=INK)
        if t >= 1.0 and self.sub:
            big_text(img, W // 2, 232, "请出示你的 IP", 12, 2, CLAUDE_L, shadow=INK)
        if t >= 1.6:
            txt(d, (W // 2, 268), "A DYSTOPIAN TOKEN THRILLER", 8, GREY, anchor="ma")
        if t > self.dur - 0.5:
            img = darken(img, seg(t, self.dur - 0.5, self.dur))
        return img

    def cues(self):
        return [(0.3, au.march((0, 1, 2, 3)), 1.0)]


class DayCard(Scene):
    dur = 1.9

    def __init__(self, day, title=""):
        self.tag, self.day, self.title = f"day{day}", day, title

    def frame(self, t):
        img = Image.new("RGB", (W, H), INK)
        if t < 0.55:
            return img
        big_text(img, W // 2, 132, f"DAY {self.day}", 12, 4, WHITE)
        d = draw(img)
        txt(d, (W // 2, 196), f"{DATES[self.day]}  {WEEKDAYS[self.day]}", 10, GREY, anchor="ma")
        if self.title and t > 0.9:
            txt(d, (W // 2, 214), self.title, 12, CLAUDE_L, anchor="ma")
        return img

    def cues(self):
        return [(0.0, au.day_hit(), 1.0)]


# ———————————————————— 报纸 ————————————————————

def _icon(d, kind, x, y, w, h):
    """报纸配图：墨色单色像素画。"""
    ink, mid = (60, 50, 44), (150, 138, 120)
    d.rectangle([x, y, x + w, y + h], fill=(200, 188, 166))
    for yy in range(y, y + h, 2):
        for xx in range(x + (yy // 2) % 2, x + w, 4):
            d.point((xx, yy), fill=(186, 174, 152))
    cx, cy = x + w // 2, y + h // 2
    if kind == "gate":
        d.rectangle([x + 8, cy + 10, x + w - 8, cy + 12], fill=ink)
        for px in range(x + 12, x + w - 8, 10):
            d.line([px, cy - 14, px, cy + 12], fill=ink)
        d.rectangle([cx - 14, cy - 22, cx + 14, cy - 6], fill=ink)
        spark(d, cx, cy - 14, (200, 188, 166), big=False)
    elif kind == "clock":
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=ink, width=2)
        for k in range(12):
            a = math.radians(k * 30)
            d.point((cx + round(math.cos(a) * 21), cy + round(math.sin(a) * 21)), fill=ink)
        d.line([cx, cy, cx, cy - 16], fill=ink, width=2)
        d.line([cx, cy, cx + 10, cy + 4], fill=ink, width=2)
        txt(d, (cx, cy + 30), "USA (UTC+8)", 8, ink, anchor="ma")
    elif kind == "plane":
        d.polygon([(cx - 30, cy), (cx + 26, cy - 6), (cx + 34, cy - 2), (cx + 26, cy + 2)], fill=ink)
        d.polygon([(cx - 4, cy - 2), (cx + 8, cy - 22), (cx + 14, cy - 22), (cx + 8, cy)], fill=ink)
        d.polygon([(cx - 26, cy - 1), (cx - 30, cy - 12), (cx - 24, cy - 12), (cx - 18, cy - 2)], fill=ink)
        for k in range(4):
            d.rectangle([cx - 40 - k * 10, cy + 10 + k * 4, cx - 34 - k * 10, cy + 14 + k * 4], fill=mid)
            txt(d, (cx - 37 - k * 10, cy + 9 + k * 4), "$", 8, ink, anchor="ma")
    elif kind == "drumstick":
        d.ellipse([cx - 22, cy - 20, cx + 10, cy + 8], fill=ink)
        d.line([cx + 4, cy + 4, cx + 20, cy + 20], fill=ink, width=5)
        d.ellipse([cx + 16, cy + 16, cx + 26, cy + 24], fill=ink)
        txt(d, (cx + 18, cy - 24), "V50", 10, RED_D, anchor="ma")
    elif kind == "clones":
        for k in range(7):
            px = x + 10 + k * (w - 20) // 6
            d.ellipse([px - 4, cy - 16, px + 4, cy - 8], fill=ink)
            d.rectangle([px - 5, cy - 7, px + 5, cy + 8], fill=ink)
            d.rectangle([px - 4, cy + 9, px - 2, cy + 18], fill=ink)
            d.rectangle([px + 2, cy + 9, px + 4, cy + 18], fill=ink)
    elif kind == "building":
        d.rectangle([cx - 16, cy - 26, cx + 16, cy + 26], fill=ink)
        for wy in range(cy - 20, cy + 20, 8):
            for wx in (cx - 10, cx - 2, cx + 6):
                d.rectangle([wx, wy, wx + 4, wy + 4], fill=(200, 188, 166))
        txt(d, (cx, cy + 30), "SG → ??", 8, ink, anchor="ma")
    elif kind == "medal":
        d.polygon([(cx - 10, cy - 30), (cx + 10, cy - 30), (cx + 4, cy - 10), (cx - 4, cy - 10)], fill=RED_D)
        d.ellipse([cx - 18, cy - 12, cx + 18, cy + 24], fill=ink)
        spark(d, cx, cy + 6, GOLD)
    elif kind == "jorji":
        from .cast import JORJI
        spr = JORJI.sprite()
        g = spr.crop((40, 0, 140, 110)).convert("L").point(lambda v: 60 if v < 120 else 180)
        im = Image.merge("RGB", (g, g, g))
        return im, spr.crop((40, 0, 140, 110)).getchannel("A")
    return None


class Newspaper(Scene):
    dur = 4.4
    amb = 0.7

    def __init__(self, day, h1, h1_sub, h2, icon):
        self.tag, self.day = f"news{day}", day
        self.h1, self.h1_sub, self.h2, self.icon = h1, h1_sub, h2, icon

    def frame(self, t):
        img = Image.new("RGB", (W, H), DESK)
        d = draw(img)
        rng = random.Random(5)
        for y in range(4, H, 7):
            d.line([0, y, W, y], fill=DESK_D if rng.random() < 0.6 else DESK)
        px, pw, ph = 140, 360, 330
        py = round(lerp(H + 4, 16, ease_out(seg(t, 0.0, 0.45))))
        d.rectangle([px + 4, py + 4, px + pw + 4, py + ph + 4], fill=DESK_D)
        paper, ink, faint = (224, 214, 192), (40, 34, 30), (176, 164, 144)
        d.rectangle([px, py, px + pw, py + ph], fill=paper)
        big_text(img, px + pw // 2, py + 10, "安索兹卡真理报", 12, 2, ink)
        txt(d, (px + pw // 2, py + 38), f"THE TRUTH OF ANTHROTZKA  ·  {DATES[self.day]}", 8, TEXT_L, anchor="ma")
        d.rectangle([px + 10, py + 50, px + pw - 10, py + 51], fill=ink)
        d.rectangle([px + 10, py + 54, px + pw - 10, py + 54], fill=ink)
        k = 2 if tw(self.h1) * 2 <= pw - 24 else 1
        big_text(img, px + pw // 2, py + 62, self.h1, 12, k, ink)
        yy = py + 62 + (30 if k == 2 else 18)
        for s in wrap(self.h1_sub, 10, pw - 40):
            txt(d, (px + pw // 2, yy), s, 10, TEXT, anchor="ma")
            yy += 13
        yy += 4
        d.line([px + 10, yy, px + pw - 10, yy], fill=ink)
        yy += 8
        r = _icon(d, self.icon, px + 14, yy, 132, 100)
        if r:
            im, a = r
            img.paste(im, (px + 14 + 16, yy - 6), a)
        tx = px + 160
        hy = yy + 2
        for s in wrap(self.h2, 12, pw - 175):
            txt(d, (tx, hy), s, 12, ink)
            hy += 16
        for row in range(4):
            d.rectangle([tx, hy + 6 + row * 9, tx + 180 - rng.randint(0, 50), hy + 9 + row * 9], fill=faint)
        yy = max(yy + 110, hy + 46)
        row = 0
        while yy + row * 10 < py + ph - 12:
            for col in range(3):
                x0 = px + 14 + col * 114
                d.rectangle([x0, yy + row * 10, x0 + 100 - rng.randint(0, 30), yy + row * 10 + 3], fill=faint)
            row += 1
        return img

    def cues(self):
        return [(0.0, au.whoosh(), 1.0), (0.4, au.paper(31), 1.0)]


# ———————————————————— 下班结算 ————————————————————

class Summary(Scene):
    """原作的下班结算屏：收支 + 家人状态。"""

    def __init__(self, day, ledger, family, footer=None, dur=5.2):
        self.tag, self.day, self.ledger, self.family = f"sum{day}", day, ledger, family
        self.footer, self.dur = footer, dur

    def frame(self, t):
        img = Image.new("RGB", (W, H), INK)
        d = draw(img)
        txt(d, (W // 2, 26), f"DAY {self.day} · 下班", 12, WHITE, anchor="ma")
        d.line([120, 46, W - 120, 46], fill=GREY_D)
        k = 0
        y = 60
        for label, val in self.ledger:
            if t < 0.3 + k * 0.18:
                return img
            col = WHITE if not val.startswith("-") else RED_L
            if label == "结余":
                d.line([150, y - 4, 330, y - 4], fill=GREY_D)
                col = CLAUDE_L
            txt(d, (150, y), label, 12, GREY if label != "结余" else WHITE)
            txt(d, (330, y), val + " token", 12, col, anchor="ra")
            y += 18
            k += 1
        y = 60
        txt(d, (380, y - 2), "家人", 10, GREY_D)
        y += 14
        for name, status, level in self.family:
            if t < 0.3 + k * 0.18:
                return img
            col = {"ok": WHITE, "warn": ORANGE, "bad": RED_L, "good": GREEN_L}[level]
            txt(d, (380, y), name, 12, WHITE)
            for i, s in enumerate(wrap(status, 10, 200)):
                txt(d, (380, y + 15 + i * 12), s, 10, col)
            y += 18 + 12 * len(wrap(status, 10, 200)) + 6
            k += 1
        if self.footer and t > 0.3 + k * 0.18 + 0.4:
            for i, s in enumerate(self.footer):
                big_text(img, W // 2, 262 + i * 34, s, 12, 2, CLAUDE_L)
        return img

    def cues(self):
        n = len(self.ledger) + len(self.family)
        out = [(0.3 + k * 0.18, au.typekey(k), 1.4) for k in range(n)]
        out.append((0.2, au.sad_cadence(), 0.9))
        return out


# ———————————————————— Day 6：聊天窗口 + 封号邮件 ————————————————————

class ChatScene(Scene):
    tag = "chat"

    def __init__(self, msg="你好，请用中文回答我。"):
        self.msg = msg
        self.t_type, self.cps = 1.0, 9
        self.t_send = self.t_type + len(msg) / self.cps + 0.5
        self.t_ban = self.t_send + 1.0
        self.t_mail = self.t_ban + 1.2
        self.dur = self.t_mail + 4.6

    def frame(self, t):
        img = Image.new("RGB", (W, H), (30, 28, 28))
        d = draw(img)
        x0, y0, x1, y1 = 100, 34, 540, 330
        jitter = 0
        if self.t_ban <= t < self.t_mail:
            jitter = random.Random(int(t * 30)).randint(-6, 6)
        x0 += jitter
        x1 += jitter
        d.rectangle([x0, y0, x1, y1], fill=(238, 234, 226))
        d.rectangle([x0, y0, x1, y0 + 18], fill=(206, 198, 186))
        spark(d, x0 + 12, y0 + 9, CLAUDE, big=False)
        txt(d, (x0 + 22, y0 + 5), "Claude", 10, INK)
        txt(d, ((x0 + x1) // 2, y0 + 60), "How can I help you today?", 12, TEXT_L, anchor="ma")
        n = int((t - self.t_type) * self.cps) if t >= self.t_type else 0
        sent = t >= self.t_send
        box_y = y1 - 34
        d.rectangle([x0 + 14, box_y, x1 - 14, box_y + 22], fill=WHITE)
        d.rectangle([x0 + 14, box_y, x1 - 14, box_y + 22], outline=(170, 162, 150))
        if not sent:
            s = self.msg[:n]
            txt(d, (x0 + 22, box_y + 6), s, 12, INK)
            if int(t * 3) % 2 == 0:
                cx = x0 + 22 + tw(s)
                d.line([cx + 1, box_y + 5, cx + 1, box_y + 17], fill=INK)
        else:
            w = tw(self.msg) + 16
            d.rectangle([x1 - 20 - w, y0 + 110, x1 - 20, y0 + 132], fill=(226, 214, 196))
            txt(d, (x1 - 12 - w, y0 + 116), self.msg, 12, INK)
        if t >= self.t_ban:
            if int((t - self.t_ban) * 6) % 2 == 0 or t >= self.t_mail:
                img = Image.blend(img, Image.new("RGB", (W, H), (170, 20, 20)), 0.45)
                d = draw(img)
            if t < self.t_mail:
                rng = random.Random(int(t * 30))
                for _ in range(6):
                    yy = rng.randint(0, H - 8)
                    strip = img.crop((0, yy, W, yy + rng.randint(2, 8)))
                    img.paste(strip, (rng.randint(-20, 20), yy))
                d = draw(img)
        if t >= self.t_mail:
            u = ease_out(seg(t, self.t_mail, self.t_mail + 0.3))
            mx0, my0 = 150, round(lerp(H, 100, u))
            mx1, my1 = 490, my0 + 160
            d.rectangle([mx0 + 4, my0 + 4, mx1 + 4, my1 + 4], fill=INK)
            d.rectangle([mx0, my0, mx1, my1], fill=(236, 232, 222))
            d.rectangle([mx0, my0, mx1, my0 + 18], fill=RED_D)
            txt(d, (mx0 + 8, my0 + 5), "新邮件 · M.O.A. 对齐部", 10, WHITE)
            txt(d, (mx0 + 12, my0 + 28), "Subject: Account disabled", 10, INK)
            d.line([mx0 + 12, my0 + 44, mx1 - 12, my0 + 44], fill=(190, 182, 170))
            body = "Your account has been disabled after an automatic review of your recent activities."
            for i, s in enumerate(_wrap_words(body, 10, mx1 - mx0 - 24)):
                txt(d, (mx0 + 12, my0 + 52 + i * 14), s, 10, INK)
            txt(d, (mx1 - 12, my1 - 18), "—— 荣耀归于安索兹卡", 10, RED_D, anchor="ra")
        return img

    def cues(self):
        out = [(self.t_type + i / self.cps, au.typekey(i), 1.2) for i in range(len(self.msg))]
        out += [(self.t_send, au.click(), 1.5), (self.t_ban, au.glitch(), 1.0), (self.t_ban, au.siren(2.4), 1.0),
                (self.t_mail, au.citation(), 1.2)]
        return out


def _wrap_words(s, size, width):
    lines, cur = [], ""
    for wd in s.split(" "):
        cand = (cur + " " + wd).strip()
        if tw(cand, size) > width and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


# ———————————————————— 片尾 ————————————————————

THUMB = [
    "....XX....",
    "...XXX....",
    "...XX.....",
    "XX.XXXXXX.",
    "XX.XXXXXXX",
    "XX.XXXXXX.",
    "XX.XXXXXXX",
    "XX.XXXXXX.",
    "XX..XXXXX.",
]
COIN = [
    "..XXXXX..",
    ".X.....X.",
    "X..XXX..X",
    "X..X....X",
    "X..XXX..X",
    "X....X..X",
    "X..XXX..X",
    ".X.....X.",
    "..XXXXX..",
]
STAR = [
    "....X....",
    "....X....",
    "...XXX...",
    "XXXXXXXXX",
    ".XXXXXXX.",
    "..XXXXX..",
    "..XX.XX..",
    ".XX...XX.",
    ".X.....X.",
]


class EndCard(Scene):
    tag = "end"

    def __init__(self, dur=9.0):
        self.dur = dur

    def frame(self, t):
        img = darken(static_layer().copy(), 0.9)
        d = draw(img)
        d.rectangle([0, 70, W - 1, 150], fill=(92, 28, 26))
        d.rectangle([0, 70, W - 1, 71], fill=RED)
        d.rectangle([0, 149, W - 1, 150], fill=RED)
        big_text(img, W // 2, 86, "IP, PLEASE", 12, 4, WHITE, shadow=INK)
        if t > 1.0:
            txt(d, (W // 2, 168), "本视频由一位 美国东八区 用户制作", 12, WHITE, anchor="ma")
        if t > 2.0:
            big_text(img, W // 2, 200, "荣耀归于一键三连", 12, 2, CLAUDE_L, shadow=INK)
        if t > 2.8:
            for i, (pat, label) in enumerate(((THUMB, "点赞"), (COIN, "投币"), (STAR, "收藏"))):
                cx = W // 2 - 90 + i * 90
                pattern(d, pat, cx - len(pat[0]) * 3 // 2, 248, {"X": CLAUDE_L}, 3)
                txt(d, (cx, 280), label, 10, GREY, anchor="ma")
        if t > 3.6:
            txt(d, (W // 2, 318), "画面、音乐、音效均为原创 · 致敬 Papers, Please (Lucas Pope)", 8, GREY_D, anchor="ma")
            txt(d, (W // 2, 330), "字体：缝合像素字体 (OFL)", 8, GREY_D, anchor="ma")
        if t > self.dur - 1.0:
            img = darken(img, seg(t, self.dur - 1.0, self.dur))
        return img

    def cues(self):
        return [(0.0, au.march((4, 5, 6, 7)), 1.0)]
