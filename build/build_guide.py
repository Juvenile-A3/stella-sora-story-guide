"""Rebuild the offline guide from a checked-out Archive snapshot and its pinned data mirror."""
import argparse
from collections import Counter, defaultdict
from graphlib import TopologicalSorter
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

from common import ARCHIVE, OUT, SITE, base_record, clean, mdid, permalink, read, revision, uniq
import main_events
import side_stories
import misc_stories
import supplement
import profile_review

MONTHS = main_events.MONTHS
CHAPTERS = "一二三四五六七八九"
OPENING_MONTH=(5,6,6,6,7,9,10,10,11)
GRADE_NAMES={"A":"正文或官方配置明确","B":"多处正文互证","C":"依人物状态、环境等推定","D":"仅玩家读序或上线线索","U":"尚无足够定位依据"}


def dated_period(s):
    """Return an editorial bin and its display rank, never imply an exact day from a bin."""
    cal=s.get("calendar") or {}
    y=cal.get("year");month=cal.get("month") or "";day=cal.get("day")
    natural=MONTHS.index(month)+1 if month in MONTHS else (int(month[:-1]) if re.fullmatch(r"(?:[1-9]|1[0-2])月",month) else 0)
    window=s["phase"]; mode=s.get("mode","")
    status=s.get("availability","")
    if "待开放" in status or "未开放" in status or "待开放" in window or "预告" in status:
        return "已预告／待开放",9_999_999,"待开放",None,""
    if s.get("nodeId")==908:
        return "994年米拉什段以前（仅知上界）",993999,"相对时窗",None,""
    if y is not None and natural:
        pre=f"前星塔历{-y}年" if y<0 else f"星塔历{y}年"
        is_branch="分支终局" in mode and y>=997
        phase=("分支未来 · " if is_branch else "")+pre+" · "+month
        clock=cal.get("clock","")
        minute=0
        if re.fullmatch(r"\d{1,2}:\d{2}",clock):
            h,m=map(int,clock.split(":")); minute=h*60+m
        order=y*1000+natural*10
        label=f"{pre} {month}"+(f"{day}日" if day else "")+(f" {clock}" if clock else "")
        if s["grade"] in ("B","C"):label+="（对读推定）"
        return phase,order,("年月日" if day else "年月"),(day or 0)*10000+minute,label
    if window in ("序章","序章与第一章之间","序章前后","序章前"):
        rank={"序章前":0,"序章前后":1,"序章":2,"序章与第一章之间":3}[window]
        return window,996048+rank/10,"相对时窗",None,""
    if window in ("第一至二章","第二章及之前","第一章以后","第四章以后","第六章以后","第六章后","主线初遇以后"):
        rank={"第一至二章":996052,"第二章及之前":996059,"第一章以后":996064,
              "第四章以后":996074,"第六章以后":996095,"第六章后":996095,"主线初遇以后":1300005}[window]
        return window+"（范围）",rank,"相对时窗",None,""
    if window in ("前星塔历 · 菲兰尼斯","前星塔历 · 角斗场往事","前星塔历","历史时期"):
        return window,-5100 if "角斗场" in window else -3900,"相对时窗",None,""
    if y is not None:
        if re.fullmatch("第[一二三四五六七八九]章",window) and not(s.get("calendar") or {}).get("month"):
            idx=CHAPTERS.index(window[1])
            return f"星塔历{y}年 · {window}内",y*1000+OPENING_MONTH[idx]*10+0.7,"年份",None,f"星塔历{y}年"
        phase=(f"前星塔历{-y}年" if y<0 else f"星塔历{y}年")+" · 月日未定"
        return phase,y*1000+0.1,"年份",None,phase
    if window in ("996年 · 霜月前后","雪愿节前后","苍梧新春前后","柔光技术大会后"):
        rank={"996年 · 霜月前后":996121,"雪愿节前后":1300005,"苍梧新春前后":997012,"柔光技术大会后":997062}[window]
        return ("相对索引 · "+window if rank>=1300000 else window+"（范围）"),rank,"相对时窗",None,""
    if s["grade"] in ("D","U"):
        return "未定位",9900000,"未定位",None,""
    if y is None and natural:
        label=f"年份未明 {month}"+(f"{day}日" if day else "")
        return "年份未明 · "+month,1290000+natural,"相对时窗",day or 0,label
    upper_bounds={"序章以前":996047,"第一章以前":996049,"第二章以前":996059}
    if window in upper_bounds:
        return window+"（仅知上界）",upper_bounds[window],"相对时窗",None,""
    if window=="三大魔物首次讨伐以后":
        return "996年清月前后（首次讨伐败退后）",996041,"相对时窗",None,""
    if window=="新讨伐队活动期间":
        return "新讨伐队活动期间（跨月范围）",996042,"相对时窗",None,""
    if re.fullmatch(r"第[一二三四五六七八九]章",window):
        return "相对索引 · "+window+"分支／未定镜头",1300020,"相对时窗",None,""
    lower_bounds={"第二章以后":996065,"雪愿节以后":996122,"取景框以后":997035,"大小姐修行以后":997045}
    if window in lower_bounds:
        return window+"（仅知下界）",lower_bounds[window],"相对时窗",None,""
    if window in ("苍梧新春","盛夏假期"):
        return window+"（跨篇推定范围）",(997012 if window=="苍梧新春" else 997082),"相对时窗",None,""
    return "相对索引 · "+("人物往事 · 年份未明" if "往事" in window else window if window not in ("未知","") else "仅有相对先后"),1300000,"相对时窗",None,""


