"""Compile every prologue, main-story and event node, including scriptless rows."""
import heapq
import re
from collections import defaultdict
from pathlib import Path

from common import MIRROR, SITE, base_record, clean, mdid, permalink, read, revision, tags, uniq
from main_event_notes import CHAPTER_REASONS, CHAPTER_ROUTE, EVENTS, STAGE_NOTES, MAIN_NOTES

MONTHS = ("雪月","旅月","鸣月","清月","花月","雨月","雷月","热月","谷月","猎月","雾月","霜月")


def cal(year=None, month="", day=None, clock=""):
    return dict(year=year, month=month, day=day, clock=clock, precision=(
        "时分" if clock else "日" if day else "月" if month else "年" if year is not None else "相对"))


def label(c):
    y = c["year"]
    return " ".join(str(x) for x in (
        (f"前星塔历{-y}年" if y < 0 else f"星塔历{y}年") if y is not None else "",
        c["month"], f'{c["day"]}日' if c["day"] else "", c["clock"]) if x)


def calendar_from_scene(year, scene):
    m = re.search(r"([^\s?？]+月)\s*(\d+)日", scene.get("date",""))
    if not m:
        return cal(year)
    clock = scene.get("time","").replace("：",":")
    return cal(year,m[1],int(m[2]),clock if re.fullmatch(r"\d{1,2}:\d{2}",clock) else "")


def cast_of(p):
    return uniq(clean(person) for field in p.get("speakers",[]) for person in re.split("[&＆]",field)
                if person not in {"旁白","？？？","???","三人","两人","众人",""} and clean(person))


def read_page(root,p,commit):
    story = root/"story_docs"
    file = story/p["page_md"]
    body = file.read_text(encoding="utf-8")
    beats = read(story/"_beats"/p["page"].replace(".html",".json"))["beats"]
    return {
        "cast":cast_of(p), "keywords":tags(body.split("## 3.",1)[-1]),
        "scenes":[{k:v for k,v in beat.items() if k in {"place","time","date"}}
                  for beat in beats if beat["k"]=="scene"],
        "textSource": permalink(commit,p["page_md"]),
    }


def topo(ids,parents):
    """Order siblings stably by their table IDs. Never connect sibling paths."""
    children = defaultdict(list)
    indegree = {}
    for i in ids:
        local = set(parents[i]).intersection(ids)
        indegree[i] = len(local)
        for parent in local:
            children[parent].append(i)
    queue = [i for i,d in indegree.items() if not d]
    heapq.heapify(queue)
    order = []
    while queue:
        node = heapq.heappop(queue)
        order.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if not indegree[child]:
                heapq.heappush(queue,child)
    if len(order)!=len(ids):
        raise ValueError("原始关卡出现环，请先核对分支条件。")
    return order,children


# These year assignments are scene-specific. The chapter subtitle dates the
# reading frame; narrators and scene cards sometimes give very different years.
SCENE_YEARS = {
    604:[992,995,996],606:[996,994,996,996],613:[1000]*4+[None],
    812:[None],821:[996,None,None,None,996,996,996,996],
    909:[994]*3,910:[994,994,995,995],920:[981,986],921:[987]*7,922:[987,988],
}

