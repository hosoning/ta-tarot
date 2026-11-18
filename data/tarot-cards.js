/**
 * 伟特塔罗 78 张完整数据
 * id: 唯一标识
 * name: 中文名
 * nameEn: 英文名
 * suit: major | wands | cups | swords | pentacles
 * number: 0-21 for major, 1-14 for minor (11=侍从,12=骑士,13=王后,14=国王)
 * upright: 正位核心关键词与简要象征
 * reversed: 逆位核心关键词与简要象征
 * themes: 适合的主题标签
 */
const TAROT_CARDS = [
  // ========== 大阿尔卡纳 ==========
  {
    id: "major-0",
    name: "愚者",
    nameEn: "The Fool",
    suit: "major",
    number: 0,
    upright: { keywords: ["新开始", "纯真", "冒险", "信任"], meaning: "轻装上阵，凭直觉踏入未知。充满可能性的起点。" },
    reversed: { keywords: ["犹豫", "鲁莽", "逃避", "准备不足"], meaning: "迟迟不敢迈步，或行动过于轻率，忽略潜在风险。" },
    themes: ["想念", "未来期待", "自由提问", "关系状态"]
  },
  {
    id: "major-1",
    name: "魔术师",
    nameEn: "The Magician",
    suit: "major",
    number: 1,
    upright: { keywords: ["创造", "意志", "资源", "显化"], meaning: "手中资源充足，主动将意愿化为现实。" },
    reversed: { keywords: ["空谈", "操控", "分散", "缺乏计划"], meaning: "想法停留在口头，或资源被误用，缺乏落地。" },
    themes: ["沟通", "约会", "未来期待", "陪伴"]
  },
  {
    id: "major-2",
    name: "女祭司",
    nameEn: "The High Priestess",
    suit: "major",
    number: 2,
    upright: { keywords: ["直觉", "沉静", "潜意识", "等待"], meaning: "安静倾听内心，信息尚未完全显露，保持观察。" },
    reversed: { keywords: ["忽视直觉", "信息封闭", "压抑"], meaning: "忽略内在声音，或重要信息被掩盖。" },
    themes: ["想念", "安慰", "沟通", "关系状态"]
  },
  {
    id: "major-3",
    name: "皇后",
    nameEn: "The Empress",
    suit: "major",
    number: 3,
    upright: { keywords: ["滋养", "丰盛", "关怀", "成长"], meaning: "温柔的照护与丰盛的能量，关系与创造都在生长。" },
    reversed: { keywords: ["过度付出", "停滞", "忽视自己"], meaning: "付出失衡，或创造力与情感暂时枯竭。" },
    themes: ["陪伴", "安慰", "约会", "想念"]
  },
  {
    id: "major-4",
    name: "皇帝",
    nameEn: "The Emperor",
    suit: "major",
    number: 4,
    upright: { keywords: ["秩序", "担当", "稳定", "权威"], meaning: "建立结构与边界，负责任地守护与引领。" },
    reversed: { keywords: ["僵化", "控制", "压力"], meaning: "规则过严或掌控欲过强，带来压迫感。" },
    themes: ["关系状态", "未来期待", "沟通"]
  },
  {
    id: "major-5",
    name: "教皇",
    nameEn: "The Hierophant",
    suit: "major",
    number: 5,
    upright: { keywords: ["传统", "指引", "共同价值", "学习"], meaning: "通过既有智慧与共同信念获得方向。" },
    reversed: { keywords: ["教条", "叛逆", "僵化规则"], meaning: "质疑既定框架，或陷入形式主义。" },
    themes: ["关系状态", "沟通", "未来期待"]
  },
  {
    id: "major-6",
    name: "恋人",
    nameEn: "The Lovers",
    suit: "major",
    number: 6,
    upright: { keywords: ["结合", "选择", "和谐", "价值一致"], meaning: "重要的选择与连接，心与价值的对齐。" },
    reversed: { keywords: ["失衡", "摇摆", "价值冲突"], meaning: "关系或选择出现不一致，需要重新对齐。" },
    themes: ["关系状态", "约会", "想念", "未来期待"]
  },
  {
    id: "major-7",
    name: "战车",
    nameEn: "The Chariot",
    suit: "major",
    number: 7,
    upright: { keywords: ["前进", "意志", "掌控", "胜利"], meaning: "方向明确，以意志推动前行并取得进展。" },
    reversed: { keywords: ["失控", "方向不明", "内耗"], meaning: "力量分散或目标模糊，行动受阻。" },
    themes: ["未来期待", "约会", "沟通"]
  },
  {
    id: "major-8",
    name: "力量",
    nameEn: "Strength",
    suit: "major",
    number: 8,
    upright: { keywords: ["勇气", "耐心", "柔韧", "内在力量"], meaning: "以柔克刚，温柔而坚定地面对挑战。" },
    reversed: { keywords: ["自我怀疑", "压抑", "急躁"], meaning: "信心不足，或情绪与力量暂时失衡。" },
    themes: ["安慰", "陪伴", "想念", "关系状态"]
  },
  {
    id: "major-9",
    name: "隐者",
    nameEn: "The Hermit",
    suit: "major",
    number: 9,
    upright: { keywords: ["内省", "独处", "指引", "沉淀"], meaning: "暂时退一步，在安静中寻找答案与方向。" },
    reversed: { keywords: ["孤立", "逃避", "封闭"], meaning: "过度退缩，或与外界连接不足。" },
    themes: ["想念", "安慰", "关系状态", "自由提问"]
  },
  {
    id: "major-10",
    name: "命运之轮",
    nameEn: "Wheel of Fortune",
    suit: "major",
    number: 10,
    upright: { keywords: ["转机", "周期", "顺势", "变化"], meaning: "局势正在转动，新的阶段即将到来。" },
    reversed: { keywords: ["反复", "阻力", "时机未到"], meaning: "变化受阻，或陷入旧有循环。" },
    themes: ["未来期待", "关系状态", "想念"]
  },
  {
    id: "major-11",
    name: "正义",
    nameEn: "Justice",
    suit: "major",
    number: 11,
    upright: { keywords: ["公平", "因果", "清晰", "责任"], meaning: "事情被如实衡量，真相与平衡浮现。" },
    reversed: { keywords: ["偏见", "失衡", "逃避责任"], meaning: "判断偏颇，或后果尚未被正视。" },
    themes: ["沟通", "关系状态", "自由提问"]
  },
  {
    id: "major-12",
    name: "倒吊人",
    nameEn: "The Hanged Man",
    suit: "major",
    number: 12,
    upright: { keywords: ["换视角", "等待", "放下", "暂停"], meaning: "暂时悬置行动，从不同角度看见新可能。" },
    reversed: { keywords: ["拖延", "无谓牺牲", "抗拒"], meaning: "该动却不动，或付出没有意义。" },
    themes: ["想念", "安慰", "关系状态"]
  },
  {
    id: "major-13",
    name: "死神",
    nameEn: "Death",
    suit: "major",
    number: 13,
    upright: { keywords: ["结束", "转化", "清理", "重生"], meaning: "旧阶段自然落幕，为新事物腾出空间。" },
    reversed: { keywords: ["抗拒结束", "停滞", "拖泥带水"], meaning: "不愿放手，变化被推迟。" },
    themes: ["关系状态", "未来期待", "安慰"]
  },
  {
    id: "major-14",
    name: "节制",
    nameEn: "Temperance",
    suit: "major",
    number: 14,
    upright: { keywords: ["调和", "节奏", "融合", "平衡"], meaning: "不同元素被温柔地调和，找到合适的节奏。" },
    reversed: { keywords: ["失衡", "极端", "失调"], meaning: "节奏被打乱，或过度偏向某一端。" },
    themes: ["陪伴", "沟通", "约会", "安慰"]
  },
  {
    id: "major-15",
    name: "恶魔",
    nameEn: "The Devil",
    suit: "major",
    number: 15,
    upright: { keywords: ["束缚", "欲望", "执念", "阴影"], meaning: "被某种习惯或执念牵制，需要看见真相。" },
    reversed: { keywords: ["松绑", "看清", "释放"], meaning: "开始挣脱束缚，欲望被重新认识。" },
    themes: ["关系状态", "想念", "自由提问"]
  },
  {
    id: "major-16",
    name: "高塔",
    nameEn: "The Tower",
    suit: "major",
    number: 16,
    upright: { keywords: ["崩塌", "冲击", "真相", "瓦解"], meaning: "旧结构突然松动，真相以冲击方式到来。" },
    reversed: { keywords: ["延迟崩塌", "压抑", "隐患"], meaning: "变化被推迟，但压力仍在累积。" },
    themes: ["关系状态", "沟通", "安慰"]
  },
  {
    id: "major-17",
    name: "星星",
    nameEn: "The Star",
    suit: "major",
    number: 17,
    upright: { keywords: ["希望", "修复", "灵感", "平静"], meaning: "在低落后看见光，疗愈与方向感同时回来。" },
    reversed: { keywords: ["信心不足", "失望", "迷失"], meaning: "希望感暂时减弱，需要重新连接内在光亮。" },
    themes: ["安慰", "想念", "未来期待", "陪伴"]
  },
  {
    id: "major-18",
    name: "月亮",
    nameEn: "The Moon",
    suit: "major",
    number: 18,
    upright: { keywords: ["迷雾", "潜意识", "不安", "直觉"], meaning: "路径不清晰，情绪与潜意识浮现，需谨慎前行。" },
    reversed: { keywords: ["迷雾渐散", "恐惧浮现", "逐渐清晰"], meaning: "不确定感开始消退，隐藏的东西慢慢显露。" },
    themes: ["想念", "安慰", "关系状态", "自由提问"]
  },
  {
    id: "major-19",
    name: "太阳",
    nameEn: "The Sun",
    suit: "major",
    number: 19,
    upright: { keywords: ["清晰", "喜悦", "活力", "成功"], meaning: "光芒照亮一切，心情与局势都明朗起来。" },
    reversed: { keywords: ["短暂受挫", "过度乐观", "光芒被遮"], meaning: "喜悦暂时被遮挡，或需要更脚踏实地。" },
    themes: ["约会", "陪伴", "未来期待", "想念"]
  },
  {
    id: "major-20",
    name: "审判",
    nameEn: "Judgement",
    suit: "major",
    number: 20,
    upright: { keywords: ["觉醒", "召唤", "释放", "重新评估"], meaning: "内在呼唤响起，过去被重新审视，准备进入新阶段。" },
    reversed: { keywords: ["自我怀疑", "拒绝改变", "拖延觉醒"], meaning: "听见召唤却犹豫，或对过去仍有未解。" },
    themes: ["关系状态", "未来期待", "沟通"]
  },
  {
    id: "major-21",
    name: "世界",
    nameEn: "The World",
    suit: "major",
    number: 21,
    upright: { keywords: ["圆满", "完成", "整合", "成就"], meaning: "一个周期完整结束，成果与整合同时到来。" },
    reversed: { keywords: ["未完成", "延迟", "缺乏收尾"], meaning: "接近终点却尚未真正合上，需要补完。" },
    themes: ["未来期待", "关系状态", "约会"]
  },

  // ========== 权杖 (Wands) ==========
  {
    id: "wands-1",
    name: "权杖一",
    nameEn: "Ace of Wands",
    suit: "wands",
    number: 1,
    upright: { keywords: ["灵感", "开端", "热情", "潜力"], meaning: "新的行动能量与灵感突然出现。" },
    reversed: { keywords: ["热情消退", "延迟", "犹豫"], meaning: "冲劲不足，或开始被推迟。" },
    themes: ["约会", "未来期待", "沟通"]
  },
  {
    id: "wands-2",
    name: "权杖二",
    nameEn: "Two of Wands",
    suit: "wands",
    number: 2,
    upright: { keywords: ["规划", "远望", "选择"], meaning: "站在高处看清方向，准备做选择。" },
    reversed: { keywords: ["犹豫", "恐惧改变", "只想不做"], meaning: "计划停留在脑海，迟迟不迈步。" },
    themes: ["未来期待", "关系状态", "约会"]
  },
  {
    id: "wands-3",
    name: "权杖三",
    nameEn: "Three of Wands",
    suit: "wands",
    number: 3,
    upright: { keywords: ["拓展", "远见", "等待回报"], meaning: "已播种，正望向更远的地平线。" },
    reversed: { keywords: ["延误", "视野狭窄", "计划落空"], meaning: "进展不如预期，或眼光需要打开。" },
    themes: ["未来期待", "陪伴", "想念"]
  },
  {
    id: "wands-4",
    name: "权杖四",
    nameEn: "Four of Wands",
    suit: "wands",
    number: 4,
    upright: { keywords: ["庆祝", "安顿", "和谐", "阶段成果"], meaning: "小小的安定与庆祝，关系有了落脚处。" },
    reversed: { keywords: ["不安定", "庆祝过早", "摩擦"], meaning: "安定感不足，或喜悦被干扰。" },
    themes: ["约会", "陪伴", "关系状态"]
  },
  {
    id: "wands-5",
    name: "权杖五",
    nameEn: "Five of Wands",
    suit: "wands",
    number: 5,
    upright: { keywords: ["竞争", "争执", "各抒己见"], meaning: "能量碰撞，观点与立场出现摩擦。" },
    reversed: { keywords: ["回避冲突", "内耗升级"], meaning: "冲突被压抑，或内斗加剧。" },
    themes: ["沟通", "关系状态"]
  },
  {
    id: "wands-6",
    name: "权杖六",
    nameEn: "Six of Wands",
    suit: "wands",
    number: 6,
    upright: { keywords: ["胜利", "认可", "自信"], meaning: "被看见、被肯定，阶段性的胜利感。" },
    reversed: { keywords: ["失落", "虚名", "骄傲"], meaning: "认可不足，或胜利感变得空洞。" },
    themes: ["约会", "未来期待", "陪伴"]
  },
  {
    id: "wands-7",
    name: "权杖七",
    nameEn: "Seven of Wands",
    suit: "wands",
    number: 7,
    upright: { keywords: ["坚守", "防御", "立场"], meaning: "在挑战中守住自己的位置与原则。" },
    reversed: { keywords: ["放弃", "力不从心", "过度防御"], meaning: "防守过度或能量耗尽。" },
    themes: ["关系状态", "沟通", "安慰"]
  },
  {
    id: "wands-8",
    name: "权杖八",
    nameEn: "Eight of Wands",
    suit: "wands",
    number: 8,
    upright: { keywords: ["快速", "消息", "推进"], meaning: "事情加速，信息与行动迅速流动。" },
    reversed: { keywords: ["延误", "混乱", "匆忙"], meaning: "节奏被打乱，或推进受阻。" },
    themes: ["沟通", "约会", "想念"]
  },
  {
    id: "wands-9",
    name: "权杖九",
    nameEn: "Nine of Wands",
    suit: "wands",
    number: 9,
    upright: { keywords: ["戒备", "坚持", "韧性"], meaning: "经历过挑战后仍保持警觉与耐力。" },
    reversed: { keywords: ["焦虑", "疲惫", "防御过度"], meaning: "警惕变成负担，身心需要休息。" },
    themes: ["安慰", "想念", "关系状态"]
  },
  {
    id: "wands-10",
    name: "权杖十",
    nameEn: "Ten of Wands",
    suit: "wands",
    number: 10,
    upright: { keywords: ["重担", "责任", "负荷"], meaning: "扛着许多，接近终点却仍感沉重。" },
    reversed: { keywords: ["减负", "放下", "委派"], meaning: "开始意识到需要卸下部分负担。" },
    themes: ["安慰", "关系状态", "未来期待"]
  },
  {
    id: "wands-11",
    name: "权杖侍从",
    nameEn: "Page of Wands",
    suit: "wands",
    number: 11,
    upright: { keywords: ["新鲜", "好奇", "消息", "热情萌芽"], meaning: "新的灵感或消息带着好奇与热情到来。" },
    reversed: { keywords: ["三分钟热度", "散漫", "消息延迟"], meaning: "热情短暂，或行动力不足。" },
    themes: ["约会", "沟通", "想念"]
  },
  {
    id: "wands-12",
    name: "权杖骑士",
    nameEn: "Knight of Wands",
    suit: "wands",
    number: 12,
    upright: { keywords: ["行动", "热情", "冒险"], meaning: "带着热情快速推进，敢于行动。" },
    reversed: { keywords: ["冲动", "急躁", "半途而废"], meaning: "行动过快，缺乏持续力。" },
    themes: ["约会", "未来期待", "沟通"]
  },
  {
    id: "wands-13",
    name: "权杖王后",
    nameEn: "Queen of Wands",
    suit: "wands",
    number: 13,
    upright: { keywords: ["自信", "热情", "感染力", "独立"], meaning: "温暖而坚定的存在感，能点燃周围。" },
    reversed: { keywords: ["嫉妒", "强势", "情绪化"], meaning: "热情变成控制，或自信受挫。" },
    themes: ["陪伴", "约会", "关系状态"]
  },
  {
    id: "wands-14",
    name: "权杖国王",
    nameEn: "King of Wands",
    suit: "wands",
    number: 14,
    upright: { keywords: ["远见", "领导", "决断"], meaning: "有远见地带领，敢于拍板。" },
    reversed: { keywords: ["专断", "急躁", "好大喜功"], meaning: "领导变成压迫，或目标过于膨胀。" },
    themes: ["未来期待", "关系状态", "沟通"]
  },

  // ========== 圣杯 (Cups) ==========
  {
    id: "cups-1",
    name: "圣杯一",
    nameEn: "Ace of Cups",
    suit: "cups",
    number: 1,
    upright: { keywords: ["新感情", "情感满溢", "接纳", "心开"], meaning: "情感之门打开，新的感受自然涌入。" },
    reversed: { keywords: ["情绪堵住", "付出无回应", "封闭"], meaning: "心暂时关着，或情感无法顺畅流动。" },
    themes: ["想念", "约会", "陪伴", "安慰"]
  },
  {
    id: "cups-2",
    name: "圣杯二",
    nameEn: "Two of Cups",
    suit: "cups",
    number: 2,
    upright: { keywords: ["互相吸引", "对等", "连接", "联盟"], meaning: "两颗心靠近，形成平等而温柔的连接。" },
    reversed: { keywords: ["失衡", "误会", "连接断裂"], meaning: "对等感消失，关系出现裂缝。" },
    themes: ["关系状态", "约会", "想念", "陪伴"]
  },
  {
    id: "cups-3",
    name: "圣杯三",
    nameEn: "Three of Cups",
    suit: "cups",
    number: 3,
    upright: { keywords: ["欢聚", "分享", "友谊", "庆祝"], meaning: "一起欢笑、分享喜悦的时刻。" },
    reversed: { keywords: ["过度玩乐", "小圈子", "孤立"], meaning: "热闹背后可能有空虚，或连接变浅。" },
    themes: ["陪伴", "约会", "安慰"]
  },
  {
    id: "cups-4",
    name: "圣杯四",
    nameEn: "Four of Cups",
    suit: "cups",
    number: 4,
    upright: { keywords: ["倦怠", "不满足", "内省", "错过"], meaning: "对眼前的机会提不起兴趣，需要重新看见。" },
    reversed: { keywords: ["重新提起兴趣", "走出低落"], meaning: "开始愿意重新看向外界。" },
    themes: ["想念", "安慰", "关系状态"]
  },
  {
    id: "cups-5",
    name: "圣杯五",
    nameEn: "Five of Cups",
    suit: "cups",
    number: 5,
    upright: { keywords: ["失落", "遗憾", "只看打翻的"], meaning: "注意力停在失去的部分，悲伤需要被看见。" },
    reversed: { keywords: ["释怀", "看见剩下的", "重新站起"], meaning: "开始转过身，看见尚未失去的。" },
    themes: ["安慰", "想念", "关系状态"]
  },
  {
    id: "cups-6",
    name: "圣杯六",
    nameEn: "Six of Cups",
    suit: "cups",
    number: 6,
    upright: { keywords: ["怀旧", "童真", "旧人旧事", "温柔回忆"], meaning: "过去的温暖被重新触碰，带着纯真的气息。" },
    reversed: { keywords: ["困在过去", "不愿向前"], meaning: "回忆变成束缚，难以活在当下。" },
    themes: ["想念", "陪伴", "安慰"]
  },
  {
    id: "cups-7",
    name: "圣杯七",
    nameEn: "Seven of Cups",
    suit: "cups",
    number: 7,
    upright: { keywords: ["幻想", "选择过多", "幻象"], meaning: "可能性很多，却容易迷失在想象里。" },
    reversed: { keywords: ["清醒", "聚焦", "做出选择"], meaning: "开始从幻象中抽身，看清真正想要的。" },
    themes: ["未来期待", "关系状态", "自由提问"]
  },
  {
    id: "cups-8",
    name: "圣杯八",
    nameEn: "Eight of Cups",
    suit: "cups",
    number: 8,
    upright: { keywords: ["离开", "寻找更深", "放下"], meaning: "主动离开不再满足的，去寻找更真实的意义。" },
    reversed: { keywords: ["停滞", "犹豫离开", "害怕空虚"], meaning: "知道该走却迈不出步。" },
    themes: ["关系状态", "想念", "安慰"]
  },
  {
    id: "cups-9",
    name: "圣杯九",
    nameEn: "Nine of Cups",
    suit: "cups",
    number: 9,
    upright: { keywords: ["满足", "愿望实现", "情感丰盛"], meaning: "心愿被回应，情感上感到充实与满足。" },
    reversed: { keywords: ["空虚", "物质满足却心空", "愿望未达"], meaning: "表面满足，内在仍有缺口。" },
    themes: ["约会", "陪伴", "未来期待"]
  },
  {
    id: "cups-10",
    name: "圣杯十",
    nameEn: "Ten of Cups",
    suit: "cups",
    number: 10,
    upright: { keywords: ["圆满", "家庭式幸福", "情感和谐"], meaning: "情感层面的完整与和谐，安心的归属感。" },
    reversed: { keywords: ["纷争", "理想破裂", "不和谐"], meaning: "原本期待的圆满出现裂缝。" },
    themes: ["关系状态", "未来期待", "陪伴"]
  },
  {
    id: "cups-11",
    name: "圣杯侍从",
    nameEn: "Page of Cups",
    suit: "cups",
    number: 11,
    upright: { keywords: ["敏感", "消息", "创意情感", "温柔靠近"], meaning: "带着柔软与好奇的情感讯息到来。" },
    reversed: { keywords: ["情绪脆弱", "不成熟", "消息延迟"], meaning: "情感表达不稳，或敏感过度。" },
    themes: ["想念", "约会", "沟通", "安慰"]
  },
  {
    id: "cups-12",
    name: "圣杯骑士",
    nameEn: "Knight of Cups",
    suit: "cups",
    number: 12,
    upright: { keywords: ["浪漫", "追求", "理想化"], meaning: "带着诗意与浪漫靠近，追求心中所想。" },
    reversed: { keywords: ["摇摆", "不切实际", "情绪化"], meaning: "承诺容易变，或沉浸在幻想里。" },
    themes: ["约会", "想念", "陪伴"]
  },
  {
    id: "cups-13",
    name: "圣杯王后",
    nameEn: "Queen of Cups",
    suit: "cups",
    number: 13,
    upright: { keywords: ["包容", "直觉", "情感成熟", "滋养"], meaning: "深深理解与包容，情感上的港湾。" },
    reversed: { keywords: ["多疑", "情绪淹没", "边界模糊"], meaning: "感受过载，或过度卷入他人情绪。" },
    themes: ["安慰", "陪伴", "想念", "关系状态"]
  },
  {
    id: "cups-14",
    name: "圣杯国王",
    nameEn: "King of Cups",
    suit: "cups",
    number: 14,
    upright: { keywords: ["成熟", "情绪稳定", "智慧关怀"], meaning: "在情感中保持清醒与温柔，能给予支持。" },
    reversed: { keywords: ["冷漠", "情绪压抑", "操控情感"], meaning: "情感被封闭，或表面平静下有暗流。" },
    themes: ["安慰", "沟通", "关系状态", "陪伴"]
  },

  // ========== 宝剑 (Swords) ==========
  {
    id: "swords-1",
    name: "宝剑一",
    nameEn: "Ace of Swords",
    suit: "swords",
    number: 1,
    upright: { keywords: ["清晰", "真相", "突破", "新思维"], meaning: "思维被锐利地切开，真相与清晰出现。" },
    reversed: { keywords: ["混乱", "沟通不畅", "真相被遮"], meaning: "思想混乱，或重要信息被误解。" },
    themes: ["沟通", "自由提问", "关系状态"]
  },
  {
    id: "swords-2",
    name: "宝剑二",
    nameEn: "Two of Swords",
    suit: "swords",
    number: 2,
    upright: { keywords: ["僵局", "两难", "回避决定"], meaning: "站在选择前，暂时闭上眼睛不愿决定。" },
    reversed: { keywords: ["打破僵局", "做出选择"], meaning: "开始愿意面对，僵局松动。" },
    themes: ["关系状态", "沟通", "未来期待"]
  },
  {
    id: "swords-3",
    name: "宝剑三",
    nameEn: "Three of Swords",
    suit: "swords",
    number: 3,
    upright: { keywords: ["心碎", "悲伤", "分离的痛"], meaning: "心被刺痛，分离或失望的情绪需要被承认。" },
    reversed: { keywords: ["释怀", "疗愈开始", "痛感减轻"], meaning: "伤口开始愈合，痛苦不再那么尖锐。" },
    themes: ["安慰", "想念", "关系状态"]
  },
  {
    id: "swords-4",
    name: "宝剑四",
    nameEn: "Four of Swords",
    suit: "swords",
    number: 4,
    upright: { keywords: ["休整", "休息", "恢复", "暂停"], meaning: "暂时放下武器，给自己安静恢复的时间。" },
    reversed: { keywords: ["焦虑难眠", "休息不足", "被迫行动"], meaning: "该休息却无法真正放松。" },
    themes: ["安慰", "想念", "陪伴"]
  },
  {
    id: "swords-5",
    name: "宝剑五",
    nameEn: "Five of Swords",
    suit: "swords",
    number: 5,
    upright: { keywords: ["争执", "赢了却失落", "冲突"], meaning: "冲突过后，即使赢了也可能留下空虚。" },
    reversed: { keywords: ["和解", "放下争斗", "承认损失"], meaning: "愿意结束无谓的对抗。" },
    themes: ["沟通", "关系状态"]
  },
  {
    id: "swords-6",
    name: "宝剑六",
    nameEn: "Six of Swords",
    suit: "swords",
    number: 6,
    upright: { keywords: ["过渡", "离开困境", "平静前行"], meaning: "带着未完全愈合的伤，驶向更平静的地方。" },
    reversed: { keywords: ["困在痛里", "难以离开", "过渡受阻"], meaning: "想离开却被过去拖住。" },
    themes: ["安慰", "想念", "未来期待"]
  },
  {
    id: "swords-7",
    name: "宝剑七",
    nameEn: "Seven of Swords",
    suit: "swords",
    number: 7,
    upright: { keywords: ["策略", "隐瞒", "独自行动"], meaning: "用巧妙或隐蔽的方式处理事情。" },
    reversed: { keywords: ["坦诚", "被识破", "良心不安"], meaning: "隐藏变得困难，或开始想要坦白。" },
    themes: ["沟通", "关系状态", "自由提问"]
  },
  {
    id: "swords-8",
    name: "宝剑八",
    nameEn: "Eight of Swords",
    suit: "swords",
    number: 8,
    upright: { keywords: ["束缚", "自我限制", "感到困住"], meaning: "感觉被困，但许多限制其实来自自己的想法。" },
    reversed: { keywords: ["挣脱", "看见出路", "释放"], meaning: "开始意识到自己可以解开束缚。" },
    themes: ["安慰", "关系状态", "想念"]
  },
  {
    id: "swords-9",
    name: "宝剑九",
    nameEn: "Nine of Swords",
    suit: "swords",
    number: 9,
    upright: { keywords: ["焦虑", "失眠", "担忧循环"], meaning: "思绪在夜里翻涌，焦虑占据心头。" },
    reversed: { keywords: ["焦虑减轻", "寻求帮助", "开始放下"], meaning: "最黑暗的时刻开始松动。" },
    themes: ["安慰", "想念", "自由提问"]
  },
  {
    id: "swords-10",
    name: "宝剑十",
    nameEn: "Ten of Swords",
    suit: "swords",
    number: 10,
    upright: { keywords: ["终结", "最低点", "彻底结束"], meaning: "一个痛苦的阶段走到尽头，必须承认结束。" },
    reversed: { keywords: ["重生", "最坏已过", "缓慢恢复"], meaning: "谷底已过，虽然慢，但开始向上。" },
    themes: ["安慰", "关系状态", "未来期待"]
  },
  {
    id: "swords-11",
    name: "宝剑侍从",
    nameEn: "Page of Swords",
    suit: "swords",
    number: 11,
    upright: { keywords: ["好奇", "观察", "新想法", "警惕"], meaning: "带着敏锐与好奇探查周围。" },
    reversed: { keywords: ["散漫", "八卦", "言语伤人"], meaning: "好奇心变成干扰，或言辞不当。" },
    themes: ["沟通", "自由提问", "想念"]
  },
  {
    id: "swords-12",
    name: "宝剑骑士",
    nameEn: "Knight of Swords",
    suit: "swords",
    number: 12,
    upright: { keywords: ["迅速", "直接", "行动力强"], meaning: "目标明确，快速切入并推进。" },
    reversed: { keywords: ["冲动", "不顾后果", "冲突升级"], meaning: "速度过快，容易造成伤害。" },
    themes: ["沟通", "约会", "关系状态"]
  },
  {
    id: "swords-13",
    name: "宝剑王后",
    nameEn: "Queen of Swords",
    suit: "swords",
    number: 13,
    upright: { keywords: ["敏锐", "清晰", "独立", "诚实"], meaning: "用清晰的头脑看透事物，保持独立判断。" },
    reversed: { keywords: ["苛刻", "冷漠", "言语锋利"], meaning: "清晰变成尖锐，伤人而不自知。" },
    themes: ["沟通", "关系状态", "自由提问"]
  },
  {
    id: "swords-14",
    name: "宝剑国王",
    nameEn: "King of Swords",
    suit: "swords",
    number: 14,
    upright: { keywords: ["公正", "理性", "权威思维"], meaning: "以逻辑与原则做决定，保持客观。" },
    reversed: { keywords: ["冷酷", "滥用权力", "教条"], meaning: "理性变成冷漠，或原则被扭曲。" },
    themes: ["沟通", "关系状态", "未来期待"]
  },

  // ========== 星币 (Pentacles) ==========
  {
    id: "pentacles-1",
    name: "星币一",
    nameEn: "Ace of Pentacles",
    suit: "pentacles",
    number: 1,
    upright: { keywords: ["新机会", "物质开端", "落地", "潜力"], meaning: "实际的新机会出现，值得用心培育。" },
    reversed: { keywords: ["机会流失", "计划不实", "延迟"], meaning: "机会未能把握，或落地困难。" },
    themes: ["未来期待", "约会", "关系状态"]
  },
  {
    id: "pentacles-2",
    name: "星币二",
    nameEn: "Two of Pentacles",
    suit: "pentacles",
    number: 2,
    upright: { keywords: ["平衡", "灵活", "多重事务"], meaning: "在变化中保持节奏，灵活调配资源。" },
    reversed: { keywords: ["失衡", "手忙脚乱", "顾此失彼"], meaning: "同时处理太多，节奏被打乱。" },
    themes: ["陪伴", "关系状态", "未来期待"]
  },
  {
    id: "pentacles-3",
    name: "星币三",
    nameEn: "Three of Pentacles",
    suit: "pentacles",
    number: 3,
    upright: { keywords: ["合作", "技艺", "共同建设"], meaning: "通过合作与技艺，一起把事情做好。" },
    reversed: { keywords: ["合作不畅", "缺乏认可", "单打独斗"], meaning: "协作出现问题，或努力未被看见。" },
    themes: ["陪伴", "沟通", "未来期待"]
  },
  {
    id: "pentacles-4",
    name: "星币四",
    nameEn: "Four of Pentacles",
    suit: "pentacles",
    number: 4,
    upright: { keywords: ["持有", "安全", "控制", "守成"], meaning: "紧紧握住已有的，寻求安全感。" },
    reversed: { keywords: ["放手", "吝啬放松", "过度控制"], meaning: "开始愿意松开，或控制欲松动。" },
    themes: ["关系状态", "想念", "未来期待"]
  },
  {
    id: "pentacles-5",
    name: "星币五",
    nameEn: "Five of Pentacles",
    suit: "pentacles",
    number: 5,
    upright: { keywords: ["匮乏感", "被排除", "艰难"], meaning: "感到被冷落或资源不足，需要看见支持。" },
    reversed: { keywords: ["转机", "接受帮助", "走出困境"], meaning: "艰难开始缓解，援助出现。" },
    themes: ["安慰", "想念", "关系状态"]
  },
  {
    id: "pentacles-6",
    name: "星币六",
    nameEn: "Six of Pentacles",
    suit: "pentacles",
    number: 6,
    upright: { keywords: ["给予", "分享", "平衡付出"], meaning: "有来有往的给予与接受，资源流动。" },
    reversed: { keywords: ["付出失衡", "附带条件", "依赖"], meaning: "给予与接受变得不对等。" },
    themes: ["陪伴", "安慰", "关系状态"]
  },
  {
    id: "pentacles-7",
    name: "星币七",
    nameEn: "Seven of Pentacles",
    suit: "pentacles",
    number: 7,
    upright: { keywords: ["等待收获", "评估", "耐心"], meaning: "已经投入，现在需要耐心等待结果。" },
    reversed: { keywords: ["焦急", "收成不佳", "怀疑投入"], meaning: "等待变得煎熬，或开始怀疑是否值得。" },
    themes: ["未来期待", "想念", "关系状态"]
  },
  {
    id: "pentacles-8",
    name: "星币八",
    nameEn: "Eight of Pentacles",
    suit: "pentacles",
    number: 8,
    upright: { keywords: ["专注", "精进", "勤奋"], meaning: "沉下心打磨，一步一步把事情做好。" },
    reversed: { keywords: ["敷衍", "缺乏专注", "倦怠"], meaning: "工作或投入变得机械，热情下降。" },
    themes: ["陪伴", "未来期待", "沟通"]
  },
  {
    id: "pentacles-9",
    name: "星币九",
    nameEn: "Nine of Pentacles",
    suit: "pentacles",
    number: 9,
    upright: { keywords: ["自给自足", "享受成果", "独立"], meaning: "靠自己的努力获得安稳与享受。" },
    reversed: { keywords: ["依赖", "孤独", "成果不稳"], meaning: "独立感不足，或享受被干扰。" },
    themes: ["陪伴", "未来期待", "关系状态"]
  },
  {
    id: "pentacles-10",
    name: "星币十",
    nameEn: "Ten of Pentacles",
    suit: "pentacles",
    number: 10,
    upright: { keywords: ["稳固", "传承", "长期安全", "家庭式丰盛"], meaning: "长期积累带来的稳固与归属。" },
    reversed: { keywords: ["不稳", "家族摩擦", "短期思维"], meaning: "稳固感出现裂痕，或只看眼前。" },
    themes: ["未来期待", "关系状态", "陪伴"]
  },
  {
    id: "pentacles-11",
    name: "星币侍从",
    nameEn: "Page of Pentacles",
    suit: "pentacles",
    number: 11,
    upright: { keywords: ["学习", "务实", "新机会萌芽"], meaning: "带着认真与好奇，开始实际的学习或机会。" },
    reversed: { keywords: ["拖延", "不切实际", "机会浪费"], meaning: "想法很好，行动却迟迟不落地。" },
    themes: ["未来期待", "约会", "沟通"]
  },
  {
    id: "pentacles-12",
    name: "星币骑士",
    nameEn: "Knight of Pentacles",
    suit: "pentacles",
    number: 12,
    upright: { keywords: ["可靠", "稳步", "责任"], meaning: "一步一个脚印，可靠地完成承诺。" },
    reversed: { keywords: ["固执", "停滞", "过于谨慎"], meaning: "稳重变成拖延，或拒绝变通。" },
    themes: ["陪伴", "关系状态", "未来期待"]
  },
  {
    id: "pentacles-13",
    name: "星币王后",
    nameEn: "Queen of Pentacles",
    suit: "pentacles",
    number: 13,
    upright: { keywords: ["务实关怀", "滋养", "安全感", "落地"], meaning: "用实际行动照顾与创造安全的环境。" },
    reversed: { keywords: ["过度操心", "自我忽视", "物质焦虑"], meaning: "照顾别人太多，或安全感不足。" },
    themes: ["陪伴", "安慰", "约会"]
  },
  {
    id: "pentacles-14",
    name: "星币国王",
    nameEn: "King of Pentacles",
    suit: "pentacles",
    number: 14,
    upright: { keywords: ["稳重", "成功", "提供支持", "长期眼光"], meaning: "以稳妥与慷慨的方式建立与守护。" },
    reversed: { keywords: ["固执", "物质至上", "控制"], meaning: "稳重变成僵化，或过于看重物质。" },
    themes: ["未来期待", "关系状态", "陪伴"]
  }
];

// 导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TAROT_CARDS };
}
