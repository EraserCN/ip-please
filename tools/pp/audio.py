"""音效和配乐：全部用 numpy 现场合成，不使用原作素材；旋律为原创。"""
import wave
from functools import lru_cache

import numpy as np
from scipy.signal import butter, lfilter

SR = 44100


def _n(dur):
    return int(dur * SR)


def _noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def _filt(x, kind, freq, order=2):
    b, a = butter(order, freq, btype=kind, fs=SR)
    return lfilter(b, a, x)


def _phase(freq, n):
    return 2 * np.pi * np.cumsum(np.broadcast_to(freq, (n,))) / SR


def _square(freq, n, duty=0.5):
    ph = (_phase(freq, n) / (2 * np.pi)) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def _tri(freq, n):
    ph = (_phase(freq, n) / (2 * np.pi)) % 1.0
    return 4 * np.abs(ph - 0.5) - 1


def _decay(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def _fade(x, a=0.004, r=0.02):
    n = len(x)
    i = np.arange(n)
    return x * np.minimum(1, i / max(1, a * SR)) * np.minimum(1, (n - i) / max(1, r * SR))


def _norm(x, peak=1.0):
    m = np.max(np.abs(x)) if len(x) else 0
    return x * (peak / m) if m > 0 else x


def _cat(*parts):
    return np.concatenate(parts)


def silence(dur):
    return np.zeros(_n(dur))


# ———————————————————— 环境 & 人声 ————————————————————

def ambient(dur):
    """室外风声 + 远处人群嗡嗡声。"""
    n = _n(dur)
    wind = _filt(_noise(n, 1), "lowpass", 380) * 3.0
    crowd = _filt(_noise(n, 2), "bandpass", [220, 900])
    t = np.arange(n) / SR
    crowd *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t) * np.sin(2 * np.pi * 0.07 * t + 1)
    return _norm(wind + crowd * 0.6, 0.06)


@lru_cache(maxsize=256)
def mumble(dur, pitch, seed, peak=0.3):
    """叽里咕噜的假语音（原作风格，不是任何语言）。"""
    rng = np.random.default_rng(seed)
    out = np.zeros(_n(dur))
    pos = 0
    while pos < len(out):
        n = min(_n(rng.uniform(0.06, 0.12)), len(out) - pos)
        if n < 64:
            break
        f0 = pitch * rng.uniform(0.85, 1.2)
        glide = np.linspace(f0, f0 * rng.uniform(0.85, 1.1), n)
        saw = (_phase(glide, n) / (2 * np.pi)) % 1.0 * 2 - 1
        f1, f2 = rng.uniform(450, 850), rng.uniform(1100, 2200)
        v = _filt(saw, "bandpass", [f1 * 0.7, f1 * 1.3]) + 0.6 * _filt(saw, "bandpass", [f2 * 0.8, f2 * 1.2])
        out[pos:pos + n] += _fade(v, 0.012, 0.03)
        pos += n + _n(rng.uniform(0.015, 0.05))
    return _norm(_filt(out, "lowpass", 3500), peak)


@lru_cache(maxsize=4)
def intercom():
    """喇叭喊'下一位'：带失真的广播腔。"""
    n = _n(0.5)
    v = mumble(0.42, 150, 11, 1.0)
    v = np.concatenate([np.zeros(_n(0.04)), v, np.zeros(n)])[:n]
    v = np.tanh(_filt(v + 0.08 * _noise(n, 12), "bandpass", [350, 2600]) * 4)
    click_ = np.zeros(n)
    click_[:_n(0.006)] = _noise(_n(0.006), 13)
    return _norm(v + click_ * 0.5, 0.4)


# ———————————————————— 桌面音效 ————————————————————

@lru_cache(maxsize=16)
def footstep(seed):
    n = _n(0.06)
    x = _filt(_noise(n, seed), "lowpass", 900) * _decay(n, 0.012)
    x += np.sin(_phase(90, n)) * _decay(n, 0.02) * 0.6
    return _norm(x, 0.16)


@lru_cache(maxsize=32)
def paper(seed=0):
    n = _n(0.18)
    rng = np.random.default_rng(seed + 100)
    x = _filt(_noise(n, seed + 100), "bandpass", [1800, 7000])
    crinkle = (rng.random(n) < 0.02) * rng.uniform(0.5, 1.5, n)
    x = x * (0.6 + _filt(crinkle, "lowpass", 300) * 8)
    env = np.minimum(1, np.arange(n) / _n(0.02)) * _decay(n, 0.05)
    return _norm(x * env, 0.2)


