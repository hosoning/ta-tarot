#!/usr/bin/env node
/**
 * Node tests for the intent classifier and response database.
 * Run: node tools/test-responses.js
 */
const path = require("path");
const dataDir = path.join(__dirname, "..", "data");

const { TAROT_CARDS } = require(path.join(dataDir, "tarot-cards.js"));
const {
  classifyQuestion,
  INTENT_IDS,
  intentToTheme,
  THEME_TO_INTENT,
} = require(path.join(dataDir, "intents.js"));
const { getResponse, RESPONSES } = require(path.join(dataDir, "responses.js"));

const INTENTS = INTENT_IDS || [
  "busy", "miss", "like", "contact", "mood", "meet", "stay", "other",
  "angry", "remember", "future", "doing", "comfort", "communication",
  "companionship", "relationship", "general",
];

const DODGE = ["换个角度", "有点难", "看不清", "超出了", "这个问题有点难", "标准答案", "本身就已经有意义"];
const BUSY_HINTS = ["忙", "顾不过来", "顾此失彼", "乱", "转不过来", "手忙脚乱", "失衡", "腾不出", "空"];

let passed = 0;
let failed = 0;
const failures = [];

function ok(name, cond, detail) {
  if (cond) {
    passed++;
  } else {
    failed++;
    failures.push(detail ? `${name}: ${detail}` : name);
  }
}

function cardById(id) {
  return TAROT_CARDS.find((c) => c.id === id);
}

// ---------- classifyQuestion ----------
const classifyCases = [
  ["你忙吗", "busy"],
  ["忙不忙", "busy"],
  ["有空吗", "busy"],
  ["忙嗎", "busy"],
  ["你忙不忙", "busy"],
  ["有没有空", "busy"],
  ["闲吗", "busy"],
  ["想我吗", "miss"],
  ["想不想我", "miss"],
  ["在想什么", "doing"],
  ["想见我吗", "meet"],
  ["会找我吗", "contact"],
  ["喜欢我吗", "like"],
  ["喜欢别人吗", "other"],
  ["你还好吗", "mood"],
  ["我们会怎样", "future"],
  ["会不会离开", "stay"],
  ["还记得我吗", "remember"],
  ["生我气了吗", "angry"],
  ["在干什么", "doing"],
  ["安慰我", "comfort"],
  ["我好累", "comfort"],
  ["陪陪我", "companionship"],
  ["我们的关系怎么样", "relationship"],
  ["想知道你喜欢我吗", "like"],
  ["为什么不回", "contact"],
  ["还在吗", "stay"],
  ["出来吗", "meet"],
  ["怎么样", "general"],
  ["我们", "general"],
  ["想", "general"],
  ["说", "general"],
  ["", "general"],
];
for (const [q, expect] of classifyCases) {
  const got = classifyQuestion(q);
  ok(`classify("${q}") === ${expect}`, got === expect, `got ${got}`);
}

ok("intentToTheme(miss) is missing", intentToTheme("miss") === "missing");
ok("intentToTheme(busy) is free", intentToTheme("busy") === "free");
ok("THEME_TO_INTENT.date is meet", THEME_TO_INTENT.date === "meet");
ok("THEME_TO_INTENT.missing is miss", THEME_TO_INTENT.missing === "miss");

// ---------- pentacles-2 reversed + 你忙吗 ----------
const p2 = cardById("pentacles-2");
ok("pentacles-2 exists", !!p2);

for (const tone of ["gentle", "direct", "playful", "quiet", "restrained"]) {
  let text = null;
  let threw = false;
  try {
    text = getResponse("free", p2, true, tone, "你忙吗");
  } catch (e) {
    threw = true;
    failures.push(`getResponse pentacles-2 / ${tone} threw: ${e.message}`);
    failed++;
    continue;
  }
  ok(`pentacles-2 reversed busy (${tone}) non-empty`, !threw && typeof text === "string" && text.length > 0);
  const dodgeHit = DODGE.filter((d) => text && text.includes(d));
  ok(`pentacles-2 reversed busy (${tone}) not a dodge`, dodgeHit.length === 0, dodgeHit.join(",") + " | " + text);
  const busyHit = BUSY_HINTS.some((h) => text && text.includes(h));
  ok(`pentacles-2 reversed busy (${tone}) talks about being busy`, busyHit, text);
}

