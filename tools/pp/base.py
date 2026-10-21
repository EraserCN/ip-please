"""公共部分：画布尺寸、调色板、像素字体、绘图小工具。"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H, SCALE, FPS = 640, 360, 3, 30

FONTS = {s: ImageFont.truetype(str(ROOT / f"assets/fonts/fusion-pixel-{s}px-zh_hans.ttf"), s) for s in (8, 10, 12)}

# —— 调色板：灰褐、低饱和；只有红章、绿章、Claude 橙是亮色 ——
INK = (22, 19, 19)
OUTLINE = (34, 27, 25)
GROUND, GROUND_D, GROUND_L = (93, 87, 78), (80, 74, 67), (104, 98, 88)
WALL, WALL_D, WALL_L = (62, 58, 55), (48, 45, 43), (82, 77, 72)
BANNER = (112, 40, 36)
ROAD, ROAD_L = (110, 104, 94), (150, 142, 124)
BOOTH_WALL, BOOTH_LOW = (52, 48, 44), (42, 39, 36)
WIN_WALL, WIN_GROUND = (64, 66, 61), (78, 76, 69)
FRAME, FRAME_D = (88, 86, 80), (30, 28, 27)
COUNTER, COUNTER_L, COUNTER_D = (98, 86, 73), (124, 110, 93), (70, 61, 52)
DESK, DESK_D, DESK_L = (68, 57, 50), (56, 47, 42), (84, 72, 63)
PAPER, PAPER_D, PAPER_LINE = (226, 215, 196), (200, 187, 167), (216, 204, 184)
PINK, PINK_D = (224, 198, 186), (196, 166, 156)
SAGE, SAGE_D = (208, 214, 190), (172, 180, 152)
TEXT, TEXT_L = (74, 56, 48), (128, 106, 92)
NAVY, NAVY_L = (42, 50, 76), (60, 70, 100)
RED, RED_D, RED_L = (180, 46, 40), (120, 30, 28), (222, 92, 76)
GREEN, GREEN_D, GREEN_L = (84, 128, 70), (56, 88, 48), (122, 178, 98)
METAL, METAL_D, METAL_L = (92, 90, 86), (60, 58, 56), (124, 122, 116)
HAIR = (42, 34, 31)
FLAG_W, FLAG_R = (210, 204, 190), (156, 52, 46)
GLASS, GLASS_L = (28, 27, 31), (118, 126, 138)
WHITE, GREY, GREY_D = (228, 223, 212), (150, 145, 136), (100, 94, 88)
ORANGE = (220, 150, 70)
CLAUDE, CLAUDE_L = (204, 112, 80), (232, 156, 116)
LED = (214, 72, 52)
SWEAT = (156, 186, 204)
BOOK, BOOK_L, GOLD = (92, 64, 50), (130, 100, 70), (190, 160, 100)
SEAL = (150, 90, 110)
XRAY_BG, XRAY_FG, XRAY_L = (18, 40, 42), (70, 140, 136), (150, 220, 210)


# ———————————————————— 绘图 ————————————————————

def draw(img):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"   # 关掉抗锯齿，保证每个像素都是实色
    return d


def txt(d, xy, s, size=12, fill=WHITE, anchor="la"):
    """y 取字形的视觉顶边（像素字体的字形比 ascender 低 3px）。"""
    d.text((xy[0], xy[1] - 3), s, font=FONTS[size], fill=fill, anchor=anchor)


def tw(s, size=12):
    return int(FONTS[size].getlength(s))


def wrap(s, size, width):
    """逐字折行（中文为主，英文单词也会被拆开，够用）。"""
    lines, cur = [], ""
    for ch in s:
        if ch == "\n":
            lines.append(cur)
            cur = ""
        elif cur and tw(cur + ch, size) > width:
            lines.append(cur)
            cur = ch.lstrip()
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def text_mask(s, size, k=1):
    f = FONTS[size]
    l, t, r, b = f.getbbox(s)
    m = Image.new("L", (max(1, r - l), max(1, b - t)), 0)
    dm = ImageDraw.Draw(m)
    dm.fontmode = "1"
    dm.text((-l, -t), s, font=f, fill=255)
    if k > 1:
        m = m.resize((m.width * k, m.height * k), Image.NEAREST)
    return m


def big_text(img, x, y, s, size, k, fill, shadow=None, align="center"):
    """把像素字放大 k 倍（整块像素），返回 (宽, 高)。"""
    m = text_mask(s, size, k)
    if align == "center":
        x -= m.width // 2
    elif align == "right":
        x -= m.width
    if shadow:
        img.paste(shadow, (x + k, y + k), m)
    img.paste(fill, (x, y), m)
    return m.width, m.height


def darken(img, alpha, color=INK, box=None):
    """把整张图（或 box 区域）往 color 方向压暗。"""
    if box is None:
        return Image.blend(img, Image.new("RGB", img.size, color), alpha)
    region = img.crop(box)
    img.paste(Image.blend(region, Image.new("RGB", region.size, color), alpha), box[:2])
    return img


def speckle(mask, rate, seed):
    """随机抠掉一些像素，做出印章缺墨 / 纸张磨损的颗粒感。"""
    rng = random.Random(seed)
    px = mask.load()
    for y in range(mask.height):
        for x in range(mask.width):
            if px[x, y] and rng.random() < rate:
                px[x, y] = 0
    return mask


SPARK_13 = [
    "......X......",
    "...X..X..X...",
    "....X.X.X....",
    ".X...XXX...X.",
    "..XX.XXX.XX..",
    "....XXXXX....",
    "XXXXXXXXXXXXX",
    "....XXXXX....",
    "..XX.XXX.XX..",
    ".X...XXX...X.",
    "....X.X.X....",
    "...X..X..X...",
    "......X......",
]
SPARK_7 = [
    "...X...",
    ".X.X.X.",
    "..XXX..",
    "XXXXXXX",
    "..XXX..",
    ".X.X.X.",
    "...X...",
]


def pattern(d, pat, x, y, colors, k=1):
    """按字符图案画像素块；colors 把字符映射到颜色，'.' 为透明。"""
    for j, row in enumerate(pat):
        for i, ch in enumerate(row):
            c = colors.get(ch)
            if c is not None:
                d.rectangle([x + i * k, y + j * k, x + i * k + k - 1, y + j * k + k - 1], fill=c)


def spark(d, cx, cy, color, big=True, k=1):
    """Claude 的星芒，像素化致意版。"""
    pat = SPARK_13 if big else SPARK_7
    r = len(pat) // 2 * k
    pattern(d, pat, cx - r, cy - r, {"X": color}, k)


CURSOR_PX = [
    "X.........",
    "XX........",
    "XWX.......",
    "XWWX......",
    "XWWWX.....",
    "XWWWWX....",
    "XWWWWWX...",
    "XWWWWWWX..",
    "XWWWWWWWX.",
    "XWWWWXXXXX",
    "XWWXWX....",
    "XWX.XWX...",
    "XX...XWX..",
    "......XX..",
]


def draw_cursor(d, x, y, mode="arrow"):
    if mode == "cross":
        for dx in range(-7, 8):
            if abs(dx) > 2:
                d.point((x + dx, y), fill=RED_L)
                d.point((x, y + dx), fill=RED_L)
        d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=RED_L)
        d.point((x, y), fill=WHITE)
        return
    pattern(d, CURSOR_PX, x, y, {"X": INK, "W": WHITE})


# ———————————————————— 缓动 ————————————————————

def clamp(u):
    return max(0.0, min(1.0, u))


def seg(t, t0, t1):
    return clamp((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t1)


def smooth(u):
    return u * u * (3 - 2 * u)


def ease_out(u):
    return 1 - (1 - u) ** 3


def lerp(a, b, u):
    return a + (b - a) * u


def lerp2(p, q, u):
    return (round(lerp(p[0], q[0], u)), round(lerp(p[1], q[1], u)))


def edge_point(box, toward):
    """box 中心朝 toward 方向射线与 box 边框的交点。"""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = toward[0] - cx, toward[1] - cy
    if dx == 0 and dy == 0:
        return round(cx), round(cy)
    sx = (x1 - x0) / 2 / abs(dx) if dx else math.inf
    sy = (y1 - y0) / 2 / abs(dy) if dy else math.inf
    s = min(sx, sy) + 0.02
    return round(cx + dx * s), round(cy + dy * s)
