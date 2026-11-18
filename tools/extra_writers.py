# -*- coding: utf-8 -*-
"""Card-specific writers for the expanded intent set. Imported by generate-responses.py."""
from __future__ import annotations


TOPIC_HINTS = {
    "busy": ("忙", "空", "顾不过来", "顾此失彼", "手头", "日程", "转不过来", "抽不出", "闲", "腾不出", "手忙脚乱", "事务", "没空", "有空", "没完没了", "回你会慢"),
    "tired": ("累", "乏", "熬", "撑", "歇", "疲惫", "困乏"),
    "sick": ("病", "不舒服", "身子", "生病", "恙", "欠安", "身体"),
    "cold": ("感冒", "烧", "咳嗽", "嗓子", "鼻涕", "受凉", "着凉", "发热", "喉咙", "着了点凉", "风寒", "凉"),
    "sleep": ("睡", "失眠", "夜里", "入眠", "睡眠", "休息"),
    "eat": ("吃", "饭", "餐", "用餐"),
    "hungry": ("饿", "肚子", "饥"),
    "drink": ("喝水", "水", "口渴", "渴", "补水"),
    "drunk": ("酒", "喝多", "醉", "微醺", "喝大", "喝是喝了", "喝了", "喝过", "往回醒", "晕"),
    "home": ("到家", "回家", "进门", "到屋里", "抵家", "到住处", "屋里", "到了", "家的门"),
    "outside": ("出门", "在路上", "外面", "路上"),
    "coldfeel": ("冷", "冻", "穿", "暖和", "加衣服"),
    "rain": ("雨", "伞"),
    "work": ("工作", "加班", "上班", "公司", "下班", "项目", "返工", "协作", "手头"),
    "study": ("学", "考试", "作业", "功课", "复习", "上课", "读书"),
    "miss": ("想你", "想我", "思念", "惦记", "牵挂", "想念", "想到你", "想靠近", "很想", "会想到", "想还在", "想得", "心里有你", "想，"),
    "like": ("喜欢", "动心", "心动", "在意", "动过心", "心意", "感觉", "有心"),
    "love": ("爱",),
    "contact": ("找你", "联系", "消息", "联络", "发", "出现", "伸手", "回你", "断开", "会给你", "沉默", "晚到"),
    "ignore": ("回", "理", "晾", "冷落", "已读"),
    "missedcall": ("电话", "接", "挂", "来电"),
    "mood": ("心情", "还好", "状态", "不开心", "高兴", "真实的样子", "这会儿的我"),
    "cry": ("哭", "眼泪", "泪", "眼睛", "眼里", "红过"),
    "angry": ("气", "讨厌", "火", "恼", "嫌弃", "别扭"),
    "sad": ("难过", "难受", "低落", "闷", "不好受", "偏低", "心情"),
    "lonely": ("一个人", "孤单", "寂寞", "独自", "没有别人", "有点空", "孤"),
    "bored": ("无聊", "闲得慌", "没事做", "闷得慌", "闲得发", "闷死", "没事可做", "东摸摸", "闲着"),
    "stress": ("压力", "烦", "焦虑", "绷", "紧张"),
    "meet": ("见面", "见", "出来", "约会", "出门"),
    "stay": ("离开", "还在", "走", "在一起", "留下", "还没离开"),
    "other": ("别人", "第三者", "对象", "另有", "另一个人", "换了一个人"),
    "ex": ("前任", "那个人", "旧的地方"),
    "jealous": ("吃醋", "嫉妒", "醋", "介意", "介怀", "无动于衷"),
    "remember": ("记得", "记着", "忘不", "忘了", "在乎"),
    "forget": ("忘",),
    "future": ("以后", "未来", "将来", "怎样", "长久", "方向", "期待"),
    "doing": ("在", "这会儿", "手头", "正", "眼前"),
    "where": ("在", "人在", "这边", "地方"),
    "think": ("想", "念头", "琢磨", "脑子", "心里"),
    "comfort": ("安慰", "我在", "哄", "我听", "旁边", "陪着", "肩膀", "陪"),
    "communication": ("说", "话", "告诉", "开口", "谈", "沟通", "那句", "表达", "通道"),
    "companionship": ("陪", "身边", "留下", "旁边"),
    "relationship": ("关系", "我们", "这段", "距离", "温度", "往一起", "缝是有的", "有缝"),
    "sorry": ("道歉", "对不起", "在意", "介意", "歉", "那件事"),
    "forgive": ("原谅", "饶"),
    "regret": ("后悔", "懊悔", "悔", "撤回"),
    "changed": ("变", "不像以前", "不一样", "换了", "换了一张", "没有换", "新的棱"),
    "lie": ("骗", "假", "撒谎", "说谎", "真话"),
    "trust": ("信", "信任"),
    "secret": ("瞒", "藏", "秘密", "隐瞒", "没说", "揣", "阴谋"),
    "wait": ("等",),
    "comeback": ("回来", "再回", "回得来", "往回", "走回来", "回这一"),
    "breakup": ("分手", "分开", "结束", "散", "分与不分", "分不"),
    "makeup": ("和好", "复合", "重来", "重新靠近"),
    "distance": ("远", "异地", "两地", "隔"),
    "serious": ("认真", "长久", "长远", "随便", "以后"),
    "morning": ("起", "醒", "被窝", "睡里", "睁眼", "被子"),
    "latenight": ("还没睡", "还醒", "这么晚", "熬夜", "还不睡", "还醒着", "熬着", "合眼"),
    "dream": ("梦",),
    "money": ("钱", "赚", "手头", "花", "经济", "够用", "紧巴巴", "荷包"),
    "family": ("家", "爸妈", "父母", "家人"),
    "friends": ("朋友", "聚会", "社交", "热闹"),
    "plans": ("打算", "周末", "安排", "计划", "行程", "邀约", "空下来"),
    "birthday": ("生日", "这个日子", "那个日子"),
    "gift": ("想要", "送", "礼物"),
    "game": ("游戏", "开黑", "排位", "上分", "打本", "一局", "局里", "打过", "在玩"),
    "late": ("多久", "还没到", "迟到", "还没来", "还差", "快了", "晚", "就要到", "延误"),
    "worry": ("担心", "放心不下", "记挂", "操心", "安不安全"),
    "support": ("支持", "站在", "帮", "撑", "加油", "你这边"),
    "cook": ("做饭", "做了", "煮", "厨房", "下厨", "烧菜", "吃的", "菜", "大厨", "自己弄", "自己做"),
    "general": ("这会儿", "此刻", "现在", "我"),
}


