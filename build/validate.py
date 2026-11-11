"""Offline integrity check for a built release. Optionally reconcile against the Archive checkout."""
import argparse
from collections import Counter
from pathlib import Path
import json
from graphlib import TopologicalSorter
from common import OUT, read


def require(condition,message):
    if not condition:raise ValueError(message)


def verify(archive=None):
    data=OUT/"data"
    s=read(data/"story-data.json");cs=read(data/"characters.json");t=read(data/"timeline.json");meta=read(data/"metadata.json")
    raw=(data/"guide.js").read_text(encoding="utf8").strip()
    require(raw.startswith("window.GUIDE=") and raw.endswith(";"),"离线数据包损坏")
    require(json.loads(raw[13:-1])==dict(stories=s,characters=cs,timeline=t,meta=meta),"JSON 与网页内置数据有差异")
    idx={r["id"]:r for r in s};identity={r["progressKey"] for r in s};all_ids=set(idx)
    require(len(idx)==len(identity)==len(s),"剧情或进度标识重复")
    for attr in ("readingOrder","chronology"):
        arr=t[attr];require(len(arr)==len(s) and set(arr)==all_ids,attr+" 不是全量目录的一次排列")
    require(all(r["grade"] in "ABCDU" and r["reason"] and r["evidence"] and r["time"] and r["positionStatus"] and r["source"].startswith("https://") for r in s),"有条目缺少考据或来源")
    graph={r["id"]:set(r.get("requires",[])+r.get("unlockRequires",[])+r.get("readAfter",[])+r.get("topologyParents",[])) for r in s}
    require(set(TopologicalSorter(graph).static_order())==all_ids,"存在前置循环或悬空引用")
    for target,parents in graph.items():
        for x in parents:require(idx[x]["route"]<idx[target]["route"],"读序越过前置 "+target)
    for e in t["edges"]:require({e["from"],e["to"]}<=all_ids,"关系引用失效")
    for who in cs:
        require(set(who["stories"])<=all_ids and set(who["first"])<=set(who["stories"]),"角色索引失效 "+who["name"])
    for group in t["history"]+t["organizations"]:require(set(group["stories"])<=all_ids,"历史／组织索引失效")
    for group in t["organizations"]:
        for e in group["links"]:require(e["story"] in all_ids,"组织关系缺少对应正文")
    if archive:
        d=archive/"story_docs"
        pages=read(d/"_data/sections.json")["pages"]
        required={p["page_md"] for p in pages}|{p.relative_to(d).as_posix() for p in (d/"_chat").glob("PM*.md")}
        require({r["archivePage"] for r in s if r.get("archivePage")}==required,"档案正文或聊天文件覆盖不全")
        nodes=read(d/"_data/chapters.json")["meta"]["nodes"]
        require(sum(r["type"] in ("主线","特别篇") for r in s)==nodes,"主线节点数不符")
        require(sum(r["type"]=="活动" for r in s)==len(read(OUT/"build/main-event-tables.json")["eventNodes"]),"活动节点数不符")
        for p in pages:
            require((d/p["page_md"]).is_file() and (d/"_beats"/p["page"].replace(".html",".json")).is_file(),"原文或结构化正文缺失")
    report=dict(snapshot=meta["snapshot"],stories=len(s),archiveFiles=len({r["archivePage"] for r in s if r.get("archivePage")}),
                core=sum(not r["optional"] for r in s),optional=sum(bool(r["optional"]) for r in s),
                coreGrades=dict(Counter(r["grade"] for r in s if not r["optional"])),
                positions=dict(Counter(r["positionStatus"] for r in s)),
                edgeTypes=dict(Counter(e["type"] for e in t["edges"])),periods=len(t["periods"]))
    return report


if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("archive",type=Path,nargs="?")
    print(json.dumps(verify(ap.parse_args().archive),ensure_ascii=False,indent=2))
