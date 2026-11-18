# 《TA 有话对你说》

面向中国内地梦女的「用户 × 梦角」塔罗传讯沉浸式互动网站。

象征性角色互动体验，仅供娱乐与自我探索，不代表真实读取 TA 的想法。

## 产品要点

- **简体中文 · 手机优先 · 无需注册**
- 完整 78 张伟特塔罗，正逆位独立随机
- **先抽牌，后解读**（禁止根据想要的答案反选牌）
- 人工风格完整段落文案，不随机拼接怪句
- 本地 IndexedDB 档案，支持导出/导入 JSON
- 静态站点，无后端、无付费 API
- **PWA**：可「添加到主屏幕」像 App 一样打开，首次访问后断网也能完整使用
- 单条传讯一键生成精美分享图（1080 宽高清 PNG，可保存 / 系统分享）
- 支持手机返回键、键盘操作、读屏（无障碍）与「减少动画」

## 技术栈

- 纯 HTML / CSS / JavaScript
- IndexedDB 本地存储
- `crypto.getRandomValues` 安全随机
- Service Worker 离线缓存 + Web App Manifest
- 无构建步骤，直接部署

## 目录结构

```
ta-tarot/
├── index.html            # 入口
├── manifest.webmanifest  # PWA 安装信息（名称、颜色、图标）
├── sw.js                 # Service Worker（离线缓存，含版本号）
├── css/styles.css        # 酒红 × 香槟金 风格
├── js/app.js             # 主逻辑
├── icons/                # App 图标（192/512、maskable、iOS、favicon）
├── data/
│   ├── tarot-cards.js    # 78 张牌核心数据
│   ├── themes.js         # 主题与语气
│   └── responses.js      # 传讯文案库 + 选择逻辑
└── README.md
```

## 本地预览

直接用任意静态服务器打开，或：

```bash
# Python
python -m http.server 8080

# Node
npx serve .
```

浏览器访问 `http://localhost:8080`。

**注意**：`file://` 协议下 IndexedDB 与部分浏览器策略可能受限，建议用本地服务器。

## 部署

可部署到任意静态托管：

- GitHub Pages
- Cloudflare Pages
- Netlify
- Vercel
- 自有 Nginx / CDN

将整个 `ta-tarot` 目录作为站点根目录即可。所有路径均为相对路径，**放在子目录下也能正常运行**（例如 `https://用户名.github.io/ta-tarot/`）。

> PWA（安装到桌面、离线缓存）要求 **HTTPS**（`localhost` 除外）。上述托管平台默认都提供 HTTPS。

### GitHub Pages（免费）

1. 新建一个 GitHub 仓库，把本目录全部文件上传到仓库根目录
2. 仓库 Settings → Pages → Source 选 `Deploy from a branch`，分支选 `main`、目录 `/ (root)`
3. 等待 1～2 分钟，访问 `https://用户名.github.io/仓库名/`

### 国内访问说明

- 页面使用 Google Fonts 作为**可选**美化字体，采用非阻塞加载：在国内网络无法访问时页面不会卡住，会自动使用系统自带的宋体 / 苹方 / 微软雅黑。
- 如希望国内用户也看到统一字体，可把 `index.html` 中的字体链接换成国内可访问的字体 CDN，或删除该行完全使用系统字体。
- 面向国内长期运营，建议使用国内服务器 / CDN 并完成 ICP 备案。

### 示例 Nginx

