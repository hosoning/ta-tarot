/**
 * 问题主题定义
 * id: 唯一标识
 * name: 显示名称
 * description: 简短说明
 * keywords: 用于自由提问的关键词匹配
 */
const THEMES = [
  {
    id: "missing",
    name: "想念",
    description: "关于思念、牵挂、想靠近的心情",
    keywords: ["想", "念", "思念", "牵挂", "想起", "惦记", "想见", "想你", "想TA"]
  },
  {
    id: "relationship",
    name: "关系状态",
    description: "目前关系的温度、距离与走向",
    keywords: ["关系", "我们", "状态", "距离", "亲近", "疏远", "怎么样", "如何"]
  },
  {
    id: "companionship",
    name: "陪伴",
    description: "关于在一起、陪着、存在感",
    keywords: ["陪", "陪伴", "一起", "在身边", "存在", "陪着"]
  },
  {
    id: "communication",
    name: "沟通",
    description: "想说的话、交流、表达与倾听",
    keywords: ["说", "聊", "沟通", "表达", "听", "告诉", "消息", "联系"]
  },
  {
    id: "date",
    name: "约会",
    description: "见面、相处、共同度过的时光",
    keywords: ["约", "见面", "约会", "出去", "一起做", "相处"]
  },
  {
    id: "comfort",
    name: "安慰",
    description: "需要被理解、被安慰、被支持的时刻",
    keywords: ["安慰", "难过", "累", "撑", "理解", "支持", "心疼", "委屈"]
  },
  {
    id: "future",
    name: "未来期待",
    description: "对之后的想象、希望与可能性",
    keywords: ["未来", "以后", "期待", "希望", "会不会", "能不能", "将来"]
  },
  {
    id: "free",
    name: "自由提问",
    description: "其他想问的，或无法归类的心情",
    keywords: []
  }
];

const TONES = [
  { id: "gentle", name: "温柔", description: "柔软、体贴、带着温度" },
  { id: "restrained", name: "克制", description: "含蓄、不直白、留有余地" },
  { id: "direct", name: "直接", description: "清晰、坦诚、不绕弯" },
  { id: "playful", name: "俏皮", description: "轻松、带一点调侃与活泼" },
  { id: "quiet", name: "安静", description: "低声、沉淀、像私下说的话" }
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { THEMES, TONES };
}