# Statement, chronological sort anchor, evidential basis, presentation mode.
MAIN_OVERRIDES = {
    110:("996年花月27日21:00分出另一种人生，经历多年后回到同日17:45。",cal(996,"花月",27,"21:00"),"叙述覆盖数年，随后经白色房间重回分歧。后面的主线不继承这条人生的岁月。","分支终局／回溯","A"),
    405:("分歧自996年雨月28日延至雷月3日，其后还写到多年后再次入林。",cal(996,"雨月",28,"09:00"),"前半有日时场记，多年后的再次搜寻另见正文及跳过概要。","分支终局／时间跳跃","A"),
    101:("第一章现时为996年花月醒神草日08:00；开场另含梦境。",cal(996,"花月",26,"08:00"),"章节时段栏与第三节同一天的场记互证。开篇先读魔王传说与梦境，醒来时人在幸运绿洲号。","梦境／现时","B"),
    102:("996年花月醒神草日09:00。",cal(996,"花月",26,"09:00"),"第一章时段栏的第二格；紧接售卖神器，与10:00商店门前的场景相连。","现时","B"),
    309:("两个月前的清月6日与996年雨月16日夜交替。",cal(996,"清月",6,"11:00"),"开篇明示两个月前的讨伐，随后场记回到雨月16日的旧协会之家。","回忆／现时","A"),
    404:("996年清月6日至7日的往事，嵌入雨月27日的谈话。",cal(996,"清月",6,"11:10"),"无名地洞的对话两度切回两个月前，与第三章《失败的讨伐》相差十分钟的清月场记互证。","回忆／现时","A"),
    415:("梦内月日以问号呈现；发生在第四章09调查与梦醒之间。",cal(),"夏花在理想生活中发现违和，概要明确指出此处是梦。梦内钟点不宜放上现世日历。","梦境","A"),
    511:("996年热月1日至2日；案情分析涉及994年以及996年花月。",cal(996,"热月",1,"02:00"),"首个场记在联合种业仓库，随后按两年前、两个月前复盘线索。","现时／回述","A"),
    604:("童年未定年 → 992年雾月16日 → 995年谷月23日 → 996年谷月5日。",cal(992,"雾月",16,"10:30"),"庭审、办公室的三处场记前均有旁白年号；早于庭审的父女相处没有年份。","多年代回忆","A"),
    606:("996年谷月5日01:30起，穿插994年雷月14日夜的秘密行动。",cal(996,"谷月",5,"01:30"),"两年前的回忆配有994年字幕；执行官办公室和贵宾招待室仍属996年。","现时／回忆","A"),
    613:("本路线四年后，1000年猎月14日至15日；末尾白色房间无日期。",cal(1000,"猎月",14),"本节在第一个场景牌以前已经给出1000年，时间只在这一种终局成立。","分支终局","A"),
    617:("996年谷月5日19:00谈话，插入992年霜月30日。",cal(996,"谷月",5,"19:00"),"眼前的结盟与往年的泄密案有独立年号。","现时／回忆","A"),
    809:("996年猎月13日18:00起；本结局还写到一年后。",cal(996,"猎月",13,"18:00"),"本支线落选后的经过延伸到一年后，未转化为其他选项的共同历史。","分支终局","A"),
    811:("996年猎月13日17:30，分支中跳到两年后。",cal(996,"猎月",13,"17:30"),"贷款谈判后，旁白回看两年前的抵押，以下三个终局沿用这条路线。","分支／时间跳跃","A"),
    812:("这一分支的998年9月起，再跨过一个月。",cal(998,"9月"),"正式年号和地点写在第一句旁白。末尾白色房间场记留空。","分支终局","A"),
    813:("《亿万》的两年后时段再过一年半，绝对日期未写。",cal(),"第一句旁白为一年半后。不能把相邻结局《自异世界》的月份挪用到这里。","分支终局","A"),
    814:("承接《亿万》的融资危机，后半再过两个月。",cal(),"经理谈及两年前的贷款，旁白另标两个月后。","分支终局","A"),
    821:("996年猎月14日至15日的登塔；穿插衰败城邦的谷月片段，年份未注。",cal(996,"猎月",14,"20:50"),"场景从菲莱星塔切到衰败城邦，又回到同晚的星塔十五层。","现时／往事","A"),
    908:("鸢尾幼年到离开孤儿院，早于994年段落；第八章在梦中呈现。",cal(),"概要与《空白的正解 中》开首的994年号共同约束童年回忆的上界。","回忆","B"),
    909:("994年清月24日至花月5日，第八章梦中追忆。",cal(994,"清月",24,"10:00"),"首句明示994年，清月与花月的场记依次指向备考与许愿。","回忆","A"),
    910:("前篇994年花月的落榜与同年霜月，续到995年鸣月25日。",cal(994,"花月",20,"10:00"),"贝林港一幕前旁白明示995年；开头承接上节考试。","回忆","B"),
    918:("996年雾月17日的谈话，含六年前的白猫往事。",cal(996,"雾月",17,"12:30"),"水吧场记与六年前、三个小时后的旁白区分讲述时刻与往事。","现时／回忆","A"),
    920:("981年花月2日，随后为986年雨月21日。",cal(981,"花月",2,"09:50"),"两处年份由旁白直接给出，画面都在埃摩灰城区安全屋。","回忆","A"),
    921:("987年鸣月17日至22日凌晨。",cal(987,"鸣月",17,"11:50"),"本节两次出现987年字幕；日期从无名街道推进到黎明近卫指挥部。","回忆","A"),
    922:("987年鸣月22日清晨，随后为988年鸣月21日。",cal(987,"鸣月",22,"05:30"),"旁白先报987年，再明示一年后与988年，后段转入灰城孤儿院。","回忆","A"),
    924:("《沙蝎的野望》支线的数月后，精确年月未注明。",cal(),"第一句旁白注明经过数月；安琪采取的行动只在本线发展。","分支／时间跳跃","A"),
    927:("分歧历史的997年埃摩，继而998年新奥勒良。",cal(997),"两处旁白明确标年。这是第八章B线的后续。","分支／时间跳跃","A"),
    928:("接续《蝴蝶效应》的B线终局；场记的年月日为空。",cal(),"《蝴蝶效应》与本节相连，白色房间的问号不能解释成实际日期。","分支终局","A"),
    1003:("996年雾月8日和12日的部署，回到18日14:00的米拉什。",cal(996,"雾月",8,"08:20"),"开篇倒退十天，场景分别落在菲莱、荒野和米拉什。","回忆／分支","A"),
    1024:("雾月18日C线的星塔战之后；后段关于未来的告白未列日历。",cal(996,"雾月",18),"安琪向魔王谈到她抵达过的未来。前一战由该线03C直接引出。","分支／回述","B"),
    1025:("C线终局，白色房间内的月日、时刻均为问号。",cal(),"终局返观星塔坠落与维塔的经历，正文隐藏了白色房间的日历坐标。","分支终局","A"),
    1026:("996年雾月18日17:00起，收束到雾月25日。",cal(996,"雾月",18,"17:00"),"主人公在本节回顾三次回到过去。游戏连线从幕间分出此路，阅读上应在三个终局后打开。","真终局／多次尝试","A"),
    1101:("场景转入前星塔历4年；人物的主观叙事承接第九章。",cal(-4),"开场重现安琪与旅团的声音；醒来后，魔王一度认错眼前的人。","历史线／主观接续","A"),
    1110:("前星塔历4年的谈话中讲述一年前的角斗场往事。",cal(-5),"艾琳娜讲起自己仍是角斗士时的经历，明确说事情发生在一年前。此处负年为依上文推算。","回忆","B"),
}


