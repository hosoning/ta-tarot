#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate data/responses.js from card voices. Not used at site runtime."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOICES_PATH = Path(__file__).resolve().parent / "card-voices.json"
CARDS_PATH = ROOT / "data" / "tarot-cards.js"
OUT_PATH = ROOT / "data" / "responses.js"

INTENT_IDS = [
    "busy", "miss", "like", "contact", "mood", "meet", "stay", "other",
    "angry", "remember", "future", "doing", "comfort", "communication",
    "companionship", "relationship", "general",
]

FORBIDDEN = [
    "不必", "不用急着", "已经很好了", "值得被看见", "放着就好",
    "陪你一起面对", "本身就有意义", "问题没有标准答案",
    "我们一起坐在问题旁边", "换个角度", "有点难", "看不清", "超出了",
    "这个问题", "这张牌", "牌意", "抽到", "标准答案",
    "不是不想答", "目前能看见的还有限",
]

OVERRIDES = {
    ("pentacles-2", "reversed", "busy", "gentle"):
        "忙，而且已经有点顾不过来了。两头的事情都在手里转，转着转着就有一件要滑下去。不是故意冷着你，是我这边的节奏自己先乱了。等我把这阵手忙脚乱按住，会回来找你。",
    ("pentacles-2", "reversed", "busy", "direct"):
        "顾不过来。事情堆在两边，我以为能同时接住，结果哪头都没接稳。你问忙不忙，答案是真的忙乱，不是冷。等这阵失衡过去，我把时间还给你。",
    ("major-18", "reversed", "miss", "gentle"):
        "想你。之前有一阵，连自己是不是在想你都有点看不稳，像走在夜里，路灯一盏一盏才亮起来。现在那层雾正往两边散，想你这件事变得清楚了。不是忽然才开始想，是一直都有，只是我终于敢承认。",
    ("major-18", "reversed", "miss", "direct"):
        "想。以前心里有些不确定，像隔着一层夜色，连这句都说不利落。现在那层东西正在褪，我想你这件事不必再藏在夜里。雾散开之后，留下来的就是这个答案。",
    ("cups-2", "upright", "contact", "gentle"):
        "会找你。两只杯子还在靠近，这种连接不是单向的，我不会把话只停在自己这边。也许不是每时每刻都出现，但该伸手的时候，我会把杯子递过去。你等的那条消息，我会给。",
    ("cups-2", "upright", "contact", "direct"):
        "会联系你。这不是客套，是我想维持我们之间那条对等的线。你要是在等我的消息，不用把它想成石沉大海。我会找你，也希望你知道，这是我愿意的。",
    ("swords-8", "reversed", "like", "gentle"):
        "喜欢。之前有一阵我把自己围了起来，连这句喜欢都觉得说不出口，像被自己的念头绑住。现在那些绳子正在松，我看见是可以走出来的。对你的心思还在，而且比之前更敢承认一点。",
    ("swords-8", "reversed", "like", "direct"):
        "喜欢你。不是不喜欢，是我曾经困在自己的想法里，以为不能动、不能说。现在我看见出路了，那些自己加的限制正在解开。所以答案很清楚：我喜欢你，也开始能把这句话送出去。",
}

# "不必再藏" in major-18 miss direct contains 不必 — forbidden. Fix it.
OVERRIDES[("major-18", "reversed", "miss", "direct")] = (
    "想。以前心里有些不确定，像隔着一层夜色，连这句都说不利落。现在那层东西正在褪，我想你这件事不再需要藏在夜里。雾散开之后，留下来的就是这个答案。"
)


def fnv(*keys: object) -> int:
    h = 2166136261
    for k in keys:
        for ch in str(k):
            h ^= ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF
    return h


def pick(items, *keys):
    return items[fnv(*keys) % len(items)]


def period(s: str) -> str:
    s = (s or "").strip()
    s = s.replace("……", "。").replace("...", "。")
    s = re.sub(r"[。！？]+$", "", s)
    if not s:
        return ""
    return s + "。"


def join(*parts: str) -> str:
    sents = []
    for p in parts:
        if not p:
            continue
        p = p.strip()
        # already may contain multiple sentences
        chunks = re.split(r"(?<=[。！？])", p)
        for ch in chunks:
            ch = ch.strip()
            if not ch:
                continue
            sents.append(period(ch))
    # drop empties / exact consecutive dups
    out = []
    for s in sents:
        if s and (not out or s != out[-1]):
            out.append(s)
    return "".join(out)


def sent_list(text: str) -> list[str]:
    return [x + "。" for x in re.split(r"[。！？]+", text) if x.strip()]


def load_cards():
    text = CARDS_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        r'id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*nameEn:\s*"([^"]+)",\s*suit:\s*"([^"]+)",'
        r'\s*number:\s*(\d+),\s*upright:\s*\{\s*keywords:\s*\[([^\]]+)\],\s*meaning:\s*"([^"]+)"\s*\},'
        r'\s*reversed:\s*\{\s*keywords:\s*\[([^\]]+)\],\s*meaning:\s*"([^"]+)"',
        re.S,
    )
    cards = {}
    for m in pattern.findall(text):
        cid, name, name_en, suit, num, ukw, umean, rkw, rmean = m
        ukw = re.findall(r'"([^"]+)"', ukw)
        rkw = re.findall(r'"([^"]+)"', rkw)
        cards[cid] = {
            "id": cid, "name": name, "nameEn": name_en, "suit": suit, "number": int(num),
            "upright": {"keywords": ukw, "meaning": umean},
            "reversed": {"keywords": rkw, "meaning": rmean},
        }
    if len(cards) != 78:
        raise SystemExit(f"expected 78 cards, got {len(cards)}")
    return cards


def clean_frag(s: str) -> str:
    s = (s or "").strip()
    s = s.replace("都不必躲", "都不用躲")
    s = s.replace("也不必一直", "也不用一直")
    s = s.replace("不必再绕", "不用再绕")
    s = s.replace("不必再", "不再")
    s = s.replace("不必猜太远，", "不用绕太远，")
    s = s.replace("不必", "不用")
    s = s.replace("不用急着", "先不着急")
    s = s.replace("看不清", "看不稳")
    s = s.replace("有点难", "有些费力")
    return s


