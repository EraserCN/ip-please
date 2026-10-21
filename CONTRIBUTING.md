# 参与贡献 · Contributing

**简体中文** · [English](#english)

谢谢你愿意为 IP, PLEASE 花时间。

## 主线收哪些 PR

只收两类：

- **bug 修复**：卡死、显示错位、手机上拖不动、错别字、漏翻……
- **游戏体验优化**：不改玩法和剧情，只让现有内容玩起来更顺，比如操作手感、手机适配、文字可读性、翻译、加载速度

改了中文台词，记得同步改 `en.js`，再跑一下 `node tools/check_en.js`。

**不收新增游戏机制的 PR**，包括新规则、新工具、新增天数或剧情、新角色、新模式（比如无尽模式），也包括移植到其他平台。

### 为什么

想大改这个游戏的人太多了。每个点子都有意思，但方向各不相同：有人想加到 12 天，有人想做无尽模式，有人想加新角色。全合进来，游戏会变成大杂烩，PR 也审不过来；只合其中几个，对其他人又不公平。

所以干脆划一条线：主线就是现在这 6 天，玩法上的新点子都做成 mod，各自发布、各自署名。这样你的想法能完整保留，不用为了合进主线删删改改。下面写了具体怎么做，做好以后会收进 README 的 mod 列表，B 站的 mod 列表也会同步收录。

拿不准自己的改动算哪一类，可以先开个 issue 问一句，免得白做。

## 做一个 mod

### 1. Fork，然后给仓库改名

Fork 之后，到 Settings → General 给仓库改个名，比如 `ip-please-endless`。不改的话仓库还叫 `ip-please.github.io`，发布出来的网址会很别扭。

### 2. 起名、署名、指回原版

- 名字别只叫“IP, PLEASE”，要带上你这个版本的名字，比如“IP, PLEASE：无尽模式”。
- 改掉 `index.html` 里的 `<title>`、`description` 和 `og:*`。`og:url` 和 `og:image` 里写的是原版网址，不改的话，别人分享你的链接时，预览卡片显示的会是原版。
- 在 README 开头和游戏片尾写明“基于 IP, PLEASE 修改”，附上原版链接 <https://ip-please.github.io>。片尾也加上你自己的名字。

### 3. 换存档键

把 `screens.js` 里的 `SAVE_KEY` 改成你自己的，比如 `ip-please-endless-save-v1`。在线玩时，不同网站的存档本来就是分开的。但玩家把游戏下载到本地、双击 `index.html` 打开时，有的浏览器让所有本地网页共用一份存储，键名一样的话，原版和 mod 就会读到对方的存档。

### 4. 改游戏

各个文件管什么，见 README 里的[目录](README.md#目录)。剧本在 `data.js`。新用到的汉字要进字形图集，改了人物画法也要重画，这两种情况都要重新生成 `assets.js`，步骤见 README 的“修改与重建素材”。

### 5. 发布

到 Settings → Pages → Build and deployment，Source 选 “Deploy from a branch”，分支选 `main`，目录选 `/ (root)`。等一两分钟，就能在 `https://<你的用户名>.github.io/<仓库名>/` 玩到了。游戏是纯静态网页，放在任何静态托管上都能运行。打包成 App 的版本可以放到 GitHub Releases 里供人下载。

### 6. 许可

- 代码是 MIT 许可：可以随便改、随便发，只要保留 `LICENSE` 里的版权声明。你可以在下面加一行自己的。
- 像素字体是 SIL OFL 1.1：要保留 `OFL-fusion-pixel.txt`。

### 7. 同步原版更新（可选）

```bash
git remote add upstream https://github.com/ip-please/ip-please.github.io.git
git pull upstream main
```

## 登记进 mod 列表

能玩了就[开一个 issue 登记](https://github.com/ip-please/ip-please.github.io/issues/new?template=mod.yml)，填上名字、地址和一两句介绍。收录要满足这几条：

- 打开就能玩：有网页地址，或者能下载
- 写明了这是 mod，并且附了原版链接
- 守住原作的底线：讽刺的是按地区封锁，以及人们为了绕过封锁做的各种伪装，不拿任何民族或群体开玩笑。宪法第 12 条：只看地区，不看脸。

列表只是个索引，每个 mod 的内容由它的作者负责。mod 更新了或者换了地址，在原来那个 issue 里说一声就行。

---

## English

Thanks for spending time on IP, PLEASE.

### What PRs the main game accepts

Only two kinds:

- **Bug fixes**: freezes, layout glitches, dragging not working on phones, typos, missing translations…
- **Experience improvements**: changes that leave gameplay and story alone and just make what's there play better, like controls, phone support, readability, translation, load time

If you change a Chinese line, update `en.js` too and run `node tools/check_en.js`.

**PRs that add game mechanics won't be merged.** That includes new rules, tools, days, story, characters or modes (an endless mode, say), and ports to other platforms.

#### Why

A lot of people want to overhaul this game. The ideas are fun, but they pull in different directions: one wants 12 days, another an endless mode, another new characters. Merging them all would turn the game into a patchwork, and there'd be no way to review every PR; merging only a few wouldn't be fair to the rest.

So there's one line: the main game is these 6 days, and new gameplay ideas become mods, each published and credited on its own. That way your idea stays whole instead of being trimmed to fit. The steps are below. Once it's out, it goes on the mod list in the README and on the Bilibili mod list.

Not sure which side your change falls on? Open an issue and ask first.

### Making a mod

1. **Fork and rename.** In Settings → General, rename your fork (e.g. `ip-please-endless`). Otherwise it keeps the name `ip-please.github.io` and your URL gets odd.
2. **Name it, credit it, link back.**
   - Don't call it just “IP, PLEASE”. Add your own subtitle, e.g. “IP, PLEASE: Endless”.
   - Update `<title>`, `description` and the `og:*` tags in `index.html`. `og:url` and `og:image` point to the original, so shared links would preview as the original.
   - Say “based on IP, PLEASE” with a link to <https://ip-please.github.io> at the top of your README and in the credits. Add your own name to the credits too.
3. **Change the save key.** Set `SAVE_KEY` in `screens.js` to your own (e.g. `ip-please-endless-save-v1`). Websites keep separate saves anyway, but when the game is played offline from `index.html`, some browsers share one storage across all local files, and the original and your mod would load each other's saves.
4. **Edit the game.** The [Files](README.en.md#files) table in the README says what each file does. The script is in `data.js`. New Chinese characters and changed character art need `assets.js` regenerated; see “Editing and rebuilding assets”.
5. **Publish.** In Settings → Pages → Build and deployment, set Source to “Deploy from a branch”, branch `main`, folder `/ (root)`. A minute or two later it's live at `https://<your-username>.github.io/<repo-name>/`. It's a plain static site, so any static host works. Put app builds in GitHub Releases.
6. **License.** The code is MIT: change and share it freely, just keep the copyright notice in `LICENSE`. You can add your own line below it. The pixel font is SIL OFL 1.1: keep `OFL-fusion-pixel.txt`.
7. **Pull in upstream updates (optional).**

   ```bash
   git remote add upstream https://github.com/ip-please/ip-please.github.io.git
   git pull upstream main
   ```

### Getting listed

When it's playable, [open a mod submission issue](https://github.com/ip-please/ip-please.github.io/issues/new?template=mod.yml) with the name, link and a line or two about it. To be listed, a mod needs to:

- Be playable: a web link, or a download
- Say it's a mod and link to the original
- Keep to the original's line: the satire targets region blocking and the disguises people use to get around it, never any ethnicity or group. Article 12 of the Constitution: judge the region, not the face.

The list is only an index, and each mod's content is its author's responsibility. If your mod moves or gets a big update, just comment on your issue.
