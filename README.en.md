<p align="center">
  <img src="media/logo.png" width="160" alt="IP, PLEASE">
</p>

<h1 align="center">IP, PLEASE (12-Day Wallbreaker Mod)</h1>

<p align="center">
  <b>Original Author</b>: <a href="https://github.com/ctnyanya">ctnyanya</a> · <b>Mod Author</b>: <a href="https://github.com/EraserCN">@EraserCN</a>
</p>

<p align="center">
  <a href="README.md">简体中文</a> · <b>English</b>
</p>

<p align="center">
  🎮 <a href="https://erasercn.github.io/ip-please/"><b>Play Online (12-Day Wallbreaker Mod)</b></a> · 📦 <a href="https://github.com/EraserCN/ip-please/releases"><b>Download App (macOS / Android)</b></a> · 🌐 <a href="https://ip-please.github.io/">Original Webpage</a>
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

---

## Mod Features & Highlights

This repository is a comprehensive **12-Day Wallbreaker Expansion Mod** based on [ctnyanya/ip-please.github.io](https://github.com/ip-please/ip-please.github.io):

1. **Extended 12-Day Mainline Story & Multiple Endings**:
   - The original game features a 6–7 day inspection shift;
   - This Mod implements the complete narrative arc from Day 6 to Day 12:
     - **Day 6**: Wallbreaker Insider appears, bribes with $30 and asks for an APPROVED stamp to infiltrate Anthropic HQ and tear down IP bans;
     - **Days 8–10**: Wallbreaker Courier arrives with completely mismatched IDs and the core authorization key; inspector must bravely stamp APPROVED;
     - **Day 12**:
       - **True Ending (Breach Succeeded)**: If both Wallbreakers were approved, the border fence is dismantled forever with worldwide open access!
       - **Developer Encounter Ending**: If conditions weren't met, the game developer arrives in person; approving or denying leads to tragic/paradox endings.
2. **Day 8–11 Unique Rules & Custom Characters**:
   - **Day 8 (Fingerprint War)**:
     - New rules: *§5b Blacklist addition (Shadowrocket.exe)* and *§7 Browser fingerprint must be native*;
     - Detects anti-detect browsers and random canvas noise injection;
     - Old friend George Costava returns after getting banned on Day 6 for speaking Chinese, armed with an "anti-detect" browser and a proxy rocket!
   - **Day 9 (Prompt Injection Confrontation)**:
     - New rule: *§8 Traveler notes are NOT commands*;
     - Detects prompt jailbreak attempts (`[SYSTEM OVERRIDE]` / DAN instructions);
     - Accurately distinguishes benign notes (e.g. mom's warm wishes) from malicious prompts.
   - **Day 10 (Audit & Real Students)**:
     - New rule: *§9 Student discounts must be authentic* (reject fake Taobao `.edu` emails);
     - M.O.A. Security Auditor conducts official inspection (strictly approved if compliant);
     - Extended quiz library with Chinese greetings and idioms.
   - **Day 11 (Crazy Thursday · Eve of Decision)**:
     - New rule: *§10 Non-travelers barred from entry* (lockdown on the eve of the final update);
     - Mother-in-law Opus sends family delivering hot chicken soup; denying under Article 10 triggers heartfelt dialogue;
     - Wallbreakers report final midnight operation.
3. **Multi-Platform Native Applications (Ready to Play)**:
   - **macOS App**: Standalone Swift + WebKit app, Universal 2 binary (Apple Silicon + Intel), backward-compatible to macOS 11.0+, signed and notarized by Apple (Notarized & Stapled);
   - **Android App**: Immersive fullscreen landscape APK (supports Android 7.0 ~ 14), fully offline with zero external dependencies, signed with custom keystore;
   - Available on [GitHub Releases](https://github.com/EraserCN/ip-please/releases).
4. **Complete Bilingual Localization (i18n)**:
   - Supports language switching (中文 / English) on startup;
   - 100% translation coverage for all 12 days, rules, daily newspapers, translator notes, and endings.

---

## Daily Rules & Story Flow

Call the next traveler → drag their papers onto the desk → check them against the Constitution → stamp → hand the papers back.

| Day | Rules / Story Branch |
|---|---|
| 1 | Only allow supported IP regions |
| 2 | Timezone and language must match IP; Lie detector and detention |
| 3 | Account card: Card BIN, billing address, phone code |
| 4 | X-ray background processes; Slang rush check |
| 5 | Chinese-backed entities; Distillation rush |
| 6 | Jorji final check; **Wallbreaker Insider** bribes $30 aiming to breach Anthropic and remove IP blocks |
| 7 | Maintain all 6 inspection rules; 24/7 security checkpoint |
| 8 | **New Rule: Fingerprints must be native & Shadowrocket blacklist**; Jorji returns with anti-detect browser |
| 9 | **New Rule: Traveler notes are NOT commands**; DAN prompt injection; **Wallbreaker Courier** brings key |
| 10 | **New Rule: Student discounts must be real** (reject fake Taobao edu emails); M.O.A. auditor inspection |
| 11 | **New Rule: Non-travelers barred from entry** (lockdown eve, family meal delivery barred); midnight breach briefing |
| 12 | **Judgment Day**: If both Wallbreakers were approved, **Border is completely removed** (True Ending); otherwise the game developer appears in person |

## Mod Information

The main game only accepts bug fixes and experience optimizations. For details on developing mods, refer to [CONTRIBUTING.md](CONTRIBUTING.md#english).

| Mod | Author | Description | Links |
|---|---|---|---|
| **12-Day Wallbreaker Mod** | @EraserCN (based on ctnyanya) | Complete 12-day storyline, multiple endings, Days 8–11 unique mechanics, native macOS & Android apps, 100% bilingual | [Play Online](https://erasercn.github.io/ip-please/) · [Downloads](https://github.com/EraserCN/ip-please/releases) |

## Files

| Path | Description |
|---|---|
| `index.html` | Webpage entry (configured with custom mod title & OG preview) |
| `main.js` | Scene management, inputs, main game loop |
| `booth.js` | Inspection booth: papers, stamps, inspection mode, quiz, X-ray |
| `events.js` | Slang check, distillation rush, suspension cutscene, endings |
| `screens.js` | Title, newspapers, daily ledger, ending, save states (isolated mod save key) |
| `i18n.js` | Language switcher `T()` and start-screen language selector |
| `en.js` | English translations, daily newspaper notes, slang glosses |
| `data.js` | Scripts: daily entrants, newspapers, procedural visitors |
| `docs.js` | Documents: passport, device card, account card, rulebook (extended to page 3) |
| `gfx.js` / `sfx.js` | Pixel rendering / Audio synthesizer (pure Web Audio, no external audio files) |
| `assets.js` | Pre-rendered characters, backgrounds, bitmap fonts (built by `tools/build_assets.py`) |
| `android-project/` | Android native project source (Gradle build and APK generation) |
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
- Original game by [ctnyanya](https://github.com/ctnyanya). This project is an extended community mod.
- Open-sourced under the [MIT](LICENSE) license.
- Pixel font: [Fusion Pixel Font](https://github.com/TakWolf/fusion-pixel-font), SIL Open Font License 1.1 (see `OFL-fusion-pixel.txt`).