@lru_cache(maxsize=4)
def thud():
    """厚重的证件拍在桌上。"""
    n = _n(0.25)
    x = np.sin(_phase(np.linspace(120, 60, n), n)) * _decay(n, 0.05)
    x += _filt(_noise(n, 81), "lowpass", 1200) * _decay(n, 0.01)
    return _norm(x, 0.45) + np.pad(paper(9) * 0.6, (0, n))[:n]


@lru_cache(maxsize=4)
def click():
    n = _n(0.012)
    x = _filt(_noise(n, 21), "highpass", 2000) * _decay(n, 0.002)
    x += np.sin(_phase(2200, n)) * _decay(n, 0.003)
    return _norm(x, 0.18)


@lru_cache(maxsize=4)
def inspect_on():
    a = _square(330, _n(0.06))
    b = _square(495, _n(0.09))
    return _norm(_filt(_fade(_cat(a, b)), "lowpass", 2500), 0.13)


@lru_cache(maxsize=4)
def inspect_off():
    a = _square(495, _n(0.05))
    b = _square(330, _n(0.07))
    return _norm(_filt(_fade(_cat(a, b)), "lowpass", 2500), 0.09)


@lru_cache(maxsize=4)
def select():
    return _norm(_filt(_fade(_square(880, _n(0.04))), "lowpass", 3000), 0.1)


@lru_cache(maxsize=4)
def discrepancy():
    """发现信息不符：低沉的三全音'咚——'。"""
    n1, n2 = _n(0.12), _n(0.4)
    a = (_square(110, n1) + _square(155.6, n1)) * 0.5
    b = (_square(98, n2) + _square(138.6, n2)) * 0.5 * _decay(n2, 0.15)
    return _norm(_filt(_fade(_cat(a, b)), "lowpass", 1400), 0.26)


@lru_cache(maxsize=4)
def tray(reverse=False):
    n = _n(0.26)
    sweep = _filt(_noise(n, 31), "bandpass", [300, 2400]) * np.sin(np.linspace(0, np.pi, n))
    m = _n(0.09)
    clunk = (np.sin(_phase(220, m)) + 0.6 * np.sin(_phase(331, m))) * _decay(m, 0.02)
    clunk += _filt(_noise(m, 32), "lowpass", 1500) * _decay(m, 0.01)
    return _norm(_cat(sweep * 0.7, clunk), 0.18 if reverse else 0.26)


@lru_cache(maxsize=4)
def stamp(kind="deny"):
    """盖章：一记闷响（准予入境的章稍微清亮一点）。"""
    n = _n(0.4)
    f = np.linspace(110, 50, n) if kind == "approve" else np.linspace(95, 42, n)
    thud_ = np.sin(_phase(f, n)) * _decay(n, 0.09)
    hit = _filt(_noise(n, 41), "lowpass", 1600) * _decay(n, 0.012)
    chk = _filt(_noise(n, 42), "bandpass", [2000, 6000]) * _decay(n, 0.006)
    return _norm(np.tanh((thud_ + hit * 0.8 + chk * 0.4) * 1.5), 0.85)


@lru_cache(maxsize=4)
def detain_btn():
    n = _n(0.3)
    x = _square(220, n) * (_square(8, n) > 0) * _decay(n, 0.2)
    return _norm(_filt(x, "lowpass", 1800), 0.2)


@lru_cache(maxsize=4)
def scuffle():
    """卫兵冲进来把人架走。"""
    out = np.zeros(_n(1.2))
    rng = np.random.default_rng(91)
    for i in range(10):
        s = footstep(60 + i % 6) * rng.uniform(0.8, 1.4)
        p = _n(i * 0.1 + rng.uniform(0, 0.03))
        out[p:p + len(s)] += s[:len(out) - p]
    grunt = mumble(0.35, 95, 92, 0.25)
    out[_n(0.35):_n(0.35) + len(grunt)] += grunt
    return out


@lru_cache(maxsize=8)
def printer(dur):
    """针式打印机：嗡嗡 + 咔哒。"""
    n = _n(dur)
    t = np.arange(n) / SR
    buzz = _square(55, n) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t)))
    tick = _filt(_noise(n, 71), "bandpass", [1500, 5000]) * (np.sin(2 * np.pi * 28 * t) > 0.8)
    return _norm(_fade(_filt(buzz, "lowpass", 900) * 0.6 + tick * 0.5, 0.01, 0.05), 0.16)


@lru_cache(maxsize=4)
def citation():
    """收到警告单：两声下行的提示音。"""
    a = _square(330, _n(0.15))
    b = _square(247, _n(0.3)) * _decay(_n(0.3), 0.12)
    return _norm(_filt(_fade(_cat(a, b)), "lowpass", 2000), 0.22)


