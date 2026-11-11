"""Index the Archive's auxiliary families, down to each note and chat segment."""
from collections import defaultdict
import re
from common import SITE, base_record, clean, mdid, permalink, read, revision, tags, uniq

NPC = {
    913301: ("三人旅团为许愿委托发愁，波西亚还在设想招人穿企鹅服。", "魔王在便利店打工前；是否同一次攀塔尚无关卡对接。", "C", 45, []),
    913302: ("魔王回忆初识旅团时误食猪排饭、被赎出，再见波西亚。", "异闻 #02 第四话救出魔王之后。", "A", 233, [("storysets",100204)]),
    917201: ("魔王跌伤胳膊，贝缇丽用针治疗，两人互报名字。", "已结识空白旅团；首次受她诊治。", "C", 234, []),
    917202: ("魔王向贝缇丽道谢，并明确想起自己在波西亚店内打过工。", "第一次诊治与异闻 #02 的便利店经历之后。", "A", 235, [("npc_bonds",917201),("storysets",100204)]),
    917301: ("珀尔娜假借白色房间不能使用，邀请魔王喝茶、吃蛋糕。", "已熟悉白色房间与回到选择的规则；未报日期。", "C", 245, []),
    917302: ("魔王主动以急性气球病的骗局反驳珀尔娜。", "珀尔娜第一话之后，再次在塔中相遇。", "A", 246, [("npc_bonds",917301)]),
    917401: ("魔王见到维嘉尔时已了解塔内食物的风险，接受她提出的挑战。", "曾被留在塔中的经历之后；具体尝试分支待考。", "C", 247, []),
    917402: ("魔王提起珀尔娜喂的蛋糕，维嘉尔首次听说此事，又请魔王托波西亚带书。", "珀尔娜的下午茶之后。", "A", 248, [("npc_bonds",917301)]),
}

# A common subject is only a reading link. Cross-family time claims are explicitly curated.
NOTE_EDITS = {
    126: ("紫槿离开弗拉维奥前后", "B", "回忆", 640, "三篇分别以尚在、即将离开、已经离开弗拉维奥开篇，适合连读。"),
    140: ("柔光技术大会之后", "B", "现时", 1115, "首篇追叙大会后着手设计，后二篇接写邀请测试、入塔试机。"),
    143: ("风影幼年及北国猎火传统", "B", "回忆", 1065, "祖父出征、幼年尾随狩猎、被接纳为猎火者分属不同叙述层次。"),
    149: ("格芮的往事／见习修者时期", "C", "回忆", 1080, "以异闻 #12 介绍角色后再读；瓶中物、战斗和孩子的片段宜结合格芮羁绊核读。"),
    158: ("雪愿节前后", "B", "现时", 1006, "任务、塔中飘雪与节后的传闻可以和雪愿节活动交叉查阅。"),
    159: ("苍梧城外的探索；与新春节庆的间距未定", "C", "现时", 1026, "新春形态在苍梧城外辨认药材和星塔，读过苍梧的活动再补此行。"),
    162: ("埃摩角斗场至菲兰尼斯守夜人时期", "B", "历史", 959, "第一篇仍在埃摩，第二篇到菲兰尼斯城门，第三篇已成为守夜人。置于历史特别篇之后避免身份剧透。"),
    130: ("夏季前的寻访，至蹲守一个月后", "C", "现时", 1105, "顺着送信的委托、提前打听营地、守候后的结果连读；文本没有给年份。"),
    144: ("千都世初识星塔至成为常客", "C", "回忆", 255, "先区分初次听说、初次攀登，再看波西亚发现她在塔内睡觉的视角。"),
    145: ("重伤醒来、再次苏醒、作出选择的同一段记忆", "C", "回忆", 1098, "镜像与面具承接少女的状态变化，先读介绍乙叶的故事再回看。"),
    137: ("幼年写生至成为旅人的时期", "C", "回忆", 1076, "三篇将童年的写生与长大后的身份压力并置。"),
}

BUBBLES = {
    "BBm00_01": "沙暴与蝴蝶", "BBm00_02":"琥珀的路标", "BBm00_03":"三人会合",
    "BBm00_04":"塔内的巨物", "BBm00_05":"为了许愿箱", "BBm00_06":"战斗尚未结束",
    "BBm_DormApproach":"琥珀的招呼", "BBm_DormIndoor":"塔内的住处", "BBm_DormOutdoor":"入口外的营地",
}


def speak(text):
    return re.findall(r"^\*\*(.+?)\*\*(?:（[^\n]+?）)?：「(.*?)」", text, re.M)