// ---------- coverage: every card × ori × intent has >= 2 answers ----------
ok("78 cards loaded", TAROT_CARDS.length === 78);
for (const card of TAROT_CARDS) {
  const block = RESPONSES[card.id];
  ok(`RESPONSES has ${card.id}`, !!block, "missing card");
  if (!block) continue;
  for (const ori of ["upright", "reversed"]) {
    ok(`${card.id} has ${ori}`, !!block[ori]);
    if (!block[ori]) continue;
    for (const intent of INTENTS) {
      const cell = block[ori][intent];
      const texts = (cell || [])
        .map((item) => (typeof item === "string" ? item : item && item.text))
        .filter(Boolean);
      ok(
        `${card.id}/${ori}/${intent} has >= 2 answers`,
        texts.length >= 2,
        `got ${texts.length}`
      );
    }
  }
}

// ---------- uniqueness of full answers across cards (same intent+ori) ----------
for (const ori of ["upright", "reversed"]) {
  for (const intent of INTENTS) {
    const seen = new Map();
    for (const card of TAROT_CARDS) {
      const cell = RESPONSES[card.id] && RESPONSES[card.id][ori] && RESPONSES[card.id][ori][intent];
      if (!cell) continue;
      for (const item of cell) {
        const text = typeof item === "string" ? item : item && item.text;
        if (!text) continue;
        if (seen.has(text) && seen.get(text) !== card.id) {
          ok(
            `unique ${intent}/${ori}`,
            false,
            `duplicate between ${seen.get(text)} and ${card.id}: ${text.slice(0, 40)}`
          );
        } else {
          seen.set(text, card.id);
        }
      }
    }
  }
}

// ---------- no-keyword / general answers for several cards both ways ----------
const sampleIds = [
  "major-0", "major-13", "major-16", "major-18", "major-21",
  "wands-10", "cups-2", "cups-5", "swords-8", "swords-9",
  "pentacles-2", "pentacles-8",
];
const noKeywordQs = ["嗯", "你好", "随便问问", "……", ""];
for (const id of sampleIds) {
  const card = cardById(id);
  for (const rev of [false, true]) {
    for (const q of noKeywordQs) {
      let text = "";
      let threw = false;
      try {
        text = getResponse("free", card, rev, "gentle", q);
      } catch (e) {
        threw = true;
        failures.push(`general ${id} ${rev} "${q}" threw: ${e.message}`);
        failed++;
        continue;
      }
      ok(`general ${id} ${rev ? "rev" : "up"} q="${q}" non-empty`, !threw && text && text.length > 0);
      const dodgeHit = DODGE.filter((d) => text && text.includes(d));
      ok(`general ${id} ${rev ? "rev" : "up"} q="${q}" not a dodge`, dodgeHit.length === 0, (dodgeHit.join(",") + " | " + text).slice(0, 120));
    }
  }
}

// ---------- getResponse never throws over a grid of inputs ----------
const tones = ["gentle", "direct", "playful", "quiet", "restrained", "", undefined];
const questions = ["你忙吗", "想我吗", "会找我吗", "喜欢我吗", "我们会怎样", "今天天气", ""];
let throwCount = 0;
for (const card of TAROT_CARDS) {
  for (const rev of [false, true]) {
    for (const tone of tones) {
      for (const q of questions) {
        try {
          const text = getResponse("free", card, rev, tone, q);
          if (typeof text !== "string" || !text.length) {
            ok("getResponse returns string", false, `${card.id} ${tone} ${q}`);
          }
        } catch (e) {
          throwCount++;
          if (throwCount <= 5) failures.push(`throw ${card.id} ${tone} ${q}: ${e.message}`);
        }
      }
    }
  }
}
ok("getResponse never throws on the sample grid", throwCount === 0, `${throwCount} throws`);

// ---------- theme-only path (no question text) still answers ----------
const themeMap = [
  ["missing", "miss"],
  ["date", "meet"],
  ["future", "future"],
  ["free", "general"],
];
for (const [themeId] of themeMap) {
  const text = getResponse(themeId, p2, true, "gentle", "");
  ok(`theme-only ${themeId} non-empty`, !!(text && text.length));
  const dodgeHit = DODGE.filter((d) => text && text.includes(d));
  ok(`theme-only ${themeId} not a dodge`, dodgeHit.length === 0, text);
}

// ---------- fine intent beats UI theme ----------
const busyViaMissing = getResponse("missing", p2, true, "direct", "你忙吗");
ok(
  "typed 你忙吗 beats theme missing",
  BUSY_HINTS.some((h) => busyViaMissing.includes(h)),
  busyViaMissing
);

// ---------- report ----------
console.log(`passed=${passed} failed=${failed}`);
if (failures.length) {
  console.log("failures:");
  for (const f of failures.slice(0, 60)) console.log(" -", f);
  if (failures.length > 60) console.log(` - ... ${failures.length - 60} more`);
}
process.exit(failed ? 1 : 0);