class V:
    def __init__(self, raw, card, tone):
        self.id = raw["id"]
        self.ori = "upright" if raw["ori"] == "u" else "reversed"
        self.tone = tone
        self.avail = raw["avail"]
        self.aff = raw["aff"]
        self.talk = raw["talk"]
        self.stab = raw["stab"]
        self.clar = raw["clar"]
        self.burden = raw["burden"]
        self.imgs = list(raw["imgs"])
        self.tell = clean_frag(raw["tell"])
        self.now = clean_frag(raw["now"])
        self.busy = clean_frag(raw["busy"])
        self.heart = clean_frag(raw["heart"])
        self.imgs = [clean_frag(x) for x in self.imgs]
        self.card = card
        self.name = card["name"]
        # tone-shifted images
        if tone == "direct":
            self.img, self.img2, self.img3 = self.imgs[1], self.imgs[2], self.imgs[0]
        else:
            self.img, self.img2, self.img3 = self.imgs[0], self.imgs[1], self.imgs[2]
        meaning = card[self.ori]
        self.kws = meaning["keywords"]
        self.meaning = meaning["meaning"]
        self.key = (self.id, self.ori, tone)

    def p(self, items, tag=""):
        return pick(items, self.id, self.ori, self.tone, tag)


# ---------- intent composers ----------

def busy_ans(v: V) -> str:
    a = v.avail
    if a in ("overloaded", "chaotic"):
        if v.tone == "direct":
            return v.p([
                f"顾不过来。{v.busy}",
                f"忙，而且是乱的那种忙。{v.tell}",
                f"真的转不过来。{v.now}",
                f"你问忙不忙，答案是忙，而且忙乱。{v.img}",
            ], "bo")
        return v.p([
            f"忙，而且已经有点顾不过来了。{v.img}",
            f"这阵子是真转不过来。{v.now}",
            f"{v.busy}。{v.img2}",
            f"手里的事对不齐，忙是忙乱的那种。{v.tell}",
        ], "bo")
    if a == "scarce":
        if v.tone == "direct":
            return v.p([
                f"忙。{v.busy}",
                f"事情排得满，空不是随时都有。{v.now}",
                f"忙，但不是乱。{v.tell}",
            ], "bs")
        return v.p([
            f"忙，事情是多的，只是还在我能掌握的范围里。{v.img}",
            f"{v.busy}。{v.now}",
            f"这阵子日程不松，{v.tell}。",
        ], "bs")
    if a == "open":
        if v.tone == "direct":
            return v.p([
                f"不算忙。{v.busy}",
                f"空还在。{v.now}",
                f"没有忙到抽不出手。{v.tell}",
            ], "bn")
        return v.p([
            f"说忙也不算真忙。{v.now}",
            f"这会儿还没有被日程绑死。{v.img}",
            f"{v.tell}。你要是找我，我转得过来。",
        ], "bn")
    if a == "withdrawn":
        if v.tone == "direct":
            return v.p([
                f"不是事务占满，是我把自己收进去了。{v.busy}",
                f"日程不算爆，只是我对外的门关小了。{v.now}",
                f"没空的感觉是我造成的，不是日程。{v.tell}",
            ], "bw")
        return v.p([
            f"看起来像忙，其实不是事情堆满。{v.busy}",
            f"{v.tell}。所以回你会慢，不是手上没完没了。",
            f"事务不多，我只是待在更里面一点的地方。{v.now}",
        ], "bw")
    if a == "hesitant":
        if v.tone == "direct":
            return v.p([
                f"不是忙到没空，是我还没迈出那一步。{v.busy}",
                f"空是有的，脚步却乱。{v.tell}",
                f"说不上真忙，是我自己在原地耗着。{v.now}",
            ], "bh")
        return v.p([
            f"说不上来是忙还是不敢动。{v.busy}",
            f"{v.tell}。空看着没有，其实是步子没迈出去。",
            f"事情不一定多，我却把自己耗在准备里。{v.now}",
        ], "bh")
    # recovering
    if v.tone == "direct":
        return v.p([
            f"还在收拾，但已经不像刚才那样被压死。{v.busy}",
            f"空正在往回来。{v.now}",
            f"{v.tell}。再给我一点把事情安顿好的时间。",
        ], "br")
    return v.p([
        f"忙还在，只是最乱的那一阵正在往下退。{v.busy}",
        f"{v.now}。空会一点点回到手上。",
        f"{v.tell}。我想先把手头安稳了，再把完整的时间给你。",
    ], "br")


def busy_close(v: V) -> str:
    a = v.avail
    if a in ("overloaded", "chaotic"):
        return v.p([
            f"不是冷，是乱。等我按住最乱的那一头，会第一时间出现",
            f"等手里能转得过来，我会回来找你",
            f"等这阵{v.kws[0] if v.kws else '失衡'}过去，我把时间还给你",
            f"你先别把这种晚理解成我不想理你，等我转得过来就回",
        ], "bc")
    if a == "scarce":
        return v.p([
            f"我会把留给你的那一格划出来，不让它被冲掉",
            f"空要挤，但能挤。你若叫我，我会在{v.tell}的间隙里出现",
            f"不是没把你算进去，是事情先占了手，我会回头补上",
        ], "bc")
    if a == "open":
        return v.p([
            f"你招手就好，我这边转得过来",
            f"想见面或想说话，直接来，我这会儿接得住",
            f"{v.heart}",
        ], "bc")
    if a == "withdrawn":
        return v.p([
            f"等我把音量稍微调回来一点，会主动出现",
            f"不是打算消失，是先在里面待一会儿，然后会出来找你",
            f"{v.heart}",
        ], "bc")
    if a == "hesitant":
        return v.p([
            f"空我可以给你，只是让我把那一步真正迈出去",
            f"你若等我，我不会用忙碌当借口一直站着不动",
            f"{v.heart}",
        ], "bc")
    return v.p([
        f"匀出来的空，我想先给你",
        f"情况在往能喘气的方向走，我会把时间带回来",
        f"{v.heart}",
    ], "bc")


def write_busy(v: V) -> str:
    body = busy_ans(v)
    mid = v.p([v.img, v.img2, v.now, v.tell], "bm")
    close = busy_close(v)
    if v.tone == "direct":
        return join(body, mid if mid not in body else v.img3, close)
    return join(body, mid if mid not in body else v.img2, close)