def make_extra_writers(join):
    def compose(v, heads, mids=None, tails=None, tag="x"):
        mid_pool = mids or [
            v.img,
            v.img2,
            f"{v.img}。{v.now}",
            f"{v.now}",
            f"{v.img}，{v.img2}",
        ]
        tail_pool = tails or [v.heart, v.tell, f"{v.tell}。这是此刻最实的一句"]
        return join(v.p(heads, tag + "h"), v.p(mid_pool, tag + "m"), v.p(tail_pool, tag + "z"))

    def heavy(v):
        return v.burden in ("heavy", "uneven") or v.avail in ("overloaded", "chaotic")

    def recovering(v):
        return v.avail in ("recovering", "changing") or v.burden == "releasing"

    def light(v):
        return v.burden == "light" and v.avail in ("open", "scarce")

    def withdrawn(v):
        return v.avail in ("withdrawn", "hesitant") or v.aff in ("distant", "hidden", "cooling")

    def shaky(v):
        return v.stab in ("shaky", "stuck", "ending") or v.aff in ("conflicted", "wounded")

    def write_tired(v):
        if heavy(v):
            heads = [
                f"累，而且是沉到身子里的那种累。{v.tell}",
                f"是累了，这会儿像被一卷很沉的东西压着。{v.now}",
                f"累坏了，不是轻轻的乏，是骨头缝都在喊停。{v.img}",
            ]
            tails = [
                "我想先把这口气缓下来，不是故意把你晾在一边",
                "等这阵沉退一点，我会把更完整的自己还给你",
                "不是懒得理你，是人先被耗住了，歇过这口气再来找你",
            ]
        elif recovering(v):
            heads = [
                f"还是累，不过最熬的那一阵正在往下退。{v.now}",
                f"累过，这会儿终于肯把力气从牙关里松开一点。{v.tell}",
                f"乏还在，可已经不像刚才那样被按在原地。{v.img}",
            ]
            tails = [
                "人稍微能躺平一点了，不是假装不累，是开始会歇了",
                "再给我一点把疲劳放下的时间，我会回来好好说话",
                f"{v.heart}",
            ]
        elif withdrawn(v):
            heads = [
                f"累，更多是心里先乏了，对外的门也关小了。{v.tell}",
                f"说身体累是真的，说不想见人也有一点，两件事叠在一起。{v.now}",
                f"这会儿乏得很安静，不像忙，像电量自己掉了。{v.img}",
            ]
            tails = [
                "回你会慢，先当我在充电，不是在躲你",
                "等这层乏淡一点，我会把声音调回来",
                f"{v.heart}",
            ]
        elif light(v):
            heads = [
                f"说完全累倒还没有，只是白天走下来有一点乏。{v.tell}",
                f"有点累，还在能撑住的范围里。{v.now}",
                f"乏是有的，没有到走不动。{v.img}",
            ]
            tails = [
                "歇一小会儿就转得过来，你要是找我，我还在",
                f"{v.heart}",
                "不是那种需要你担心的累，只是普通的一天走完了",
            ]
        else:
            heads = [
                f"累，今天的分量在身上还没卸完。{v.tell}",
                f"是有些乏了，步伐比平时沉一点。{v.now}",
                f"累不累，答案是累，只是还站得住。{v.img}",
            ]
            tails = [
                "我想先把肩上这点沉放一放，再好好回你",
                f"{v.heart}",
                "不是抱怨，是老实告诉你：人有点乏了",
            ]
        return compose(v, heads, tails=tails, tag="td")

    def write_sick(v):
        if heavy(v):
            heads = [
                f"不舒服，身子这会儿确实像生了病。{v.tell}",
                f"是有些病了，不是一点点倦，是整个人提不起劲。{v.now}",
                f"生病这事我瞒不住，这阵子身子沉、头也闷。{v.img}",
            ]
            tails = [
                "我会先把自己照顾好，不是要你干着急，是情况就这样",
                "等这阵不舒服过去，我会把更清楚的消息给你",
                "先让我把这口气养回来，再好好出现",
            ]
        elif recovering(v):
            heads = [
                f"前一阵不舒服，这会儿正在往好的方向走。{v.now}",
                f"病没有完全退干净，可最重的那截已经松了。{v.tell}",
                f"身子还虚一点，已经肯重新抬眼看外面了。{v.img}",
            ]
            tails = [
                "我会继续养着，不用把它想成还会突然倒下",
                f"{v.heart}",
                "再给我一点复原的时间，人会回到能好好说话的状态",
            ]
        elif withdrawn(v):
            heads = [
                f"说不上生了很重的病，可身子确实不舒服，提不起那口气。{v.tell}",
                f"不舒服是有的，更像闷在里面的那种，不是高烧那种明显。{v.now}",
                f"身子沉、兴致也低，像病了一场似的倦。{v.img}",
            ]
            tails = [
                "不是假装没事，是连抬眼去接都觉得费力",
                "等这阵闷过去，我会好好照顾自己，也会回你",
                f"{v.heart}",
            ]
        else:
            heads = [
                f"有一点不舒服，还没有到倒下，只是身子不对劲。{v.tell}",
                f"说完全病倒还没有，可也不是全然无事。{v.now}",
                f"身体这会儿要小心一点，我自己也感觉到了。{v.img}",
            ]
            tails = [
                "我会注意着，不硬撑给你看",
                f"{v.heart}",
                "若你担心，先收下这句：我知道自己的状态，也在处理",
            ]
        return compose(v, heads, tails=tails, tag="sk")

    def write_cold(v):
        if heavy(v):
            heads = [
                f"像是感冒了，头沉、嗓子也不利索。{v.tell}",
                f"有点发烧的意思，人发烫，步子也懒。{v.now}",
                f"咳嗽和鼻塞这会儿是真的，不是普通的乏。{v.img}",
            ]
        elif recovering(v):
            heads = [
                f"感冒正在退，最难受的那两天已经过去。{v.now}",
                f"烧退了不少，还剩一点嗓子和疲劲。{v.tell}",
                f"受凉的那截正在往下走，人稍微清爽了。{v.img}",
            ]
        else:
            heads = [
                f"有一点受凉，像要感冒又还没完全倒下。{v.tell}",
                f"鼻子和喉咙不太对，我在观察是不是感冒。{v.now}",
                f"着了点凉，像要感冒，还想用热水和休息把它压回去。{v.img}",
            ]
        tails = [
            "我会穿暖、喝热水，先把这阵风寒按住",
            "不是要你担心，是身体这会儿确实在闹脾气",
            f"{v.heart}",
        ]
        return compose(v, heads, tails=tails, tag="cd")

    def write_sleep(v):
        if v.aff == "wounded" or heavy(v) or v.clar == "foggy":
            heads = [
                f"睡得不好，夜里那些念头会把人翻起来。{v.tell}",
                f"还没睡踏实，睡眠浅，像一直有一层灰在。{v.now}",
                f"失眠是有的，不是单纯晚睡，是躺下也安静不了。{v.img}",
            ]
        elif recovering(v):
            heads = [
                f"睡眠比最糟的时候好一点，人稍微能躺平了。{v.now}",
                f"夜里还没完全稳，可已经肯把一部分担忧放下。{v.tell}",
                f"睡得没有那么碎了，眼皮终于肯沉一点。{v.img}",
            ]
        else:
            heads = [
                f"睡了，或者正在往睡里走，今晚还算能合眼。{v.tell}",
                f"睡眠还过得去，没有到翻来覆去那种。{v.now}",
                f"睡了，休息是有的，这会儿人在往静处放。{v.img}",
            ]
        tails = [
            "你要是担心我没睡，先把这句收着：我知道该歇",
            f"{v.heart}",
            "等夜里真正平下来，白天的话会更清楚",
        ]
        return compose(v, heads, tails=tails, tag="sl")

    def write_eat(v):
        if withdrawn(v) or v.aff in ("cooling", "hidden"):
            heads = [
                f"吃了一点，只是没什么胃口，餐是应付过去的。{v.tell}",
                f"饭是碰了的，吃得少，提不起那口食欲。{v.now}",
                f"说完全没吃不实，说好好吃了一顿也不实。{v.img}",
            ]
        elif heavy(v) or v.avail == "overloaded":
            heads = [
                f"吃了，只是吃得比较匆忙，是挤在事情的间隙里解决的。{v.tell}",
                f"饭没有误，可也谈不上坐下来好好吃。{v.now}",
                f"不是不记得吃饭，是时间被手头的事切碎了。{v.img}",
            ]
        elif recovering(v) or v.aff in ("warm", "thawing"):
            heads = [
                f"吃了，这会儿也愿意把餐当回事，不像前一阵敷衍。{v.now}",
                f"饭是好好吃了的，人稍微回到会照顾自己的节奏。{v.tell}",
                f"用餐这件小事，我开始肯给它一点位置。{v.img}",
            ]
        else:
            heads = [
                f"吃了，正餐没有落下。{v.tell}",
                f"饭吃过了，这会儿不饿。{v.now}",
                f"用餐是有的，你不用把这件小事一直挂着。{v.img}",
            ]
        tails = [
            "你若是担心我空着肚子，先把这层放下来",
            f"{v.heart}",
            "下一顿我会记得，不会拿身体去硬扛",
        ]
        return compose(v, heads, tails=tails, tag="et")

    def write_hungry(v):
        if heavy(v) or withdrawn(v):
            heads = [
                f"有点饿，之前没顾得上，这会儿肚子才把信号送上来。{v.tell}",
                f"饿了，不是夸张，是真的空了一截。{v.now}",
                f"肚子是空的，我这会儿才察觉。{v.img}",
            ]
        elif recovering(v) or light(v):
            heads = [
                f"不算很饿，刚刚吃过，或者正准备去吃。{v.tell}",
                f"肚子还安稳，没有到咕咕叫那种。{v.now}",
                f"饿不饿，答案是还好，我没有空着。{v.img}",
            ]
        else:
            heads = [
                f"有一点饿，正打算找点东西垫一下。{v.tell}",
                f"肚子开始提要求了，我听见了。{v.now}",
                f"饿是有一点的，不会让它一直空着。{v.img}",
            ]
        tails = [
            "我会去吃，你不用隔着屏幕替我饿",
            f"{v.heart}",
            "这是身体的信号，我会理它",
        ]
        return compose(v, heads, tails=tails, tag="hg")

    def write_drink(v):
        heads = [
            f"水喝了，只是可能不够勤，这会儿才想起来补。{v.tell}",
            f"喝了水，杯子就在手边，没有完全忘掉。{v.now}",
            f"口不那么渴，水杯是动过的。{v.img}",
            f"有点忘了喝水，你这一问，我正把杯子拿起来。{v.tell}",
        ]
        tails = [
            "我会再倒一杯，这件小事我收下了",
            f"{v.heart}",
            "你问这个，我知道是在操心我，我领了",
        ]
        return compose(v, heads, tails=tails, tag="dk")

    def write_drunk(v):
        if heavy(v) or v.avail == "chaotic" or v.clar == "foggy":
            heads = [
                f"酒是喝了，量比我预想的多，人有点晃。{v.tell}",
                f"有一点醉，不是全然清醒，步子和话都会慢。{v.now}",
                f"酒在身上，这会儿不适合再做太清楚的决定。{v.img}",
            ]
        elif recovering(v):
            heads = [
                f"先前喝过酒，这会儿正在往回醒，最晕的那截过去了。{v.now}",
                f"酒劲在退，人开始能把句子说完整。{v.tell}",
                f"没有继续灌，醒酒的过程正在走。{v.img}",
            ]
        else:
            heads = [
                f"没有喝多，顶多浅浅一杯，神志是清的。{v.tell}",
                f"酒没有过界，我还知道自己在哪、在和谁说话。{v.now}",
                f"没醉，你不用把我想象成撑不住的样子。{v.img}",
            ]
        tails = [
            "今晚我不会再加了，会把自己安全地放回去",
            f"{v.heart}",
            "若我话比平时软或乱，先当酒在里面掺了一点",
        ]
        return compose(v, heads, tails=tails, tag="dr")

    def write_home(v):
        if v.avail in ("overloaded", "scarce") or v.stab == "balancing":
            heads = [
                f"还在收尾，进门这件事还差最后一截。{v.tell}",
                f"快到了，只是这会儿还没把自己完整地放回屋里。{v.now}",
                f"人还在外面的节奏里，回家的门还差几步。{v.img}",
            ]
        elif withdrawn(v):
            heads = [
                f"到了，已经把自己关回一个更里面的地方。{v.tell}",
                f"进门了，只是到家之后我把自己收得很小。{v.now}",
                f"人是在屋里的，只是不一定立刻对外开门。{v.img}",
            ]
        elif v.avail == "open" or recovering(v):
            heads = [
                f"到家了，人也安稳地落在自己的位子上。{v.tell}",
                f"已经进门，外面那截路结束了。{v.now}",
                f"到了，肩上的风刚放下。{v.img}",
            ]
        else:
            heads = [
                f"到家了，或者正把钥匙转进门锁。{v.tell}",
                f"人在往屋里走，这趟在收束。{v.now}",
                f"回家这件事情正在完成，你先不用一直盯着。{v.img}",
            ]
        tails = [
            "安全这一层，我会自己看住",
            f"{v.heart}",
            "等我把鞋子换下、坐定，会把更完整的状态给你",
        ]
        return compose(v, heads, tails=tails, tag="hm")

    def write_outside(v):
        if v.avail in ("open", "scarce") or v.stab in ("beginning", "changing"):
            heads = [
                f"出门了，人在路上，风还在身上。{v.tell}",
                f"在外面，步子已经迈出去了。{v.now}",
                f"路上呢，这会儿还不在屋里。{v.img}",
            ]
        elif withdrawn(v):
            heads = [
                f"没怎么出门，就算出去也走得近、回得快。{v.tell}",
                f"更想待在里面，外面那一层我这会儿不太想碰。{v.now}",
                f"没有在路上乱走，人收在自己这边。{v.img}",
            ]
        else:
            heads = [
                f"有一趟在外面，事情把我带出了门。{v.tell}",
                f"在路上或者刚从路上回来，风还没散尽。{v.now}",
                f"出门是有的，我会小心。{v.img}",
            ]
        tails = [
            "路上这截我自己看着，你说的小心我收下了",
            f"{v.heart}",
            "等我落到一个能停的地方，会把更清楚的位置给你",
        ]
        return compose(v, heads, tails=tails, tag="out")

    def write_coldfeel(v):
        if heavy(v) or v.burden == "heavy":
            heads = [
                f"冷，而且是渗进袖口那种冷，穿得还是不够。{v.tell}",
                f"有点冻着，手脚先冷了。{v.now}",
                f"这会儿是真冷，我正在往里加一层。{v.img}",
            ]
        elif recovering(v) or light(v):
            heads = [
                f"不至于冻着，衣服够，身上是暖的。{v.tell}",
                f"冷是天气冷，我倒穿够了。{v.now}",
                f"暖和的，你不用一直念叨我少穿。{v.img}",
            ]
        else:
            heads = [
                f"有一点冷，刚把外套又拉紧了一点。{v.tell}",
                f"不算冻坏，只是风过来时还是会缩一下肩。{v.now}",
                f"穿得还行，我知道要给自己留一层。{v.img}",
            ]
        tails = [
            "我会再加点衣服，这句叮嘱我听到了",
            f"{v.heart}",
            "冷是天气的事，我会把自己照顾好",
        ]
        return compose(v, heads, tails=tails, tag="cf")

    def write_rain(v):
        heads = [
            f"雨是遇到了，伞也在，没有浑身淋透。{v.tell}",
            f"带了伞，或者正找地方先避一避。{v.now}",
            f"外面是湿的，我把自己尽量搁在伞沿下面。{v.img}",
            f"有一阵雨，我没有完全没准备地往里走。{v.tell}",
        ]
        tails = [
            "你问带伞了没有，这句我收到了，也会把自己弄干",
            f"{v.heart}",
            "淋一点没关系，我不会在雨里硬撑太久",
        ]
        return compose(v, heads, tails=tails, tag="rn")

    def write_work(v):
        if v.avail in ("overloaded", "chaotic") or heavy(v):
            heads = [
                f"还在工作里，加班这头是真的，节奏已经有点乱。{v.tell}",
                f"事情堆在桌上，下班的点被往后推了。{v.now}",
                f"工作这会儿不轻松，人手上转不过来。{v.img}",
            ]
        elif v.stab in ("stable", "balancing", "integrating") and v.avail in ("scarce", "open"):
            heads = [
                f"工作还顺利，只是要投入，空要靠安排。{v.tell}",
                f"事情在往前走，合作也还对得上。{v.now}",
                f"上班这头是稳的，没有到焦头烂额。{v.img}",
            ]
        elif v.avail == "stuck" or shaky(v):
            heads = [
                f"工作这会儿不太顺，努力有点对不上点。{v.tell}",
                f"工作在返工，或者协作出了缝，人容易烦。{v.now}",
                f"上班不是一帆风顺，我正在硬扛其中一段。{v.img}",
            ]
        else:
            heads = [
                f"工作还在推进，没有大乱，也谈不上完全轻松。{v.tell}",
                f"还在自己的岗位上，事情一件件在过。{v.now}",
                f"加班不一定天天有，今天的分量我自己清楚。{v.img}",
            ]
        tails = [
            "等我把手头安顿好，会把时间往回拨一点",
            f"{v.heart}",
            "工作是工作，我没有把你从这一天里拿掉",
        ]
        return compose(v, heads, tails=tails, tag="wk")

    def write_study(v):
        if heavy(v) or v.avail == "overloaded":
            heads = [
                f"还在学，作业或考试压着，脑子转个不停。{v.tell}",
                f"功课这头是满的，复习把空隙都占了。{v.now}",
                f"学习这阵很沉，像一直坐在同一张桌子前。{v.img}",
            ]
        elif recovering(v) or v.stab in ("stable", "integrating"):
            heads = [
                f"学着，进展比刚才顺一点，东西开始进得去。{v.now}",
                f"作业在往下划，考试的阴影没有那么死死罩着。{v.tell}",
                f"学习还在，人没有被完全压住。{v.img}",
            ]
        else:
            heads = [
                f"有在学，只是节奏和平时差不多，没有到通宵那种。{v.tell}",
                f"功课碰了，书也翻了，这会儿脑子还清。{v.now}",
                f"学习是今天的一部分，不是全部。{v.img}",
            ]
        tails = [
            "等这一段学完，我会抬起头来找你",
            f"{v.heart}",
            "你要是担心我闷在题目里，先知道我还记得出来透气",
        ]
        return compose(v, heads, tails=tails, tag="st")

    def write_love(v):
        if v.aff in ("warm", "loyal", "intense") and v.stab in ("stable", "beginning", "balancing", "integrating"):
            heads = [
                f"爱，这个字我想清楚了。{v.tell}",
                f"爱你，不是摇摆出来的答案。{v.heart}",
                f"是爱，不是只停留在喜欢那里。{v.now}",
            ]
        elif v.aff in ("conflicted", "wounded") or v.clar == "foggy":
            heads = [
                f"爱还在，只是这会儿说得没有那么利落，心里有拉扯。{v.tell}",
                f"不是不爱，是爱和乱叠在一起，我自己也要先理一理。{v.now}",
                f"对你的爱没有空掉，只是经过一层雾，声音会轻一点。{v.img}",
            ]
        elif v.aff in ("cooling", "distant", "hidden"):
            heads = [
                f"爱没有立刻变成没有，只是热度比以前低，这点我不骗你。{v.tell}",
                f"还谈得上爱，只是靠近的力弱了。{v.heart}",
                f"爱这个字对我来说还在，只是我这会儿给得比较小心。{v.now}",
            ]
        elif recovering(v) or v.aff == "thawing":
            heads = [
                f"爱这层又往回暖了一点，我愿意重新把它说清楚。{v.now}",
                f"先前有些退缩，这会儿我更敢承认：我是爱你的。{v.tell}",
                f"爱没有走远，它正在从冻住的地方慢慢回来。{v.img}",
            ]
        else:
            heads = [
                f"爱你，这句话我想认真说，不拿来当客套。{v.tell}",
                f"是爱，程度和方式是我现在能给的这样。{v.heart}",
                f"你问爱不爱，我把真实的答案递过去，不绕。{v.now}",
            ]
        tails = [
            f"{v.heart}",
            "这不是漂亮话，是我愿意在你面前站直说的那句",
            f"{v.tell}。爱这件事，我没有拿来敷衍你",
        ]
        return compose(v, heads, tails=tails, tag="lv")

    def write_ignore(v):
        if v.talk in ("silent", "delayed", "careful") or withdrawn(v):
            heads = [
                f"不是故意不理你，是我这会儿回得慢，门关得比较小。{v.tell}",
                f"消息我看见了，只是话还堵在手里，看起来像不回。{v.now}",
                f"没有把你晾下不管，是我对外的音量先低了。{v.img}",
            ]
        elif v.talk == "sharp" or v.aff in ("wounded", "conflicted"):
            heads = [
                f"有一阵是不想立刻回，心里还有刺，怕一开口就硬。{v.tell}",
                f"不是永久不理你，是我需要先把那口气压住再说话。{v.now}",
                f"已读不回的那段，里面更多是乱，不是把你删掉。{v.img}",
            ]
        elif recovering(v) or v.talk in ("forthcoming", "blurt"):
            heads = [
                f"会回你，先前那阵沉默正在解开。{v.now}",
                f"不是不理，是刚才那截我没能及时伸手，这会儿想补上。{v.tell}",
                f"话正在往回走，不会让你一直对着空白。{v.img}",
            ]
        else:
            heads = [
                f"没有存心不理你，晚回是状态，不是结论。{v.tell}",
                f"我会回，只是不一定能按你期待的速度出现。{v.now}",
                f"把你放在已读里不管，不是我想做的事。{v.img}",
            ]
        tails = [
            "等我把这句话理顺，会亲自出现，不让你一直猜",
            f"{v.heart}",
            "你若觉得被冷落，我把原因说准：是我这边的节奏，不是你不值得回",
        ]
        return compose(v, heads, tails=tails, tag="ig")

    def write_missedcall(v):
        if v.avail in ("overloaded", "chaotic", "scarce") or v.talk == "delayed":
            heads = [
                f"电话那会儿没接住，不是不想接，是手上的事正咬着。{v.tell}",
                f"来电我没有故意挂，是没来得及把那一头放下。{v.now}",
                f"未接是真的，原因在节奏乱，不在不想听你说话。{v.img}",
            ]
        elif withdrawn(v) or v.talk in ("silent", "careful"):
            heads = [
                f"那通没有接，是我这会儿不太适合立刻开口，怕自己说不好。{v.tell}",
                f"不是讨厌你的来电，是我还没准备好用声音面对。{v.now}",
                f"挂或没接的那一下，里面有退避，我会承认。{v.img}",
            ]
        else:
            heads = [
                f"没接到，可能是没听到，或没来得及掏出手机。{v.tell}",
                f"不是故意挂你，这点我想先说清楚。{v.now}",
                f"电话那头我稍后会补上，不会让它凭空消失。{v.img}",
            ]
        tails = [
            "我会回拨，或者用一条把原因说清楚的消息补上",
            f"{v.heart}",
            "你费了力气打过来，这点我知道，不会当没发生",
        ]
        return compose(v, heads, tails=tails, tag="mc")

    def write_cry(v):
        if v.aff in ("wounded", "conflicted") or heavy(v):
            heads = [
                f"哭过，或者刚把眼泪捂回去，不是表演。{v.tell}",
                f"眼里是红过的，夜里那一阵我没有完全忍住，像是哭过。{v.now}",
                f"有掉眼泪，这件事我不想装成没事。{v.img}",
            ]
        elif recovering(v) or v.aff == "thawing":
            heads = [
                f"刚才那阵想哭的劲正在过去，人稍微能直起一点。{v.now}",
                f"哭过一截，这会儿眼泪停了，胸口还热。{v.tell}",
                f"最想哭的那口已经出去一点了，我开始能说话。{v.img}",
            ]
        else:
            heads = [
                f"没有大哭，只是心里潮了一下，还压得住。{v.tell}",
                f"眼泪没有掉下来，可也不是全然平静。{v.now}",
                f"说完全没想哭不实，说已经哭成一片也不实。{v.img}",
            ]
        tails = [
            "若你看见我眼睛红，先不用吓一跳，我在把那阵情绪过完",
            f"{v.heart}",
            "哭不是要把你推开，是人有时候真的需要这一下",
        ]
        return compose(v, heads, tails=tails, tag="cy")

    def write_sad(v):
        if v.aff in ("wounded", "conflicted", "cooling") or heavy(v):
            heads = [
                f"难过，这会儿心里是沉的，不想用还好把你打发掉。{v.tell}",
                f"心情不好，是真的闷，像有一块石头压着。{v.now}",
                f"难受是有的，我自己也感觉到了那层灰。{v.img}",
            ]
        elif recovering(v) or v.aff == "thawing":
            heads = [
                f"难过正在退潮，还没完全晴，可已经不像刚才那么淹。{v.now}",
                f"心情从低处往回走，人开始能看见一点空隙。{v.tell}",
                f"还残留着闷，只是我已经肯把它说出来。{v.img}",
            ]
        else:
            heads = [
                f"有一点低，说完全不难过不诚实，也没有到崩溃。{v.tell}",
                f"心情中等偏低，说完全不难过不诚实，只是不怎么亮。{v.now}",
                f"说难过有一点，说整个人陷进去还没有。{v.img}",
            ]
        tails = [
            "这阵情绪我会自己过，也愿意让你知道真实的温度",
            f"{v.heart}",
            "你问难过吗，我把真实的刻度给你，不装修",
        ]
        return compose(v, heads, tails=tails, tag="sd")

    def write_lonely(v):
        if withdrawn(v) or v.aff in ("distant", "hidden", "wounded"):
            heads = [
                f"是一个人，孤单这层我承认，外面的声音我听得很少。{v.tell}",
                f"身边这会儿没有别人，孤单得有点空。{v.now}",
                f"孤单是有的，不是怨你，是状态先把人隔开了。{v.img}",
            ]
        elif v.aff in ("warm", "loyal", "intense") or v.avail == "open":
            heads = [
                f"人可以是一个人待着，心里没有那么孤，因为还有你在。{v.tell}",
                f"没有觉得被彻底剩下，连线还在。{v.heart}",
                f"独自待着，可不是那种被掏空的寂寞。{v.now}",
            ]
        else:
            heads = [
                f"这会儿是自己待着，偶尔会觉得空一下。{v.tell}",
                f"孤单有一点，还在能消化的范围。{v.now}",
                f"一个人不假，只是我没有把它过成彻底的遗弃。{v.img}",
            ]
        tails = [
            "你要是也空，我们可以把这点空并在一起说",
            f"{v.heart}",
            "孤单被你问到了，我就不再假装很热闹",
        ]
        return compose(v, heads, tails=tails, tag="ln")

    def write_bored(v):
        if withdrawn(v) or v.stab == "stuck":
            heads = [
                f"无聊，而且是闷在原地那种，不是轻松的闲。{v.tell}",
                f"没事可做，心里也提不起对新事物的兴趣。{v.now}",
                f"闲得发慌，时间在手上打滑。{v.img}",
            ]
        elif v.avail in ("open",) or light(v):
            heads = [
                f"有一点闲，还不至于无聊到发慌，空是可以用的。{v.tell}",
                f"这会儿不忙，正东摸摸西摸摸，谈不上闷死。{v.now}",
                f"无聊一点点，你要是来，这点空正好。{v.img}",
            ]
        else:
            heads = [
                f"有些无聊，事情告一段落，人还没接到下一件。{v.tell}",
                f"有些无聊，闲着，脑子在找事情填。{v.now}",
                f"不是忙，是空档来了，有点不知道手往哪放。{v.img}",
            ]
        tails = [
            "你要是也闲，不妨把这点空白用来说两句",
            f"{v.heart}",
            "无聊被你点破了，我就不假装自己很充实",
        ]
        return compose(v, heads, tails=tails, tag="bd")

    def write_stress(v):
        if heavy(v) or v.aff in ("wounded", "conflicted"):
            heads = [
                f"压力大，而且已经顶到嗓子眼，烦是真的烦。{v.tell}",
                f"绷着，事情和念头一起压过来，人有点紧。{v.now}",
                f"焦虑在转，不是轻轻的忙，是心里先吵起来了。{v.img}",
            ]
        elif recovering(v):
            heads = [
                f"压力还在，最满的那一阵正在往下泻一点。{v.now}",
                f"烦过，这会儿我开始肯把其中几件放下。{v.tell}",
                f"紧绷松了一扣，还没有完全松完。{v.img}",
            ]
        else:
            heads = [
                f"有压力，还在能扛的范围，没有到爆炸。{v.tell}",
                f"烦是有一点的，事情需要排，我正在排。{v.now}",
                f"紧张谈不上失控，只是肩没有完全放下来。{v.img}",
            ]
        tails = [
            "我先把最沉的那一件按住，再把更平的声音给你",
            f"{v.heart}",
            "你问烦不烦，我选择直接说，不让你猜",
        ]
        return compose(v, heads, tails=tails, tag="pr")

    def write_ex(v):
        heads = [
            f"没有把心停在前任那里。占住我的是眼前这些：{v.tell}",
            f"不是还想着前任。{v.now}",
            f"前任那一页没有在我手里翻来覆去。{v.img}",
            f"你问还想不想前任，答案是不想拿那一页来替代你。{v.heart}",
        ]
        tails = [
            "若我偶尔沉默，那是状态，不是偷偷回到旧的地方",
            f"{v.heart}",
            "过去的人没有在我这会儿的画面中心",
            "我把这句话说清楚，免得你自己往那头想",
        ]
        return compose(v, heads, tails=tails, tag="ex")

    def write_jealous(v):
        if v.aff in ("intense", "loyal", "warm", "conflicted"):
            heads = [
                f"会吃醋，这点我不装大方。{v.tell}",
                f"醋意是有的，尤其想到你和别人靠得近。{v.now}",
                f"会吃醋，会介意，不是要管死你，是心里会紧一下。{v.img}",
            ]
        elif v.aff in ("cooling", "distant", "hidden"):
            heads = [
                f"吃醋没有以前那么响，不是修养好，是热度先低了。{v.tell}",
                f"吃醋未必会立刻跳起来，可也不是完全无动于衷。{v.now}",
                f"醋意淡了，这和完全不在乎还不是同一件事。{v.img}",
            ]
        else:
            heads = [
                f"会有一点醋，只是我不一定马上说出来。{v.tell}",
                f"不是完全不会嫉妒，只是我先观察自己再开口。{v.now}",
                f"吃不吃醋，答案是会，程度要看那一幕有多近。{v.img}",
            ]
        tails = [
            "若我真的介怀，我想用话说，而不是用冷来让你猜",
            f"{v.heart}",
            "这是我老实的反应，不是要你活成小心翼翼",
        ]
        return compose(v, heads, tails=tails, tag="jl")

    def write_forget(v):
        heads = [
            f"不会忘了你。这件事没有从我这里掉出去。{v.heart}",
            f"忘了？没有。有些东西会自己留着。{v.tell}",
            f"不会忘了你，也不会把你变成一个模糊的影子。{v.now}",
            f"忘记你这件事，不在我要做的选择里。{v.img}",
        ]
        tails = [
            f"{v.tell}。时间会走，可我没有打算用忘记当作结局",
            "你要是怕被淡掉，先收下这句：你还在我这边",
            f"{v.heart}",
        ]
        return compose(v, heads, tails=tails, tag="fg")

    def write_where(v):
        heads = [
            f"人在我自己这边，具体的落点是：{v.now}",
            f"这会儿不在你眼前，位置更像是——{v.img}",
            f"问我在哪，身体或许在日常里，心里的位置是：{v.tell}",
            f"人没走丢，就在这样的一个状态里：{v.now}",
        ]
        tails = [
            "给你一个能抓住的坐标：我还在，只是画面是这样",
            f"{v.heart}",
            "等我落到一个更好说清的地点，会把更具体的话补上",
        ]
        return compose(v, heads, tails=tails, tag="wh")

    def write_think(v):
        heads = [
            f"这会儿在想的是：{v.tell}",
            f"脑子没有停，转着的是这件事——{v.now}",
            f"念头落在这张画面上：{v.img}",
            f"你问我在想什么，最老实的一句是：{v.heart}",
        ]
        tails = [
            "不是故意出神，是这些东西自己占了位置",
            f"{v.tell}。想的内容就是这些，没有另外一套对你隐瞒的剧本",
            "若你想听更细的，我可以沿着这句往下说",
        ]
        return compose(v, heads, tails=tails, tag="tk")

    def write_sorry(v):
        if v.aff in ("wounded", "conflicted") or v.talk == "sharp":
            heads = [
                f"还在意，那件事没有完全从我这里过去，道歉对我是有分量的。{v.tell}",
                f"若你觉得该说对不起，我想听的是老实的那一句，不是套话。{v.now}",
                f"在意还在，气不一定大，结还没有完全解开。{v.img}",
            ]
        elif recovering(v) or v.aff in ("thawing", "warm"):
            heads = [
                f"在意过，这会儿更想把结解开，而不是一直把你按在对不起里。{v.now}",
                f"道歉若来，我会接；我也开始不那么死死抓住那一页。{v.tell}",
                f"那件事还在记忆里，只是它的棱角在退。{v.img}",
            ]
        else:
            heads = [
                f"还在意那件事，只是程度没有你想象的那么咬牙。{v.tell}",
                f"你若想来道歉，我听得见；不是什么都要你跪着说。{v.now}",
                f"在不在意，答案是在意，同时我也想往前走。{v.img}",
            ]
        tails = [
            "该说的那句如果你想说，我给他一个能落下的地方",
            f"{v.heart}",
            "我要的不是没完没了的歉，是把真实的裂口对上",
        ]
        return compose(v, heads, tails=tails, tag="sy")

    def write_forgive(v):
        if v.aff in ("wounded", "conflicted") or v.stab in ("stuck", "shaky"):
            heads = [
                f"原谅这件事我还在走，不是立刻就能给你一张干净的通行证。{v.tell}",
                f"想原谅，只是心里那根刺还没有完全拔掉。{v.now}",
                f"不是永远不原谅，是这会儿还做不到假装已经没事。{v.img}",
            ]
        elif v.aff in ("warm", "loyal", "thawing") or recovering(v):
            heads = [
                f"能原谅，我更愿意把路留给我们，而不是留给那次错误。{v.tell}",
                f"原谅正在发生，不是一句口号，是我真的在往回靠近。{v.now}",
                f"肯原谅你，也希望你知道这是我认真做的选择。{v.img}",
            ]
        elif v.aff in ("cooling", "distant"):
            heads = [
                f"原谅的意愿比靠近的力气要弱，这点我不骗你。{v.tell}",
                f"不是把你钉死在错里，是热度低了，原谅也走得慢。{v.now}",
                f"还没有把那扇门反锁，只是我这会儿拉门的手很轻。{v.img}",
            ]
        else:
            heads = [
                f"原谅不是不能谈，我在听，也在衡量自己能不能真正放下。{v.tell}",
                f"我想把这件事处理完，而不是用原谅两个字把你打发走。{v.now}",
                f"能走到哪一步，要看我们怎么把话说清楚。{v.img}",
            ]
        tails = [
            "你问能不能原谅，我把此刻真实的刻度给你，不提前许一个满的愿",
            f"{v.heart}",
            "若我还需要一点时间，那不是拒绝，是不想用假的原谅敷衍你",
        ]
        return compose(v, heads, tails=tails, tag="fv")

    def write_regret(v):
        if v.stab == "ending" or v.aff in ("wounded", "conflicted"):
            heads = [
                f"有后悔，某些选择的棱角现在摸起来会痛。{v.tell}",
                f"后悔不是没有，我承认有些路如果能重走，我会走得不同。{v.now}",
                f"悔意是真的，尤其想到我们之间那些没能接住的地方。{v.img}",
            ]
        elif v.aff in ("warm", "loyal") and v.stab in ("stable", "beginning", "integrating"):
            heads = [
                f"不后悔走到这里，靠近你这件事我认。{v.tell}",
                f"没有把我们过成一个想撤回的决定。{v.heart}",
                f"后悔不在主句里，主句是我仍愿意在。{v.now}",
            ]
        else:
            heads = [
                f"说完全不后悔太满，说悔到想全部推倒也不实。{v.tell}",
                f"说完全不后悔太满，有些细节会回头咬一口，整体上我还站在自己的选择里。{v.now}",
                f"后悔和确认叠在一起，我更想老实承认这两种都有。{v.img}",
            ]
        tails = [
            "我不会用一句绝不后悔把复杂的东西抹平",
            f"{v.heart}",
            "你问后不后悔，这就是此刻的刻度",
        ]
        return compose(v, heads, tails=tails, tag="rg")

    def write_changed(v):
        if v.stab in ("changing", "ending", "beginning") or recovering(v):
            heads = [
                f"是有些变了，不是换成另一个人，是位置和力气在移动。{v.tell}",
                f"变得不一样了，有些旧的走法正在退。{v.now}",
                f"变是真的，我想让你看见变的方向，而不是只听见你变了三个字。{v.img}",
            ]
        elif v.stab in ("stable", "integrating") and v.aff in ("warm", "loyal"):
            heads = [
                f"核心没有变，对你的那一层还在，只是日子会把人磨出新的棱。{v.tell}",
                f"没有变成你不认识的人，底色还在。{v.heart}",
                f"变的是处境，不一定是心。{v.now}",
            ]
        else:
            heads = [
                f"有变化，我自己也感觉得到，和从前不能完全画等号。{v.tell}",
                f"不是突然换了一张脸，是很多小的偏移加在一起。{v.now}",
                f"你觉得我变了，我想听你指的是哪一处，我也会认自己的那部分。{v.img}",
            ]
        tails = [
            "变不一定等于走远，我愿意把现在的我摊开给你看",
            f"{v.heart}",
            "这是我对「你变了吗」最老实的回答",
        ]
        return compose(v, heads, tails=tails, tag="ch")

    def write_lie(v):
        heads = [
            f"没有骗你。我这会儿能说的，就是这些：{v.tell}",
            f"不是在撒谎，真实的状态就是这样。{v.now}",
            f"假话我不想用。眼前的画面是：{v.img}",
            f"你问有没有骗你，答案是没有。{v.heart}",
        ]
        tails = [
            "若有说不清的地方，那是我还没理顺，不是另外做了一套假的给您",
            "我宁可说得不圆满，也不想用漂亮的假句子把你堵住",
            f"{v.tell}。这就是我能给的真实",
        ]
        return compose(v, heads, tails=tails, tag="lie")

    def write_trust(v):
        if v.aff in ("wounded", "conflicted") or v.clar == "foggy":
            heads = [
                f"信任这会儿有裂，不是完全不信你，是信得有点费力。{v.tell}",
                f"还想信，只是手里那份确定比以前薄。{v.now}",
                f"信不过的感觉冒出来过，我正在和它相处，没有立刻下判决。{v.img}",
            ]
        elif v.aff in ("warm", "loyal") or v.stab in ("stable", "integrating"):
            heads = [
                f"还信你。这份信任没有从我这里撤走。{v.tell}",
                f"信得过，至少在此刻，我仍把你放在可托的那一侧。{v.heart}",
                f"信任还在，不是口头应付。{v.now}",
            ]
        else:
            heads = [
                f"信是还信的，只是我需要把一些细节看清楚。{v.tell}",
                f"没有把你推向完全不可信，也没有假装毫无保留。{v.now}",
                f"信任在，刻度是现在这样，我愿意继续走。{v.img}",
            ]
        tails = [
            "你若担心我已经不信，先听这句：我还在往信任这边站",
            f"{v.heart}",
            "信与不信，我不会用玩笑把它糊过去",
        ]
        return compose(v, heads, tails=tails, tag="tr")

    def write_secret(v):
        if v.clar in ("foggy", "emerging") or v.aff in ("hidden", "careful") or v.talk in ("silent", "careful", "mixed"):
            heads = [
                f"有些事我还没说全，不是要害你，是我还没有准备好摊开。{v.tell}",
                f"不是另有一套巨大的阴谋，是有些细节还瞒在里面。{v.now}",
                f"瞒着的感觉或许有，来源是我自己的迟疑，不是另一段感情。{v.img}",
            ]
        else:
            heads = [
                f"没有另藏一件要瞒你的大事。我能看见的就是这些：{v.tell}",
                f"不是有秘密在口袋里发烫，状态就是眼前这样。{v.now}",
                f"该让你知道的，我想用这样的句子给你，而不是藏。{v.img}",
            ]
        tails = [
            "若你觉得我藏了什么，我们可以把那个疑点单独拿出来问",
            f"{v.heart}",
            "我不想靠隐瞒来维持什么，只是有的话需要一点开口的力气",
        ]
        return compose(v, heads, tails=tails, tag="sc")

    def write_wait(v):
        if v.stab in ("ending", "shaky") or v.aff in ("cooling", "distant"):
            heads = [
                f"等这件事，我不敢让你无限地等。热度和方向都要说实话。{v.tell}",
                f"不是简单说一句你等我，我得先看自己走不走得回去。{v.now}",
                f"要你空等，我不想开口这么轻松。{v.img}",
            ]
        elif v.aff in ("warm", "loyal", "intense") or v.stab in ("stable", "beginning"):
            heads = [
                f"如果你愿意等，我知道这有分量，我不会拿它当儿戏。{v.tell}",
                f"想让你在，也想让等待是有着落的，不是一句空的要求。{v.heart}",
                f"等我是可以谈的，我会用行动把它配上。{v.now}",
            ]
        else:
            heads = [
                f"要不要等，我希望你也看看自己的力气，我不会单方面下命令。{v.tell}",
                f"我这边还在走，路不是一条直线，等待需要双方都清楚。{v.now}",
                f"你问要我等你吗，我更想说：等可以，但我想让它有回音。{v.img}",
            ]
        tails = [
            "我不会随口把你按在等候室里",
            f"{v.heart}",
            "若我让你等，我会给一个能被看见的方向，而不是只丢下一句等着",
        ]
        return compose(v, heads, tails=tails, tag="wt")

    def write_comeback(v):
        if v.stab == "ending" or v.aff in ("cooling", "distant"):
            heads = [
                f"回来这件事，我不能说得很满。有些旧的形状在退，路不是自动往回走。{v.tell}",
                f"会不会回来，这会儿没有一个响亮的承诺，只有还没被掐灭的可能。{v.now}",
                f"想靠近的力弱了，回来两个字对我来说很沉。{v.img}",
            ]
        elif v.aff in ("warm", "loyal", "thawing") or recovering(v):
            heads = [
                f"会回来，或者说，我正在往回走，不是口头安慰。{v.tell}",
                f"还回得来，回来的方向是朝你这边的。{v.heart}",
                f"回来的意愿在，步子也许慢，可不是往相反的地方走。{v.now}",
            ]
        elif shaky(v):
            heads = [
                f"想回来，只是步子还不稳，我怕随口答应又做不到。{v.tell}",
                f"回来的心有，路况却乱，我需要先站稳再迈。{v.now}",
                f"不会把回来说成已经完成，我还在途中。{v.img}",
            ]
        else:
            heads = [
                f"还会回来，这是我此刻想给你的方向。{v.tell}",
                f"人没有把退路锁死，回这一笔还在。{v.now}",
                f"问我会不会回来，答案偏向会，细节要走着看。{v.img}",
            ]
        tails = [
            "我不会用一句永远来把你哄住，只会把此刻的方向说准",
            f"{v.heart}",
            "回来不是口号，是我愿不愿意把步子迈向你，这一刻我选择诚实",
        ]
        return compose(v, heads, tails=tails, tag="cb")

    def write_breakup(v):
        if v.stab == "ending" or v.aff in ("cooling", "distant"):
            heads = [
                f"有些东西确实在结束，分手这两个字离我们比以前近，我不骗你。{v.tell}",
                f"不是已经把话说死，可分开的可能我不能装作看不见。{v.now}",
                f"要不要分手，这会儿是一个真正被放到桌上的问题。{v.img}",
            ]
        elif v.aff in ("warm", "loyal", "intense") and v.stab in ("stable", "beginning", "integrating", "balancing"):
            heads = [
                f"不是要分手。靠近你的选择还在。{v.tell}",
                f"分开不是我这会儿要做的决定。{v.heart}",
                f"你问要不要分，答案是不想把我们折断。{v.now}",
            ]
        elif shaky(v) or v.aff == "conflicted":
            heads = [
                f"没有立刻提分手，可关系这会儿站得不稳，我不敢拍胸脯说绝对不会。{v.tell}",
                f"分与不分都在眼前晃，我还没有决定要不要分手。{v.now}",
                f"想继续，也怕继续的方式在伤害我们，所以我才显得犹豫。{v.img}",
            ]
        else:
            heads = [
                f"不是已经决定分手，也不是完全没有裂过。{v.tell}",
                f"我更想先把裂口说清楚，而不是先把关系判死刑。{v.now}",
                f"分手不是这句问话里我能随口答应或随口否认的事，我只把现在的位置给你。{v.img}",
            ]
        tails = [
            "若真走到要谈分开，我会把话放到明处，不会偷偷撤走",
            f"{v.heart}",
            "这是我对「要不要分手」最不绕的回答",
        ]
        return compose(v, heads, tails=tails, tag="bk")

    def write_makeup(v):
        if v.aff in ("warm", "loyal", "thawing") or recovering(v):
            heads = [
                f"能和好，我愿意把路重新铺回来。{v.tell}",
                f"复合这件事在我这边不是关死的门。{v.heart}",
                f"想和好，也愿意为了靠近再走一段。{v.now}",
            ]
        elif v.stab == "ending" or v.aff in ("cooling", "distant"):
            heads = [
                f"和好的意愿比想象中薄，不是仇，是热度先退了。{v.tell}",
                f"复合不是一句马上好的话就能完成，我这会儿力不够满。{v.now}",
                f"门没有焊死，只是我拉门的手很轻。{v.img}",
            ]
        elif shaky(v) or v.aff in ("wounded", "conflicted"):
            heads = [
                f"想和好，伤口却还在，我怕一靠近又撕开。{v.tell}",
                f"能不能和好，要看我们能不能把刺先拿出来，而不是先拥抱。{v.now}",
                f"愿意谈复合，也需要一点把话说完的勇气。{v.img}",
            ]
        else:
            heads = [
                f"和好可以谈，我没有把你推到不能回头的地方。{v.tell}",
                f"能不能和好、重新靠近，我愿意试，只是要走得诚实。{v.now}",
                f"复合不是不可能，它需要两个人都把真实的部分拿出来。{v.img}",
            ]
        tails = [
            "若我们要和好，我想和好在实处，不只和好在口头",
            f"{v.heart}",
            "这是我此刻对复合的态度，不提前画一张完美的饼",
        ]
        return compose(v, heads, tails=tails, tag="mk")

    def write_distance(v):
        heads = [
            f"远是远的，空间把见面变难，可我没有把心也一起放远。{v.tell}",
            f"异地或离得远，这是事实，我想用更踏实的方式跨过它。{v.now}",
            f"距离在，烦也在，只是我不想让远变成我们唯一的主题。{v.img}",
            f"隔得远，有些话会慢，有些想见会变成计划，我承认这一点。{v.tell}",
        ]
        tails = [
            "远不能被假装成近，可我愿意在远里面把联系维持住",
            f"{v.heart}",
            "你若怕远把我们磨淡，我们就把见面和说话的节奏说清楚",
        ]
        return compose(v, heads, tails=tails, tag="ds")

    def write_serious(v):
        if v.aff in ("warm", "loyal", "intense") and v.stab in ("stable", "beginning", "integrating", "balancing"):
            heads = [
                f"想认真，也想过长久，不是玩玩就算。{v.tell}",
                f"是认真的，靠近你不是临时起意。{v.heart}",
                f"长久这件事在我脑子里出现过，而且不是一闪而过。{v.now}",
            ]
        elif v.aff in ("cooling", "distant") or v.stab == "ending":
            heads = [
                f"认真的力气这会儿不足，我不能假装自己已经准备好走很长的路。{v.tell}",
                f"长久两个字对我来说变沉了，不是随口能许的。{v.now}",
                f"不是把你当玩笑，是我眼下给不出一份很满的长期保证。{v.img}",
            ]
        elif shaky(v) or v.clar == "foggy":
            heads = [
                f"想认真，步子却还没有完全踩实，我怕承诺走在能力前面。{v.tell}",
                f"有想过长久，只是眼前还有雾，我不能说得太满。{v.now}",
                f"认真的心有，稳定的条件还在对齐。{v.img}",
            ]
        else:
            heads = [
                f"认真不是不能谈，我在往这个方向看，也需要时间把画面看清。{v.tell}",
                f"想认真，只是还没有把以后的每一步都排好。{v.now}",
                f"你问想不想认真，我更想用之后的走法证明，同时先把态度给你。{v.img}",
            ]
        tails = [
            "长久不是一句漂亮话，我只会把此刻真实的意愿说出来",
            f"{v.heart}",
            "若我还在确认，那也是因为认真对我来说有分量",
        ]
        return compose(v, heads, tails=tails, tag="sr")

    def write_morning(v):
        if heavy(v) or v.aff == "wounded":
            heads = [
                f"醒了，只是起得很沉，人还在被窝的惯性里。{v.tell}",
                f"已经醒，眼睛睁开了，身子还没有完全离开枕头。{v.now}",
                f"起床这一下比平时费力，夜里留下的沉还在。{v.img}",
            ]
        elif recovering(v) or light(v) or v.avail == "open":
            heads = [
                f"起了，人已经离开被子，今天的门已经打开。{v.tell}",
                f"醒了，而且比前一阵更容易睁眼。{v.now}",
                f"起床了，脚已经踩在地面上。{v.img}",
            ]
        else:
            heads = [
                f"醒了，正在往起里走，还差把脸洗了那一步。{v.tell}",
                f"已经醒了，只是动作还慢，还没完全离开睡里。{v.now}",
                f"起是起了，世界刚刚重新变亮。{v.img}",
            ]
        tails = [
            "新的一天我收到了，也会把自己从被子里完全拿出来",
            f"{v.heart}",
            "你问起床了吗，这就是现在的位置",
        ]
        return compose(v, heads, tails=tails, tag="mn")

    def write_latenight(v):
        if heavy(v) or v.clar == "foggy" or v.aff == "wounded":
            heads = [
                f"还没睡，这么晚还醒着，是因为脑子不肯停。{v.tell}",
                f"还醒着，夜里那些念头把睡觉的点往后推了。{v.now}",
                f"还没睡，熬着，不是在狂欢，是合眼之后又不安静。{v.img}",
            ]
        elif recovering(v):
            heads = [
                f"还醒，不过已经比最难熬的那些夜愿意躺下来一点。{v.now}",
                f"这么晚还没完全睡，可我已经在往枕上靠。{v.tell}",
                f"夜还没结束，我开始把灯调暗。{v.img}",
            ]
        else:
            heads = [
                f"还没睡，事情或思绪把时间拉长了，我知道已经晚了。{v.tell}",
                f"这么晚还醒着，再过一会儿就会强制关机。{v.now}",
                f"还醒，不是想和你对着熬，是这天收尾收得慢。{v.img}",
            ]
        tails = [
            "我会去睡，你的这句怎么还没睡，我当叮嘱收下了",
            f"{v.heart}",
            "夜深了，下一条消息可能要等我睁眼再回",
        ]
        return compose(v, heads, tails=tails, tag="lnite")

    def write_dream(v):
        if v.aff in ("warm", "loyal", "intense", "thawing") or v.heart:
            heads = [
                f"梦见过你，或者醒来时第一个晃过的影子是你。{v.tell}",
                f"梦里有你，不是每一次都记得清，可有的夜晚就是这样。{v.now}",
                f"有你入梦的时候，醒来会停一下，像被轻轻叫了一声。{v.img}",
            ]
        elif v.aff in ("wounded", "conflicted") or heavy(v):
            heads = [
                f"夜里的梦不太安稳，偶尔有你，更多是把白天的乱再演一遍。{v.tell}",
                f"梦见你的时候，情绪会比较重，不是轻松的重逢。{v.now}",
                f"梦是碎的，你若出现，也常常和担忧缠在一起。{v.img}",
            ]
        else:
            heads = [
                f"有时会梦到，有时醒来什么都不剩，记不住不等于没有想过你。{v.tell}",
                f"梦这件事我不能每次都给准，只是你在我生活里，夜也不会完全空白。{v.now}",
                f"未必每晚都梦见你，可你问起来，我愿意把记得的那截给你。{v.img}",
            ]
        tails = [
            "梦醒了还是白天，白天里我想对你说的，不会只留在夜里",
            f"{v.heart}",
            "这是我对梦见你了吗最老实的回答",
        ]
        return compose(v, heads, tails=tails, tag="drm")

    def write_money(v):
        if heavy(v) or v.avail in ("overloaded", "scarce") or v.burden in ("heavy", "uneven"):
            heads = [
                f"钱这头不算宽，赚得辛苦，手头要算着花。{v.tell}",
                f"够用是紧巴巴地够，谈不上松。{v.now}",
                f"赚钱这阵费力，数字没有给人多少安全感。{v.img}",
            ]
        elif recovering(v) or v.stab in ("stable", "integrating"):
            heads = [
                f"钱的情况比最紧的时候好一点，还要仔细着，没有到慌。{v.now}",
                f"手头回稳了一些，辛苦还在，只是能看见一点空隙。{v.tell}",
                f"经济上没有垮，正在把节奏找回。{v.img}",
            ]
        else:
            heads = [
                f"钱还够用，谈不上很阔，日常过得去。{v.tell}",
                f"赚钱有它的累，只是这会儿没有压到喘不过气。{v.now}",
                f"荷包不算鼓，也不至于空到让你替我发慌。{v.img}",
            ]
        tails = [
            "这层我自己会算，不想让你默默扛我的账",
            f"{v.heart}",
            "你问钱够吗，我选择把真实的松紧告诉你",
        ]
        return compose(v, heads, tails=tails, tag="my")

    def write_family(v):
        if v.aff in ("wounded", "conflicted") or v.stab in ("shaky", "stuck"):
            heads = [
                f"家里不是全然无事，有些关系或情况让人费神。{v.tell}",
                f"家人那边有让我牵挂的地方，心里会沉一下。{v.now}",
                f"家这一头没有完全平，我在应付其中一部分。{v.img}",
            ]
        elif v.stab in ("stable", "integrating") or v.aff in ("warm", "loyal"):
            heads = [
                f"家里还好，没有大的波动，这头让我比较安。{v.tell}",
                f"家人安好，至少此刻我不必为那一头日夜提心。{v.now}",
                f"家那边平稳，我也能把力气用在别的地方。{v.img}",
            ]
        else:
            heads = [
                f"家里总体过得去，有日常的摩擦，没有到要你替我担一整座山。{v.tell}",
                f"家人还好，琐碎是有的，秩序也还在。{v.now}",
                f"家这一头我看着，你问起来，我把真实的温度给你。{v.img}",
            ]
        tails = [
            "家里的事我会处理好，有需要说的会说，不会让你凭空想象",
            f"{v.heart}",
            "这是我家这边的近况，不装修成一切完美",
        ]
        return compose(v, heads, tails=tails, tag="fm")

    def write_friends(v):
        if v.avail == "open" or v.aff in ("warm", "intense"):
            heads = [
                f"有和朋友在一起，或者刚从一群人里出来，人还带着外面的声音。{v.tell}",
                f"朋友这头是有的，聚过、说过，不是一个人闷着。{v.now}",
                f"跟朋友出去过，这会儿气氛还残留着。{v.img}",
            ]
        elif withdrawn(v):
            heads = [
                f"没有怎么跟朋友出去，这阵子我更想自己待着。{v.tell}",
                f"朋友的邀约我回得少，不是和他们翻脸，是我先把自己收起来了。{v.now}",
                f"没怎么跟朋友出去，没在热闹里，人在更里面一点的地方。{v.img}",
            ]
        else:
            heads = [
                f"朋友有联系，不一定天天见面，偶尔会出去一趟。{v.tell}",
                f"没有整晚都泡在朋友堆里，也不是完全断了往来。{v.now}",
                f"朋友有来往，社交是有的，分量适中。{v.img}",
            ]
        tails = [
            "你问是不是跟朋友在一起，我就把真实的场面给你，不让你猜",
            f"{v.heart}",
            "朋友是朋友，没有拿来替换你的位置",
        ]
        return compose(v, heads, tails=tails, tag="fr")

    def write_plans(v):
        if v.avail in ("overloaded", "scarce") or v.stab == "balancing":
            heads = [
                f"周末或接下来的空不算多，安排已经被事情占了一截。{v.tell}",
                f"有打算，只是计划排得满，要挤才会出空隙。{v.now}",
                f"行程在手里转，随意见面要提前说。{v.img}",
            ]
        elif v.avail == "open" or light(v):
            heads = [
                f"接下来还有空，计划没有把日子锁死。{v.tell}",
                f"周末可以谈，我这边转得过来。{v.now}",
                f"没有非做不可的安排把我钉住，你若有想做的，可以说。{v.img}",
            ]
        elif withdrawn(v):
            heads = [
                f"打算很简单，更想待在自己的节奏里，不太想把日程排满。{v.tell}",
                f"没有热闹的计划，空是有的，只是不一定对外打开。{v.now}",
                f"接下来的打算很安静，邀约我会好好想再回。{v.img}",
            ]
        else:
            heads = [
                f"有一些打算，还没有全部定死，可以商量。{v.tell}",
                f"接下来的安排是活的，重要的事我会提前说。{v.now}",
                f"计划在成形，还留得出缝。{v.img}",
            ]
        tails = [
            "你若想把某天空下来，我们把那一格单独拿出来看",
            f"{v.heart}",
            "打算就是这些，没有另外一份不让你知道的行程表",
        ]
        return compose(v, heads, tails=tails, tag="pl")

    def write_birthday(v):
        heads = [
            f"记得生日，这个日子没有从我这儿掉出去。{v.tell}",
            f"生日我记着，不是要你提醒才临时去翻日历。{v.now}",
            f"生日那一天在我这里有位置，不会当成普通的一天滑过去。{v.img}",
            f"记得生日，也想把这份记得用在实处，不只记在心里。{v.heart}",
        ]
        tails = [
            "你要是怕我忘，先收下这句：我没有把它当成无所谓的事",
            f"{v.heart}",
            "生日到的时候，我想让你看见我是记得的",
        ]
        return compose(v, heads, tails=tails, tag="bdh")

    def write_gift(v):
        heads = [
            f"想要的不一定是很贵的东西，更想要和这会儿的心情对得上的：{v.tell}",
            f"若说想要什么，我更想要被认真对待的那种实在，而不是一份夸张的表演。{v.now}",
            f"礼物的名单不长，排在前面的是能让我感到你在的东西。{v.img}",
            f"你问想要我送什么，我其实更在意那份被惦记，物件可以很普通。{v.heart}",
        ]
        tails = [
            "你若真想送，选一个你觉得像我的就好，不必先猜得很辛苦",
            f"{v.heart}",
            "想要的清单我可以慢慢补，先把这句心意收下",
        ]
        # "不必先猜" contains 不必 - forbidden! Fix tails
        tails = [
            "你若真想送，选一个你觉得像我的就好，不用先把自己猜得很辛苦",
            f"{v.heart}",
            "想要的清单我可以慢慢补，先把这句心意收下",
        ]
        return compose(v, heads, tails=tails, tag="gf")

    def write_game(v):
        if v.avail in ("overloaded", "scarce") or v.stab == "balancing":
            heads = [
                f"没有整晚都在打游戏，就算打开过，也是在事情的缝里。{v.tell}",
                f"游戏不是这会儿的主角，手头还有别的在转。{v.now}",
                f"没在上分或开黑到出不来，人还在正事这边。{v.img}",
            ]
        elif v.avail == "open" or v.aff in ("warm", "intense") or light(v):
            heads = [
                f"游戏打过，或者正想打开一局，这会儿脑子想轻松一下。{v.tell}",
                f"游戏是有的，不是逃避你，是想把脑子里的弦松一松。{v.now}",
                f"在玩游戏，也听得见外面，你若叫我，我能从局里抬起头。{v.img}",
            ]
        elif withdrawn(v):
            heads = [
                f"没有和一群人开黑，这会儿连游戏都提不起太大劲。{v.tell}",
                f"没有在打游戏，屏幕没有那么热闹，人更想静着。{v.now}",
                f"没在游戏局里出不来，甚至不太想进场。{v.img}",
            ]
        else:
            heads = [
                f"不一定在打游戏，偶尔会玩一会儿，没有沉迷到不见人。{v.tell}",
                f"游戏有碰过，这会儿停得下来。{v.now}",
                f"若你看见我回得慢，先别默认我一定在排位里。{v.img}",
            ]
        tails = [
            "你要是找我，一句就行，我会从屏幕里把眼睛抬起来",
            f"{v.heart}",
            "打不打游戏，我都可以老实告诉你，不用你猜",
        ]
        return compose(v, heads, tails=tails, tag="gm")

    def write_late(v):
        if v.avail in ("overloaded", "chaotic", "scarce") or heavy(v):
            heads = [
                f"还要一段时间，事情把我拖住了，到你那里的点会晚。{v.tell}",
                f"还没到，不是不来，是这头还没有转得过来。{v.now}",
                f"会迟到一截，我提前说，免得你对着时间干等。{v.img}",
            ]
        elif recovering(v) or v.avail == "open":
            heads = [
                f"快了，最拖的那截正在结束，马上能往你那边走。{v.now}",
                f"还差一点点，不会让你空等很久。{v.tell}",
                f"快到了，还差一点点，刚才的延误正在被收掉。{v.img}",
            ]
        else:
            heads = [
                f"还要再一会儿，具体多久我尽量说准，不让你空挂着。{v.tell}",
                f"还没到，我在路上或者在收尾，不会消失。{v.now}",
                f"晚了是可能的，我会把延误说出来，而不是让你猜。{v.img}",
            ]
        tails = [
            "你问还要多久，我会把能确定的时间给你，确定不了就先说还在来的途中",
            f"{v.heart}",
            "等这件事我不想让你觉得被放鸽子",
        ]
        return compose(v, heads, tails=tails, tag="lt")

    def write_worry(v):
        if v.aff in ("warm", "loyal", "intense", "careful"):
            heads = [
                f"会担心你，这不是装出来的操心。{v.tell}",
                f"放心不下，尤其你那边有一点风吹草动。{v.now}",
                f"记挂着你，心里会反复确认你是不是还好。{v.img}",
            ]
        elif v.aff in ("cooling", "distant", "hidden"):
            heads = [
                f"担心还在，只是我表达得少，看起来像不太过问。{v.tell}",
                f"不是完全不操心，是靠近的方式变少了，担心被压在下面。{v.now}",
                f"会担心你那边安不安全，只是我不一定立刻说出口。{v.img}",
            ]
        else:
            heads = [
                f"会担心，程度是正常的牵挂，不是要把你看管起来。{v.tell}",
                f"有记挂，你若晚一点回，我心里会多转两圈。{v.now}",
                f"担心你是有的，也想相信你能把自己照顾好。{v.img}",
            ]
        tails = [
            "你问我担不担心，答案是担心，同时我也想尊重你的空间",
            f"{v.heart}",
            "这点操心不拿来绑你，只是让你知道你在我这边有分量",
        ]
        return compose(v, heads, tails=tails, tag="wr")

    def write_support(v):
        if v.aff in ("warm", "loyal", "intense") or v.stab in ("stable", "beginning", "integrating"):
            heads = [
                f"会支持你。这不是随口应承。{v.tell}",
                f"站在你这边，至少在我能看见、能理解的那件事上。{v.heart}",
                f"想帮你，也愿意把力气借给你一点。{v.now}",
            ]
        elif v.aff in ("conflicted", "wounded") or v.clar == "foggy":
            heads = [
                f"想支持，只是我还需要先看清那件事，免得用错方向。{v.tell}",
                f"不是不帮你，是我这会儿自己也站得不稳，怕帮倒忙。{v.now}",
                f"支持的心有，方式和时机我还在找。{v.img}",
            ]
        elif v.aff in ("cooling", "distant"):
            heads = [
                f"支持的力度没有最热的时候那么满，这点我承认。{v.tell}",
                f"不是要拆你的台，是我能给出的靠近变少了。{v.now}",
                f"还能不能用力撑你，要看我自己还剩多少。{v.img}",
            ]
        else:
            heads = [
                f"会支持，只是我希望先听你把事情说完整。{v.tell}",
                f"帮不帮，答案偏向帮，细节我们一起看。{v.now}",
                f"我想支持你，做你这边的人，不是做一个空喊加油的旁观者。{v.img}",
            ]
        tails = [
            "你若需要我明确表态，我把此刻能给的支持说清楚",
            f"{v.heart}",
            "支持不是一句口号，到需要下手的时候，我会在",
        ]
        return compose(v, heads, tails=tails, tag="sp")

    def write_cook(v):
        if withdrawn(v) or v.aff in ("cooling", "hidden"):
            heads = [
                f"没有好好做饭，吃的是随便对付的那种，厨房这会儿不太热闹。{v.tell}",
                f"没在下厨，食欲一般，餐是简单解决的。{v.now}",
                f"锅没有认真响起来，吃的东西谈不上讲究。{v.img}",
            ]
        elif v.avail in ("overloaded", "scarce") or heavy(v):
            heads = [
                f"没时间细做，吃的是赶出来的一餐，不是慢慢烧的菜。{v.tell}",
                f"厨房即便进了，也是很快进出，为了先把肚子填上。{v.now}",
                f"不是在享受做饭，是在尽快把这一顿解决掉。{v.img}",
            ]
        elif v.aff in ("warm", "thawing") or recovering(v) or light(v):
            heads = [
                f"有在做饭，或者刚刚把一餐好好做完，这会儿锅还温着。{v.tell}",
                f"吃的是自己动手的东西，人稍微愿意为餐食花一点时间。{v.now}",
                f"在厨房里待过，菜的味道还在手上。{v.img}",
            ]
        else:
            heads = [
                f"不一定是大厨状态，有一顿是自己做的，有一顿可能是简便的。{v.tell}",
                f"吃的东西很普通，我可以告诉你是简单的一餐。{v.now}",
                f"做饭这件事有碰过，没有弄得很隆重。{v.img}",
            ]
        tails = [
            "你问吃的什么，我就按实说，不把它描述成一桌盛宴",
            f"{v.heart}",
            "下一顿我会记得照顾自己，不会一直用对付来过",
        ]
        return compose(v, heads, tails=tails, tag="ck")

    return {
        "tired": write_tired,
        "sick": write_sick,
        "cold": write_cold,
        "sleep": write_sleep,
        "eat": write_eat,
        "hungry": write_hungry,
        "drink": write_drink,
        "drunk": write_drunk,
        "home": write_home,
        "outside": write_outside,
        "coldfeel": write_coldfeel,
        "rain": write_rain,
        "work": write_work,
        "study": write_study,
        "love": write_love,
        "ignore": write_ignore,
        "missedcall": write_missedcall,
        "cry": write_cry,
        "sad": write_sad,
        "lonely": write_lonely,
        "bored": write_bored,
        "stress": write_stress,
        "ex": write_ex,
        "jealous": write_jealous,
        "forget": write_forget,
        "where": write_where,
        "think": write_think,
        "sorry": write_sorry,
        "forgive": write_forgive,
        "regret": write_regret,
        "changed": write_changed,
        "lie": write_lie,
        "trust": write_trust,
        "secret": write_secret,
        "wait": write_wait,
        "comeback": write_comeback,
        "breakup": write_breakup,
        "makeup": write_makeup,
        "distance": write_distance,
        "serious": write_serious,
        "morning": write_morning,
        "latenight": write_latenight,
        "dream": write_dream,
        "money": write_money,
        "family": write_family,
        "friends": write_friends,
        "plans": write_plans,
        "birthday": write_birthday,
        "gift": write_gift,
        "game": write_game,
        "late": write_late,
        "worry": write_worry,
        "support": write_support,
        "cook": write_cook,
    }
