"""Translate the guide's first-read chapter windows and researched reading notes into edges."""
from graphlib import TopologicalSorter


# Main-route entry and continuation ending, excluding the optional branch endings.
# 第六章与第七章之间的《谜影的序曲》另有独立节点，不能从关卡 ID 推算章节。
CHAPTERS = {
    1: (101, 112), 2: (204, 217), 3: (304, 318),
    4: (403, 417), 5: (504, 519), 6: (604, 622),
    7: (804, 825), 8: (901, 926), 9: (1001, 1026),
}
CHAPTER_NAMES = "序一二三四五六七八九"

# Additional recommendations explicitly supported by the edited reason/evidence in
# nova-notes, bond-notes, disc-notes and main_event_notes. A related reference alone
# is not a prerequisite. Each group lists stories sharing one reading milestone.
MILESTONES = {
    "prologue:STm00_02": ["npc_bonds:917201", "characters:11201"],
    "storysets:100204": ["characters:11101"],
    "storysets:100103": ["mirror/DiscIP/214031"],
    "main:211": ["storysets:100101"],
    "main:217": ["characters:10301", "storysets:100601", "events:201010201"],
    "storysets:100603": ["characters:10701"],
    "characters:14903": ["discs:214036"],
    "main:412": ["discs:214006", "events:111000201", "mirror/DiscIP/213005"],
    "main:417": ["storysets:100501", "characters:13301", "characters:13401", "characters:15601"],
    "characters:15603": ["discs:214037"],
    "main:622": ["events:101090201", "storysets:100801", "storysets:101001", "storysets:100901"],
    "events:101090210": ["characters:10801", "characters:11401"],
    "characters:11403": ["discs:214029"],
    "main:6512": ["characters:14501", "storysets:100401", "characters:15001"],
    "characters:14503": ["discs:214045"],
    "storysets:100803": ["characters:11801"],
    "storysets:100903": ["characters:13501"],
    "storysets:100403": ["characters:11901", "discs:214028"],
    "characters:11003": ["discs:214004"],
    "storysets:100503": ["characters:15001", "storysets:101601", "mirror/DiscIP/214056"],
    "storysets:101003": ["characters:11601"],
    "main:825": ["events:101080201"],
    "main:1026": ["storysets:101801", "characters:13901", "discs:214061", "mirror/DiscIP/214062"],
    "main:1110": ["characters:16201", "soldier:ST_sys_soldier_intro"],
    "main:1124": ["discs:214066", "mirror/DiscIP/214067"],  # 资料已收录，推荐等到特别篇全篇结束
    "events:201010214": ["storysets:100701", "discs:214048", "characters:12601", "events:101040201",
                         "mirror/DiscIP/214041"],
    "characters:12603": ["mirror/DiscIP/213016"],  # 贝法娜的公开身份
    "events:101070203": ["mirror/DiscIP/214003"],  # 《监护人》
    "storysets:100303": ["events:101040201", "discs:214027"],
    "events:101040211": ["characters:15901", "characters:11301", "characters:14101"],
    "characters:15903": ["discs:214044"],
    "events:101070211": ["characters:12001"],
    "discs:214016": ["events:101050201"],
    "events:101050212": ["characters:14301", "storysets:101401"],
    "storysets:101403": ["characters:14701"],
    "discs:214005": ["storysets:101101", "mirror/DiscIP/213006", "mirror/DiscIP/214020",
                     "mirror/DiscIP/214011"],
    "events:111000202": ["discs:214038", "discs:214057"],
    "storysets:101103": ["characters:13001", "events:101060201"],
    "events:101060212": ["characters:12501", "characters:12701", "discs:214008", "mirror/DiscIP/214047"],
    "events:101080210": ["discs:214054", "mirror/CharacterArchiveContent/14002"],
    "events:201030201": ["characters:16001"],
    "characters:16003": ["discs:214055"],
}


