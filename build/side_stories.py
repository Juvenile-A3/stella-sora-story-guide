"""Build the three side-story collections from the archive index and edited evidence notes."""
import re
from pathlib import Path

from common import MIRROR, SITE, base_record, mdid, permalink, read, revision, tags, uniq

HERE = Path(__file__).parent
PREFIX = {"storysets": "n", "characters": "c", "discs": "d", "events": "e", "main": "m"}
TYPES = {"storysets": "诺瓦异闻", "characters": "角色羁绊", "discs": "秘闻"}
RELEASES = {
    3:"2025-11-11 04:00", 4:"2025-11-11 04:00", 5:"2025-12-02 12:00",
    6:"2025-12-02 12:00", 7:"2025-12-30 12:00", 8:"2026-01-27 12:00",
    9:"2026-02-17 12:00", 10:"2026-02-17 12:00", 11:"2026-03-10 12:00",
    12:"2026-03-10 12:00", 13:"2026-03-31 12:00", 14:"2026-04-30 12:00",
    15:"2026-05-26 12:00", 16:"2026-07-14 12:00", 17:"2026-09-01 12:00", 18:"2026-10-13 12:00",
}
OFFICIAL_NOVA_19 = "https://stellasora.yostar.cn/news/5077"
POSTER_NOVA_19 = "https://webusstatic.yo-star.com/web-cms-test/upload/content/2026/11/09/OvmfWJ_5.jpg"
# Prerequisites mean explicit dependence or a scene shown earlier that makes a referenced event intelligible.
# Other thematic parallels stay under related. Internal bond levels mean a reading dependency.
BEFORE = {
    "n100201":["p2"], "n100901":["m412"], "n101201":["m112"], "n101301":["m416"],
    "n100501":["m217"], "n101701":["n101103"], "n101501":["n100603"], "n101801":["m622"], "n100701":["d214005"],
    "c13201":["m216"], "c14401":["n100103"], "c14901":["n101204"],
    "c11501":["e101070211"], "c15801":["e201010214"], "c13701":["e101110210"],
    "c15501":["e111000202"], "c15701":["e111000202"], "c14001":["e101080205"],
    "c16201":["m1103"], "d214007":["m216"], "d214026":["n100103"],
    "d214028":["n101301"], "d214036":["n101204"], "d214051":["e101070211"], "d214059":["e101110211","c13703"],
    "d214066":["m1103"], "d214017":["c13403"],
}
ENCOUNTERS = {"n101201":["格芮"], "n101301":["花原"], "c13701":["薇薇安","卡特琳"], "n100203":["波西亚"], "d214028":["唯咲","秋葵"]}
NOVA_PLACES = {
    1001:"埃摩／水道桥",1002:"星塔",1003:"苍梧",1004:"菲莱",1005:"千塔之城／地理协会",
    1006:"帝国卫队拍摄场",1007:"埃摩／千塔郊区",1008:"黄昏裁判第七监狱",1009:"园区",
    1010:"菲莱",1011:"万送屋",1012:"埃摩／星塔",1013:"埃莉诺租住的房子",1014:"埃摩／星塔",
    1015:"帝国卫队拍摄场",1016:"千塔之城／协会之家",1017:"寻宝途中",1018:"菲莱郊外",
}
# Discrete anchors for the calendar. Multi-period records describe the linked scene in 'time'.
def calendar(year, month="", day=None, clock=""):
    return {"year":year, "month":month,"day":day,"clock":clock,
            "precision":"时分" if clock else "日" if day else "月" if month else "年"}

def rows(name):
    return {int(parts[0]):parts[1:] for line in (HERE/name).read_text("utf-8-sig").splitlines()
            if line.strip() and not line.startswith("#") and (parts:=line.split("|"))}

def make_index(pages):
    result={}
    for page in pages:
        family=page["family"]
        if family in PREFIX: result[PREFIX[family]+str(page["id"])]=page
        if family=="prologue": result["p"+str(int(page["id"].split("_")[-1]))]=page
    return result

def names(page):
    names=[v for label in page.get("speakers",[]) for v in re.split("[&＆]",label)]
    return uniq(v for v in names if v not in {"旁白","？？？","???","两人","三人","众人","录音声"})