@lru_cache(maxsize=4)
def xray():
    n = _n(0.8)
    t = np.arange(n) / SR
    hum = np.sin(_phase(np.linspace(80, 160, n), n)) + 0.5 * np.sin(_phase(np.linspace(160, 320, n), n))
    beep = np.zeros(n)
    m = _n(0.06)
    beep[-m:] = _square(1320, m) * 0.5
    return _norm(_fade(hum * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) + beep, 0.05, 0.05), 0.18)


@lru_cache(maxsize=16)
def typekey(seed):
    n = _n(0.03)
    x = _filt(_noise(n, 300 + seed), "bandpass", [1200, 5000]) * _decay(n, 0.004)
    return _norm(x, 0.12)


@lru_cache(maxsize=4)
def gunshot():
    n = _n(0.5)
    crack = _filt(_noise(n, 61), "lowpass", 4000) * _decay(n, 0.02)
    boom = np.sin(_phase(np.linspace(90, 40, n), n)) * _decay(n, 0.12)
    echo = np.roll(crack, _n(0.11)) * 0.25
    return _norm(np.tanh((crack + boom + echo) * 2), 0.7)


def siren(dur):
    n = _n(dur)
    t = np.arange(n) / SR
    f = 620 + 260 * (np.sin(2 * np.pi * 0.9 * t) > 0)
    return _norm(_fade(_filt(_square(f, n, 0.4), "lowpass", 2200), 0.05, 0.2), 0.16)


@lru_cache(maxsize=4)
def glitch():
    n = _n(0.6)
    rng = np.random.default_rng(55)
    x = np.zeros(n)
    for _ in range(14):
        p = rng.integers(0, n - 2000)
        m = rng.integers(400, 2000)
        x[p:p + m] += _square(rng.uniform(200, 2000), m) * rng.uniform(0.3, 1)
    return _norm(x, 0.25)


def crowd_fight(dur):
    out = np.zeros(_n(dur))
    rng = np.random.default_rng(77)
    for i in range(int(dur * 6)):
        s = mumble(0.25, rng.uniform(110, 220), 400 + i, 0.25)
        p = _n(rng.uniform(0, dur - 0.3))
        out[p:p + len(s)] += s
    hits = _filt(_noise(len(out), 78), "lowpass", 800) * (rng.random(len(out)) < 0.0004)
    return _norm(out + _filt(hits, "lowpass", 400) * 30, 0.3)


@lru_cache(maxsize=4)
def whoosh():
    n = _n(0.3)
    x = _filt(_noise(n, 88), "bandpass", [400, 3000]) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return _norm(x, 0.2)


# ———————————————————— 配乐（原创苏式小调进行曲） ————————————————————

def _f(m):
    return 440.0 * 2 ** ((m - 69) / 12)


THEME = [
    [(62, 1), (62, .5), (64, .5), (65, 1), (69, 1)],
    [(67, 1.5), (65, .5), (64, 2)],
    [(60, 1), (64, .5), (65, .5), (67, 1), (70, 1)],
    [(69, 3), (None, 1)],
    [(74, 1), (72, .5), (70, .5), (69, 1), (65, 1)],
    [(67, 1), (70, .5), (69, .5), (67, 1), (64, 1)],
    [(65, 1), (64, .5), (62, .5), (61, 1), (64, 1)],
    [(62, 3), (None, 1)],
]
CHORDS = [(38, (62, 65, 69)), (36, (60, 64, 67)), (36, (60, 64, 70)), (41, (65, 69, 72)),
          (46, (62, 65, 70)), (43, (62, 67, 70)), (45, (61, 64, 69)), (38, (62, 65, 69))]


def _lead(m, dur):
    n = _n(dur)
    t = np.arange(n) / SR
    f = _f(m) * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.25))
    x = _square(f, n, 0.25) * 0.6 + _square(f * 1.003, n, 0.5) * 0.4 + np.sin(_phase(f / 2, n)) * 0.3
    env = np.minimum(1, t / 0.012) * (0.75 + 0.25 * np.exp(-t / 0.08))
    return _filt(_fade(x * env, 0.005, 0.05), "lowpass", 2600)


def _bass(m, dur):
    n = _n(dur)
    return _fade(_tri(_f(m), n) * _decay(n, 0.35), 0.004, 0.04)


def _pad(chord, dur):
    n = _n(dur)
    t = np.arange(n) / SR
    x = sum(_square(_f(m - 12), n) for m in chord) / len(chord)
    return _filt(_fade(x * np.minimum(1, t / 0.15), 0.02, 0.2), "lowpass", 900)