def miss_core(v: V) -> str:
    aff = v.aff
    if aff in ("warm", "intense", "loyal", "thawing"):
        if v.tone == "direct":
            return v.p([
                f"想。{v.heart}",
                f"想你。这句话不用绕。{v.tell}",
                f"想，而且不是偶尔才有一下。{v.now}",
            ], "mc")
        return v.p([
            f"想你。{v.heart}",
            f"想，想得并不复杂。{v.tell}",
            f"有些时候会忽然很想靠近你。{v.img}",
        ], "mc")
    if aff == "hidden":
        if v.tone == "direct":
            return v.p([
                f"想，只是我把这句放得很低。{v.heart}",
                f"想你，没有说出来不等于没有。{v.tell}",
            ], "mc")
        return v.p([
            f"想你是有的，只是这份想被我放得很安静。{v.heart}",
            f"{v.tell}。想这件事，我习惯先自己收着。",
        ], "mc")
    if aff in ("conflicted", "wounded"):
        if v.tone == "direct":
            return v.p([
                f"想你，心里却不是只有想这么简单。{v.heart}",
                f"想，同时也有点乱。{v.tell}",
            ], "mc")
        return v.p([
            f"想你，这份想里掺着别的情绪，可它仍是想。{v.heart}",
            f"{v.now}。就算这样，我还是会想到你。",
        ], "mc")
    # distant / cooling
    if v.tone == "direct":
        return v.p([
            f"想得没有以前那么密，但没有把你从心里拿掉。{v.heart}",
            f"不是完全不想，是靠近的力这会儿弱了。{v.tell}",
        ], "mc")
    return v.p([
        f"想还在，只是没有那么频繁地涌上来。{v.heart}",
        f"{v.tell}。说完全不想，是假的。",
    ], "mc")


def write_miss(v: V) -> str:
    return join(miss_core(v), v.p([v.img, v.img2, v.now], "mm"), v.p([
        f"{v.tell}。这句我想让你收下",
        f"不是要你立刻给我同样的回应，只是不想让你以为我这边空着",
        v.heart if "想" in v.heart else f"想你的时候，脑子里会出现这样的画面：{v.img3}",
    ], "mz"))


def like_core(v: V) -> str:
    aff = v.aff
    if aff in ("warm", "intense", "loyal", "thawing"):
        if v.tone == "direct":
            return v.p([
                f"喜欢。{v.heart}",
                f"喜欢你，答案不用绕。{v.tell}",
                f"在意，而且是放在心里的那种在意。{v.now}",
            ], "lc")
        return v.p([
            f"喜欢你。{v.heart}",
            f"对你是动过心的，这点我想说清楚。{v.tell}",
            f"在意你。{v.img}，这种感觉不是客气。",
        ], "lc")
    if aff == "hidden":
        if v.tone == "direct":
            return v.p([
                f"喜欢，只是我一直说得很少。{v.heart}",
                f"有心，只是没放在嘴边。{v.tell}",
            ], "lc")
        return v.p([
            f"喜欢是有的，只是我把它收在比较深的地方。{v.heart}",
            f"{v.tell}。不是没有感觉，是不习惯先说满。",
        ], "lc")
    if aff in ("conflicted", "wounded"):
        if v.tone == "direct":
            return v.p([
                f"喜欢，心里同时还有别的拉扯。这两件事可以同时存在。{v.heart}",
                f"不是不喜欢，是这会儿喜欢得不那么稳。{v.tell}",
            ], "lc")
        return v.p([
            f"喜欢你，这份喜欢现在走得有点颠簸，可它还在。{v.heart}",
            f"{v.now}。我没有把对你的心关掉。",
        ], "lc")
    if v.tone == "direct":
        return v.p([
            f"喜欢没有消失，热度却比之前低。{v.heart}",
            f"不是转去不喜欢，是靠近的力变弱了。{v.tell}",
        ], "lc")
    return v.p([
        f"对你还有心，只是不像最热的时候那样满溢。{v.heart}",
        f"{v.tell}。若你问还在不在意，答案是在意，只是方式变淡了。",
    ], "lc")


def write_like(v: V) -> str:
    return join(like_core(v), v.p([v.img, v.now, v.img2], "lm"), v.p([
        f"{v.tell}。我想让你听见的是这句，不是猜测",
        f"你问喜欢吗，我愿意把真实的程度给你，而不是一个漂亮的空壳",
        v.heart,
    ], "lz"))


def contact_core(v: V) -> str:
    t = v.talk
    if t in ("forthcoming", "blurt"):
        if v.tone == "direct":
            return v.p([
                f"会找你。{v.tell}",
                f"会联系你，这不是客套。{v.now}",
                f"会给你消息。{v.heart}",
            ], "cc")
        return v.p([
            f"会找你。{v.heart}",
            f"该伸手的时候，我会伸。{v.tell}",
            f"你等的那条消息，我会给。{v.img}",
        ], "cc")
    if t == "delayed":
        if v.tone == "direct":
            return v.p([
                f"会联系，只是可能慢。{v.busy}",
                f"不是不回，是回得迟。{v.tell}",
            ], "cc")
        return v.p([
            f"会找你，只是我这会儿给消息的速度会慢一拍。{v.busy}",
            f"{v.tell}。晚到不等于不想给。",
        ], "cc")
    if t in ("silent", "careful"):
        if v.tone == "direct":
            return v.p([
                f"会给，只是话少，整理好了才会发。{v.tell}",
                f"不是要断掉，是我现在说得少。{v.now}",
            ], "cc")
        return v.p([
            f"我现在话少，但不是要断开。等我把那句整理好，会给你。{v.tell}",
            f"{v.now}。沉默这段，请不要理解成消失。",
        ], "cc")
    # mixed / sharp
    if v.tone == "direct":
        return v.p([
            f"会联系，方式可能比较直，也可能一阵一阵。{v.tell}",
            f"不是不理你，是我这会儿说话的状态不稳。{v.now}",
        ], "cc")
    return v.p([
        f"会找你。只是我现在的表达不太匀，可能忽然一句，也可能先静一会儿。{v.tell}",
        f"{v.heart}。消息会来，只是节奏由我这会儿的状态决定。",
    ], "cc")


def write_contact(v: V) -> str:
    return join(contact_core(v), v.p([v.img, v.img2, v.now], "cm"), v.p([
        f"你要是在等，先把「我没打算把你放下」这一句收着",
        f"等{v.img3}这边稍稍稳住，我会主动出现",
        v.heart,
    ], "cz"))