```nginx
server {
  listen 80;
  server_name your-domain.com;
  root /path/to/ta-tarot;
  index index.html;
  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

## 验收自测清单

### 抽牌正确性

- [ ] 从完整 78 张中真实随机
- [ ] 正逆位独立随机（约 50/50）
- [ ] 先固定抽牌结果，再检索文案
- [ ] 同一流程不会出现「想要什么牌就出什么牌」

### 内容质量

- [ ] 同类问题不同牌面，解读方向不同且不矛盾
- [ ] 文案为完整自然段落，无主语/情绪/事件乱拼
- [ ] 不编造用户当天遭遇、同居/见面/结婚等事实
- [ ] 结果页有明确免责声明

### 档案与本地存储

- [ ] 关闭页面再进入，历史记录完整保留
- [ ] 旧记录不因文案库更新而改变
- [ ] 收藏 / 删除 / 清空（有确认）正常
- [ ] JSON 导出与导入（结构校验）正常
- [ ] 单条生成分享图片正常

### 体验与适配

- [ ] iPhone 竖屏流程完整流畅
- [ ] 安卓主流浏览器可用
- [ ] 按钮触控区域足够
- [ ] 「减少动画」开关有效
- [ ] 设置页说明记录仅本地、建议备份

### PWA

- [ ] 浏览器可「添加到主屏幕 / 安装」，桌面图标正确
- [ ] 从桌面打开为全屏（无地址栏）
- [ ] 打开过一次后，开启飞行模式仍可抽牌、查看档案
- [ ] 发布新版本后，用户会看到「有新版本可用 · 更新」提示

## 买家自定义指南

| 想改什么 | 改哪里 |
|---|---|
| 网站名称 | `index.html` 的 `<title>`、`apple-mobile-web-app-title`、封面标题；`manifest.webmanifest` 的 `name` / `short_name`；`js/app.js` 分享图标题（搜索「TA 有话对你说」） |
| 配色 | `css/styles.css` 顶部 `:root` 变量；同时修改 `manifest.webmanifest` 与 `index.html` 中的 `theme-color` / `background_color` |
| App 图标 | 替换 `icons/` 下同名 PNG（192、512、maskable 192/512、apple-touch-icon 180、favicon 64）。maskable 图标主体需在中心 80% 范围内 |
| 文案 / 主题 / 语气 | 见下方「内容扩展指南」 |
| 免责声明 | `index.html` 结果页与设置页；`js/app.js` 分享图底部 |

**⚠️ 每次修改任何文件后发布，务必把 `sw.js` 顶部的 `VERSION` 改大一号（例如 `1.1.0` → `1.1.1`）**，并在 `js/app.js` 的 `APP_VERSION` 同步修改。否则已访问过的用户会继续使用旧的离线缓存。新增文件时，请把路径加入 `sw.js` 的 `PRECACHE` 列表。

### 数据说明

- 用户档案存放在浏览器 IndexedDB（库名 `ta-message-archive`），名字与设置存放在 localStorage。
- 修改域名后，旧域名下的用户记录不会自动迁移，可提示用户先「导出备份」再到新域名「导入」。
- 导出文件为 JSON 数组，导入时会逐条校验，无效条目自动跳过，相同 id 的记录会被覆盖更新。

## 内容扩展指南

### 增加精确文案

在 `data/responses.js` 的 `RESPONSES` 对象中按：

```
themeId → cardId → upright|reversed → toneId → [文案数组]
```

添加即可。选择逻辑会优先使用精确匹配。

### 增加主题

1. 在 `data/themes.js` 的 `THEMES` 数组追加
2. 在 `GENERIC_RESPONSES` 中补充对应极性文案
3. 可选：为高频牌补充精确 `RESPONSES`

### 牌义维护

`data/tarot-cards.js` 中每张牌含：

- `upright` / `reversed` 关键词与简要象征
- `themes` 关联标签（辅助，非强制）

## 语气说明

用户主动选择的代入风格，不宣称精准还原特定版权角色：

| 语气 | 感觉 |
|------|------|
| 温柔 | 柔软、体贴、带着温度 |
| 克制 | 含蓄、留有余地 |
| 直接 | 清晰、坦诚 |
| 俏皮 | 轻松、带一点调侃 |
| 安静 | 低声、沉淀 |

## 版本

- v1.1.0 · 2026-11：PWA（离线 + 可安装 + 更新提示）、高清分享图预览/保存/分享、档案详情页可生成图片、全部主题筛选、导入校验与结果提示、自定义确认弹窗、返回键支持、无障碍与响应式优化、修复收藏按钮状态残留与文本注入问题
- 首版 · 2026-11

---

象征性角色互动体验，仅供娱乐与自我探索。