def main_timing(ch,node,record,parents,children,nodes,page_data):
    cid,sid = ch["id"],node["sid"]
    year = -4 if cid==11 else 996 if ch["year"].replace(" ","")=="星塔历996年" else None
    scenes = record["scenes"]
    if sid in SCENE_YEARS and len(SCENE_YEARS[sid])!=len(scenes):
        raise ValueError(f"{sid} 的跨年代场景数量改变，请重新校勘镜头年号。")
    for i,scene in enumerate(scenes):
        override = SCENE_YEARS.get(sid,())
        scene["year"] = None if re.search(r"[?？]",scene.get("date","?")) else (override[i] if i<len(override) else year)
    if sid in MAIN_OVERRIDES:
        t,c,e,m,g=MAIN_OVERRIDES[sid]
        return t,c,e,m,g
    dated = [s for s in scenes if re.search(r"[^?？\s]月\s*\d+日",s.get("date",""))]
    if dated:
        first,last=dated[0],dated[-1]
        c=calendar_from_scene(first["year"],first)
        t=label(c)
        if first!=last:
            t+=" 起；篇末有时标的场景为"+last["date"]+" "+last.get("time","")
        e="场记注明"+first.get("place","本节场景")+"，"+first["date"]+" "+first.get("time","")+"。"
        if first!=last:
            e+="末处有时标的地点为"+last.get("place","未署名地点")+"。"
        return t,c,e,"分支终局" if node["is_branch"] else "现时","A"
    if cid==11:
        return "前星塔历4年，所在节没有独立的月日场记。",cal(-4),"章节标题注明前星塔历4年；本节承接"+("上文所述的旅程。" if not parents[sid] else "《"+nodes[parents[sid][0]]["title"]+"》的行动。"),"历史线","A"
    if sid in (507,508,509):
        return ("996年雷月31日的分头调查。",cal(996,"雷月",31),"从02节已标时的办公日开始，三组分别进入公司不同部门；当夜04节收拢线索。","分头视角","B")
    # Battle stages often omit scene cards. Use bounded neighbouring scenes and
    # never assign the nearest clock time as if it were stamped on the battle.
    neighbours=[]
    for side,direction in (("前",parents[sid]),("后",children.get(sid,[]))):
        for i in direction:
            n=nodes.get(i,{})
            sc=page_data.get(i,{}).get("scenes",[])
            marker=(sc[-1] if side=="前" else sc[0]) if sc else None
            if marker and not re.search(r"[?？]",marker.get("date","?")):
                neighbours.append((side,n,marker))
    dates=uniq(m["date"] for side,n,m in neighbours)
    if dates:
        where="；".join(f"{side}接《{n['title']}》{m['date']} {m.get('time','')}" for side,n,m in neighbours)
        bounded=len({side for side,n,m in neighbours})==2
        if len(dates)==1 and bounded:
            date=calendar_from_scene(year,{"date":dates[0]})
            return label(date)+"（前后场记夹定，分钟未标）",date,"本节无独立场记；"+where+"。","战斗" if node["kind"]=="battle" else "现时","B"
        common_month=uniq(calendar_from_scene(year,{"date":d})["month"] for d in dates)
        coarse=cal(year,common_month[0]) if len(common_month)==1 else cal(year)
        position=(" 至 ".join(dates)+"之间") if bounded else dates[0]+("之后" if neighbours[0][0]=="前" else "之前")
        return (f"{ch['year']} · {position}（场景边界）",coarse,where+"；本节未标独立钟点。","战斗" if node["kind"]=="battle" else "现时","B")
    return (ch["year"]+"；本节未提供可独立核对的日期。",cal(year),
            "篇章年号可核；通过正式关卡及前置连线定位，场景没有单独日历。",
            "战斗" if node["kind"]=="battle" else "现时","B")