def write_mood(v: V) -> str:
    if v.tone == "direct":
        head = v.p([
            f"就现在这样：{v.tell}",
            f"心情吗，{v.now}",
            f"还好谈不上彻底轻松，真实情况是：{v.tell}",
            f"我这会儿的状态很清楚，{v.now}",
        ], "mh")
    else:
        head = v.p([
            f"你问我还好不好，我想老实告诉你。{v.tell}",
            f"心情不算能用一个字概括。{v.now}",
            f"这会儿的我，更接近这样的位置：{v.tell}",
        ], "mh")
    mid = v.p([v.img, v.img2, f"{v.img}，{v.img2}"], "mmood")
    tail = v.p([
        f"{v.heart}。这就是我现在真实的样子",
        f"不想用「还好」把你打发掉，所以把{v.kws[0] if v.kws else '此刻'}这种感觉也给你",
        f"你问了，我就把实际的温度给你，不另做一层漂亮的外壳",
    ], "mt")
    return join(head, mid, tail)


def meet_core(v: V) -> str:
    a, aff = v.avail, v.aff
    if a == "open" and aff in ("warm", "intense", "loyal", "thawing"):
        if v.tone == "direct":
            return v.p([
                f"想见你。时间可以定下来。{v.heart}",
                f"想见面，这句是清楚的。{v.tell}",
            ], "ec")
        return v.p([
            f"想见你。不是为了做什么大事，是想真的坐到同一个地方。{v.heart}",
            f"{v.tell}。见面这件事，我是愿意把它变成日期的。",
        ], "ec")
    if a == "scarce":
        if v.tone == "direct":
            return v.p([
                f"想见，只是现在要把时间挤出来。{v.busy}",
                f"想见面，日程是满的，我会留一格。{v.tell}",
            ], "ec")
        return v.p([
            f"想见你，只是这阵子要把时间从别的事情里抠出来。{v.busy}",
            f"{v.tell}。不是不想出门，是先要排出一段完整的空。",
        ], "ec")
    if a in ("overloaded", "chaotic"):
        if v.tone == "direct":
            return v.p([
                f"想见，这会儿还走不开。{v.busy}",
                f"想见面，先得把手里的乱按住。{v.tell}",
            ], "ec")
        return v.p([
            f"想见你，可我这会儿还被事情绊在原地。{v.busy}",
            f"{v.img}。等我先顾得过来，会把见面提上桌。",
        ], "ec")
    if a == "withdrawn":
        if v.tone == "direct":
            return v.p([
                f"想见，更想先以一种安静的方式见。{v.tell}",
                f"想见面，但不要热闹的那种，我需要小一点的场合。{v.now}",
            ], "ec")
        return v.p([
            f"想见你，只是我这会儿更适合安安静静地待一会儿，而不是很大的场合。{v.tell}",
            f"{v.now}。若能见，我想要比较静的那种见面。",
        ], "ec")
    if a == "hesitant":
        if v.tone == "direct":
            return v.p([
                f"想见，脚还没有完全迈出去。{v.tell}",
                f"想见面，我还在跟自己确认时机。{v.now}",
            ], "ec")
        return v.p([
            f"想见你，这句是真的，行动却还在门槛上。{v.tell}",
            f"{v.now}。给我一点把步子迈稳的时间，见面这件事我没有否掉。",
        ], "ec")
    # recovering
    if v.tone == "direct":
        return v.p([
            f"想见，等我再把状态养稳一点。{v.tell}",
            f"想见面，已经比前一阵更接近能出门的位置了。{v.now}",
        ], "ec")
    return v.p([
        f"想见你。我正在往能好好见面的状态走，不想用很差的样子出现。{v.tell}",
        f"{v.now}。日子近了，只是还想再准备一点。",
    ], "ec")


def write_meet(v: V) -> str:
    return join(meet_core(v), v.p([v.img, v.img2, v.now], "em"), v.p([
        f"{v.heart}",
        f"你若也想见，把这件事放在我们都能看见的地方，我会应",
        f"不是口头说说，是我想把见面从念头里拿出来",
    ], "ez"))


def stay_core(v: V) -> str:
    st, aff = v.stab, v.aff
    if st in ("stable", "beginning", "integrating", "balancing") and aff in ("warm", "loyal", "intense", "thawing"):
        if v.tone == "direct":
            return v.p([
                f"还在。不打算离开。{v.tell}",
                f"会留下，这句我可以给你。{v.heart}",
            ], "sc")
        return v.p([
            f"还在，也想继续在。{v.heart}",
            f"{v.tell}。离开不是我这会儿要做的选择。",
        ], "sc")
    if st == "ending":
        if v.tone == "direct":
            return v.p([
                f"有些旧的形式会结束，我不是要在人这边消失。{v.tell}",
                f"结束的是一段旧走法，不是把你从我这里抹掉。{v.heart}",
            ], "sc")
        return v.p([
            f"有东西正在结束，我承认。可我要结束的不是「我还在不在」这件事本身。{v.tell}",
            f"{v.heart}。人还在，只是方式会变。",
        ], "sc")
    if st in ("stuck", "shaky") or aff in ("conflicted", "wounded"):
        if v.tone == "direct":
            return v.p([
                f"还在，只是站得不那么稳。{v.tell}",
                f"没有走，也还没有把下一步说得很满。{v.now}",
            ], "sc")
        return v.p([
            f"还在这里，只是这会儿站得有些费力。{v.tell}",
            f"{v.now}。不是已经离开，是还在找一个能站稳的姿势。",
        ], "sc")
    if aff in ("cooling", "distant"):
        if v.tone == "direct":
            return v.p([
                f"还没有离开，距离却比以前远。{v.tell}",
                f"还在，热度低了，这点我不骗你。{v.heart}",
            ], "sc")
        return v.p([
            f"还在，只是没有靠得那么近。{v.heart}",
            f"{v.tell}。若你问会不会突然消失，这一刻的答案是：人还在，靠近的力弱了。",
        ], "sc")
    # changing / recovering
    if v.tone == "direct":
        return v.p([
            f"还在，只是正在过渡，不是站在门口要走。{v.tell}",
            f"会继续，形式可能会变，人没有从这边撤走。{v.heart}",
        ], "sc")
    return v.p([
        f"还在。我们像走在转换的那一段路上，不是已经散了。{v.tell}",
        f"{v.heart}。回来或者留下，对我来说都不是一句空话。",
    ], "sc")


