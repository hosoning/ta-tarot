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
  INTENTS,
  intentToTheme,
  THEME_TO_INTENT,
} = require(path.join(dataDir, "intents.js"));
const { getResponse, RESPONSES } = require(path.join(dataDir, "responses.js"));

const namedIntents = (INTENT_IDS || []).filter((id) => id !== "general");
const ALL_INTENTS = INTENT_IDS || namedIntents.concat("general");

const DODGE = ["换个角度", "有点难", "看不清", "超出了", "这个问题有点难", "标准答案", "本身就已经有意义"];
const BUSY_HINTS = ["忙", "顾不过来", "顾此失彼", "乱", "转不过来", "手忙脚乱", "失衡", "腾不出", "空", "事务", "没空", "有空"];
const TIRED_HINTS = ["累", "乏", "熬", "撑", "歇", "疲惫", "困乏"];
const SICK_HINTS = ["病", "不舒服", "身子", "生病", "恙", "欠安", "身体"];
const EAT_HINTS = ["吃", "饭", "餐", "用餐"];
const LOVE_HINTS = ["爱"];

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

function cellTexts(cell) {
  return (cell || [])
    .map((item) => (typeof item === "string" ? item : item && item.text))
    .filter(Boolean);
}

// ---------- intent inventory ----------
ok("named intent groups >= 68", namedIntents.length >= 68, `got ${namedIntents.length}`);
ok("INTENTS entries match named groups", INTENTS.length === namedIntents.length, `${INTENTS.length} vs ${namedIntents.length}`);
const kwCounts = INTENTS.map((i) => (i.keywords || []).length);
ok("every named intent has keywords", kwCounts.every((n) => n > 0));
ok("keyword lists are generous (min >= 15)", Math.min(...kwCounts) >= 15, `min=${Math.min(...kwCounts)}`);

