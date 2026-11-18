# 《TA 有话对你说》

面向中国内地梦女的「用户 × 梦角」塔罗传讯沉浸式互动网站。

象征性角色互动体验，仅供娱乐与自我探索，不代表真实读取 TA 的想法。

## 产品要点

- **简体中文 · 手机优先 · 无需注册**
- 完整 78 张伟特塔罗，正逆位独立随机
- **先抽牌，后解读**（禁止根据想要的答案反选牌）
- 人工风格完整段落文案，不随机拼接怪句
- 本地 IndexedDB 档案，支持导出/导入 JSON
- 静态站点，无后端、无付费 API、可离线（除字体）

## 技术栈

- 纯 HTML / CSS / JavaScript
- IndexedDB 本地存储
- `crypto.getRandomValues` 安全随机
- 无构建步骤，直接部署

## 目录结构

```
ta-tarot/
├── index.html          # 入口
├── css/styles.css      # 酒红 × 香槟金 风格
├── js/app.js           # 主逻辑
├── data/
│   ├── tarot-cards.js  # 78 张牌核心数据
│   ├── themes.js       # 主题与语气
│   └── responses.js    # 传讯文案库 + 选择逻辑
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

将整个 `ta-tarot` 目录作为站点根目录即可。

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

首版 · 2026-11

---

象征性角色互动体验，仅供娱乐与自我探索。
