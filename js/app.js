/**
 * 《TA 有话对你说》主应用逻辑
 * 静态前端，IndexedDB 本地档案，crypto 安全随机抽牌
 */

(function () {
  "use strict";

  // ========== 状态 ==========
  const state = {
    userName: "",
    taName: "",
    themeId: null,
    customQuestion: "",
    toneId: "gentle",
    currentDraw: null, // { card, isReversed, response, timestamp }
    archiveFilter: "all",
    reduceMotion: false,
  };

  // ========== IndexedDB ==========
  const DB_NAME = "ta-message-archive";
  const DB_VERSION = 1;
  const STORE_NAME = "messages";
  let db = null;

  function openDB() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onerror = () => reject(req.error);
      req.onsuccess = () => {
        db = req.result;
        resolve(db);
      };
      req.onupgradeneeded = (e) => {
        const database = e.target.result;
        if (!database.objectStoreNames.contains(STORE_NAME)) {
          const store = database.createObjectStore(STORE_NAME, { keyPath: "id" });
          store.createIndex("createdAt", "createdAt", { unique: false });
          store.createIndex("themeId", "themeId", { unique: false });
          store.createIndex("favorited", "favorited", { unique: false });
        }
      };
    });
  }

  function saveMessage(record) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, "readwrite");
      const store = tx.objectStore(STORE_NAME);
      const req = store.put(record);
      req.onsuccess = () => resolve(record);
      req.onerror = () => reject(req.error);
    });
  }

  function getAllMessages() {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, "readonly");
      const store = tx.objectStore(STORE_NAME);
      const req = store.getAll();
      req.onsuccess = () => {
        const list = req.result || [];
        list.sort((a, b) => b.createdAt - a.createdAt);
        resolve(list);
      };
      req.onerror = () => reject(req.error);
    });
  }

  function deleteMessage(id) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, "readwrite");
      const store = tx.objectStore(STORE_NAME);
      const req = store.delete(id);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }

  function clearAllMessages() {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, "readwrite");
      const store = tx.objectStore(STORE_NAME);
      const req = store.clear();
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }

  // ========== 安全随机 ==========
  function secureRandomInt(max) {
    const array = new Uint32Array(1);
    crypto.getRandomValues(array);
    return array[0] % max;
  }

  function secureRandomBool() {
    return secureRandomInt(2) === 1;
  }

  // ========== 抽牌（先抽后解读） ==========
  function drawCard() {
    const idx = secureRandomInt(TAROT_CARDS.length);
    const card = TAROT_CARDS[idx];
    const isReversed = secureRandomBool();
    return { card, isReversed };
  }

  // ========== 屏幕切换 ==========
  function showScreen(id) {
    document.querySelectorAll(".screen").forEach((el) => el.classList.remove("active"));
    const screen = document.getElementById("screen-" + id);
    if (screen) screen.classList.add("active");

    // 底部导航高亮
    document.querySelectorAll(".nav-item").forEach((el) => {
      el.classList.toggle("active", el.dataset.screen === id);
    });
  }

  // ========== 封面 ==========
  function initCover() {
    document.getElementById("btn-enter").addEventListener("click", () => {
      loadNames();
      showScreen("setup");
    });
  }

  // ========== 名字设置 ==========
  function loadNames() {
    try {
      const saved = JSON.parse(localStorage.getItem("ta-names") || "{}");
      state.userName = saved.userName || "";
      state.taName = saved.taName || "";
      document.getElementById("input-user-name").value = state.userName;
      document.getElementById("input-ta-name").value = state.taName;
    } catch (e) {}
  }

  function saveNames() {
    state.userName = document.getElementById("input-user-name").value.trim() || "我";
    state.taName = document.getElementById("input-ta-name").value.trim() || "TA";
    localStorage.setItem("ta-names", JSON.stringify({
      userName: state.userName,
      taName: state.taName
    }));
  }

  function initSetup() {
    document.getElementById("btn-setup-next").addEventListener("click", () => {
      saveNames();
      showScreen("theme");
      renderThemes();
    });
  }

  // ========== 主题与语气 ==========
  function renderThemes() {
    const grid = document.getElementById("theme-grid");
    grid.innerHTML = THEMES.map((t) => `
      <div class="theme-card ${state.themeId === t.id ? "selected" : ""}" data-id="${t.id}">
        <div class="name">${t.name}</div>
        <div class="desc">${t.description}</div>
      </div>
    `).join("");

    grid.querySelectorAll(".theme-card").forEach((el) => {
      el.addEventListener("click", () => {
        state.themeId = el.dataset.id;
        grid.querySelectorAll(".theme-card").forEach((c) => c.classList.remove("selected"));
        el.classList.add("selected");
        const freeArea = document.getElementById("free-question-area");
        freeArea.classList.toggle("hidden", state.themeId !== "free");
      });
    });

    // 语气
    const toneRow = document.getElementById("tone-row");
    toneRow.innerHTML = TONES.map((t) => `
      <div class="tone-chip ${state.toneId === t.id ? "selected" : ""}" data-id="${t.id}">${t.name}</div>
    `).join("");
    toneRow.querySelectorAll(".tone-chip").forEach((el) => {
      el.addEventListener("click", () => {
        state.toneId = el.dataset.id;
        toneRow.querySelectorAll(".tone-chip").forEach((c) => c.classList.remove("selected"));
        el.classList.add("selected");
      });
    });
  }

  function initTheme() {
    document.getElementById("btn-theme-next").addEventListener("click", () => {
      if (!state.themeId) {
        alert("请先选择一个问题主题");
        return;
      }
      if (state.themeId === "free") {
        state.customQuestion = document.getElementById("input-custom-question").value.trim();
        // 简单关键词分类尝试
        if (state.customQuestion) {
          const matched = tryClassifyQuestion(state.customQuestion);
          if (matched) {
            // 静默使用匹配主题，仍保留原问题
            state.themeId = matched;
          }
        }
      } else {
        state.customQuestion = document.getElementById("input-specific-question").value.trim();
      }
      startDraw();
    });
  }

  function tryClassifyQuestion(text) {
    for (const t of THEMES) {
      if (t.id === "free") continue;
      for (const kw of t.keywords) {
        if (text.includes(kw)) return t.id;
      }
    }
    return null;
  }

  // ========== 抽牌仪式 ==========
  function startDraw() {
    showScreen("draw");
    const cardBack = document.getElementById("card-back");
    const cardFront = document.getElementById("card-front");
    const hint = document.getElementById("draw-hint");
    const btnReveal = document.getElementById("btn-reveal");

    cardBack.style.display = "flex";
    cardFront.classList.remove("revealed");
    cardFront.style.display = "none";
    btnReveal.classList.add("hidden");
    hint.textContent = "深呼吸，把问题放在心里。点击牌背开始抽牌。";

    // 先抽好结果（禁止根据答案反选）
    const { card, isReversed } = drawCard();
    const response = getResponse(state.themeId, card, isReversed, state.toneId);

    state.currentDraw = {
      card,
      isReversed,
      response,
      timestamp: Date.now()
    };

    let shuffled = false;

    cardBack.onclick = () => {
      if (shuffled) return;
      shuffled = true;
      cardBack.classList.add("shuffling");
      hint.textContent = "牌正在显现……";

      setTimeout(() => {
        cardBack.classList.remove("shuffling");
        cardBack.style.display = "none";
        // 填充正面
        cardFront.querySelector(".card-name").textContent = card.name;
        cardFront.querySelector(".card-orient").textContent = isReversed ? "逆位" : "正位";
        const meaning = isReversed ? card.reversed : card.upright;
        cardFront.querySelector(".card-keywords").textContent = meaning.keywords.join(" · ");
        cardFront.style.display = "flex";
        cardFront.classList.add("revealed");
        hint.textContent = "牌已抽出。点击下方查看完整传讯。";
        btnReveal.classList.remove("hidden");
      }, state.reduceMotion ? 100 : 900);
    };

    btnReveal.onclick = () => {
      showResult();
    };
  }

  // ========== 结果页 ==========
  function showResult() {
    const d = state.currentDraw;
    if (!d) return;

    showScreen("result");

    document.getElementById("result-names").textContent =
      `${state.userName} × ${state.taName}`;
    const theme = THEMES.find((t) => t.id === state.themeId);
    document.getElementById("result-theme").textContent =
      theme ? theme.name + (state.customQuestion ? " · " + state.customQuestion.slice(0, 20) : "") : "";

    const meaning = d.isReversed ? d.card.reversed : d.card.upright;
    document.getElementById("result-card-name").textContent = d.card.name;
    document.getElementById("result-card-orient").textContent = d.isReversed ? "逆位" : "正位";
    document.getElementById("result-card-meaning").textContent = meaning.meaning;

    // 替换文案中的 TA 为实际梦角名（可选，保持「TA」也可）
    let msg = d.response;
    // 保持「TA」统一，不做替换，符合产品要求
    document.getElementById("message-text").textContent = msg;

    // 保存到档案
    const record = {
      id: "msg-" + d.timestamp + "-" + secureRandomInt(10000),
      createdAt: d.timestamp,
      userName: state.userName,
      taName: state.taName,
      themeId: state.themeId,
      themeName: theme ? theme.name : "",
      customQuestion: state.customQuestion,
      cardId: d.card.id,
      cardName: d.card.name,
      isReversed: d.isReversed,
      cardMeaning: meaning.meaning,
      response: d.response,
      toneId: state.toneId,
      favorited: false
    };

    saveMessage(record).catch(console.error);
    state.lastRecordId = record.id;
  }

  function initResult() {
    document.getElementById("btn-favorite").addEventListener("click", async () => {
      if (!state.lastRecordId) return;
      const list = await getAllMessages();
      const rec = list.find((r) => r.id === state.lastRecordId);
      if (rec) {
        rec.favorited = !rec.favorited;
        await saveMessage(rec);
        document.getElementById("btn-favorite").textContent =
          rec.favorited ? "已收藏" : "收藏";
      }
    });

    document.getElementById("btn-again").addEventListener("click", () => {
      showScreen("theme");
      renderThemes();
    });

    document.getElementById("btn-to-archive").addEventListener("click", () => {
      showScreen("archive");
      renderArchive();
    });

    document.getElementById("btn-share-image").addEventListener("click", () => {
      generateShareImage();
    });
  }

  // ========== 档案馆 ==========
  async function renderArchive() {
    const listEl = document.getElementById("archive-list");
    let list = await getAllMessages();

    if (state.archiveFilter === "fav") {
      list = list.filter((r) => r.favorited);
    } else if (state.archiveFilter !== "all") {
      list = list.filter((r) => r.themeId === state.archiveFilter);
    }

    if (list.length === 0) {
      listEl.innerHTML = `<div class="archive-empty">暂无传讯记录<br>完成一次抽牌后，记录会出现在这里</div>`;
      return;
    }

    listEl.innerHTML = list.map((r) => {
      const date = new Date(r.createdAt);
      const dateStr = `${date.getMonth() + 1}/${date.getDate()} ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
      return `
        <div class="archive-item" data-id="${r.id}">
          <div class="meta">
            <span>${dateStr} · ${r.themeName}</span>
            <span class="fav">${r.favorited ? "★" : ""}</span>
          </div>
          <div class="title">${r.cardName}${r.isReversed ? "（逆）" : ""} · ${r.userName} × ${r.taName}</div>
          <div class="preview">${r.response}</div>
        </div>
      `;
    }).join("");

    listEl.querySelectorAll(".archive-item").forEach((el) => {
      el.addEventListener("click", () => openArchiveDetail(el.dataset.id));
    });
  }

  async function openArchiveDetail(id) {
    const list = await getAllMessages();
    const r = list.find((x) => x.id === id);
    if (!r) return;

    const overlay = document.getElementById("modal-overlay");
    const sheet = document.getElementById("modal-sheet");
    const date = new Date(r.createdAt);

    sheet.innerHTML = `
      <div class="modal-handle"></div>
      <div class="result-header">
        <div class="result-names">${r.userName} × ${r.taName}</div>
        <div class="result-theme">${r.themeName}${r.customQuestion ? " · " + r.customQuestion : ""}</div>
      </div>
      <div class="result-card-info">
        <div class="name">${r.cardName}</div>
        <div class="orient">${r.isReversed ? "逆位" : "正位"}</div>
        <div class="meaning">${r.cardMeaning}</div>
      </div>
      <div class="message-box">
        <div class="message-text">${r.response}</div>
      </div>
      <div class="result-actions">
        <button class="btn btn-ghost btn-block" id="modal-fav">${r.favorited ? "取消收藏" : "收藏"}</button>
        <button class="btn btn-ghost btn-block" id="modal-delete">删除此条</button>
        <button class="btn btn-text btn-block" id="modal-close">关闭</button>
      </div>
      <p class="disclaimer">记录时间：${date.toLocaleString("zh-CN")}</p>
    `;

    overlay.classList.add("show");

    document.getElementById("modal-close").onclick = () => overlay.classList.remove("show");
    document.getElementById("modal-fav").onclick = async () => {
      r.favorited = !r.favorited;
      await saveMessage(r);
      overlay.classList.remove("show");
      renderArchive();
    };
    document.getElementById("modal-delete").onclick = async () => {
      if (confirm("确定删除这条传讯记录？")) {
        await deleteMessage(r.id);
        overlay.classList.remove("show");
        renderArchive();
      }
    };
  }

  function initArchive() {
    document.querySelectorAll(".archive-filters .chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        state.archiveFilter = chip.dataset.filter;
        document.querySelectorAll(".archive-filters .chip").forEach((c) => c.classList.remove("active"));
        chip.classList.add("active");
        renderArchive();
      });
    });

    document.getElementById("btn-export").addEventListener("click", async () => {
      const list = await getAllMessages();
      const blob = new Blob([JSON.stringify(list, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `ta-archive-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    });

    document.getElementById("btn-import").addEventListener("click", () => {
      document.getElementById("import-file").click();
    });

    document.getElementById("import-file").addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      try {
        const text = await file.text();
        const data = JSON.parse(text);
        if (!Array.isArray(data)) throw new Error("格式错误");
        // 简单校验
        for (const item of data) {
          if (!item.id || !item.createdAt || !item.response) continue;
          await saveMessage(item);
        }
        alert("导入完成");
        renderArchive();
      } catch (err) {
        alert("导入失败，请检查文件格式");
      }
      e.target.value = "";
    });

    document.getElementById("btn-clear-archive").addEventListener("click", async () => {
      if (confirm("确定清空全部传讯记录？此操作不可恢复。")) {
        await clearAllMessages();
        renderArchive();
      }
    });
  }

  // ========== 设置 ==========
  function initSettings() {
    const motionToggle = document.getElementById("toggle-motion");
    const saved = localStorage.getItem("ta-reduce-motion") === "1";
    state.reduceMotion = saved;
    if (saved) {
      document.body.classList.add("reduce-motion");
      motionToggle.classList.add("on");
    }

    motionToggle.addEventListener("click", () => {
      state.reduceMotion = !state.reduceMotion;
      motionToggle.classList.toggle("on", state.reduceMotion);
      document.body.classList.toggle("reduce-motion", state.reduceMotion);
      localStorage.setItem("ta-reduce-motion", state.reduceMotion ? "1" : "0");
    });

    document.getElementById("btn-edit-names").addEventListener("click", () => {
      showScreen("setup");
    });
  }

  // ========== 分享图（简单 canvas） ==========
  function generateShareImage() {
    const d = state.currentDraw;
    if (!d) return;

    const canvas = document.createElement("canvas");
    canvas.width = 600;
    canvas.height = 800;
    const ctx = canvas.getContext("2d");

    // 背景
    ctx.fillStyle = "#2d0f18";
    ctx.fillRect(0, 0, 600, 800);

    // 装饰线
    ctx.strokeStyle = "#d4af7a";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(80, 60);
    ctx.lineTo(520, 60);
    ctx.stroke();

    // 标题
    ctx.fillStyle = "#e8d5b5";
    ctx.font = "20px serif";
    ctx.textAlign = "center";
    ctx.fillText("TA 有话对你说", 300, 100);

    // 名字
    ctx.fillStyle = "#b8956a";
    ctx.font = "14px sans-serif";
    ctx.fillText(`${state.userName} × ${state.taName}`, 300, 130);

    // 牌信息
    ctx.fillStyle = "#e8d5b5";
    ctx.font = "18px serif";
    ctx.fillText(`${d.card.name} · ${d.isReversed ? "逆位" : "正位"}`, 300, 180);

    // 传讯正文
    ctx.fillStyle = "#f7f0e6";
    ctx.font = "16px serif";
    const lines = wrapText(ctx, d.response, 440);
    let y = 240;
    lines.forEach((line) => {
      ctx.fillText(line, 300, y);
      y += 28;
    });

    // 底部
    ctx.fillStyle = "rgba(184, 149, 106, 0.5)";
    ctx.font = "11px sans-serif";
    ctx.fillText("象征性角色互动体验 · 仅供娱乐与自我探索", 300, 760);

    // 下载
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `ta-message-${Date.now()}.png`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  function wrapText(ctx, text, maxWidth) {
    const chars = text.split("");
    const lines = [];
    let line = "";
    for (const ch of chars) {
      const test = line + ch;
      if (ctx.measureText(test).width > maxWidth && line) {
        lines.push(line);
        line = ch;
      } else {
        line = test;
      }
    }
    if (line) lines.push(line);
    return lines;
  }

  // ========== 底部导航 ==========
  function initNav() {
    document.querySelectorAll(".nav-item").forEach((el) => {
      el.addEventListener("click", () => {
        const s = el.dataset.screen;
        if (s === "archive") {
          showScreen("archive");
          renderArchive();
        } else if (s === "settings") {
          showScreen("settings");
        } else if (s === "theme") {
          showScreen("theme");
          renderThemes();
        } else if (s === "cover") {
          showScreen("cover");
        }
      });
    });
  }

  // ========== 启动 ==========
  async function init() {
    await openDB();
    initCover();
    initSetup();
    initTheme();
    initResult();
    initArchive();
    initSettings();
    initNav();
    showScreen("cover");
  }

  // DOM Ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