def collect_main(root,sec,chapters,tables,by_id,commit):
    results=[]
    cond=tables["mainConditions"]
    nodes={n["sid"]:n for ch in chapters for n in ch["nodes"]}
    by_key={n["story_id"]:n["sid"] for n in nodes.values()}
    ids={sid:by_id["main",sid] if ("main",sid) in by_id else f"main/{n['story_id']}"
         for sid,n in nodes.items()}
    page_data={sid:read_page(root,sec["main",sid],commit) for sid in nodes if ("main",sid) in sec}
    for ch in chapters:
        cc = ch["id"]
        group=ch["name"]+" · "+ch["title"]
        group_ids={n["sid"] for n in ch["nodes"]}
        parents={}
        for sid in group_ids:
            n=nodes[sid]
            upstream=n["parents"] or cond.get(n.get("condition"),{}).get("parents",[])
            parents[sid]=uniq(by_key[k] for k in upstream if k in by_key and by_key[k] in group_ids)
        order,children=topo(group_ids,parents)
        for ordinal,sid in enumerate(order,1):
            n=nodes[sid]
            p=sec.get(("main",sid))
            pending = n["state"]=="unreleased" or (n["title"]=="敬请期待" and not p)
            source=SITE+n["page"] if n.get("page") else permalink(commit,"_data/chapters.json")
            r=base_record(ids[sid],n["code"]+" · "+n["title"],"特别篇" if ch["special"] else "主线",group,ordinal,source)
            if p:
                r.update(page_data[sid])
            else:
                r.update(scenes=[],keywords=[])
            rawparents=[ids[i] for i in parents[sid]]
            routes=CHAPTER_ROUTE.get(cc,1190)
            r.update(route=routes+ordinal/100,optional=False,requires=[],related=[],readAfter=[],
                     unlockRequires=rawparents if len(rawparents)==1 else [],
                     alternativeParents=rawparents if len(rawparents)>1 else [],
                     branches=[ids[i] for i in sorted(children[sid])] if len(children[sid])>1 else [],
                     topologyParents=rawparents, nodeId=sid,storyKey=n["story_id"],code=n["code"],
                     availability="待开放" if pending else "已收录" if p else "无独立对白",
                     released=not pending,places=uniq(s.get("place") for s in r["scenes"] if s.get("place","").strip("?？ ")),
                     phase=ch["name"] if not ch["special"] else ("前星塔历" if cc==11 else "第六章后"),
                     risk="高" if cc>=5 or n["is_branch"] else "低" if cc==1 and ordinal<3 else "中",
                     reason=CHAPTER_REASONS.get(cc,"依本章内的原始关卡导航阅读。"))
            if not parents[sid]:
                gate=[ids[by_key[k]] for k in ch["prev_stories"] if k in by_key]
                r["unlockRequires"]=gate
                r["readAfter"]=gate
            if cc==1 and sid==101:
                r["readAfter"]=[by_id["prologue","STm00_02"]]
            if cc==11:
                r["aliases"]=["遗尘之庭 银沙黎明","遗尘之庭·银沙黎明","遺塵之庭 銀沙黎明","暁天を破る、創生の光"]
            if len(rawparents)>1:
                r["reason"]+=" 本节汇合的是不同来路，任选适用路线接续；详情页的前置选项可回看。"
            if len(children[sid])>1:
                r["reason"]+=" 此处可通向不同路线，选择后沿该线阅读。"
            if n["is_branch"]:
                r["reason"]+=" 此为该路线的独立终局。阅读其他走向时回到分歧点。"
            if sid==1026:
                r["readAfter"]=[ids[i] for i in [1011,1018,1025]]
            if pending:
                r.update(grade="U",phase="待开放",calendar=cal(),mode="待开放",
                         time="第九章后的特别篇续段；仅有关卡预留，正文时刻未定。",
                         evidence="快照中仅有编号与“敬请期待”；10月28日延期公告改列11月13日。",route=1190+ordinal/100,
                         reason="排在本特别篇已公开段落之后。待实际更新再核时点和剧透。")
            else:
                t,c,e,m,g=main_timing(ch,n,r,parents,children,nodes,page_data)
                r.update(time=t,calendar=c,evidence=e,mode=m,grade=g)
                if c["year"] is not None and (c["year"] not in [996] or cc==11):
                    r["phase"]=label(cal(c["year"]))
                if sid==908:r["phase"]="序章前"
                if not p:
                    r["evidence"]+=" 关卡表保留此战，档案未取得独立气泡剧本。"
            if cc==11:
                r["refs"]=["https://stellasora.yostar.cn/news/4887","https://stellasora.stargazer-games.com/news/4972",
                           "https://stellasora.yostar.cn/news/5001"]
            if n["kind"]=="battle":
                r["nodeKind"]="战斗"
            if sid in MAIN_NOTES:
                r["summary"]=MAIN_NOTES[sid]
            results.append(r)
    return results,ids


