"""Apply the separately researched DiscIP prose-only annotations to the merged catalog."""
from pathlib import Path

from common import mdid, uniq
from side_stories import make_index


def apply(stories, pages):
    page_list = pages["pages"] if isinstance(pages, dict) and "pages" in pages else pages
    idx = make_index(page_list)
    existing = {s["id"]: s for s in stories}
    path = Path(__file__).with_name("prose-review.tsv")
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line or line.startswith("#"):
            continue
        num, grade, mode, time, evidence, route, refs = line.split("|")
        story = existing.get("mirror/DiscIP/" + num)
        if story is None:
            continue
        links = ["mirror/DiscIP/" + ref[1:] if ref.startswith("p") else mdid(idx[ref]) for ref in refs.split()]
        links = [sid for sid in links if sid in existing]
        for sid in links:
            entry=existing[sid]
            story["sources"].append({"label":"对照 · " + entry["title"],"url":entry["source"]})
        places = [name for name in ("苍梧","埃摩","米拉什","菲莱","北境","弗拉维奥","菲兰尼斯","万送屋","移动工坊") if name in time+evidence]
        anchor = existing[links[0]]["title"] if links else ""
        reason = (f"可与《{anchor}》对读，阅读时留意{mode.split('／')[0]}的视角。" if anchor
                  else "独立短篇，可在熟悉星塔及旅人世界后选读。正文没有提供具名主线事件。")
        story.update(grade=grade, mode=mode, phase="未知" if grade=="U" else "仅有相对先后",
                     route=float(route),time=time,evidence=evidence.rstrip("。")+"。",reason=reason,
                     places=uniq(story.get("places",[])+places),related=uniq(story.get("related",[])+links))
        if num=="214002":
            story.update(phase="年份未明 · 清月",calendar={"year":None,"month":"清月","day":21,"clock":"","precision":"日"})
        if num=="214067":
            story.update(phase="前星塔历 · 菲兰尼斯",risk="高",reason="建议完整读完特别篇后再看此回望。快照中尚未完整开放，提前展开涉及结局。")
        if num in ("214060","214042","214046","214039","214058") and links:
            story["readAfter"]=links
        if num in ("213015","214010","214062","214043"):
            story["risk"]="高"