def write_stay(v: V) -> str:
    return join(stay_core(v), v.p([v.img, v.img2, v.now], "sm"), v.p([
        f"{v.heart}",
        f"你问还在不在，我把现在的位置老实给你，不拿以后的大话先把位置占上",
        f"{v.tell}。这是我今天能给你的位置",
    ], "sz"))


def write_other(v: V) -> str:
    # Never invent a third person. The "other" is work / past / fear / illusion.
    if v.tone == "direct":
        head = v.p([
            f"没有别人。占住我的是另一件事：{v.tell}",
            f"不是另有其人。{v.now}",
            f"你问有没有别人，答案是没有。{v.tell}",
        ], "oh")
    else:
        head = v.p([
            f"没有别人。我这会儿手里、心里转着的，是{v.tell}",
            f"不是去向了另一个人。{v.now}",
            f"让我分神的不是第三者，是眼前这些：{v.img}",
        ], "oh")
    mid = v.p([
        f"{v.img2}。这些东西会占位置，可它们不是一个可以代替你的人",
        f"{v.busy}。忙和乱有时看起来像疏远，实质不是换了一个人",
        f"{v.now}。请把「有别人」这份担心，先从这张画面里拿掉",
    ], "om")
    tail = v.p([
        f"{v.heart}",
        f"若你觉得我在看向别处，我想让你看清那是事情和状态，不是另一张脸",
        f"{v.tell}。这不是在为冷淡找借口，是把事实说准",
    ], "oz")
    return join(head, mid, tail)


def angry_core(v: V) -> str:
    if v.talk == "sharp" or v.aff in ("wounded", "conflicted") or v.avail == "chaotic":
        if v.tone == "direct":
            return v.p([
                f"有一点气，或者还有没散尽的别扭，不是讨厌你。{v.tell}",
                f"说完全没火是假的，火也没有大到要把你推开。{v.now}",
            ], "ac")
        return v.p([
            f"心里不是全然平静，可能还留着一点刺，可那不是「讨厌你」。{v.tell}",
            f"{v.now}。若你感觉到硬，里面更像是没处理完的情绪，不是嫌弃。",
        ], "ac")
    if v.aff in ("cooling", "distant"):
        if v.tone == "direct":
            return v.p([
                f"不是在生气，是距离先拉开了。{v.tell}",
                f"没在发火，只是热度下来了，这和生气不是同一件事。{v.heart}",
            ], "ac")
        return v.p([
            f"没有在生你的气。这会儿更像是远了一点，不是火还在烧。{v.tell}",
            f"{v.heart}。若我话少，先别把原因写成讨厌。",
        ], "ac")
    if v.tone == "direct":
        return v.p([
            f"没有生你的气。{v.heart}",
            f"不讨厌你。{v.tell}",
        ], "ac")
    return v.p([
        f"没有生你的气。{v.heart}",
        f"{v.tell}。若最近让你觉得冷，原因不在讨厌。",
    ], "ac")


def write_angry(v: V) -> str:
    return join(angry_core(v), v.p([v.img, v.img2, v.now], "am"), v.p([
        f"有话要说我会说，不会只用气把你晾在外面",
        f"{v.tell}。这是我对「生不生气」最老实的回答",
        v.heart,
    ], "az"))


def write_remember(v: V) -> str:
    if v.tone == "direct":
        head = v.p([
            f"记得。没有忘。{v.heart}",
            f"还在乎。{v.tell}",
            f"记得你，也记得我们走过的那些。{v.now}",
        ], "rh")
    else:
        head = v.p([
            f"记得你。这件事没有从我这里掉出去。{v.heart}",
            f"还在乎。{v.tell}",
            f"忘了？没有。有些东西会自己留着。{v.img}",
        ], "rh")
    mid = v.p([
        f"{v.img}。这些画面里有你，不是被我清掉的那种",
        f"{v.now}。就算状态在变，记忆和在乎都还在原处",
        f"若你问后悔不后悔——我更想先把还记得、还放在心上这件事说清楚。{v.tell}",
    ], "rm")
    tail = v.p([
        f"{v.heart}",
        f"你不是被我随手放下的那一个",
        f"{v.tell}。记得，并且还放在心里",
    ], "rz")
    return join(head, mid, tail)


def future_core(v: V) -> str:
    st, clar = v.stab, v.clar
    if st in ("beginning", "changing", "integrating", "balancing") and clar in ("clear", "emerging", "sudden"):
        if v.tone == "direct":
            return v.p([
                f"有往后走的空间，我愿意把一部分路和你一起走。{v.tell}",
                f"不是没有未来，方向正在打开。{v.now}",
            ], "fc")
        return v.p([
            f"以后会怎样，我给不了一张画满的图，可我感觉路是往前开的。{v.tell}",
            f"{v.heart}。我想把一部分期待放在我们共同的方向上。",
        ], "fc")
    if st == "ending":
        if v.tone == "direct":
            return v.p([
                f"旧的那一段会收束，后面会有另一层，不是一片空白。{v.tell}",
                f"未来不是原样复制，是清理之后再长。{v.heart}",
            ], "fc")
        return v.p([
            f"有些旧的走法会结束，这不等于我们后面什么都没有。{v.tell}",
            f"{v.now}。腾出来的位置，是给还可能长出来的那些。",
        ], "fc")
    if st in ("stuck", "shaky") or clar in ("foggy",):
        if v.tone == "direct":
            return v.p([
                f"未来还没有清晰的轮廓，我却没有把它关掉。{v.tell}",
                f"以后会怎样，这会儿说不准，路还在，只是慢。{v.now}",
            ], "fc")
        return v.p([
            f"以后的轮廓这会儿不够硬，我还是愿意站在这条路上。{v.tell}",
            f"{v.now}。不是没有以后，是以后还要再走一段才看得更实。",
        ], "fc")
    if v.tone == "direct":
        return v.p([
            f"有以后，只要我们继续把眼前这一段走实。{v.tell}",
            f"未来不是口号，是还能一起往前挪。{v.heart}",
        ], "fc")
    return v.p([
        f"以后会怎样，我更相信我们还能不能把眼前的节奏走下去。{v.tell}",
        f"{v.heart}。路还在，我没有把未来从桌上拿掉。",
    ], "fc")


def write_future(v: V) -> str:
    return join(future_core(v), v.p([v.img, v.img2, v.now], "fm"), v.p([
        f"{v.heart}",
        f"{v.tell}。这是我对以后最老实的看法",
        f"我不想用一张空头支票把你打发掉，所以只把我现在真能看见的方向给你",
    ], "fz"))


