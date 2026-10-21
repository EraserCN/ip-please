#!/usr/bin/env node
// 查英文版缺哪些译文：扫根目录 JS 里所有含中文的字符串字面量，看 en.js 里有没有对应的键。
//
//   node tools/check_en.js
//
// - 地名这类“中国 · 浙江 · 电信”，每一段都有译文就算有
// - 'dv.归属' 这种检查模式的栏位引用不显示，跳过
// - 拼接出来的含中文模板字符串（`…${x}…`）英文版翻不了，会单独列出来，改成 T('…{0}…', x)
// - i18n.js（开局双语画面）、en.js、assets.js 不扫
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const SKIP = new Set(['assets.js', 'en.js', 'i18n.js']);
const CJK = /[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]/;

const ctx = {};
vm.runInNewContext(fs.readFileSync(path.join(ROOT, 'en.js'), 'utf8') + '\nthis.EN = EN;', ctx);
const has = (s) => Object.prototype.hasOwnProperty.call(ctx.EN, s) || (s.includes(' · ') && s.split(' · ').every(has));

// 粗糙的 JS 词法：只为了拿到字符串字面量（跳过注释和正则）
function literals(src) {
  const out = [];
  let i = 0, line = 1, prev = '';
  const read = (q) => {
    let s = '', parts = [];
    const start = line;
    for (i++; i < src.length && src[i] !== q; i++) {
      if (src[i] === '\\') { s += src[i + 1]; i++; continue; }
      if (src[i] === '\n') line++;
      if (q === '`' && src[i] === '$' && src[i + 1] === '{') {
        let depth = 1, j = i + 2;
        while (depth && j < src.length) { if (src[j] === '{') depth++; else if (src[j] === '}') depth--; j++; }
        out.push(...literals(src.slice(i + 2, j - 1)).map((l) => ({ ...l, line: l.line + line - 1 })));
        parts.push(s); s = ''; i = j - 1;
        continue;
      }
      s += src[i];
    }
    parts.push(s);
    out.push({ s: parts.join('{…}'), line: start, tpl: parts.length > 1 });
    i++;
  };
  while (i < src.length) {
    const c = src[i];
    if (c === '\n') { line++; i++; continue; }
    if (c === '/' && src[i + 1] === '/') { while (i < src.length && src[i] !== '\n') i++; continue; }
    if (c === '/' && src[i + 1] === '*') { const j = src.indexOf('*/', i + 2); line += src.slice(i, j).split('\n').length - 1; i = j + 2; continue; }
    if (c === '"' || c === "'" || c === '`') { read(c); prev = 'x'; continue; }
    if (c === '/' && /[(,=:[!&|?{};]|^$/.test(prev)) {        // 正则字面量
      for (i++; i < src.length && src[i] !== '/'; i++) if (src[i] === '\\') i++;
      i++; prev = 'x'; continue;
    }
    if (!/\s/.test(c)) prev = c;
    i++;
  }
  return out;
}

let missing = 0, joined = 0;
for (const f of fs.readdirSync(ROOT).filter((f) => f.endsWith('.js') && !SKIP.has(f)).sort()) {
  for (const { s, line, tpl } of literals(fs.readFileSync(path.join(ROOT, f), 'utf8'))) {
    if (!CJK.test(s) || /^[a-z0-9]+\.\S+$/.test(s)) continue;
    if (tpl) { joined++; console.log(`${f}:${line}  拼接的中文（改成 T 模板）：${s}`); continue; }
    if (!has(s)) { missing++; console.log(`${f}:${line}  缺译文：${s}`); }
  }
}
console.log(missing || joined ? `\n缺译文 ${missing} 条，拼接的中文 ${joined} 处` : '英文译文齐全');
process.exit(missing || joined ? 1 : 0);