def build(root):
    root=Path(root)
    docs=root/"story_docs"
    pages=read(docs/"_data/sections.json")["pages"]
    index=make_index(pages)
    commit=revision(root)
    upstream=read(root/".upstream_sync_state.json")["stella_sora_data_commit"]
    table=f"{MIRROR}/blob/{upstream}/CN"
    nova,scenes,bonds,discs=map(rows,("nova-notes.tsv","nova-scenes.tsv","bond-notes.tsv","disc-notes.tsv"))
    locales=read(HERE/"nova-locales.json")
    records=[]
    previous={}
    for p in sorted((p for p in pages if p["family"] in TYPES),key=lambda p:(p["family"],p["group"]["id"],p["id"])):
        family=p["family"]; g=p["group"]; group_id=g["id"]; idx=p["id"]
        code=PREFIX[family]+str(idx)
        sid=mdid(p)
        group=g.get("label","")
        order=idx%100 if family!="discs" else 1
        if family=="storysets": group=f"{g['no']}《{group}》"
        if family=="characters": group=f"{group} · {re.sub(r'[ ]?[上中下]$', '',p['title'])}"
        if family=="discs": group="秘闻 · "+("、".join(g.get("characters",[])) or p["title"])
        r=base_record(sid,p["title"],TYPES[family],group,order,SITE+p["page"])
        body=(docs/p["page_md"]).read_text("utf8")
        beats=read(docs/"_beats"/p["page"].replace(".html",".json"))["beats"]
        cards=[{k:v for k,v in b.items() if k in ("place","date","time")} for b in beats if b["k"]=="scene"]
        r.update(textSource=permalink(commit,p["page_md"]),keywords=tags(body.split("## 3.",1)[-1]),
                 cast=names(p),scenes=cards,availability="已收录",released=True,optional=False,sources=[],
                 encounters=ENCOUNTERS.get(code,[]))
        refs=""; gr="U"; ph="未知"; tm="正文暂未完成定位。"; rt=1250; risk="中"
        mode="现时"; why="新增条目待核对，暂列补完区。"; ev="上游已有正文，尚未建立跨篇时序证据。"; loc=""
        if family=="storysets" and group_id in nova and idx in scenes:
            gr,ph,tm,rt,risk,mode,why,refs=nova[group_id]
            row=scenes[idx]; ev=row[0]
            if len(row)>1: tm=row[1]
            number=group_id-1000
            loc=NOVA_PLACES.get(group_id,"")
            r.update(seriesNo=g["no"],column=g["tab"],releaseAt=RELEASES.get(number,""),
                     sources=[{"label":"编号与开放批次（配置）","url":table+"/bin/StorySetChapter.json"}])
            if str(group_id) in locales:
                r["localizedTitles"]=locales[str(group_id)]
                r["keywords"]=uniq(r["keywords"]+list(r["localizedTitles"].values()))
                r["sources"].append({"label":"繁中地区 · 同一篇号标题","url":f"{MIRROR}/blob/{upstream}/TW/language/zh_TW/StorySetChapter.json"})
            if idx==100101:
                r["calendar"]=calendar(996,"花月",26); gr="B"
            if idx==100103:
                gr="A"; r["calendar"]=calendar(996,"雨月",2,"04:15")
            if group_id==1002: r["calendar"]=calendar(996)
            if idx==100802: loc="星塔"
            if idx==100803:
                loc="黄昏裁判第七监狱／菲莱／埃摩灰城区地下诊所"; r["calendar"]=calendar(996,"雨月",2,"08:28")
            if group_id==1018:
                r["calendar"]=calendar(996,"谷月",24,"10:00" if idx==101801 else "")
                r["sources"].append({"label":"官方 · 第十八篇开放公告","url":"https://stellasora.yostar.cn/news/4757"})
            if group_id==1007:
                gr="B";ph="996年 · 霜月";tm="万送屋成立后首个雪愿节。很可能与996年霜月的圣夜活动同届；前夜、派件当日与团聚按话次区分。"
                r["calendar"]=calendar(996,"霜月",25 if idx!=100701 else None)
                why="圣夜04C与本篇都写恩赐意志请万送屋在埃摩派件，却只寄了一套合苍兰尺寸的使者服。读完圣夜再换入信使视角。"
            if group_id==1014: rt=1065; why="读过北境事件里的尊者，再看风影怎样把这一知识带进地理协会的调查。幻境内的演出另记。"
            if group_id in (1009,1010):
                r["sources"].append({"label":"运营公告 · 两篇同时常驻","url":"https://www.taptap.cn/moment/770970063556576761"})
            if group_id==1014:
                r["sources"].append({"label":"运营公告 · 第十四篇","url":"https://www.taptap.cn/moment/797779987368247603"})
        elif family=="characters" and group_id in bonds:
            gr,tm,rt,risk,why,notes,refs,loc=bonds[group_id]
            ev=notes.split("；")[order-1]+"。"; mode="羁绊／连续故事"
            ph=({"U":"未知","C":"仅有相对先后"}.get(gr,"人物相对时间"))
            r["unlock"]=f"好感等级 {p['affinity']}"
            if group_id in (132,144):ph="第二章以后"
            if group_id in (133,134):ph="第四章以后"
            if group_id==110:ph="第六章以后"
            if group_id==145:ph="6.5章后至第七章交锋前（推定）"
            if group_id==149:
                ph="997年花月十五日起（仅知下界）"
                if order==1:
                    r["calendar"]=calendar(None,"花月",15)
                else:
                    tm="承接上篇花月十五日的委托，最早在997年。本话未单独标注日期。"
            if group_id in (119,):
                ev+=" 花原在下篇确认当日生日，角色资料将生日列为4月20日。"
                r["sources"].append({"label":"角色档案 · 花原生日","url":table+"/language/zh_CN/CharacterArchiveBaseInfo.json"})
            if group_id==162: ph="前星塔历 · 菲兰尼斯"; r["calendar"]=calendar(-4)
            if group_id in (158,159,160): ph={158:"雪愿节以后",159:"苍梧新春",160:"盛夏假期"}[group_id]
            if group_id==137 and order==1: ev+=" 当面的初次介绍属于魔王与两名挚友。"
            # Independent lower bound where the scene starts a week later.
            if idx==11503: tm="找米夏一事过去一个星期后，仍在火垂结识魔王之后。"
        elif family=="discs" and idx in discs:
            gr,ph,tm,rt,risk,mode,ev,why,refs,loc=discs[idx]
            r["systemNote"]="档案库「秘闻」；剧本与同页的秘纹附文分别标记。"
            if idx==214057: r["sources"].append({"label":"角色档案 · 花铃生日","url":table+"/language/zh_CN/CharacterArchiveBaseInfo.json"})
            if idx==214066: r["calendar"]=calendar(-4)
        for k in refs.split():
            ref=index[k]
            if k!=code: r["sources"].append({"label":"对照 · "+ref["title"],"url":SITE+ref["page"]})
        r.update(grade=gr,phase=ph,time=tm,route=float(rt)+order/1000,reason=why,
                 evidence=ev,risk=risk,mode=mode,places=uniq(loc.split("／")+[s.get("place") for s in cards]),
                 related=uniq(mdid(index[k]) for k in refs.split() if k!=code),
                 requires=[mdid(index[k]) for k in BEFORE.get(code,[])])
        if family!="discs" and (family,group_id) in previous:
            r["requires"].append(previous[family,group_id])
        previous[family,group_id]=sid
        records.append(r)
    if not any(p["family"]=="storysets" and p["group"]["id"]==1019 for p in pages):
        r=base_record("announced/nova-19","比“宝石”更耀眼的","诺瓦异闻","#19《比“宝石”更耀眼的》",1,OFFICIAL_NOVA_19)
        r.update(availability="待开放",released=False,grade="U",phase="待开放",time="未公开故事内时间。",route=1490,
                 seriesNo="#19",releaseAt="2026-11-27 12:00",mode="公告占位",
                 reason="官方预告已命名，当前快照无正文或分话。开放后再定位。",optional=True,
                 evidence="11月版本说明末张长图给出篇号、篇名与常驻开放时间。",
                 sources=[{"label":"官方长图 · 最后一栏","url":POSTER_NOVA_19}])
        records.append(r)
    return records