def _kick(n=None):
    n = _n(0.3)
    return np.sin(_phase(np.linspace(75, 45, n), n)) * _decay(n, 0.09)


def _snare(seed=0):
    n = _n(0.14)
    return _filt(_noise(n, 500 + seed), "bandpass", [1500, 6000]) * _decay(n, 0.04) + \
        np.sin(_phase(190, n)) * _decay(n, 0.03) * 0.5


def _place(out, t, x, g=1.0):
    p = _n(t)
    if p >= len(out):
        return
    m = min(len(x), len(out) - p)
    out[p:p + m] += x[:m] * g


@lru_cache(maxsize=16)
def march(bars=tuple(range(8)), bpm=104, drums=True, lead=1.0, tail=1.5):
    beat = 60 / bpm
    bar = 4 * beat
    out = np.zeros(_n(len(bars) * bar + tail))
    for bi, b in enumerate(bars):
        t0 = bi * bar
        tt = t0
        for m, beats in THEME[b]:
            if m:
                last = bi == len(bars) - 1 and beats >= 3
                _place(out, tt, _lead(m, beats * beat * (1.4 if last else 0.92)), 0.33 * lead)
            tt += beats * beat
        root, chord = CHORDS[b]
        for k in range(4):
            _place(out, t0 + k * beat, _bass(root if k % 2 == 0 else root + 7, beat * 0.85), 0.3)
        _place(out, t0, _pad(chord, bar), 0.1)
        if drums:
            for k in range(4):
                if k % 2 == 0:
                    _place(out, t0 + k * beat, _kick(), 0.5)
                else:
                    _place(out, t0 + k * beat, _snare(k + bi), 0.22)
            if b in (3, 7):
                for r in range(4):
                    _place(out, t0 + 3 * beat + r * beat / 4, _snare(20 + r), 0.12 + 0.03 * r)
    return _norm(out, 0.6)


@lru_cache(maxsize=4)
def sad_cadence():
    """下班结算：慢速、无鼓的收尾两小节。"""
    return _norm(march((6, 7), bpm=84, drums=False, lead=0.8, tail=2.0), 0.4)


@lru_cache(maxsize=4)
def day_hit():
    """日期卡：定音鼓滚奏 + 重击。"""
    out = np.zeros(_n(1.6))
    for r in range(10):
        _place(out, r * 0.05, _kick(), 0.15 + r * 0.03)
    _place(out, 0.55, _kick(), 1.0)
    _place(out, 0.55, _pad((62, 65, 69), 0.9), 0.35)
    return _norm(out, 0.5)


@lru_cache(maxsize=4)
def fanfare():
    """全片唯一一次正经放行：D 大调号角。"""
    beat = 60 / 120
    out = np.zeros(_n(3.6))
    for i, (m, b) in enumerate(((62, .5), (66, .5), (69, .5), (74, 2.5))):
        _place(out, i * 0.25, _lead(m, b * beat), 0.4)
    for i in range(4):
        _place(out, i * 0.25, _kick(), 0.4)
    _place(out, 0.75, _pad((62, 66, 69, 74), 2.6), 0.18)
    _place(out, 0.75, _bass(38, 2.0), 0.4)
    return _norm(out, 0.6)


def tension(dur):
    """低音嗡鸣 + 心跳。"""
    n = _n(dur)
    t = np.arange(n) / SR
    drone = _filt(_square(_f(26), n) * 0.5 + _square(_f(33) * 1.002, n) * 0.4, "lowpass", 300)
    drone *= np.minimum(1, t / 1.5)
    out = drone * 0.5
    for k in np.arange(0, dur - 0.3, 0.8):
        _place(out, k, _kick(), 0.6)
        _place(out, k + 0.2, _kick(), 0.4)
    return _norm(_fade(out, 0.1, 0.4), 0.35)


class Mixer:
    def __init__(self, dur):
        self.dur = dur
        self.buf = np.zeros(_n(dur) + SR * 4)

    def add(self, t, x, gain=1.0):
        i = _n(max(0, t))
        n = min(len(x), len(self.buf) - i)
        if n > 0:
            self.buf[i:i + n] += x[:n] * gain

    def write(self, path):
        y = self.buf[:_n(self.dur)]
        y = np.tanh(y * 1.1) / np.tanh(1.1)
        y = _norm(y, 0.89)
        y[-_n(0.5):] *= np.linspace(1, 0, _n(0.5))
        pcm = (np.repeat(y[:, None], 2, axis=1) * 32767).astype(np.int16)
        with wave.open(str(path), "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