def sources_for(r):
    links=list(r.get("sources",[]))+list(r.get("evidenceSources",[]))
    if r.get("textSource"):links.append(dict(label="核对固定版本正文",url=r["textSource"]))
    for url in r.get("refs",[]):
        label=("游戏内活动回顾年月表" if "ActivityStoryChapter" in url else
               "繁中服运营公告" if "stargazer" in url else "大陆服运营公告" if "yostar.cn" in url else "补充资料")
        links.append(dict(label=label,url=url))
    out={}
    for l in links:
        if isinstance(l,str):l={"label":"参考资料","url":l}
        if l.get("url"):out[l["url"]]=l
    return list(out.values())


def add_relations(stories,pages,tables):
    idx={r["id"]:r for r in stories}
    ids={(p["family"],p["id"]):mdid(p) for p in pages}
    def key(fam,n):return ids[fam,n]
    def link(a,field,b):
        if a in idx and b in idx:idx[a][field]=uniq(idx[a].get(field,[])+[b])
    m=lambda n:key("main",n)
    n=lambda i:key("storysets",i)
    e=lambda i:key("events",i)
    b=lambda i:key("characters",i)
    start=key("prologue","STm00_01")
    # Encounter means a witnessed meeting of this incarnation and the contemporary protagonist.
    for sid,people in [(start,["琥珀","鸢尾","尘沙"]),(m(102),["贝修莉娜"]),(m(312),["雾语"]),(m(104),["千都世"])]:
        idx[sid]["encounters"]=uniq(idx[sid].get("encounters",[])+people)
    idx[m(104)]["cast"]=uniq(idx[m(104)]["cast"]+["千都世"])
    idx[m(104)]["sources"]=idx[m(104)].get("sources",[])+[dict(label="回认水道桥上的相遇",url=idx[m(211)]["source"])]
    idx[start]["cast"]=uniq(idx[start]["cast"]+["魔王"])
    # A precise shared scene, and a separate cross-perspective rescue whose day is unknown.
    for sid in (m(208),n(100103)):idx[sid]["parallelKey"]="水道桥走廊 · 雨月2日04:15"
    for sid in (e(201030209),e(101100203)):idx[sid]["parallelKey"]="海上救援 · 同一事件的不同视角"
    for start_node,children,label in [(817,(818,819),"猎月14日11:35 · 缆车与酒店"),
                                     (506,(507,508,509),"雷月31日 · 旅团分头调查")]:
        root=idx[m(start_node)];root["parallelNext"]=[m(i) for i in children]
        root["branches"]=[x for x in root.get("branches",[]) if x not in root["parallelNext"]]
        for i in children:idx[m(i)]["parallelKey"]=label
    merge=idx[m(824)]
    merge["readAfter"]=uniq(merge.get("readAfter",[])+[m(821),m(823)])
    merge["reason"]="队伍分头行动后的汇合点。读完缆车和城内筹资两方的经过，可接上登塔与竞标的结果。"
    annotations=[
        (m(825),"开场场记为996年猎月15日18:15。中标通知落款猎月16日，末段再推进一周。","现时／时间跳跃"),
        (e(101050201),"活动框为997年清月，开场另插入数周前的经历。","现时／倒叙"),
        (e(101050212),"活动框为997年清月；结尾另记一周后，未单独标月日。","现时／时间跳跃"),
        (e(101080210),"活动回顾记997年雨月。本话开场已距前事一周，具体月日未写。","后日谈"),
        (e(101100206),"当下行动属997年热月，片中另有几个月前的镜头。","现时／倒叙")]
    for sid,tm,mode in annotations:
        idx[sid].update(time=tm,mode=mode,dateScope=tm)
    for a,bid in [(n(100103),m(208)),(n(100803),m(211)),(n(101801),m(622)),(n(100203),key("npc_bonds",913302)),
                  (e(101080210),"_chat/PM14001@04"),(n(101201),"_chat/PM14901@01"),
                  (b(10303),"_chat/PM10302@01"),(m(1110),"mirror/CharacterArchiveContent/16211")]:
        link(a,"related",bid)
    link("_chat/PM14901@01","readAfter",n(101204))
    link(key("npc_bonds",913301),"related",n(100203))
    for i in (16211,16212,16213):link(f"mirror/CharacterArchiveContent/{i}","readAfter",m(1110))
    for i in (11711,11712):
        other=11712 if i==11711 else 11711
        link(f"mirror/CharacterArchiveContent/{i}","related",f"mirror/CharacterArchiveContent/{other}")
    for i in (16001,16002,16003):
        r=idx[b(i)];r["calendar"]=dict(year=997,month="热月",day=None,clock="",precision="月")
        r["dateScope"]="活动回顾给出997年热月；度假、沙滩安全与鲨鱼袭击用于跨篇对读。月份为推定，三话的绝对日均未定。"
        link(r["id"],"related",e(201030209))
    def revise(sid, grade,time,reason,peer=None,route=None,phase="仅有相对先后"):
        r=idx[sid];r.update(grade=grade,time=time,evidence=reason,phase=phase)
        if peer:
            link(sid,"related",peer)
            r["sources"]=r.get("sources",[])+[dict(label="对读 · "+idx[peer]["title"],url=idx[peer]["source"])]
        if route is not None:r["route"]=route
    for no in (1,5):
        revise(f"_chat/PM10302@{no:02}","B","认识小黑之后；与寻猫委托隔了几天未明。","双方已能直接谈论小黑。《寻猫记 下》中两人一起向它打招呼。",b(10303),254)
    revise("_chat/PM11002@02","B","菲莱公司设立、魔王协议持股以后。","翡冷翠以股东身份称呼魔王。第七章《投标日》中魔王代表股东表态。",m(807),757)
    revise("_chat/PM13502@04","B","魔王协议人力派遣公司成立之后。","雾语打趣魔王以公司首席执行官身份出现在联合种业门口，第二章可核公司解冻经过。",m(215),680)
    for no in (4,5,7,10):
        revise(f"_chat/PM14001@{no:02}","B","魔王派已可工作，晚于柔光大会的设计构想。","活动 EX 里莱欧还在等造好后的消息；本段已经谈论魔王派的实际使用。",e(101080210),1118,"柔光技术大会后")
    for no in (2,3,5,6):
        revise(f"_chat/PM15802@{no:02}","C","与魔王相识后的雪愿节期间；是否就是活动的那一年仍待考。","聊天谈到当天派礼物、节日活动或节期气氛；只据节俗收窄范围。",e(201010212),1008,"雪愿节前后")
    for no in (6,8,10):
        revise(f"_chat/PM13901@{no:02}","C","魔王已经认识艾蕾与孤儿院的孩子。","此段直接谈及孤儿院和熟悉的孩子；结合米拉什的故事，宜在第八章之后回看。",m(922),940)
    for k,tm,proof in [(15802,"某年雪愿节前夕发起节服提议，文中回顾习俗起源。","档案把节服的由来写成过去某年，年份未标。"),
            (15809,"本年雪愿节服饰出现后。","菈露评价今年服装，同时提到明年，无法辨明是哪一年。"),
            (15811,"雪愿节刚过的深冬。","开篇以午夜钟声与雪愿节结束标明相对时点。"),
            (15813,"某次雪愿节前约一个月。","首段交代奥尔贝德把长鞭交给菈露的相对日期。")]:
        revise(f"mirror/CharacterArchiveContent/{k}","A",tm,proof,e(201010212),1010,"雪愿节前后")
    revise("mirror/CharacterArchiveContent/14002","B","魔王派进入可测试阶段。","斯帕克拉把在星塔中检验魔王派写成当旅人的理由；活动 EX 的机器仍在制作。",e(101080210),1117,"柔光技术大会后")
    # Optional material receives a cast-specific place on the reading route even when it has no global timestamp.
    anchors={p["group"]["label"]:idx[mdid(p)] for p in pages if p["family"]=="characters" and p["id"]%100==3}
    anchors.update({p["group"]["label"]:idx[mdid(p)] for p in pages if p["family"]=="npc_bonds" and p["id"]%100==2})
    for rec in stories:
        if not rec.get("optional") or rec["route"]<1200 or rec["type"] in ("尖兵陷阵结果","尖兵陷阵选项"):continue
        # Dispatch may need more than one character introduction. Do not date an anonymous landmark by a possible companion.
        specific=[anchors[n] for n in rec["cast"][:1] if n in anchors] if rec["type"]!="委托对话" else [anchors[n] for n in rec["cast"] if n in anchors]
        if not specific:continue
        anchor=max(specific,key=lambda s:s["route"])
        for a in specific:link(rec["id"],"readAfter",a["id"])
        rec["route"]=anchor["route"]+0.35+min(rec["order"]%100,99)/10000
        rec["reason"]+=" 可在《"+anchor["title"]+"》之后选读。"
    # Shared ID does not imply the same family, e.g. note 917201 and NPC story 917201.
    for rec in stories:
        if rec.get("keysFromTable"):
            cfg=rec["keysFromTable"]
            if cfg.get("story"):
                parent=next((p["id"] for p in stories if p.get("nodeId")==cfg["story"] and p["type"] in ("特别篇","主线")),None)
                if parent:link(rec["id"],"unlockRequires",parent)
        if rec["id"].startswith("_chat/") and rec.get("cast"):
            who=rec["group"].split(" · ")[0]
            act={"菈露（圣夜）":201010212,"科洛妮丝（新春）":101040201,"薇洛（盛夏）":201030211}.get(who)
            if act:link(rec["id"],"readAfter",e(act))
    # Character dossier after a story only gates disclosure. It never dates the dossier's content.
    for rec in stories:
        if rec["id"].startswith("mirror/CharacterArchiveContent/") and rec.get("keysFromTable"):
            due=[idx[x]["route"] for x in rec.get("unlockRequires",[])]
            if due:rec["route"]=max(due)+0.25
            if any(idx[x].get("released") is False for x in rec.get("unlockRequires",[])):
                rec.update(availability="改订条件待开放",released=False)
                rec["reason"]+=" 触发条件指向尚未开放的关卡，当前仅登记版本差异。"
        if rec.get("encounters"):
            rec["cast"]=uniq(rec["cast"]+rec["encounters"])
    for v in tables.rows("CharacterArchiveBaseInfo").values():
        profile=idx.get(f"mirror/CharacterArchiveContent/{v['CharacterId']}01")
        if not profile or not (v.get("UpdateStory1") or v.get("UpdatePlot1")):continue
        lang=tables.lang("CharacterArchiveBaseInfo")
        if v.get("UpdateContent1") not in lang:continue
        old=lang.get(v.get("Content"));new=lang[v["UpdateContent1"]]
        title=lang.get(v["Title"],"档案字段")
        profile.setdefault("fieldRevisions",[]).append(dict(field=title,original=old,revised=new,afterStory=v.get("UpdateStory1"),afterPlot=v.get("UpdatePlot1")))
        profile["sources"]=profile.get("sources",[])+[dict(label=f"基本信息 · {title} 的改订配置",url=tables.url("CharacterArchiveBaseInfo",v["Id"],False))]
    history=[
        ("角斗场与守夜人时期",[m(1110),"mirror/CharacterArchiveContent/16211","mirror/CharacterArchiveContent/16212"]),
        ("同一历史的两种记述：《新诺瓦前史》与《旧诺瓦前史》",[m(101),m(605),m(1001)]),
        ("沙漠星塔的许愿箱",[start,key("prologue","STm00_02"),n(100201)]),
        ("水道桥与地下诊所",[m(104),m(208),n(100103),n(100803),m(211)]),
        ("三大魔物讨伐的前后",[m(309),m(404),m(416),n(101301)]),
        ("达尔茜亚事件后的菲莱",[m(622),n(101801)]),
        ("两支队伍记录的海上救援",[e(201030209),e(101100203)]),
        ("怀璟食府的代理店长日记",["mirror/CharacterArchiveContent/11711","mirror/CharacterArchiveContent/11712"]),
    ]
    return [dict(label=label,stories=items,source=idx[items[0]]["source"]) for label,items in history]