// ---------- classifyQuestion ----------
const classifyCases = [
  ["你忙吗", "busy"],
  ["忙不忙", "busy"],
  ["有空吗", "busy"],
  ["忙嗎", "busy"],
  ["你忙不忙", "busy"],
  ["有没有空", "busy"],
  ["闲吗", "busy"],
  ["工作忙吗", "busy"],
  ["你累吗", "tired"],
  ["累不累", "tired"],
  ["累嗎", "tired"],
  ["累吗", "tired"],
  ["是不是累坏了", "tired"],
  ["生病了吗", "sick"],
  ["生病了嗎", "sick"],
  ["是不是病了", "sick"],
  ["不舒服", "sick"],
  ["病了", "sick"],
  ["感冒了吗", "cold"],
  ["发烧了吗", "cold"],
  ["吃饭了吗", "eat"],
  ["吃飯了嗎", "eat"],
  ["吃了吗", "eat"],
  ["饿不饿", "hungry"],
  ["喝水了吗", "drink"],
  ["喝多了吗", "drunk"],
  ["醉了吗", "drunk"],
  ["到家了吗", "home"],
  ["到家没", "home"],
  ["出门了吗", "outside"],
  ["冷不冷", "coldfeel"],
  ["带伞了吗", "rain"],
  ["加班吗", "work"],
  ["工作顺利吗", "work"],
  ["作业做了吗", "study"],
  ["想我吗", "miss"],
  ["想不想我", "miss"],
  ["喜欢我吗", "like"],
  ["喜欢别人吗", "other"],
  ["爱我吗", "love"],
  ["愛我嗎", "love"],
  ["会找我吗", "contact"],
  ["为什么不回", "ignore"],
  ["为什么不理我", "ignore"],
  ["为什么没接电话", "missedcall"],
  ["你还好吗", "mood"],
  ["是不是哭了", "cry"],
  ["生我气了吗", "angry"],
  ["难过吗", "sad"],
  ["孤单吗", "lonely"],
  ["无聊吗", "bored"],
  ["压力大吗", "stress"],
  ["想见我吗", "meet"],
  ["出来吗", "meet"],
  ["会不会离开", "stay"],
  ["还在吗", "stay"],
  ["还想前任吗", "ex"],
  ["会吃醋吗", "jealous"],
  ["还记得我吗", "remember"],
  ["会不会忘了我", "forget"],
  ["我们会怎样", "future"],
  ["在干什么", "doing"],
  ["在想什么", "think"],
  ["你在哪", "where"],
  ["安慰我", "comfort"],
  ["我好累", "comfort"],
  ["陪陪我", "companionship"],
  ["我们的关系怎么样", "relationship"],
  ["想知道你喜欢我吗", "like"],
  ["我该不该道歉", "sorry"],
  ["能原谅我吗", "forgive"],
  ["后悔吗", "regret"],
  ["你变了吗", "changed"],
  ["有没有骗我", "lie"],
  ["还信我吗", "trust"],
  ["有事瞒着我吗", "secret"],
  ["要我等你吗", "wait"],
  ["还会回来吗", "comeback"],
  ["要分手吗", "breakup"],
  ["能不能和好", "makeup"],
  ["离得远吗", "distance"],
  ["想认真吗", "serious"],
  ["起床了吗", "morning"],
  ["怎么还没睡", "latenight"],
  ["梦见我了吗", "dream"],
  ["钱够吗", "money"],
  ["家里还好吗", "family"],
  ["跟朋友出去了吗", "friends"],
  ["周末有空吗", "plans"],
  ["记得生日吗", "birthday"],
  ["想要什么", "gift"],
  ["在打游戏吗", "game"],
  ["还要多久", "late"],
  ["在担心我吗", "worry"],
  ["会支持我吗", "support"],
  ["在做饭吗", "cook"],
  ["吃的什么", "cook"],
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
ok("intentToTheme(tired) is free", intentToTheme("tired") === "free");
ok("intentToTheme(love) is relationship", intentToTheme("love") === "relationship");
ok("intentToTheme(forgive) is comfort", intentToTheme("forgive") === "comfort");
ok("THEME_TO_INTENT.date is meet", THEME_TO_INTENT.date === "meet");
ok("THEME_TO_INTENT.missing is miss", THEME_TO_INTENT.missing === "miss");

// ---------- topic answers on required examples ----------
function expectTopic(label, themeId, card, reversed, tone, question, hints) {
  let text = null;
  let threw = false;
  try {
    text = getResponse(themeId, card, reversed, tone, question);
  } catch (e) {
    threw = true;
    failures.push(`${label} threw: ${e.message}`);
    failed++;
    return null;
  }
  ok(`${label} non-empty`, !threw && typeof text === "string" && text.length > 0);
  const dodgeHit = DODGE.filter((d) => text && text.includes(d));
  ok(`${label} not a dodge`, dodgeHit.length === 0, dodgeHit.join(",") + " | " + text);
  const hit = hints.some((h) => text && text.includes(h));
  ok(`${label} talks about the topic`, hit, text);
  return text;
}

const p2 = cardById("pentacles-2");
const s9 = cardById("swords-9");
const c4 = cardById("cups-4");
const p3 = cardById("pentacles-3");
const m6 = cardById("major-6");
ok("required cards exist", !!(p2 && s9 && c4 && p3 && m6));

for (const tone of ["gentle", "direct", "playful", "quiet", "restrained"]) {
  expectTopic(`pentacles-2 reversed busy (${tone})`, "free", p2, true, tone, "你忙吗", BUSY_HINTS);
}

const tiredSample = expectTopic("swords-9 reversed tired", "free", s9, true, "gentle", "你累吗", TIRED_HINTS);
const sickSample = expectTopic("cups-4 upright sick", "free", c4, false, "gentle", "生病了吗", SICK_HINTS);
const eatSample = expectTopic("pentacles-3 upright eat", "free", p3, false, "gentle", "吃饭了吗", EAT_HINTS);
const loveSample = expectTopic("major-6 upright love", "free", m6, false, "gentle", "爱我吗", LOVE_HINTS);

// Several cards for tired / sick / busy, unique paragraphs
const topicGrid = [
  ["tired", "你累吗", TIRED_HINTS],
  ["sick", "生病了吗", SICK_HINTS],
  ["busy", "你忙吗", BUSY_HINTS],
];
const topicCards = ["major-0", "major-13", "wands-10", "cups-4", "swords-9", "pentacles-2", "pentacles-3", "major-6"];
for (const [intent, question, hints] of topicGrid) {
  const seen = new Set();
  for (const id of topicCards) {
    const card = cardById(id);
    for (const rev of [false, true]) {
      const text = expectTopic(`${intent} ${id} ${rev ? "rev" : "up"}`, "free", card, rev, "direct", question, hints);
      if (text) {
        const key = text;
        ok(`${intent} unique across sample cards`, !seen.has(key), `duplicate: ${id} ${text.slice(0, 40)}`);
        seen.add(key);
      }
    }
  }
}

// ---------- coverage: every card × ori × intent has >= 1 answer ----------
ok("78 cards loaded", TAROT_CARDS.length === 78);
for (const card of TAROT_CARDS) {
  const block = RESPONSES[card.id];
  ok(`RESPONSES has ${card.id}`, !!block, "missing card");
  if (!block) continue;
  for (const ori of ["upright", "reversed"]) {
    ok(`${card.id} has ${ori}`, !!block[ori]);
    if (!block[ori]) continue;
    for (const intent of ALL_INTENTS) {
      const texts = cellTexts(block[ori][intent]);
      ok(
        `${card.id}/${ori}/${intent} has >= 1 answer`,
        texts.length >= 1,
        `got ${texts.length}`
      );
    }
  }
}

// ---------- uniqueness of full answers across cards (same intent+ori) ----------
for (const ori of ["upright", "reversed"]) {
  for (const intent of ALL_INTENTS) {
    const seen = new Map();
    for (const card of TAROT_CARDS) {
      const cell = RESPONSES[card.id] && RESPONSES[card.id][ori] && RESPONSES[card.id][ori][intent];
      if (!cell) continue;
      for (const text of cellTexts(cell)) {
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
const questions = ["你忙吗", "你累吗", "生病了吗", "吃饭了吗", "爱我吗", "想我吗", "会找我吗", "我们会怎样", "今天天气", ""];
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
const tiredViaMissing = getResponse("missing", s9, true, "gentle", "你累吗");
ok(
  "typed 你累吗 beats theme missing",
  TIRED_HINTS.some((h) => tiredViaMissing.includes(h)),
  tiredViaMissing
);

// ---------- report ----------
console.log(`named_intents=${namedIntents.length} total_ids=${ALL_INTENTS.length}`);
console.log(`keyword_min=${Math.min(...kwCounts)} keyword_max=${Math.max(...kwCounts)}`);
console.log(`passed=${passed} failed=${failed}`);
if (failures.length) {
  console.log("failures:");
  for (const f of failures.slice(0, 80)) console.log(" -", f);
  if (failures.length > 80) console.log(` - ... ${failures.length - 80} more`);
}
process.exit(failed ? 1 : 0);