def add_reading_gates(stories):
    by_key = {s["progressKey"]: s for s in stories}
    by_id = {s["id"]: s for s in stories}
    added = {s["id"]: set() for s in stories}

    def gate(s, parent_key):
        added[s["id"]].add(by_key[parent_key]["id"])

    for parent, targets in MILESTONES.items():
        for target in targets:
            gate(by_key[target], parent)

    for s in stories:
        key = s["progressKey"]
        if s["type"] in ("序章", "主线", "特别篇"):
            continue
        # routePosition() labels these slots as 第 N 章阶段 or 第 N 章后.
        # It is a chapter reading window, never a dependency on the adjacent sorted story.
        chapter, slot = divmod(s["route"], 100)
        if chapter in CHAPTERS and s.get("seriesNo") != "#02":
            entry, ending = CHAPTERS[chapter]
            gate(s, f"main:{ending if slot >= 40 else entry}")
        if s["type"] == "战斗气泡" and key.startswith("battles_unmounted:BBm00_"):
            gate(s, "prologue:STm00_01")
        if s["type"] == "回归剧情":
            gate(s, "storysets:100204")
        if s["type"] == "尖兵陷阵" or key.startswith("_chat/PM162"):
            gate(s, "main:1110")
        if s["type"] == "心链" and s["group"].split(" · ")[0] in ("尘沙", "琥珀", "鸢尾"):
            gate(s, "main:217")
        if s["type"] == "邀约":
            places = s.get("places", [])
            if "因苏拉" in places:
                gate(s, "main:1106")
            elif any(p.startswith("菲兰尼斯") for p in places):
                gate(s, "main:1103")
            elif s["cast"] == ["魔王"]:
                # Generic location encounters have a player character, but no fixed companion.
                gate(s, "prologue:STm00_02")
        if s["type"] == "逸闻笔记":
            owner = int(key.split(":")[1]) // 100
            # These notes have a custom reading rationale and bypass the ordinary owner anchor.
            parent = {140: "events:101080210", 143: "events:101050212", 149: "storysets:101204",
                      158: "events:201010214", 159: "events:101040211", 162: "main:1110",
                      130: "events:101060212", 144: "storysets:100103", 145: "characters:14501",
                      137: "events:101110210"}.get(owner)
            if parent:
                gate(s, parent)
        if key.startswith("mirror/CharacterArchiveContent/158") and s["type"] == "旅人档案":
            gate(s, "events:201010214")
        if key.startswith("dispatch:") and s["group"].startswith(("薇洛（盛夏）", "尘沙（源初）")):
            gate(s, "events:201030201" if s["group"].startswith("薇洛") else "main:1110")

    # Keep the graph compact. Only drop an added gate if every valid route through
    # another prerequisite already includes it. A merge need not traverse both alternatives.
    graph = {}
    required = {}
    alternatives = {}
    for sid, s in by_id.items():
        either = set(s.get("alternativeParents", []))
        fixed = set(s.get("topologyParents", [])) - either
        for field in ("requires", "unlockRequires", "readAfter"):
            fixed.update(s.get(field, []))
        required[sid], alternatives[sid] = fixed, either
        graph[sid] = fixed | either | added[sid]
    ancestors = {}
    for sid in TopologicalSorter(graph).static_order():
        either = alternatives[sid]
        guaranteed = set.intersection(*(ancestors[p] for p in either)) if either else set()
        for p in required[sid]:
            guaranteed.update(ancestors[p])
        extra = sorted(added[sid] - guaranteed)
        for p in extra:
            if not any(p in ancestors[other] for other in extra if other != p):
                by_id[sid].setdefault("readAfter", []).append(p)
        for p in extra:
            guaranteed.update(ancestors[p])
        ancestors[sid] = guaranteed | {sid}
        s = by_id[sid]
        chapter, slot = divmod(s["route"], 100)
        if s.get("seriesNo") == "#02":
            s["routeLabel"] = "序章后可读"
        elif (chapter in CHAPTERS and slot < 40 and s["type"] not in ("主线", "特别篇")
              and by_key[f"main:{CHAPTERS[chapter][1]}"]["id"] in guaranteed):
            s["routeLabel"] = f"第{CHAPTER_NAMES[int(chapter)]}章后"