EVENT_MOMENTS = {
    101090202:("几个月前的苍梧回忆；讲述框为996年谷月。",cal(),"回忆／现时"),
    101090203:("回顾不久前的千塔行；讲述框为996年谷月。",cal(),"回忆"),
    201010208:("996年霜月25日交谈；童年的遭遇与雪愿树精灵的起源传说各自未署年。",cal(996,"霜月",25),"现时／回忆／传说"),
    201010209:("996年霜月25日讲述的童年往事；回忆只明说是大雪纷飞的一天，未标年份或日号。",cal(),"回忆"),
    201010210:("菈露童年的飞行；回到996年霜月25日送礼当天。",cal(996,"霜月",25),"回忆／现时"),
    201010214:("996年霜月25日深夜，尾声写到雪愿节结束、新的一天将至。",cal(996,"霜月",25),"现时"),
    101070204:("997年鸣月谈话，回忆的是大约一年前。",cal(997,"鸣月"),"现时／回忆"),
    101110203:("活动回顾标997年清月；正文从训练推进一个月，起止日未写。",cal(997),"时间跳跃"),
    101050211:("997年清月的决战穿插埃妲过往；回忆本身又跨过数月。",cal(997,"清月"),"现时／回忆"),
}


def collect_events(root,sec,tables,by_id,commit):
    records=[]
    source_url=f"{MIRROR}/blob/{tables['upstreamCommit']}/CN/language/zh_CN/ActivityStoryChapter.json"
    event_ids={}
    groups=defaultdict(list)
    for row in tables["eventNodes"]:
        sid=row["id"]
        event_ids[sid]=by_id.get(("events",sid),f"events/{row['group']}/{sid}")
        groups[row["group"]].append(row)
    for cid,rows in sorted(groups.items()):
        rows.sort(key=lambda x:x["id"])
        period=tables["eventPeriods"][str(cid)]
        y_and_month=re.fullmatch(r"星塔历\s*(\d+)\s*年\s*(\S+月)",period["time"])
        yr=int(y_and_month[1]) if y_and_month else None
        month=y_and_month[2] if y_and_month else ""
        pos,place,reason=EVENTS.get(cid,(1180,"","关卡按活动内前置顺序阅读；新增活动的跨篇关系待考。"))
        group=next((sec["events",n["id"]]["group"]["label"] for n in rows if ("events",n["id"]) in sec),period["title"])
        parents={n["id"]:n["parents"] for n in rows}
        order,children=topo(set(parents),parents)
        notes=STAGE_NOTES.get(cid,[])
        for rawpos,n in enumerate(rows):
            sid=n["id"]
            p=sec.get(("events",sid))
            ordinal=order.index(sid)+1
            r=base_record(event_ids[sid],n["code"]+" · "+n["title"],"活动",group,ordinal,
                          SITE+f"events/{cid}/{sid}.html")
            if p:
                r.update(read_page(root,p,commit))
            else:
                r.update(scenes=[],keywords=[])
            date=cal(yr,month,25 if cid==20101 else None)
            t=label(date)+(" · 雪愿节" if cid==20101 else "（活动回顾所标全篇时段，具体日未写）")
            if cid==10111 and rawpos>=2:
                t="回顾标997年清月；训练已经过一个月，当前独立月日未写。"
                date=cal(997)
            t,date,mode=EVENT_MOMENTS.get(sid,(t,date,"战斗" if not p else "现时"))
            notes_for_stage=notes[rawpos] if rawpos<len(notes) else "此节点只从原始表取得篇内位置，待补正文交叉定位。"
            pr=[event_ids[i] for i in n["parents"] if i in event_ids]
            r.update(route=pos+ordinal/100,optional=False,phase=period["time"] or "未知",
                     nodeId=sid,code=n["code"],groupId=cid,calendar=date,time=t,mode=mode,
                     grade="A" if y_and_month else "U",reason=reason,
                     evidence=f"活动回顾 {period['key']} 载“{period['time']}”。"+notes_for_stage,
                     places=uniq([s.get("place") for s in r["scenes"]]+([place+"（活动范围）"] if place else [])),
                     refs=[source_url],risk="高" if cid in (10107,10105,10109,10111) or rawpos>=len(rows)-2 else "中",
                     requires=pr if len(pr)==1 else [],readAfter=[],related=[],
                     alternativeParents=pr if len(pr)>1 else [],topologyParents=pr,
                     branches=[event_ids[i] for i in children[sid]] if len(children[sid])>1 else [],
                     availability="已收录" if p else "无独立对白",released=True)
            if not p:
                r.update(nodeKind="战斗",evidence=r["evidence"]+" 关卡表未挂接独立AVG。")
            r["summary"]=notes_for_stage
            if cid==10104:
                r["aliases"]=[period["title"]]
            if sid in [101090202,101090203,201010209]:
                r["phase"]="已知相对顺序"
            if len(pr)>1 or len(children[sid])>1:
                r["reason"]+=" 同一问题有多种处理路线，平行选读后返回公共节点。"
            records.append(r)
    return records,event_ids