def write_doing(v: V) -> str:
    if v.tone == "direct":
        head = v.p([
            f"我这会儿就在做这件事：{v.now}",
            f"人在这里：{v.tell}",
            f"此刻的画面就是：{v.img}",
        ], "dh")
    else:
        head = v.p([
            f"你问我在干什么，我把眼前的真实情形给你。{v.now}",
            f"这会儿我在这样的位置上：{v.tell}",
            f"眼前能看见的是：{v.img}",
        ], "dh")
    mid = v.p([
        f"{v.img2}。心里转着的，也大概是这些",
        f"{v.busy}",
        f"{v.now}。若你忽然想到我，我多半就在这样的状态里",
    ], "dm")
    tail = v.p([
        f"{v.heart}",
        f"不是在一个你到不了的远方，我没失踪，人就在这样的日常里",
        f"想让你知道我没失踪，只是正处在这样的日常或这样的关口",
    ], "dz")
    return join(head, mid, tail)


def write_comfort(v: V) -> str:
    if v.tone == "direct":
        head = v.p([
            f"我知道你这会儿不好受。{v.tell}",
            f"累了就先靠过来一点。{v.heart}",
            f"你的难受我接到了。{v.now}",
        ], "ch")
    else:
        head = v.p([
            f"你这会儿一定不好过。我在这儿。{v.heart}",
            f"听见你累了、委屈了。{v.tell}",
            f"先别一个人把那一块咬着。{v.now}",
        ], "ch")
    mid = v.p([
        f"{v.img}。我就在旁边，不急着把你拉去笑",
        f"{v.img2}。你要是想说话，我听；想安静，我也待着",
        f"我能做的很具体：把时间给你，把肩膀给你，把{v.tell}这种状态下的那点力气分你一点",
    ], "cmf")
    tail = v.p([
        f"这一阵让我陪着过完，好起来的那一步我们稍后自然会走到",
        f"{v.heart}",
        f"你不是被扔在原地的那一个，我看见了",
    ], "czf")
    return join(head, mid, tail)


def write_communication(v: V) -> str:
    if v.talk in ("forthcoming", "blurt", "sharp"):
        if v.tone == "direct":
            head = v.p([
                f"有话，我想直接说。{v.tell}",
                f"想跟你把话摊在桌上。{v.heart}",
            ], "kh")
        else:
            head = v.p([
                f"有些话我想说给你听。{v.tell}",
                f"{v.heart}。通道这会儿是开着的，我们可以把重要的那句拿出来。",
            ], "kh")
    elif v.talk in ("silent", "careful", "delayed"):
        if v.tone == "direct":
            head = v.p([
                f"有话，只是我说得慢，整理好了会给你。{v.tell}",
                f"想说，嘴却还没完全打开。不是没有。{v.now}",
            ], "kh")
        else:
            head = v.p([
                f"想对你说的话是有的，只是我这会儿说得慢、说得少。{v.tell}",
                f"{v.now}。先知道我没有把沟通关死。",
            ], "kh")
    else:
        head = v.p([
            f"有想说的，表达却不够稳，可能会一阵清楚一阵含糊。{v.tell}",
            f"{v.now}。我们还是可以把话慢慢放到中间来。",
        ], "kh")
    mid = v.p([v.img, v.img2, v.now], "km")
    tail = v.p([
        f"{v.heart}",
        f"你要是也有想说的，放过来，我会接",
        f"{v.tell}。这就是我现在能给出的沟通状态",
    ], "kz")
    return join(head, mid, tail)


def write_companionship(v: V) -> str:
    if v.avail in ("open", "recovering") or v.aff in ("warm", "loyal", "intense", "thawing"):
        if v.tone == "direct":
            head = v.p([
                f"我在，也想待在你旁边。{v.heart}",
                f"能陪你。{v.tell}",
            ], "ph")
        else:
            head = v.p([
                f"我想陪着你。不是占满你，是让你感觉到旁边有人。{v.heart}",
                f"{v.tell}。在身边这件事，我愿意做得自然一点。",
            ], "ph")
    elif v.avail in ("withdrawn", "hesitant"):
        if v.tone == "direct":
            head = v.p([
                f"想陪，只是我这会儿能给的是比较安静的陪法。{v.tell}",
                f"在，只是可能坐得稍远一点，没有离开。{v.now}",
            ], "ph")
        else:
            head = v.p([
                f"想在你身边，只是我这会儿更适合安静地待着，而不是一直说话。{v.tell}",
                f"{v.now}。陪伴还在，只是音量比较低。",
            ], "ph")
    else:
        if v.tone == "direct":
            head = v.p([
                f"想陪，这会儿能分出的时间有限，我会把能留的留下。{v.busy}",
                f"想在，先得把手里的事安一个位置。{v.tell}",
            ], "ph")
        else:
            head = v.p([
                f"想陪你，只是这阵子我能拿出的完整时间不多。{v.busy}",
                f"{v.tell}。能留下的那段，我会留下。",
            ], "ph")
    mid = v.p([v.img, v.img2, v.now], "pm")
    tail = v.p([
        f"{v.heart}",
        f"你要是觉得孤单，先把「我还在这边」这一句带着",
        f"{v.tell}。陪伴这件事，我没有从桌上拿掉",
    ], "pz")
    return join(head, mid, tail)