def build(root):
    docs=root/"story_docs"
    pages=read(docs/"_data/sections.json")["pages"]
    bykey={(p["family"],p["id"]):mdid(p) for p in pages}
    stamp=revision(root)
    records=[]
    for p in pages:
        family=p["family"]
        if family not in {"npc_bonds","battles_unmounted","dispatch","returnee","soldier","anecdotes"}:
            continue
        text=(docs/p["page_md"]).read_text(encoding="utf8")
        group=p["group"]["label"]
        sid=mdid(p)
        url=SITE+p["page"]
        n=p["id"]
        types={"npc_bonds":"NPC羁绊","anecdotes":"逸闻笔记","dispatch":"委托对话","soldier":"尖兵陷阵",
               "returnee":"回归剧情","battles_unmounted":"战斗气泡"}
        item=base_record(sid,p["title"],types[family],group,0,url)
        item["cast"]=uniq(p["speakers"])
        item["keywords"]=tags(text.split("## 2.",1)[-1])
        item["sources"]=[dict(label="固定版本正文",url=permalink(stamp,p["page_md"]))]
        if family=="anecdotes":
            beats=read(docs/"_beats"/(p["page"].removesuffix(".html")+".json"))["beats"]
            for no,b in enumerate((x for x in beats if x.get("k")=="anecdote"),1):
                time,grade,mode,route,why=NOTE_EDITS.get(n,("篇内见闻；与主线的距离待考","U","人物侧写",1250,
                             f"读过{group}的介绍后，按同册三篇的编排补读。通关次数或默契要求只决定笔记何时解锁。"))
                body=b["story"]
                line=text[:text.index("### "+b["title"])].count("\n")+1
                entry={**item,"id":sid+"@"+str(b["id"]),"title":b["title"],"order":no,
                       "group":p["title"],"cast":[group],"type":"逸闻笔记","time":time,"grade":grade,"mode":mode,
                       "route":route+no/100,"reason":why,"keywords":tags(body),"risk":"高" if n in (162,145,149,143) else "中",
                       "source":permalink(stamp,p["page_md"],line),"unlock":b["source"],
                       "evidence":f"笔记 {b['id']} · {b['title']}。"+clean(body.splitlines()[0])[:22]+"…",
                       "sources":[dict(label="档案库同册三篇",url=url)],"archivePage":p["page_md"]}
                if n in (162,140,158,126,143):
                    entry["phase"]={162:"前星塔历 · 菲兰尼斯",140:"997年 · 雨月",158:"996年 · 霜月前后",
                                    126:"人物往事",143:"人物往事"}[n]
                if n==162:
                    entry["places"]=[("埃摩角斗场","菲兰尼斯城门","菲兰尼斯")[no-1]]
                if n==158 and no==3:entry["time"]="雪愿节过后不久；钓鱼时听说塔中雪已停止。"
                if n==140:
                    entry["related"]=[bykey[("events",101080210)]]
                    entry["phase"]="柔光技术大会后"
                if n==149:entry["related"]=[bykey[("storysets",101201)]]
                if n==158:entry["related"]=[next(mdid(r) for r in pages if r["family"]=="events" and r["group"]["id"]==20101)]
                records.append(entry)
            continue
        if family=="npc_bonds":
            ev,tm,grade,route,deps=NPC[n]
            item.update(evidence=ev,time=tm,grade=grade,route=route,reason=ev+"按这段经历安排阅读。",
                        group=group+" · 星塔NPC好感",order=n%100,optional=False,places=["星塔"],
                        phase="序章前后" if n==913301 else "仅有相对先后", unlock=f"NPC 好感 {p['affinity']} 级",
                        requires=[bykey[k] for k in deps])
            if n==917201:item["encounters"]=["贝缇丽"]
        elif family=="battles_unmounted":
            pre=str(n).startswith("BBm00")
            item.update(group="序章 · 沙漠星塔" if pre else "营地气泡",title=BUBBLES.get(n,n)+" · "+n,
                        route=3 if pre else 1255,order=int(n[-2:]) if pre else 0,grade="B" if pre else "U",
                        phase="序章" if pre else "未知",time="寻找许愿箱期间，与序章第一节同场。" if pre else "挂载关卡未明，只有场景对白。",
                        risk="低",mode="战斗对白",reason="读过沙漠许愿箱一幕，可回看三人的行动。" if pre else "按接近、室内或室外场景补读。",
                        evidence=p.get("mount_note","")+"。"+BUBBLES.get(n,n),related=[bykey[("prologue","STm00_01")]] if pre else [],
                        places=["沙漠星塔"] if pre else [])
        elif family=="dispatch":
            voices=speak(text)
            item.update(route=1390,group=group+" · 委托",mode="可重复演出",risk="低",
                        time="特殊报酬的委托结算时，按编队抽取。",
                        reason="在认识本次编队角色后选读。同组不同结算可独立触发。",
                        evidence=f"{p['stems'][0]}；本段有 {len(voices)} 句对白，配置权重 {p.get('weight','未列')}。"+
                        ("开场由"+voices[0][0]+"发言。" if voices else ""))
        elif family=="returnee":
            item.update(group="归星漫途",grade="A",phase="仅有相对先后",time="魔王外出委托，缺席数日后，在午饭时回来。",
                        reason="先认识旅行车的四位同伴再读。可在重返游戏时单独回看。",route=275,
                        evidence="尘沙连续准备四人份饭菜，鸢尾追问魔王外出所接的委托。",mode="重逢",risk="低")
        elif family=="soldier":
            opening=bykey[("soldier","ST_sys_soldier_intro")]
            item.update(group="尖兵陷阵",route=965,mode="模式开场" if sid==opening else "条件终局",risk="高",
                        reason="读过历史特别篇已公开部分再看联军调查，留意完璧之城的呼应。",
                        time="尊者降临、先遣队无功而返之后；和主线的确切间距待考。",places=["发生异变的星塔"],
                        evidence="贝修莉娜回溯数日前的异变、派遣先遣队与本次征召。" if sid==opening else
                                 f"SoldierEndingPlan {n} 将此段列为独立终局，可从该模式开场进入阅读。",
                        requires=[] if sid==opening else [opening],order=0 if sid==opening else int(n)%100)
        records.append(item)
    records.extend(chats(docs,stamp,bykey))
    return records