def build(root):
    root=Path(root)
    commit=revision(root)
    table_file=Path(__file__).with_name("main-event-tables.json")
    tables=read(table_file)
    if tables["upstreamCommit"]!=read(root/".upstream_sync_state.json")["stella_sora_data_commit"]:
        raise ValueError("上游固定版本已改变，请运行 refresh_main_tables.py 更新游戏回顾和拓扑表。")
    data=root/"story_docs"/"_data"
    sections=read(data/"sections.json")["pages"]
    by_id={(p["family"],p["id"]):mdid(p) for p in sections}
    sec={(p["family"],p["id"]):p for p in sections}
    results=[]
    for i,p in enumerate(sorted((x for x in sections if x["family"]=="prologue"),key=lambda x:x["id"]),1):
        r=base_record(mdid(p),p["code"]+" · "+p["title"],"序章","序章 · 最初的起点",i,SITE+p["page"])
        r.update(read_page(root,p,commit),grade="A",risk="低",route=(i-1)/100,optional=False,phase="序章",
                 mode="现时",availability="已收录",released=True,calendar=cal(),code=p["code"],nodeId=p["id"],
                 places=["沙漠星塔"] if i==1 else ["幸运绿洲号","另一座星塔"],
                 evidence="沙漠星塔里，尘沙、琥珀、鸢尾从许愿箱中找到主角。" if i==1 else "醒来的人与旅团初步相识，随她们登塔；第一章已经追问身份。",
                 reason="从三人找到许愿箱开始，随后进入失忆者的视角。两份脚本各自保留阅读进度。",
                 time="开箱、失忆者醒来，早于第一章进城；本文无年月日。",
                 requires=[] if i==1 else [results[0]["id"]])
        results.append(r)
    main,mid=collect_main(root,sec,read(data/"chapters.json")["chapters"],tables,by_id,commit)
    events,eid=collect_events(root,sec,tables,by_id,commit)
    results.extend(main+events)
    index={r["id"]:r for r in results}
    def links(start,field,items):
        index[start][field]=uniq(index[start].get(field,[])+items)
    # Narrative/review links are explicitly distinct from game unlock conditions.
    links(eid[101070201],"requires",[eid[201010212]])
    links(eid[101060206],"requires",[eid[111000210]])
    links(eid[101060201],"readAfter",[eid[111000211]])
    links(eid[101110201],"readAfter",[by_id["storysets",101303]])
    links(eid[101110201],"requires",[by_id["storysets",101303]])
    links(eid[101040201],"related",[by_id["storysets",100303]])
    links(eid[201010206],"related",[by_id["storysets",100701],by_id["storysets",100702]])
    links(eid[101050212],"related",[by_id["storysets",101403]])
    links(eid[101090210],"related",[mid[6506],mid[911]])
    links(eid[101100201],"readAfter",[eid[111000211],eid[201030211]])
    links(eid[101100201],"requires",[eid[111000210]])
    links(eid[201030201],"readAfter",[eid[111000211]])
    links(eid[201030209],"related",[eid[101100203]])
    links(eid[101100203],"related",[eid[201030209]])
    links(eid[101100204],"related",[eid[201030211]])
    links(mid[309],"related",[mid[404]])
    links(mid[404],"related",[mid[309]])
    links(mid[1012],"readAfter",[mid[1011]])
    links(mid[1019],"readAfter",[mid[1018]])
    index[mid[1002]]["reason"]+=" 本节对白会读取先前的结局记录：先走A，再回此处依次走B、C、真终局。外界的日期重复，魔王会记得上一次。"
    index[mid[1012]]["evidence"]+=" 魔王明确利用A线撤退后所得的信息，这里的回溯只保留了主角的记忆。"
    index[mid[1026]]["evidence"]+=" 《点燃》的历史条件文本逐项检查是否已读A、B、C终局；第四个抉择关联E1004。"
    for i,j in ((507,508),(508,509),(509,507),(818,819),(819,818),(820,822),(822,820),(821,823),(823,821)):
        links(mid[i],"related",[mid[j]])
        index[mid[i]]["mode"]="分头视角" if i not in (821,) else "分头视角／回忆"
        index[mid[i]]["reason"]+=" 本段属于分头行动的一个视角；切换到另一组时会回看重叠时段。"
    for i in [506,817]:
        index[mid[i]]["reason"]="从这一节点起可以切换视角。分别阅读各组的行动，并在汇合处回到同一条调查或竞拍线。"
    links(mid[908],"related",[mid[101]])
    geography={
        100:"埃摩灰城区 · 灰城孤儿院后门",101:"幸运绿洲号／埃摩",102:"埃摩 · 心相商店",
        201:"埃摩 · 水道桥／灰城区",202:"埃摩 · 水道桥",203:"埃摩 · 水道桥",
        301:"菲莱城外",302:"菲莱城外 · 讨伐地",401:"菲莱城外 · 森林",402:"菲莱城外 · 森林",
        501:"菲莱星塔",502:"菲莱温室区",503:"菲莱温室区 · 一百号温室",
        507:"菲莱 · 联合种业研发部",508:"菲莱 · 联合种业市场部",509:"菲莱 · 联合种业生产部",
        601:"菲莱 · 联合种业",602:"菲莱城外 · 旅人营地",603:"菲莱温室区 · 实验室核心区",
        6501:"菲莱 · 晚宴会场一带",6502:"菲莱 · 酒店一带",
        802:"菲莱 · 酒店",803:"菲莱星塔",902:"菲莱",908:"埃摩 · 灰城孤儿院",
        912:"米拉什",925:"米拉什 · 矿井",1004:"米拉什",1010:"米拉什 · 矿道",
        1013:"米拉什",1020:"沙漠星塔",1023:"沙漠星塔 · 第五十层",1024:"沙漠星塔",
        1101:"押送囚车",1102:"菲兰尼斯城外 · 森林",1103:"菲兰尼斯",1104:"菲兰尼斯 · 奥林匹娅大浴场",
        1105:"菲兰尼斯 · 大浴场",1110:"埃摩大角斗场（回忆）",
    }
    for i,place in geography.items():
        if not index[mid[i]]["places"]:
            index[mid[i]]["places"]=[place]
    index[mid[603]]["summary"]="在菲莱实验室核心区，与改变自身形态的达尔茜娅交锋。"
    index[mid[507]]["related"]=uniq(index[mid[507]]["related"]+[mid[509]])
    index[mid[801]]["evidence"]+=" 夏花通过通讯回应魔王，此段气泡没有说明她的具体位置。"
    index[mid[924]]["places"]=["双子城 · 天穹保险业务部","埃摩城外 · 地理协会"]
    index[mid[927]]["places"]=["埃摩城外 · 地理协会","新奥勒良"]
    links(mid[1101],"related",[mid[1026]])
    links(by_id["prologue","STm00_02"],"related",[by_id["storysets",100201],by_id["storysets",100204]])
    index[eid[101060206]]["evidence"]+=" 魔王认出对方是上次在六角鲸岛上见过的人，直接锚定于《幽灵船》之后。"
    index[eid[101060201]]["reason"]="同为997年雨月，先读《幽灵船》再接此委托。第04节明确认出上回在六角鲸岛见过的寻宝旅人。"
    index[eid[201010206]]["evidence"]=("活动回顾为996年霜月。本节苍兰抱怨恩赐意志给万送屋少发制服，只能自己穿；"
        "异闻 #07 第一话也明写只收到一套，尺码只合苍兰。两段很可能是同届派送（跨篇互证B）。")
    index[eid[201010206]]["summary"]="在埃摩遇见身穿雪愿服的苍兰；只有她拿到制服的经过，可与异闻 #07 的派送委托对读。"
    index[eid[101110201]]["evidence"]+=" 埃莉诺亲述绑架时是前辈和谷风家政的花原相救，能具体对照异闻 #13。"
    index[eid[101090203]]["places"]=["千塔之城 · 灰城区"]
    index[eid[101090202]]["places"]=["苍梧","米拉什（回述框架）"]
    # The notice announces a future activity; it does not provide a chapter list.
    announced=base_record("announced/event-5077","执笔展卷，勾勒未名之境","活动预告","已预告活动",1,"https://stellasora.yostar.cn/news/5077")
    announced.update(route=1195,phase="待开放",calendar=cal(),grade="U",risk="低",optional=False,
                     time="仅知现实更新计划，正文尚未收入本次快照。",mode="预告",availability="待开放",released=False,
                     cast=["优叶","魔王"],places=["沉寂海"],evidence="版本前瞻称优叶带队考察沉寂海上的新岛屿。公告更新日不提供故事日期。",
                     reason="暂列预告区。活动正文上线后再确定其与雨月、热月的优叶故事有无具体承接。")
    return results+[announced]
