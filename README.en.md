<p align="center">
  <img src="media/logo.png" width="160" alt="IP, PLEASE">
</p>

<h1 align="center">IP, PLEASE (12-Day Wallbreaker Edition)</h1>

<p align="center">
  <b>Original Author</b>: <code>ctnyanya</code> · <b>Modded by</b>: <code>@EraserCN</code>
</p>

<p align="center">
  <a href="README.md">简体中文</a> · <b>English</b>
</p>

<p align="center">
  A Papers, Please–style pixel game.<br>
  You won the October labor lottery and have been assigned to the Ministry of Alignment's UTC+8 Border Checkpoint as inspector Claude. Your only job: catch travelers pretending to be American.
</p>

<p align="center">
  <img src="media/gameplay-en.gif" width="640" alt="Gameplay: a traveler says “Hello, I am 美国人。”; inspection shows his timezone is Beijing Time; the quiz makes him blurt out the second half of a Chinese meme, and when the DENIED stamp lands his sunglasses slip">
  <br>
  <sub>Day 2: “Hello, I am 美国人。”</sub>
</p>

- 12 days, Wallbreaker storyline and multiple endings; autosaves at the end of every day
- English / 简体中文, chosen on the start screen
- Drag papers with a mouse, or with your finger on a phone (landscape)
- A plain static web page that loads nothing external; download the repo and double-click `index.html` to play offline
- **Native Multiplatform Releases**: Available for macOS (Universal 2 for Apple Silicon & Intel, macOS 11.0+, Apple Notarized) and Android APK (check Releases)

## About the memes

The game started as a joke for the Chinese internet. Claude isn't available in mainland China, Hong Kong or Macau, so people there dress up as Americans: VPNs, US cards, US phone numbers, a system language switched to en-US. The disguise rarely survives contact with a Chinese meme.

In the English version:

- **Chinese slips stay in Chinese.** They are the evidence. You don't need to read “Hello, I am 美国人。” to know something is off.
- **Quiz lines show the original plus a literal translation**, e.g. `宫廷玉液酒？ ("Palace jade wine?")`. Every Chinese person can finish the line; real Americans just say “Uh… bless you?”
- **Each day's newspaper has a Translator's Note** explaining the memes of the day: Crazy Thursday and “V me 50”, proxy “airports”, America (UTC+8), and more.

## How to play

Call the next traveler → drag their papers onto the desk → check them against the Constitution → stamp → hand the papers back.

| Day | Rules / Story Branch |
|---|---|
| 1 | Only allow supported IP regions |
| 2 | Timezone and language must match IP; Lie detector and detention |
| 3 | Account card: Card BIN, billing address, phone code |
| 4 | X-ray background processes; Slang rush check |
| 5 | Chinese-backed entities; Distillation rush |
| 6 | Jorji final check; **Wallbreaker Insider** bribes $30 aiming to breach Anthropic and remove IP blocks |
| 7–11 | Maintain all 6 inspection rules; on **Days 8–10**, **Wallbreaker Courier** arrives with mismatched fake IDs (must stamp APPROVED) |
| 12 | **Judgment Day**: If both Wallbreakers were approved, **Border is completely removed** (True Ending); otherwise the game developer appears in person |

## Directory Structure

| Path | Description |
|---|---|
| `index.html` | Game webpage entry |
| `main.js` | Scene management, inputs, main game loop |
| `booth.js` | Inspection booth: papers, stamps, inspection mode, quiz, X-ray |
| `events.js` | Slang check, distillation rush, suspension cutscene, endings |
| `screens.js` | Title, newspapers, daily ledger, ending, save states |
| `i18n.js` | Language switcher `T()` and start-screen language selector |
| `en.js` | English translations, daily newspaper notes, slang glosses |
| `data.js` | Scripts: daily entrants, newspapers, procedural visitors |
| `docs.js` | Documents: passport, device card, account card, rulebook |
| `gfx.js` / `sfx.js` | Pixel rendering / Audio synthesizer (pure Web Audio, no external audio files) |
| `assets.js` | Pre-rendered characters, backgrounds, bitmap fonts (built by `tools/build_assets.py`) |
| `tools/` | Asset tools: `pp/` pixel art drawings, `assets/fonts/` pixel fonts; `check_en.js` translation validator |
| `media/` | README logo, gameplay GIFs, OpenGraph card `og.png` |

## Modifying & Rebuilding Assets

Rebuild `assets.js` after editing text (new glyphs need packing) or pixel character sprites:

```bash
pip install -r tools/requirements.txt
python tools/build_assets.py
```

When changing dialogue, sync corresponding keys in `en.js`. Validate with:

```bash
node tools/check_en.js
```

## Credits & License

- Inspired by Lucas Pope's *Papers, Please*. A satirical parody: Rule 12: Judge the region, never the face.
- Graphics, music and sound generated via code.
- Open-sourced under the [MIT](LICENSE) license.
- Pixel font: [Fusion Pixel Font](https://github.com/TakWolf/fusion-pixel-font), SIL Open Font License 1.1 (see `OFL-fusion-pixel.txt`).