def chats(docs,commit,keys):
    result=[]
    chat_ids={}
    pending={}
    for path in sorted((docs/"_chat").glob("PM*.md")):
        text=path.read_text(encoding="utf8")
        name=re.search(r"\*\*联系人\*\*：(.+?)（AddressBookId",text)[1]
        headings=list(re.finditer(r"^## \d+\. 第 (\d+) 段[^\n]*",text,re.M))
        for pos,m in enumerate(headings):
            no=int(m[1])
            body=text[m.end():headings[pos+1].start() if pos+1<len(headings) else len(text)]
            sid=f"_chat/{path.stem}@{no:02}"
            raw=(path.relative_to(docs)).as_posix()
            line=text[:m.start()].count("\n")+1
            item=base_record(sid,f"{name} · 第{no:02}段","心链",f"{name} · {path.stem}",no,permalink(commit,raw,line))
            words=speak(body)
            dialogue=" ".join(v for _,v in words)
            clue=tags(dialogue)
            gate=re.search(r"\*\*解锁条件\*\*：([^\n]+)",body)
            chat=re.search(r"\*\*Chat ID\*\*：`(\d+)`",body)
            pre=re.search(r"\*\*前置聊天\*\*：([^\n]+)",body)
            pending[sid]=re.findall(r"`(\d+)`",pre[1]) if pre else []
            if chat:chat_ids[chat[1]]=sid
            item.update(cast=uniq([name]+[n for n,_ in words]),mode="手机聊天",
                        evidence=f"{path.stem} 第{no:02}段，"+("谈及"+"、".join(clue[:4])+"。" if clue else "见本段开头及其回复选项。"),
                        keywords=clue,archivePage=raw,route=1280,reason=f"认识{name}后，可依本段聊天前置补读；同一联系人可以有多条独立话题。",
                        time="已能与联系人通讯；没有可对齐主线的日期。",unlock=gate[1].split("（Trigger")[0] if gate else "未见聊天表挂载",
                        sources=[dict(label="整份心链剧本",url=permalink(commit,raw))])
            if not chat:item["availability"]="有正文 · 未挂载";item["reason"]+="脚本中有此段，但聊天表缺行，游戏内触发待核。"
            if name=="格芮":
                item.update(route=1210,readAfter=[keys[("storysets",101203)]],reason="先读异闻 #12 的委托与初遇，再看格芮已能联络魔王的口吻。")
            if name in ("琥珀","鸢尾","尘沙"):item.update(route=277,reason="第二章后开放旅团通讯选读，保留初遇与主线的揭示。")
            if name=="尘沙（源初）":item.update(route=961,risk="高",reason="看过前星塔历特别篇后再读。心链使用手机，具体叙事框架待核，不能直接套上古纪年。")
            if name in ("菈露（圣夜）","科洛妮丝（新春）","薇洛（盛夏）"):
                act,route={"菈露（圣夜）":(20101,1008),"科洛妮丝（新春）":(10104,1028),"薇洛（盛夏）":(20103,1146)}[name]
                item.update(route=route,reason="先在对应活动中认识这一形态，再补读聊天。不同话题未必发生在活动当天。",risk="中")
            if path.stem=="PM15801" and no==6:
                item.update(grade="C",phase="雪愿节前后",time="恩赐意志布置雪愿树的节期；无法锁定具体日子。")
            if path.stem=="PM15901" and no in (2,3,5,6):
                item.update(grade="C",phase="苍梧新春前后",time="在苍梧节庆及周边活动的生活窗口，精确日期未明。")
            if path.stem=="PM14001" and no==4:
                item.update(grade="B",phase="柔光技术大会后",time="魔王派已造出，此时正追加按摩功能。",
                            reason="柔光活动与《魔王派》逸闻之后阅读更容易辨认工坊道具。",route=1118)
            if path.stem=="PM11101" and no==7:
                item.update(grade="A",phase="仅有相对先后",time="魔王加入空白旅团后。",evidence="鸢尾主动询问加入旅团、共同爬塔后是否适应。")
            result.append(item)
    for item in result:
        item["unlockRequires"]=[chat_ids[x] for x in pending[item["id"]] if x in chat_ids]
    return result