def graphs(stories,tables,history):
    narrative=sorted(stories,key=lambda r:(r["route"],r["order"],r["id"]))
    names=defaultdict(list);first=defaultdict(list);rels=set()
    for r in narrative:
        for n in r["cast"]:names[n].append(r["id"])
        for n in r.get("encounters",[]):first[n].append(r["id"])
        for field,kind,reverse in [("requires","prerequisite",True),("readAfter","reading",True),("unlockRequires","unlock",True),
                ("related","related",False),("branches","branch",False),("parallelNext","parallel",False),("alternativeParents","alternative",True)]:
            for target in r.get(field,[]):
                a,b=(target,r["id"]) if reverse else (r["id"],target)
                if a!=b:rels.add((a,b,kind) if kind!="related" else (*sorted([a,b]),kind))
        for x in r.get("topologyParents",[]):
            if not any((x,r["id"],ty) in rels for ty in ("branch","parallel","unlock","alternative","prerequisite")):
                rels.add((x,r["id"],"path"))
    ch=[];orgs={};departments={}
    for row in tables.rows("Character").values():
        if row.get("Available") and row.get("Visible"):
            char=tables.lang("Character")[row["Name"]]
            org=tables.rows("CharacterDes")[str(row["Id"])]["Force"]
            force=tables.rows("Force")[str(org)]
            departments[char]=tables.lang("Force")[force["Title"]]
    lookup={s["id"]:s for s in stories}
    for name in sorted(names,key=lambda n:(n not in departments,n)):
        shape=dict(name=name,stories=names[name],first=first[name],firstIndexed=names[name][0],
                   forms=[other for other in departments if other!=name and other.split("（")[0]==name.split("（")[0]])
        org=departments.get(name)
        if org:
            shape["organization"]=org
            ob=orgs.setdefault(org,dict(name=org,members=[],stories=[],links=[]))
            ob["members"].append(name)
            # Explicit affiliations in the file are distinct from a member acting privately.
            ob["stories"].extend([i for i in names[name] if org in lookup[i].get("keywords",[]) or org in lookup[i]["evidence"]])
        ch.append(shape)
    orgs.setdefault("联合种业",dict(name="联合种业",members=[],stories=[],links=[]))
    orgs.setdefault("白垩商会",dict(name="白垩商会",members=[],stories=[],links=[]))
    orgs.setdefault("菲莱公司",dict(name="菲莱公司",members=[],stories=[],links=[]))
    firm=next(x for x in stories if x.get("nodeId")==807 and x["type"]=="主线")
    for name,to in [("菲莱公司","联合种业"),("联合种业","菲莱公司")]:
        orgs[name]["links"].append(dict(to=to,label="投标日后，翡冷翠与岭川的“所属”档案改为菲莱公司",story=firm["id"]))
        orgs[name]["stories"].append(firm["id"])
    for one,two,label,typ,i in [
        ("空白旅团","灰风俱乐部","代替孩子们爬塔","主线",107),("灰风俱乐部","白垩商会","被迫为商会爬塔","主线",107),
        ("空白旅团","万送屋","承接投递委托","活动",101060201),("花令旅团","联合种业","公司对讨伐队施压","主线",404),
        ("恩赐意志","帝国卫队","共同参与星塔联合作战","尖兵陷阵",None)]:
        r=next(x for x in stories if x["type"]==typ and (x.get("nodeId")==i if i is not None else "开场剧情" in x["title"]))
        for aa,bb in [(one,two),(two,one)]:
            orgs[aa]["links"].append(dict(to=bb,label=label,story=r["id"]))
            orgs[aa]["stories"].append(r["id"])
    for org in orgs.values():org["stories"]=uniq(org["stories"])
    periods={s["phase"]:s.pop("_periodOrder") for s in stories}
    timeline=dict(periods=[dict(id=k,label=k,order=v) for k,v in sorted(periods.items(),key=lambda x:(x[1],x[0]))],
                  edges=[dict(from_=a,to=b,type=c) for a,b,c in sorted(rels)],history=history,organizations=list(orgs.values()))
    for ed in timeline["edges"]:ed["from"]=ed.pop("from_")
    return ch,timeline