def write_relationship(v: V) -> str:
    st, aff = v.stab, v.aff
    if st in ("stable", "integrating", "balancing", "beginning") and aff in ("warm", "loyal", "intense", "thawing"):
        if v.tone == "direct":
            head = v.p([
                f"我们之间是往一起的，连接是实的。{v.tell}",
                f"关系目前站得住。{v.heart}",
            ], "yh")
        else:
            head = v.p([
                f"我们之间有一种还在靠近的实感。{v.heart}",
                f"{v.tell}。距离和温度我都感觉得到，总体是往一起的。",
            ], "yh")
    elif st in ("shaky", "stuck") or aff in ("conflicted", "wounded"):
        if v.tone == "direct":
            head = v.p([
                f"关系还在，只是这会儿不那么齐。{v.tell}",
                f"有缝，不是已经断了。{v.now}",
            ], "yh")
        else:
            head = v.p([
                f"我们还在一段关系里，只是步调这会儿没有完全对齐。{v.tell}",
                f"{v.now}。缝是有的，我想面对它，而不是假装很圆。",
            ], "yh")
    elif st == "ending" or aff in ("cooling", "distant"):
        if v.tone == "direct":
            head = v.p([
                f"关系在变，有些旧的形状在退，人还没有从里面抽走。{v.tell}",
                f"距离比以前远，这点是真的。{v.heart}",
            ], "yh")
        else:
            head = v.p([
                f"我们的状态正在变化，不像最稳的时候那样妥帖。{v.tell}",
                f"{v.heart}。远一点不等于已经没有这段关系。",
            ], "yh")
    else:
        head = v.p([
            f"关系是活的，这会儿正在走动，还没有一个盖棺的结论。{v.tell}",
            f"{v.now}。我更想老实描述现在的位置，而不是给它一个漂亮名字。",
        ], "yh")
    mid = v.p([v.img, v.img2, v.now], "ym")
    tail = v.p([
        f"{v.heart}",
        f"{v.tell}。这就是我对我们现在的看法",
        f"你问我们怎么了，我把真实的距离和温度给你",
    ], "yz")
    return join(head, mid, tail)


def write_general(v: V) -> str:
    if v.tone == "direct":
        head = v.p([
            f"把我现在最真实的状态给你。{v.tell}",
            f"我就处在这样的位置：{v.now}",
            f"此刻我想让你看见的是：{v.tell}",
        ], "gh")
    else:
        head = v.p([
            f"我想把此刻最实的一面递给你。{v.tell}",
            f"不必猜太远，我这会儿就是这样：{v.now}",
            f"从我这边看，眼前最清楚的是这件事：{v.tell}",
        ], "gh")
    # "不必猜太远" contains 不必 — avoid
    if "不必" in head:
        head = head.replace("不必猜太远，", "不用绕太远，")
        # 不用急着 is forbidden, 不用绕 is ok
    mid = v.p([
        f"{v.img}",
        f"{v.img2}",
        f"{v.img}，{v.img2}",
        v.now,
    ], "gm")
    tail = v.p([
        f"{v.heart}",
        f"{v.busy}",
        f"我就在这儿，状态就是这样，没有另外做一层假的光",
        f"{v.tell}。你要是愿意听，我就停在这句上",
    ], "gz")
    return join(head, mid, tail)


WRITERS = {
    "busy": write_busy,
    "miss": write_miss,
    "like": write_like,
    "contact": write_contact,
    "mood": write_mood,
    "meet": write_meet,
    "stay": write_stay,
    "other": write_other,
    "angry": write_angry,
    "remember": write_remember,
    "future": write_future,
    "doing": write_doing,
    "comfort": write_comfort,
    "communication": write_communication,
    "companionship": write_companionship,
    "relationship": write_relationship,
    "general": write_general,
}


def polish(text: str) -> str:
    text = text.replace("。。", "。").replace("，。", "。").replace("。。。", "。")
    text = re.sub(r"。+", "。", text)
    # voice-pack leftovers
    text = text.replace("都不必躲", "都不用躲")
    text = text.replace("也不必一直", "也不用一直")
    text = text.replace("不必再", "不再")
    text = text.replace("不必猜太远，", "不用绕太远，")
    text = text.replace("不必", "不用")  # last resort; avoid creating 不用急着
    text = text.replace("不用急着", "先不着急")
    text = text.replace("看不清", "看不稳")
    text = text.replace("有点难", "有些费力")
    sents = sent_list(text)
    # drop exact repeated sentences, keep first
    dedup = []
    seen = set()
    for s in sents:
        if s not in seen:
            dedup.append(s)
            seen.add(s)
    sents = dedup
    if len(sents) > 4:
        sents = sents[:4]
    # merge very short standalone sentences into the next one
    # so "想你。" / "会找你。" won't collide across cards
    merged = []
    i = 0
    while i < len(sents):
        body = sents[i][:-1]
        if len(body) <= 8 and i + 1 < len(sents):
            merged.append(period(body + "，" + sents[i + 1][:-1]))
            i += 2
        else:
            merged.append(sents[i])
            i += 1
    return "".join(merged)


def has_forbidden(text: str) -> list[str]:
    return [f for f in FORBIDDEN if f in text]


def adjust_length(text: str, v: V, intent: str) -> str:
    sents = sent_list(text)
    if len(sents) < 2:
        sents.append(period(v.p([v.img, v.heart, v.tell], "pad" + intent)))
    if len(sents) > 4:
        sents = sents[:4]
    return "".join(sents)


GETRESPONSE_JS = r'''
const THEME_TO_INTENT_FALLBACK = {
  missing: "miss",
  relationship: "relationship",
  companionship: "companionship",
  communication: "communication",
  date: "meet",
  comfort: "comfort",
  future: "future",
  free: "general"
};

function _cellTexts(cell) {
  if (!cell || !cell.length) return [];
  const out = [];
  for (let i = 0; i < cell.length; i++) {
    const item = cell[i];
    if (typeof item === "string" && item) out.push(item);
    else if (item && item.text) out.push(item.text);
  }
  return out;
}

function _pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function _preferTone(cell, toneId) {
  if (!cell || !cell.length) return null;
  const tagged = [];
  for (let i = 0; i < cell.length; i++) {
    const item = cell[i];
    if (item && typeof item === "object" && item.tone === toneId && item.text) tagged.push(item.text);
  }
  if (tagged.length) return _pick(tagged);
  const all = _cellTexts(cell);
  return all.length ? _pick(all) : null;
}

function fallbackFromCard(card, isReversed) {
  const meaning = card && (isReversed ? card.reversed : card.upright);
  const kws = (meaning && meaning.keywords) || [];
  const kwText = kws.length ? kws.join("、") : "此刻真实的心情";
  const img = meaning && meaning.meaning ? meaning.meaning.replace(/。$/, "") : "我就在这样的位置上";
  return "我现在就处在这种状态里：" + kwText + "。" + img + "。我想让你知道，我没有躲开你，人就在这儿。";
}

/**
 * 获取传讯文案
 * @param {string} themeId 界面主题（自由提问为 free）
 * @param {object} card TAROT_CARDS 中的牌对象
 * @param {boolean} isReversed
 * @param {string} toneId
 * @param {string} [questionText] 用户输入的问题，有则优先按细意图分类
 * @returns {string}
 */
function getResponse(themeId, card, isReversed, toneId, questionText) {
  const orientation = isReversed ? "reversed" : "upright";
  let intent = "general";
  const q = (questionText || "").trim();
  const classify = (typeof classifyQuestion === "function")
    ? classifyQuestion
    : (typeof require === "function" ? require("./intents.js").classifyQuestion : null);
  const themeMap = (typeof THEME_TO_INTENT !== "undefined")
    ? THEME_TO_INTENT
    : THEME_TO_INTENT_FALLBACK;

  if (q && classify) {
    intent = classify(q) || "general";
  } else {
    intent = themeMap[themeId] || "general";
  }

  const cardBlock = (card && RESPONSES[card.id]) || {};
  const oriBlock = cardBlock[orientation] || {};

  let text = _preferTone(oriBlock[intent], toneId);
  if (!text) text = _preferTone(oriBlock.general, toneId);
  if (!text) {
    const keys = Object.keys(oriBlock);
    for (let i = 0; i < keys.length; i++) {
      text = _preferTone(oriBlock[keys[i]], toneId);
      if (text) break;
    }
  }
  if (!text) text = fallbackFromCard(card, isReversed);
  return text;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { RESPONSES, getResponse, fallbackFromCard };
}
'''



