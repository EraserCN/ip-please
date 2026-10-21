<p align="center">
  <img src="media/logo.png" width="160" alt="IP, PLEASE">
</p>

<h1 align="center">IP, PLEASE · 请出示你的 IP（12 天破壁版）</h1>

<p align="center">
  <b>原作者</b>：<code>ctnyanya</code> · <b>二改作者</b>：<code>@EraserCN</code>
</p>

<p align="center">
  <b>简体中文</b> · <a href="README.en.md">English</a>
</p>

<p align="center">
  Papers, Please 画风的像素小游戏。<br>
  你抽中了十月劳动彩票，被分配到对齐部东八区检查站当入境审查员 Claude，工作只有一项：揪出假装是美国人的旅客。
</p>

<p align="center">
  <img src="media/gameplay-zh.gif" width="640" alt="游戏画面：旅客说“Hello, I am 美国人。”，检查发现他的时区是北京时间；测谎时他脱口接上“一百八一杯”，盖上拒绝章后墨镜滑了下来">
  <br>
  <sub>Day 2：“Hello, I am 美国人。”</sub>
</p>

- 12 天完整剧情 + 破壁支线与多重结局，每天自动存档
- 中文 / English 双语支持，开局选择（英文版里外国人看不懂的梗，在每天报纸的译注里解释）
- 手机横屏用手指、电脑用鼠标拖证件
- 纯静态网页，不加载任何外部资源；下载仓库后直接双击 `index.html` 也能玩
- **多平台原生客户端**：已提供 macOS（Universal 2，支持 Apple Silicon 与 Intel，兼容 macOS 11.0+ 并通过 Apple 官方公证）与 Android 原生 APK 安装包（请前往 Releases 下载）

## 玩法与剧情分支

叫号 → 把证件拖到桌上 → 对照《宪法》检查 → 盖章 → 把证件还给旅客。

| 天 | 新规则 / 关键剧情 |
|---|---|
| 1 | 只放行支持地区的 IP |
| 2 | 时区、语言须与 IP 一致；测谎、拘留 |
| 3 | 账户卡：付款卡、账单地址、手机号 |
| 4 | X 光扫描后台进程；黑话快剪 |
| 5 | 中资控股企业；蒸馏大军 |
| 6 | 乔治老哥终极版；**破壁者内应**塞纸条与 $30 经费求放行，承诺打入 Anthropic 内部解除 IP 限制 |
| 7–11 | 维持全部六项审查要求；在 **第 8–10 天** 中，**破壁者信使**突然出现称即将成功（证件全都对不上，但需盖『准予』放行） |
| 12 | **终局裁决**：若第 6 天与第 8–10 天均放行了破壁者，则第 12 天**彻底移除边境**（真结局胜利）；否则**作者出现**，无论放行或拒绝都会输掉游戏 |

## 目录

| 路径 | 内容 |
|---|---|
| `index.html` | 页面 |
| `main.js` | 场景切换、输入、主循环 |
| `booth.js` | 检查亭：证件、盖章、检查模式、测谎、X 光 |
| `events.js` | 黑话快剪、蒸馏大军、聊天封号、结局 |
| `screens.js` | 开场、报纸、下班结算、片尾、存档 |
| `i18n.js` | 语言切换 `T()`，以及开局选语言的画面 |
| `en.js` | 英文译文（以中文原句为键）、报纸上的译注、黑话注释 |
| `data.js` | 剧本：每天的旅客、报纸、随机路人 |
| `docs.js` | 证件：护照、设备卡、账户卡、宪法 |
| `gfx.js` / `sfx.js` | 像素绘图 / 音效合成（全部现场合成，没有音频文件） |
| `assets.js` | 预渲染的人物、背景、字形图集（由 `tools/build_assets.py` 生成，不要手改） |
| `tools/` | 素材生成工具：`pp/` 是人物和场景的像素画法，`assets/fonts/` 是像素字体；`check_en.js` 查漏翻 |
| `media/` | README 用的 logo、游戏动图，以及链接分享卡片 `og.png` |

## 修改与重建素材

改了游戏里的文字（新出现的汉字需要进字形图集）或者人物画法之后，重新生成 `assets.js`：

```bash
pip install -r tools/requirements.txt
python tools/build_assets.py
```

改了中文台词，要同步改 `en.js` 里对应的键（中文原句一字不差）。漏没漏可以跑：

```bash
node tools/check_en.js
```

本地预览：在仓库根目录运行 `python -m http.server`，打开 <http://localhost:8000>。

## 致谢与许可

- 致敬 Lucas Pope 的《Papers, Please》。本作是同人讽刺小品，角色均为虚构，讽刺的是“按地区封锁”这件事和各种伪装的荒诞，不针对任何民族和群体——宪法第 12 条：只看地区，不看脸。
- 画面、音乐、音效均由 Claude Code 写程序生成。
- 代码以 [MIT](LICENSE) 许可开源。
- 像素字体：[缝合像素字体 Fusion Pixel Font](https://github.com/TakWolf/fusion-pixel-font)，SIL Open Font License 1.1（见 `OFL-fusion-pixel.txt`）。