def build(root,cache):
    root=root.resolve()
    state=read(root/".upstream_sync_state.json");snap=revision(root)
    tables=supplement.Tables(root,cache)
    pages=read(root/"story_docs/_data/sections.json")["pages"]
    catalog={mdid(p):p for p in pages}
    stats=Counter(p["family"] for p in pages)
    all_stories=main_events.build(root)+side_stories.build(root)+misc_stories.build(root)+supplement.build(root,tables)
    from prose_review import apply as review_disc_prose
    review_disc_prose(all_stories,pages)
    hist=add_relations(all_stories,pages,tables)
    profile_review.apply(all_stories,pages)
    ids=set();progress=set()
    for r in all_stories:
        rid=r["id"]
        p=catalog.get(rid)
        if rid in ids:raise ValueError("Duplicate "+rid)
        ids.add(rid)
        if p:
            r["progressKey"]=p["family"]+":"+str(p["id"]);r["archivePage"]=p["page_md"]
        elif rid.startswith("anecdotes/"):
            r["progressKey"]="anecdotes:"+rid.split("@")[-1]
        elif r.get("nodeId") and r["type"] in ("主线","特别篇","活动"):
            r["progressKey"]=("events:" if r["type"]=="活动" else "main:")+str(r["nodeId"])
        else:r["progressKey"]=rid
        if r["progressKey"] in progress:raise ValueError("Conflicting progress ID "+r["progressKey"])
        progress.add(r["progressKey"])
        if p and r["id"].startswith("npc_bonds/"):r.setdefault("textSource",permalink(snap,p["page_md"]))
        if p and not r.get("summary") and p.get("recap") and r["type"] in ("主线","特别篇","序章"):
            # The research notes already provide a spoiler-safe entry point and an individual rationale.
            r["keywords"]=uniq(r.get("keywords",[])+[p.get("code")])
        r["cast"]=uniq(clean(n) for c in r["cast"] for n in re.split(r"[&＆]",c)
                       if n.strip() not in ("旁白","？？？","???","三人","二人","两人","众人","匿名",""))
        r["sources"]=sources_for(r)
        r["availability"]=r.get("availability") or "已收录"
        r["timeWindow"]=r["phase"]
        r["phase"],r["_periodOrder"],r["positionStatus"],sort,date=dated_period(r)
        if sort is not None:r["chronoSort"]=sort
        if date:r["dateLabel"]=date
        r["sceneLabels"]=[]
        for scene in r.get("scenes",[]):
            if not isinstance(scene,dict):continue
            y=scene.get("year")
            year=f"前星塔历{-y}年" if isinstance(y,int) and y<0 else f"星塔历{y}年" if y else ""
            place=scene.get("place","")
            r["sceneLabels"].append(" · ".join(filter(None,[year,scene.get("date"),scene.get("time"),place])))
        if r.get("parallelKey") and "04:15" in r["parallelKey"]:
            r["dateScope"]="04:15 是两篇共有的场景。各篇还叙述了其他时段。"
        if r.get("parallelKey") and "救援" in r["parallelKey"]:
            r["dateScope"]="两篇交叉描写同一救援；日历上的具体日子仍未给出。"
    # An editorial slot can place a backstory late. Inside that reading plan, do
    # not offer a chat/revision before its real unlock or its chosen reading prerequisites.
    rows={r["id"]:r for r in all_stories}
    prereqs={r["id"]:{x for field in ("requires","unlockRequires","readAfter","topologyParents")
                      for x in r.get(field,[])} for r in all_stories}
    for sid in TopologicalSorter(prereqs).static_order():
        if not prereqs[sid]:continue
        latest=max(rows[x]["route"] for x in prereqs[sid])
        if rows[sid]["route"]<=latest:rows[sid]["route"]=round(latest+0.00001,6)
    characters,timeline=graphs(all_stories,tables,hist)
    covered={r["archivePage"] for r in all_stories if r.get("archivePage")}
    wanted={p["page_md"] for p in pages}|{p.relative_to(root/"story_docs").as_posix() for p in (root/"story_docs/_chat").glob("PM*.md")}
    if covered!=wanted:raise ValueError(f"Coverage mismatch: missing {wanted-covered}, extra {covered-wanted}")
    for r in all_stories:
        if not all(r.get(k) for k in ("source","time","grade","reason","evidence","phase","positionStatus")):raise ValueError("Incomplete record "+r["id"])
        if r["grade"] not in GRADE_NAMES or urlparse(r["source"]).scheme not in ("http","https"):raise ValueError("Invalid basis "+r["id"])
    for e in timeline["edges"]:
        if not {e["from"],e["to"]}<=ids:raise ValueError("Dangling relationship "+str(e))
    raw_count={ty:dict(Counter(z["grade"] for z in all_stories if z["type"]==ty)) for ty in sorted({r["type"] for r in all_stories})}
    snapshot_date=state["last_synced_at"].split("T")[0]
    meta=dict(snapshot=snap,date=snapshot_date,archiveUrl=SITE,upstream=state,grades=GRADE_NAMES,
              stats=dict(archivePages=len(pages),archiveFamilies=dict(stats),archiveScripts=len(wanted),stories=len(all_stories),
                         types={k:sum(v.values()) for k,v in raw_count.items()},gradeByType=raw_count,
                         positions=dict(Counter(z["positionStatus"] for z in all_stories))))
    # Stable output order makes a new snapshot diffable while retaining editorial routes in their own file.
    all_stories.sort(key=lambda r:(r["route"],r["group"],r["order"],r["id"]))
    timeline["readingOrder"]=[r["id"] for r in all_stories]
    phase_pos={p["id"]:p["order"] for p in timeline["periods"]}
    timeline["chronology"]=[r["id"] for r in sorted(all_stories,key=lambda r:(phase_pos[r["phase"]],r.get("chronoSort",0),r["group"],r["order"]))]
    obj={"stories":all_stories,"characters":characters,"timeline":timeline,"meta":meta}
    dest=OUT/"data";dest.mkdir(exist_ok=True)
    def emit(name,data,pretty=True):
        (dest/name).write_text(json.dumps(data,ensure_ascii=False,indent=2 if pretty else None)+"\n",encoding="utf8")
    emit("story-data.json",all_stories);emit("characters.json",characters);emit("timeline.json",timeline);emit("metadata.json",meta)
    (dest/"guide.js").write_text("window.GUIDE="+json.dumps(obj,ensure_ascii=False,separators=(",",":")).replace("\u2028","\\u2028").replace("\u2029","\\u2029")+";\n",encoding="utf8")
    return meta


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive",type=Path,help="local stellasora-archive Git checkout")
    parser.add_argument("--cache",type=Path,required=True,help="directory for pinned upstream source tables")
    args=parser.parse_args()
    print(json.dumps(build(args.archive,args.cache)["stats"],ensure_ascii=False,indent=2))