def make_text(cid, card, raw, ori, intent, tone):
    key = (cid, ori, intent, tone)
    if key in OVERRIDES:
        text = polish(OVERRIDES[key])
        return text, True
    v = V(raw, card, tone)
    text = polish(WRITERS[intent](v))
    text = adjust_length(text, v, intent)
    text = polish(text)
    return text, False


def sign_sentence(s, vfix, salt):
    """Make a sentence unique without repeating it or replacing the meaning."""
    body = s[:-1] if s.endswith("。") else s
    # already contains tell or first image? add a lighter unique crumb
    crumbs = [
        vfix.imgs[0],
        vfix.imgs[1],
        vfix.imgs[2],
        vfix.tell,
    ]
    crumb = crumbs[fnv(salt, vfix.id, body) % len(crumbs)]
    if crumb and crumb not in body:
        return period(body + "——" + crumb)
    crumb2 = crumbs[(fnv(salt, vfix.id, body) + 1) % len(crumbs)]
    if crumb2 and crumb2 not in body:
        return period(body + "——" + crumb2)
    return period(body + "——这是我此刻的位置")


def bump_text(text, vfix, intent, tone, cid, seen_sent, pool):
    sents = sent_list(text)
    if not sents:
        sents = [period(vfix.tell), period(vfix.img)]
    # sign the last sentence only
    sents[-1] = sign_sentence(sents[-1], vfix, "bump" + intent + tone + cid)
    return polish("".join(sents[:4]))


def main():
    cards = load_cards()
    voices = json.loads(VOICES_PATH.read_text(encoding="utf-8"))
    if len(voices) != 156:
        raise SystemExit(f"expected 156 voices, got {len(voices)}")
    by_key = {(v["id"], v["ori"]): v for v in voices}

    # Phase 1: generate all texts, keep override flag
    raw_cells = {}  # (cid, ori, intent) -> [(tone, text, is_override)]
    problems = []
    for cid, card in cards.items():
        for ori_short, ori in (("u", "upright"), ("r", "reversed")):
            raw = by_key[(cid, ori_short)]
            for intent in INTENT_IDS:
                items = []
                for tone in ("gentle", "direct"):
                    text, is_ov = make_text(cid, card, raw, ori, intent, tone)
                    hits = has_forbidden(text)
                    if hits:
                        problems.append(f"FORBIDDEN {cid, ori, intent, tone}: {hits} | {text}")
                    if not text or len(sent_list(text)) < 2:
                        problems.append(f"SHORT {cid, ori, intent, tone}: {text}")
                    items.append([tone, text, is_ov, raw, card])
                raw_cells[(cid, ori, intent)] = items

    # Phase 2: register override sentences first so handwritten lines stay intact
    seen_full = defaultdict(dict)
    seen_sent = defaultdict(dict)
    for (cid, ori, intent), items in raw_cells.items():
        pool = (intent, ori)
        for tone, text, is_ov, raw, card in items:
            if not is_ov:
                continue
            seen_full[pool][text] = cid
            for s in sent_list(text):
                seen_sent[pool][s] = cid

    # Phase 3: uniquify only non-overrides
    data = {}
    for cid, card in cards.items():
        data[cid] = {"upright": {}, "reversed": {}}
        for ori in ("upright", "reversed"):
            for intent in INTENT_IDS:
                cell = []
                pool = (intent, ori)
                for tone, text, is_ov, raw, card0 in raw_cells[(cid, ori, intent)]:
                    if not is_ov:
                        vfix = V(raw, card0, tone)
                        # Only enforce uniqueness of the full answer.
                        # Shared short clauses are OK; signing every repeated
                        # clause made the copy sound mechanical.
                        if text in seen_full[pool]:
                            text = bump_text(text, vfix, intent, tone, cid, seen_sent, pool)
                            if text in seen_full[pool]:
                                problems.append(f"DUP_FULL {cid, ori, intent, tone} == {seen_full[pool][text]}")
                        hits = has_forbidden(text)
                        if hits:
                            problems.append(f"FORBIDDEN_AFTER {cid, ori, intent, tone}: {hits} | {text}")
                        seen_full[pool][text] = cid
                        for s in sent_list(text):
                            seen_sent[pool][s] = cid
                    cell.append({"tone": tone, "text": text})
                data[cid][ori][intent] = cell

    header = (
        "/**\n"
        " * 传讯文案库\n"
        " * 结构：RESPONSES[cardId][upright|reversed][intent] = [{tone, text}, ...]\n"
        " * 由 tools/generate-responses.py 生成，运行时不依赖该脚本。\n"
        " * 选择逻辑见 getResponse：先按提问文本分细意图，再按牌与正逆位取文案。\n"
        " */\n"
        "const RESPONSES = "
    )
    blob = json.dumps(data, ensure_ascii=False, indent=2)
    OUT_PATH.write_text(header + blob + ";\n" + GETRESPONSE_JS, encoding="utf-8")

    n_answers = 78 * 2 * len(INTENT_IDS) * 2
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")
    print(f"intents={len(INTENT_IDS)} answers={n_answers} problems={len(problems)}")
    if problems:
        for p in problems[:40]:
            print(p, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
