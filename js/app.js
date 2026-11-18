/**
 * 《TA 有话对你说》主应用逻辑
 * 静态前端，IndexedDB 本地档案，crypto 安全随机抽牌，PWA 离线可用
 */

(function () {
  "use strict";

  const APP_VERSION = "1.1.0";

  // ========== 状态 ==========
  const state = {
    userName: "",
    taName: "",
    themeId: null,
    customQuestion: "",
    toneId: "gentle",
    currentDraw: null, // { card, isReversed, response, timestamp }
    lastRecordId: null,
    archiveFilter: "all",
    reduceMotion: false,
    screen: "cover",
  };

  const $ = (id) => document.getElementById(id);

  // ========== 工具 ==========
  function esc(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function pad2(n) { return String(n).padStart(2, "0"); }

  function formatShortDate(ts) {
    const d = new Date(ts);
    return `${d.getMonth() + 1}/${d.getDate()} ${pad2(d.getHours())}:${pad2(d.getMinutes())}`;
  }

  function formatFullDate(ts) {
    const d = new Date(ts);
    return `${d.getFullYear()}.${pad2(d.getMonth() + 1)}.${pad2(d.getDate())} ${pad2(d.getHours())}:${pad2(d.getMinutes())}`;
  }

  // ========== 轻提示 ==========
  let toastTimer = null;
  function showToast(message, opts = {}) {
    const el = $("toast");
    el.innerHTML = "";
    const span = document.createElement("span");
    span.textContent = message;
    el.appendChild(span);
    if (opts.action) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "toast-action";
      b.textContent = opts.action.label;
      b.addEventListener("click", () => { hideToast(); opts.action.fn(); });
      el.appendChild(b);
    }
    el.classList.add("show");
    clearTimeout(toastTimer);
    if (opts.duration !== 0) toastTimer = setTimeout(hideToast, opts.duration || 2600);
  }
  function hideToast() { $("toast").classList.remove("show"); }

  // ========== IndexedDB ==========
  const DB_NAME = "ta-message-archive";
  const DB_VERSION = 1;
  const STORE_NAME = "messages";
  let db = null;

  function openDB() {
    return new Promise((resolve, reject) => {
      if (!("indexedDB" in window)) return reject(new Error("no-indexeddb"));
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onerror = () => reject(req.error);
      req.onsuccess = () => { db = req.result; resolve(db); };
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

  function tx(mode, fn) {
    return new Promise((resolve, reject) => {
      if (!db) return reject(new Error("db-unavailable"));
      const t = db.transaction(STORE_NAME, mode);
      const req = fn(t.objectStore(STORE_NAME));
      t.oncomplete = () => resolve(req ? req.result : undefined);
      t.onerror = () => reject(t.error);
      t.onabort = () => reject(t.error);
    });
  }

  const saveMessage = (record) => tx("readwrite", (s) => s.put(record)).then(() => record);
  const getMessage = (id) => tx("readonly", (s) => s.get(id));
  const deleteMessage = (id) => tx("readwrite", (s) => s.delete(id));
  const clearAllMessages = () => tx("readwrite", (s) => s.clear());
  function getAllMessages() {
    return tx("readonly", (s) => s.getAll()).then((list) => (list || []).sort((a, b) => b.createdAt - a.createdAt));
  }

  // ========== 安全随机（无模偏差） ==========
  function secureRandomInt(max) {
    const limit = Math.floor(0x100000000 / max) * max;
    const array = new Uint32Array(1);
    do { crypto.getRandomValues(array); } while (array[0] >= limit);
    return array[0] % max;
  }
  const secureRandomBool = () => secureRandomInt(2) === 1;

  // ========== 抽牌（先抽后解读） ==========
  function drawCard() {
    const card = TAROT_CARDS[secureRandomInt(TAROT_CARDS.length)];
    return { card, isReversed: secureRandomBool() };
  }

  // ========== 屏幕切换 + 返回键支持 ==========
  const NAV_SCREENS = ["theme", "result", "archive", "settings"];

  function showScreen(id, opts = {}) {
    if (id === "draw" && !state.currentDraw) id = "theme";
    if (id === "result" && !state.currentDraw) id = "theme";
    const prev = state.screen;
    state.screen = id;

    document.querySelectorAll(".screen").forEach((el) => el.classList.remove("active"));
    const screen = $("screen-" + id);
    if (screen) screen.classList.add("active");

    $("bottom-nav").classList.toggle("hidden", !NAV_SCREENS.includes(id));
    document.querySelectorAll(".nav-item").forEach((el) => {
      const on = el.dataset.screen === id || (id === "result" && el.dataset.screen === "theme");
      el.classList.toggle("active", on);
      if (on) el.setAttribute("aria-current", "page"); else el.removeAttribute("aria-current");
    });

    if (id === "theme") renderThemes();
    if (id === "archive") renderArchive();
    if (id === "setup") loadNames();

    if (opts.push !== false && prev !== id) history.pushState({ screen: id }, "");
    window.scrollTo(0, 0);

    // 无障碍：切换后把焦点移到标题，读屏能感知页面变化
    if (opts.focus !== false && prev !== id) {
      const title = screen && screen.querySelector("[tabindex='-1']");
      if (title) title.focus({ preventScroll: true });
    }
  }

  function goBack() {
    if (history.state && history.length > 1) history.back();
    else showScreen("cover");
  }

  window.addEventListener("popstate", (e) => {
    if (modalOpen) { hideModal(); return; }
    const s = (e.state && e.state.screen) || "cover";
    showScreen(s === "draw" ? "theme" : s, { push: false });
  });

  // ========== 弹层 ==========
  let modalOpen = false;
  let modalReturnFocus = null;
  let modalCleanup = null;

  function openModal(html, opts = {}) {
    const overlay = $("modal-overlay");
    const sheet = $("modal-sheet");
    if (modalCleanup) { modalCleanup(); modalCleanup = null; }
    sheet.innerHTML = `<div class="modal-handle" aria-hidden="true"></div>` + html;
    sheet.setAttribute("aria-label", opts.label || "详情");
    modalCleanup = opts.onClose || null;
    if (!modalOpen) {
      modalReturnFocus = document.activeElement;
      modalOpen = true;
      overlay.classList.add("show");
      overlay.setAttribute("aria-hidden", "false");
      document.body.classList.add("modal-open");
      history.pushState({ screen: state.screen, modal: true }, "");
    }
    sheet.scrollTop = 0;
    const first = sheet.querySelector("button, [href], input");
    (first || sheet).focus({ preventScroll: true });
  }

  function hideModal() {
    if (!modalOpen) return;
    modalOpen = false;
    const overlay = $("modal-overlay");
    overlay.classList.remove("show");
    overlay.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
    if (modalCleanup) { modalCleanup(); modalCleanup = null; }
    if (modalReturnFocus && document.contains(modalReturnFocus)) modalReturnFocus.focus({ preventScroll: true });
  }

  function closeModal() {
    if (!modalOpen) return;
    if (history.state && history.state.modal) history.back(); // popstate -> hideModal
    else hideModal();
  }

  function confirmDialog(message, okText = "确定", danger = false) {
    return new Promise((resolve) => {
      let answered = false;
      openModal(`
        <p class="confirm-text">${esc(message)}</p>
        <div class="result-actions">
          <button type="button" class="btn ${danger ? "btn-danger" : "btn-primary"} btn-block" data-ok>${esc(okText)}</button>
          <button type="button" class="btn btn-text btn-block" data-cancel>取消</button>
        </div>`, {
        label: "确认",
        onClose: () => { if (!answered) resolve(false); },
      });
      const sheet = $("modal-sheet");
      sheet.querySelector("[data-cancel]").focus();
      sheet.querySelector("[data-ok]").onclick = () => { answered = true; resolve(true); closeModal(); };
      sheet.querySelector("[data-cancel]").onclick = () => { answered = true; resolve(false); closeModal(); };
    });
  }

  function initModal() {
    const overlay = $("modal-overlay");
    overlay.addEventListener("click", (e) => { if (e.target === overlay) closeModal(); });
    document.addEventListener("keydown", (e) => {
      if (!modalOpen) return;
      if (e.key === "Escape") { e.preventDefault(); closeModal(); }
      if (e.key === "Tab") {
        const f = [...$("modal-sheet").querySelectorAll("button, [href], input, textarea")].filter((x) => !x.disabled && x.offsetParent);
        if (!f.length) return;
        const first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  // ========== 封面 ==========
  async function initCover() {
    $("btn-enter").addEventListener("click", () => showScreen("setup"));
    $("btn-cover-archive").addEventListener("click", () => showScreen("archive"));
    try {
      const list = await getAllMessages();
      $("btn-cover-archive").classList.toggle("hidden", list.length === 0);
    } catch (e) { /* 忽略 */ }
  }

  // ========== 名字设置 ==========
  function loadNames() {
    try {
      const saved = JSON.parse(localStorage.getItem("ta-names") || "{}");
      state.userName = saved.userName || "";
      state.taName = saved.taName || "";
    } catch (e) { /* 忽略 */ }
    $("input-user-name").value = state.userName === "我" ? "" : state.userName;
    $("input-ta-name").value = state.taName === "TA" ? "" : state.taName;
  }

  function saveNames() {
    state.userName = $("input-user-name").value.trim() || "我";
    state.taName = $("input-ta-name").value.trim() || "TA";
    try {
      localStorage.setItem("ta-names", JSON.stringify({ userName: state.userName, taName: state.taName }));
    } catch (e) { /* 存储不可用时仍可继续 */ }
  }

  function ensureNames() {
    if (state.userName && state.taName) return;
    loadNames();
    state.userName = state.userName || "我";
    state.taName = state.taName || "TA";
  }

  function initSetup() {
    const next = () => { saveNames(); showScreen("theme"); };
    $("btn-setup-next").addEventListener("click", next);
    $("input-user-name").addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); $("input-ta-name").focus(); } });
    $("input-ta-name").addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); next(); } });
  }

  // ========== 主题与语气 ==========
  function renderThemes() {
    const grid = $("theme-grid");
    grid.innerHTML = THEMES.map((t) => `
      <button type="button" role="radio" aria-checked="${state.themeId === t.id}" class="theme-card ${state.themeId === t.id ? "selected" : ""}" data-id="${esc(t.id)}">
        <span class="name">${esc(t.name)}</span>
        <span class="desc">${esc(t.description)}</span>
      </button>
    `).join("");

    grid.querySelectorAll(".theme-card").forEach((el) => {
      el.addEventListener("click", () => {
        state.themeId = el.dataset.id;
        grid.querySelectorAll(".theme-card").forEach((c) => {
          const on = c === el;
          c.classList.toggle("selected", on);
          c.setAttribute("aria-checked", String(on));
        });
        grid.classList.remove("need-select");
        $("free-question-area").classList.toggle("hidden", state.themeId !== "free");
        $("specific-question-area").classList.toggle("hidden", state.themeId === "free");
      });
    });
    $("free-question-area").classList.toggle("hidden", state.themeId !== "free");
    $("specific-question-area").classList.toggle("hidden", state.themeId === "free");

    const toneRow = $("tone-row");
    toneRow.innerHTML = TONES.map((t) => `
      <button type="button" role="radio" aria-checked="${state.toneId === t.id}" class="tone-chip ${state.toneId === t.id ? "selected" : ""}" data-id="${esc(t.id)}">${esc(t.name)}</button>
    `).join("");
    const updateToneDesc = () => {
      const t = TONES.find((x) => x.id === state.toneId);
      $("tone-desc").textContent = t ? t.description : "";
    };
    toneRow.querySelectorAll(".tone-chip").forEach((el) => {
      el.addEventListener("click", () => {
        state.toneId = el.dataset.id;
        toneRow.querySelectorAll(".tone-chip").forEach((c) => {
          const on = c === el;
          c.classList.toggle("selected", on);
          c.setAttribute("aria-checked", String(on));
        });
        updateToneDesc();
      });
    });
    updateToneDesc();
  }

  function initTheme() {
    $("btn-theme-next").addEventListener("click", () => {
      if (!state.themeId) {
        const grid = $("theme-grid");
        grid.classList.remove("need-select");
        void grid.offsetWidth;
        grid.classList.add("need-select");
        showToast("请先选择一个问题主题");
        grid.querySelector(".theme-card").focus();
        return;
      }
      ensureNames();
      let themeId = state.themeId;
      if (themeId === "free") {
        state.customQuestion = $("input-custom-question").value.trim();
        if (state.customQuestion) {
          const matched = tryClassifyQuestion(state.customQuestion);
          if (matched) themeId = matched; // 静默使用匹配主题，仍保留原问题
        }
      } else {
        state.customQuestion = $("input-specific-question").value.trim();
      }
      startDraw(themeId);
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
  function startDraw(themeId) {
    // 先抽好结果（禁止根据答案反选）
    const { card, isReversed } = drawCard();
    const response = getResponse(themeId, card, isReversed, state.toneId);
    state.currentDraw = { card, isReversed, response, themeId, timestamp: Date.now(), saved: false };
    state.lastRecordId = null;

    showScreen("draw");
    const cardBack = $("card-back");
    const cardFront = $("card-front");
    const hint = $("draw-hint");
    const btnReveal = $("btn-reveal");

    cardBack.classList.remove("shuffling", "hidden");
    cardBack.disabled = false;
    cardFront.classList.remove("revealed", "is-reversed");
    btnReveal.classList.add("hidden");
    hint.textContent = "深呼吸，把问题放在心里。点击牌背开始抽牌。";
    setTimeout(() => cardBack.focus({ preventScroll: true }), 50);

    cardBack.onclick = () => {
      if (cardBack.disabled) return;
      cardBack.disabled = true;
      cardBack.classList.add("shuffling");
      hint.textContent = "牌正在显现……";
      setTimeout(() => {
        cardBack.classList.remove("shuffling");
        cardBack.classList.add("hidden");
        const meaning = isReversed ? card.reversed : card.upright;
        cardFront.querySelector(".card-name").textContent = card.name;
        cardFront.querySelector(".card-name-en").textContent = card.nameEn || "";
        cardFront.querySelector(".card-orient").textContent = isReversed ? "逆位" : "正位";
        cardFront.querySelector(".card-keywords").textContent = meaning.keywords.join(" · ");
        cardFront.classList.toggle("is-reversed", isReversed);
        cardFront.classList.add("revealed");
        hint.textContent = "牌已抽出。点击下方查看完整传讯。";
        btnReveal.classList.remove("hidden");
        btnReveal.focus({ preventScroll: true });
      }, state.reduceMotion ? 120 : 1100);
    };

    btnReveal.onclick = () => showResult();
  }

  // ========== 结果页 ==========
  function buildRecord(d) {
    const theme = THEMES.find((t) => t.id === d.themeId);
    const meaning = d.isReversed ? d.card.reversed : d.card.upright;
    return {
      id: "msg-" + d.timestamp + "-" + secureRandomInt(10000),
      createdAt: d.timestamp,
      userName: state.userName,
      taName: state.taName,
      themeId: d.themeId,
      themeName: theme ? theme.name : "",
      customQuestion: state.customQuestion,
      cardId: d.card.id,
      cardName: d.card.name,
      isReversed: d.isReversed,
      cardMeaning: meaning.meaning,
      response: d.response,
      toneId: state.toneId,
      favorited: false,
    };
  }

  function showResult() {
    const d = state.currentDraw;
    if (!d) return;
    const record = buildRecord(d);
    renderResult(record);
    showScreen("result");

    if (!d.saved) {
      d.saved = true;
      saveMessage(record)
        .then(() => { state.lastRecordId = record.id; $("btn-cover-archive").classList.remove("hidden"); })
        .catch((err) => { console.warn(err); showToast("本次记录未能保存到档案（浏览器存储不可用）"); });
      state.currentRecord = record;
    }
  }

  function renderResult(r) {
    $("result-names").textContent = `${r.userName} × ${r.taName}`;
    $("result-theme").textContent = r.themeName + (r.customQuestion ? " · " + r.customQuestion.slice(0, 30) : "");
    $("result-card-name").textContent = r.cardName;
    $("result-card-orient").textContent = r.isReversed ? "逆位" : "正位";
    $("result-card-meaning").textContent = r.cardMeaning;
    $("message-text").textContent = r.response; // 保持「TA」统一，不做替换，符合产品要求
    setFavButton(false);
  }

  function setFavButton(on) {
    const b = $("btn-favorite");
    b.textContent = on ? "★ 已收藏" : "☆ 收藏";
    b.setAttribute("aria-pressed", String(on));
    b.classList.toggle("is-on", on);
  }

  function initResult() {
    $("btn-favorite").addEventListener("click", async () => {
      if (!state.lastRecordId) { showToast("记录保存中，请稍候"); return; }
      try {
        const rec = await getMessage(state.lastRecordId);
        if (!rec) return;
        rec.favorited = !rec.favorited;
        await saveMessage(rec);
        setFavButton(rec.favorited);
        showToast(rec.favorited ? "已加入收藏" : "已取消收藏");
      } catch (e) { showToast("操作失败，请重试"); }
    });
    $("btn-again").addEventListener("click", () => showScreen("theme"));
    $("btn-to-archive").addEventListener("click", () => showScreen("archive"));
    $("btn-share-image").addEventListener("click", () => {
      if (state.currentRecord) openShareImage(state.currentRecord);
    });
  }

  // ========== 档案馆 ==========
  function renderFilters() {
    const filters = [{ id: "all", name: "全部" }, { id: "fav", name: "★ 收藏" }]
      .concat(THEMES.map((t) => ({ id: t.id, name: t.name })));
    const wrap = $("archive-filters");
    wrap.innerHTML = filters.map((f) => `
      <button type="button" class="chip ${state.archiveFilter === f.id ? "active" : ""}" aria-pressed="${state.archiveFilter === f.id}" data-filter="${esc(f.id)}">${esc(f.name)}</button>
    `).join("");
    wrap.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        state.archiveFilter = chip.dataset.filter;
        renderFilters();
        renderArchive();
      });
    });
  }

  async function renderArchive() {
    const listEl = $("archive-list");
    let all;
    try { all = await getAllMessages(); }
    catch (e) {
      listEl.innerHTML = `<div class="archive-empty">当前浏览器不支持本地存储（可能处于无痕模式），档案功能不可用。</div>`;
      return;
    }
    $("archive-count").textContent = all.length ? ` 共 ${all.length} 条。` : "";

    let list = all;
    if (state.archiveFilter === "fav") list = all.filter((r) => r.favorited);
    else if (state.archiveFilter !== "all") list = all.filter((r) => r.themeId === state.archiveFilter);

    if (list.length === 0) {
      listEl.innerHTML = all.length
        ? `<div class="archive-empty">这个分类下还没有记录</div>`
        : `<div class="archive-empty">暂无传讯记录<br>完成一次抽牌后，记录会出现在这里<br><button type="button" class="btn btn-ghost" id="btn-empty-draw">去抽一张</button></div>`;
      const b = $("btn-empty-draw");
      if (b) b.onclick = () => showScreen(state.userName ? "theme" : "setup");
      return;
    }

    listEl.innerHTML = list.map((r) => `
      <div class="archive-item" role="button" tabindex="0" data-id="${esc(r.id)}" aria-label="${esc(r.cardName + (r.isReversed ? "逆位" : "正位") + "，" + formatShortDate(r.createdAt) + "，查看详情")}">
        <div class="meta">
          <span>${esc(formatShortDate(r.createdAt))} · ${esc(r.themeName)}</span>
          <span class="fav" aria-label="${r.favorited ? "已收藏" : ""}">${r.favorited ? "★" : ""}</span>
        </div>
        <div class="title">${esc(r.cardName)}${r.isReversed ? "（逆）" : ""} · ${esc(r.userName)} × ${esc(r.taName)}</div>
        <div class="preview">${esc(r.response)}</div>
      </div>
    `).join("");

    listEl.querySelectorAll(".archive-item").forEach((el) => {
      el.addEventListener("click", () => openArchiveDetail(el.dataset.id));
      el.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openArchiveDetail(el.dataset.id); }
      });
    });
  }

  async function openArchiveDetail(id) {
    const r = await getMessage(id);
    if (!r) return;
    openModal(`
      <div class="result-header">
        <div class="result-names">${esc(r.userName)} × ${esc(r.taName)}</div>
        <div class="result-theme">${esc(r.themeName)}${r.customQuestion ? " · " + esc(r.customQuestion) : ""}</div>
      </div>
      <div class="result-card-info">
        <div class="name">${esc(r.cardName)}</div>
        <div class="orient">${r.isReversed ? "逆位" : "正位"}</div>
        <div class="meaning">${esc(r.cardMeaning)}</div>
      </div>
      <div class="message-box">
        <div class="message-text">${esc(r.response)}</div>
      </div>
      <div class="result-actions">
        <div class="result-actions-row">
          <button type="button" class="btn btn-ghost" id="modal-fav" aria-pressed="${!!r.favorited}">${r.favorited ? "★ 取消收藏" : "☆ 收藏"}</button>
          <button type="button" class="btn btn-ghost" id="modal-share">生成图片</button>
        </div>
        <button type="button" class="btn btn-ghost btn-block btn-danger-ghost" id="modal-delete">删除此条</button>
        <button type="button" class="btn btn-text btn-block" id="modal-close">关闭</button>
      </div>
      <p class="disclaimer">记录时间：${esc(formatFullDate(r.createdAt))}</p>
    `, { label: "传讯详情" });

    $("modal-close").onclick = closeModal;
    $("modal-fav").onclick = async () => {
      r.favorited = !r.favorited;
      await saveMessage(r);
      $("modal-fav").textContent = r.favorited ? "★ 取消收藏" : "☆ 收藏";
      $("modal-fav").setAttribute("aria-pressed", String(r.favorited));
      showToast(r.favorited ? "已加入收藏" : "已取消收藏");
      renderArchive();
    };
    $("modal-share").onclick = () => openShareImage(r);
    $("modal-delete").onclick = async () => {
      if (await confirmDialog("确定删除这条传讯记录？", "删除", true)) {
        await deleteMessage(r.id);
        showToast("已删除");
        renderArchive();
      }
    };
  }

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.rel = "noopener";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
  }

  function normalizeImported(item) {
    if (!item || typeof item !== "object") return null;
    const { id, createdAt, response, cardName } = item;
    if (typeof id !== "string" || !id || typeof response !== "string" || !response) return null;
    const ts = typeof createdAt === "number" ? createdAt : Date.parse(createdAt);
    if (!isFinite(ts)) return null;
    return {
      id: id.slice(0, 80),
      createdAt: ts,
      userName: String(item.userName || "我").slice(0, 20),
      taName: String(item.taName || "TA").slice(0, 20),
      themeId: String(item.themeId || "free"),
      themeName: String(item.themeName || ""),
      customQuestion: String(item.customQuestion || "").slice(0, 200),
      cardId: String(item.cardId || ""),
      cardName: String(cardName || "未知牌"),
      isReversed: !!item.isReversed,
      cardMeaning: String(item.cardMeaning || ""),
      response: response.slice(0, 5000),
      toneId: String(item.toneId || "gentle"),
      favorited: !!item.favorited,
    };
  }

  function initArchive() {
    renderFilters();

    $("btn-export").addEventListener("click", async () => {
      const list = await getAllMessages();
      if (!list.length) { showToast("暂无记录可导出"); return; }
      const blob = new Blob([JSON.stringify(list, null, 2)], { type: "application/json" });
      downloadBlob(blob, `ta-archive-${new Date().toISOString().slice(0, 10)}.json`);
      showToast(`已导出 ${list.length} 条记录`);
    });

    $("btn-import").addEventListener("click", () => $("import-file").click());

    $("import-file").addEventListener("change", async (e) => {
      const file = e.target.files[0];
      e.target.value = "";
      if (!file) return;
      try {
        if (file.size > 10 * 1024 * 1024) throw new Error("too-large");
        const data = JSON.parse(await file.text());
        const arr = Array.isArray(data) ? data : (data && (data.records || data.messages));
        if (!Array.isArray(arr)) throw new Error("格式错误");
        const existing = new Set((await getAllMessages()).map((r) => r.id));
        let added = 0, updated = 0, skipped = 0;
        for (const raw of arr) {
          const rec = normalizeImported(raw);
          if (!rec) { skipped++; continue; }
          if (existing.has(rec.id)) updated++; else added++;
          await saveMessage(rec);
        }
        if (!added && !updated) throw new Error("no-valid");
        showToast(`导入完成：新增 ${added} 条${updated ? `，更新 ${updated} 条` : ""}${skipped ? `，跳过 ${skipped} 条无效记录` : ""}`, { duration: 4000 });
        renderArchive();
      } catch (err) {
        showToast("导入失败，请选择本站导出的 JSON 备份文件", { duration: 4000 });
      }
    });

    $("btn-clear-archive").addEventListener("click", async () => {
      const list = await getAllMessages();
      if (!list.length) { showToast("档案已经是空的"); return; }
      if (await confirmDialog(`确定清空全部 ${list.length} 条传讯记录？此操作不可恢复，建议先导出备份。`, "清空", true)) {
        await clearAllMessages();
        showToast("已清空");
        renderArchive();
      }
    });
  }

  // ========== 设置 ==========
  function applyMotion(on) {
    state.reduceMotion = on;
    document.body.classList.toggle("reduce-motion", on);
    const t = $("toggle-motion");
    t.classList.toggle("on", on);
    t.setAttribute("aria-checked", String(on));
  }

  let deferredInstall = null;
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  const isStandalone = () => window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;

  function initSettings() {
    let saved = null;
    try { saved = localStorage.getItem("ta-reduce-motion"); } catch (e) { /* 忽略 */ }
    const systemReduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    applyMotion(saved === null ? systemReduce : saved === "1");

    $("toggle-motion").addEventListener("click", () => {
      applyMotion(!state.reduceMotion);
      try { localStorage.setItem("ta-reduce-motion", state.reduceMotion ? "1" : "0"); } catch (e) { /* 忽略 */ }
    });

    $("btn-edit-names").addEventListener("click", () => showScreen("setup"));
    $("app-version").textContent = "版本 " + APP_VERSION;

    // 安装到桌面
    const installBtn = $("btn-install");
    if (isIOS && !isStandalone()) installBtn.classList.remove("hidden");
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferredInstall = e;
      installBtn.classList.remove("hidden");
    });
    window.addEventListener("appinstalled", () => {
      installBtn.classList.add("hidden");
      showToast("已添加到桌面");
    });
    installBtn.addEventListener("click", async () => {
      if (deferredInstall) {
        deferredInstall.prompt();
        await deferredInstall.userChoice.catch(() => {});
        deferredInstall = null;
        return;
      }
      openModal(`
        <h3 class="modal-title">添加到手机桌面</h3>
        <ol class="install-steps">
          ${isIOS
            ? "<li>用 Safari 打开本页</li><li>点击底部的「分享」按钮</li><li>选择「添加到主屏幕」</li>"
            : "<li>打开浏览器菜单（右上角 ⋮ 或 ≡）</li><li>选择「添加到主屏幕」或「安装应用」</li>"}
        </ol>
        <p class="settings-note">添加后可像 App 一样从桌面打开，断网时也能使用。</p>
        <button type="button" class="btn btn-primary btn-block" data-close>知道了</button>
      `, { label: "添加到手机桌面" });
      $("modal-sheet").querySelector("[data-close]").onclick = closeModal;
    });
  }

  // ========== 分享图 ==========
  const SERIF = '"Noto Serif SC", "Songti SC", "STSong", "SimSun", serif';
  const SANS = '"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif';
  const NO_LINE_START = "，。！？、；：”’」』）》…—,.!?;:)";

  function wrapText(ctx, text, maxWidth) {
    const lines = [];
    String(text).split(/\n/).forEach((para) => {
      let line = "";
      for (const ch of para) {
        const test = line + ch;
        if (ctx.measureText(test).width > maxWidth && line) {
          if (NO_LINE_START.includes(ch)) { // 避头点：标点不出现在行首
            lines.push(test);
            line = "";
          } else {
            lines.push(line);
            line = ch;
          }
        } else {
          line = test;
        }
      }
      if (line) lines.push(line);
    });
    return lines;
  }

  function drawStar(ctx, x, y, r) {
    ctx.beginPath();
    for (let i = 0; i < 8; i++) {
      const rr = i % 2 === 0 ? r : r * 0.3;
      const a = -Math.PI / 2 + (i * Math.PI) / 4;
      ctx.lineTo(x + rr * Math.cos(a), y + rr * Math.sin(a));
    }
    ctx.closePath();
    ctx.fill();
  }

  async function renderShareCanvas(r) {
    try { if (document.fonts && document.fonts.ready) await document.fonts.ready; } catch (e) { /* 忽略 */ }
    const W = 1080, PAD = 110, TEXT_W = W - PAD * 2 - 40;
    const measure = document.createElement("canvas").getContext("2d");
    measure.font = `40px ${SERIF}`;
    const lines = wrapText(measure, r.response, TEXT_W);
    const LINE_H = 74;
    const msgTop = 640;
    const blockH = 90 + lines.length * LINE_H;
    const H = Math.max(1440, msgTop + blockH + 280);
    const msgStart = msgTop + Math.max(0, (H - 280 - msgTop - blockH) / 2); // 文字少时垂直居中

    const canvas = document.createElement("canvas");
    canvas.width = W;
    canvas.height = H;
    const ctx = canvas.getContext("2d");

    // 背景
    const g = ctx.createRadialGradient(W * 0.3, H * 0.15, 50, W * 0.5, H * 0.5, H * 0.9);
    g.addColorStop(0, "#5e2236");
    g.addColorStop(0.55, "#3a1422");
    g.addColorStop(1, "#22090f");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // 双线边框
    ctx.strokeStyle = "rgba(212,175,122,0.75)";
    ctx.lineWidth = 3;
    ctx.strokeRect(44, 44, W - 88, H - 88);
    ctx.strokeStyle = "rgba(212,175,122,0.35)";
    ctx.lineWidth = 1.5;
    ctx.strokeRect(62, 62, W - 124, H - 124);
    ctx.fillStyle = "#d4af7a";
    [[44, 44], [W - 44, 44], [44, H - 44], [W - 44, H - 44]].forEach(([x, y]) => drawStar(ctx, x, y, 16));

    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";

    // 标题
    ctx.fillStyle = "#e8d5b5";
    ctx.font = `600 58px ${SERIF}`;
    ctx.fillText("TA 有话对你说", W / 2, 200);
    ctx.fillStyle = "#b8956a";
    ctx.font = `30px ${SANS}`;
    ctx.fillText(`${r.userName} × ${r.taName}`, W / 2, 256);

    // 分隔
    const lg = ctx.createLinearGradient(PAD, 0, W - PAD, 0);
    lg.addColorStop(0, "rgba(212,175,122,0)");
    lg.addColorStop(0.5, "rgba(212,175,122,0.9)");
    lg.addColorStop(1, "rgba(212,175,122,0)");
    ctx.fillStyle = lg;
    ctx.fillRect(PAD, 300, W - PAD * 2, 2);
    ctx.fillStyle = "#d4af7a";
    drawStar(ctx, W / 2, 301, 14);

    // 牌信息框
    ctx.fillStyle = "rgba(247,240,230,0.07)";
    ctx.strokeStyle = "rgba(212,175,122,0.35)";
    ctx.lineWidth = 2;
    roundRect(ctx, PAD, 350, W - PAD * 2, 220, 24);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#e8d5b5";
    ctx.font = `600 50px ${SERIF}`;
    ctx.fillText(r.cardName, W / 2, 432);
    ctx.fillStyle = "#d4af7a";
    ctx.font = `28px ${SANS}`;
    ctx.fillText(`${r.isReversed ? "逆位" : "正位"} · ${r.themeName || ""}`, W / 2, 482);
    ctx.fillStyle = "rgba(247,240,230,0.7)";
    ctx.font = `26px ${SANS}`;
    const meaningLine = wrapText(ctx, r.cardMeaning || "", W - PAD * 2 - 80)[0] || "";
    ctx.fillText(meaningLine, W / 2, 532);

    // 正文
    ctx.fillStyle = "#b8956a";
    ctx.font = `26px ${SANS}`;
    ctx.fillText("— 来自 TA 的话 —", W / 2, msgStart);
    ctx.fillStyle = "#f7f0e6";
    ctx.font = `40px ${SERIF}`;
    ctx.textAlign = "left";
    let y = msgStart + 90;
    lines.forEach((line) => { ctx.fillText(line, PAD + 20, y); y += LINE_H; });

    // 底部
    ctx.textAlign = "center";
    ctx.fillStyle = "rgba(212,175,122,0.75)";
    ctx.font = `26px ${SANS}`;
    ctx.fillText(formatFullDate(r.createdAt), W / 2, H - 170);
    ctx.fillStyle = "rgba(184,149,106,0.55)";
    ctx.font = `22px ${SANS}`;
    ctx.fillText("象征性角色互动体验 · 仅供娱乐与自我探索", W / 2, H - 120);

    return canvas;
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  async function openShareImage(r) {
    showToast("正在生成图片……");
    let blob;
    try {
      const canvas = await renderShareCanvas(r);
      blob = await new Promise((res, rej) => canvas.toBlob((b) => (b ? res(b) : rej(new Error("toBlob"))), "image/png"));
    } catch (e) {
      showToast("图片生成失败，请重试");
      return;
    }
    hideToast();
    const url = URL.createObjectURL(blob);
    const filename = `ta-message-${r.createdAt}.png`;
    const file = typeof File === "function" ? new File([blob], filename, { type: "image/png" }) : null;
    const canShareFile = !!(file && navigator.canShare && navigator.canShare({ files: [file] }));

    openModal(`
      <h3 class="modal-title">传讯图片</h3>
      <img class="share-image" src="${url}" alt="传讯图片：${esc(r.cardName)}${r.isReversed ? "逆位" : "正位"}" />
      <p class="share-tip">手机上也可以长按图片保存到相册</p>
      <div class="result-actions">
        <div class="result-actions-row">
          <button type="button" class="btn btn-primary" id="share-save">保存图片</button>
          ${canShareFile ? '<button type="button" class="btn btn-ghost" id="share-native">分享</button>' : ""}
        </div>
        <button type="button" class="btn btn-text btn-block" id="share-close">关闭</button>
      </div>
    `, { label: "传讯图片", onClose: () => setTimeout(() => URL.revokeObjectURL(url), 1000) });

    $("share-save").onclick = () => { downloadBlob(blob, filename); showToast("图片已保存"); };
    $("share-close").onclick = closeModal;
    if (canShareFile) {
      $("share-native").onclick = () => navigator.share({ files: [file], title: "TA 有话对你说" }).catch(() => {});
    }
  }

  // ========== 底部导航 / 返回 ==========
  function initNav() {
    document.querySelectorAll(".nav-item").forEach((el) => {
      el.addEventListener("click", () => {
        const s = el.dataset.screen;
        if (s === "theme" && !state.userName) { loadNames(); if (!state.userName) { showScreen("setup"); return; } }
        showScreen(s);
      });
    });
    document.querySelectorAll("[data-back]").forEach((el) => el.addEventListener("click", goBack));
  }

  // ========== Service Worker ==========
  function initServiceWorker() {
    if (!("serviceWorker" in navigator) || location.protocol === "file:") return;
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").then((reg) => {
        const promptUpdate = (worker) => {
          showToast("有新版本可用", {
            duration: 0,
            action: { label: "更新", fn: () => worker.postMessage({ type: "SKIP_WAITING" }) },
          });
        };
        if (reg.waiting && navigator.serviceWorker.controller) promptUpdate(reg.waiting);
        reg.addEventListener("updatefound", () => {
          const nw = reg.installing;
          if (!nw) return;
          nw.addEventListener("statechange", () => {
            if (nw.state === "installed" && navigator.serviceWorker.controller) promptUpdate(nw);
          });
        });
      }).catch((err) => console.warn("SW 注册失败", err));

      let reloading = false;
      navigator.serviceWorker.addEventListener("controllerchange", () => {
        if (reloading) return;
        reloading = true;
        location.reload();
      });
    });
  }

  // ========== 启动 ==========
  async function init() {
    history.replaceState({ screen: "cover" }, "");
    initModal();
    initSettings();
    initSetup();
    initTheme();
    initResult();
    initNav();
    initServiceWorker();
    try {
      await openDB();
    } catch (e) {
      console.warn("IndexedDB 不可用", e);
      showToast("当前浏览器无法保存记录（可能为无痕模式），抽牌仍可使用", { duration: 5000 });
    }
    initArchive();
    initCover();
    loadNames();
    showScreen("cover", { push: false, focus: false });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
