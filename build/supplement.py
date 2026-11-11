"""Public CN table narratives beyond the HTML Archive; cache by mirror revision."""
import concurrent.futures
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path
from common import MIRROR, base_record, clean, mdid, read, tags, uniq


NAMES = ("Character CharacterDes Force CharacterArchive CharacterArchiveContent CharacterArchiveBaseInfo "
         "Disc DiscIP DatingCharacterEvent DatingStartEndEvent DatingLandmarkEvent DatingLandmark DatingBranch "
         "StarTowerTalk StarTowerEvent StarTowerEventAction StarTowerEventOptionAction SoldierStoryType "
         "SoldierStoryResult SoldierOptionType")
NO_LANGUAGE={"CharacterArchive","Disc","StarTowerEvent"}


class Tables:
    def __init__(self, root, cache):
        state=read(root/".upstream_sync_state.json")
        self.rev=state["stella_sora_data_commit"]
        self.lua=state["ss_lua_commit"]
        self.data={}
        self.lines={}
        cache=Path(cache)/self.rev
        cache.mkdir(parents=True,exist_ok=True)
        files=[f"{pre}/{name}.json" for name in NAMES.split() for pre in ("bin","language/zh_CN")
               if pre=="bin" or name not in NO_LANGUAGE]
        def load(key):
            disk=cache/key.replace("/","-")
            if not disk.is_file():
                with urllib.request.urlopen(f"https://raw.githubusercontent.com/AutumnVN/StellaSoraData/{self.rev}/CN/{key}",timeout=35) as response:
                    content=response.read()
                json.loads(content)
                disk.write_bytes(content)
            body=disk.read_text(encoding="utf-8-sig")
            lines={m[1]:i for i,s in enumerate(body.splitlines(),1) if (m:=re.match(r'^  "([^"]+)":',s))}
            return key,json.loads(body),lines
        with concurrent.futures.ThreadPoolExecutor(8) as pool:
            for key,data,lines in pool.map(load,files):
                self.data[key]=data
                self.lines[key]=lines

    def rows(self,name):
        return self.data[f"bin/{name}.json"]

    def lang(self,name):
        return self.data[f"language/zh_CN/{name}.json"]

    def url(self,name,key,lang=True):
        path=("language/zh_CN/" if lang else "bin/")+name+".json"
        line=self.lines[path].get(str(key))
        return f"{MIRROR}/blob/{self.rev}/CN/{path}"+(f"#L{line}" if line else "")


def build(root,t):
    pages=read(root/"story_docs/_data/sections.json")["pages"]
    main={p["id"]:mdid(p) for p in pages if p["family"]=="main"}
    bonds={p["id"]:mdid(p) for p in pages if p["family"]=="characters"}
    existing={p["id"] for p in pages if p["family"]=="discs"}
    active={int(k):t.lang("Character").get(v["Name"]) for k,v in t.rows("Character").items() if v.get("Visible") and v.get("Available")}
    results=[]
    def entry(table,row,field,title,typ,group,order=0,cast=(),extra_text=""):
        key=row.get(field,"")
        body=t.lang(table).get(key,"")
        available=body or extra_text
        if not available:raise ValueError(f"No body in {table}/{row['Id']}: {field}")
        r=base_record(f"mirror/{table}/{row['Id']}",title,typ,group,order,t.url(table,key))
        r.update(cast=list(cast),keywords=tags(body+" "+extra_text),sourceTable=table,
                 sources=[dict(label=f"{table} 配置 {row['Id']}",url=t.url(table,row["Id"],False))],
                 evidence=f"{table} {row['Id']} · {field}。",availability="上游有文",route=1350)
        results.append(r)
        return r,body

    for k,v in t.rows("DiscIP").items():
        n=int(k)
        if n in existing:continue
        l=t.lang("DiscIP")
        title=l.get(v["StoryName"])
        r,body=entry("DiscIP",v,"StoryDesc",title,"秘纹散文","秘纹 · 独立散文",n,[active[a] for a in v.get("CharId",[]) if a in active])
        r.update(mode="散文",reason="阅读对应人物或团体的介绍后补读。此记录有独立的秘纹文案，未挂接秘闻演出。",
                 evidence=f"秘纹 {n} 的 StoryDesc，以《{title}》为故事名。",risk="中")
        if n==214067:r.update(route=962,risk="高",mode="历史侧写",reason="先读前星塔历特别篇，再看同一角色的独立秘纹文案。")
        if n==214046:r.update(route=1068,reason="先读北境活动，留意标题和人物所指；没有可独立确认的叙事日期。")
        if n==214047:r.update(route=1108,reason="在邮递主题活动后补读多娜的文字视角。")
        if n==214002:r.update(time="清月二十一日；年份待考。",grade="A",phase="年份未明 · 清月",evidence="散文以清月二十一日的晨间天气开篇。")

    lang=t.lang("CharacterArchiveContent")
    configs=t.rows("CharacterArchiveContent")
    for k,gate in t.rows("CharacterArchive").items():
        who=active.get(gate["CharacterId"])
        if not who:continue
        row=configs[str(gate["RecordId"])]
        if row["Content"] not in lang:continue
        label=lang.get(row["Title"],"档案")
        r,body=entry("CharacterArchiveContent",row,"Content",label,"旅人档案",who+" · 旅人档案",gate["Sort"],[who])
        sub=body.splitlines()[0].strip()
        if label.startswith("简历摘录") and len(sub)<28:r["title"]=label+" · "+sub
        r.update(unlock=f"好感 {gate.get('UnlockAffinityLevel',0)} 级",mode="档案记录",
                 reason=f"先认识{who}再查阅此份{label}。档案的解锁等级不能为所记事件定年。",
                 evidence=f"档案 {k}，记录项为“{label}”。",risk="高" if gate["Sort"]>=8 or gate["CharacterId"]==162 else "中")
        dated={
            "10310":("票据写作星塔历9██年热月8日，年份有意遮盖。","年份未明 · 热月",None),
            "11611":("试验田日记从鸣月3日记到猎月3日，未写年份。","年份未明 · 跨月",None),
            "11711":("星塔历994年鸣月2日至花月2日；代理店长最初的营业记录。","994年",dict(year=994,month="鸣月",day=2)),
            "11712":("星塔历994年花月13日至雨月1日；续记餐馆经营。","994年",dict(year=994,month="花月",day=13)),
            "13303":("调查报告标星塔历996年，月日未明。","996年 · 月份未明",dict(year=996)),
            "13304":("星塔历996年，《菲莱周报》第350期。","996年 · 月份未明",dict(year=996)),
        }
        if k in dated:
            time,phase,cal=dated[k];r.update(time=time,phase=phase,grade="A",evidence=time)
            if cal:r["calendar"]=cal
        if k=="14313":
            r.update(time="枪械首次许愿于星塔历987年；墓园对话在此之后，日期未知。",phase="仅有相对先后",grade="A",
                     evidence="风影解释旧枪之名纪念首次许愿年份，墓园中展示的已是改造后的枪。",risk="高")
        if k in ("16211","16212","16213"):
            r.update(route=960,grade="B",phase="前星塔历 · 角斗场往事",mode="回忆",
                     time="埃摩角斗场时期；与特别篇现时之间的准确年数待考。",
                     evidence={"16211":"老角斗士接过刚出生的婴儿。","16212":"回引数年前老角斗士的预言，十八号已展现战斗天赋。","16213":"矛隼与余音为还被称作十八号的少女谈论挑选武器。"}[k])
        change=row.get("UpdateContent1")
        if change in lang and (row.get("UpdatePlot1") or row.get("UpdateStory1")):
            pre=(main.get(row.get("UpdateStory1")) or bonds.get(row.get("UpdatePlot1")))
            changed={**r,"id":r["id"]+"@revision","title":r["title"]+" · 改订后","mode":"条件改订","risk":"高",
                     "source":t.url("CharacterArchiveContent",change),"grade":"U","phase":"未知",
                     "time":"改订文本的阅读门槛明确，所记内容可能回溯更早。",
                     "evidence":f"配置在 {'Story '+str(row['UpdateStory1']) if row.get('UpdateStory1') else 'Plot '+str(row.get('UpdatePlot1'))} 后替换正文。",
                     "reason":"读完触发改订的故事再对照原档。涉及身份、评价或经历变化。",
                     "related":[r["id"]],"unlockRequires":[pre] if pre else [],"keysFromTable":dict(story=row.get("UpdateStory1"),plot=row.get("UpdatePlot1")),
                     "keywords":tags(lang[change])}
            changed.pop("calendar",None);results.append(changed)

    sites={r["Id"]:t.lang("DatingLandmark")[r["Name"]] for r in t.rows("DatingLandmark").values()}
    for name in ("DatingCharacterEvent","DatingLandmarkEvent","DatingStartEndEvent","DatingBranch"):
        for v in t.rows(name).values():
            l=t.lang(name); params=v.get("DatingEventParams",[])
            people=[active[x] for x in params if x in active]
            places=[sites[x] for x in params if x in sites]
            label=(l.get(v.get("Name")) or {"DatingBranch":"路线选择","DatingLandmarkEvent":"地点片段","DatingStartEndEvent":"相约" if v.get("DatingEventType")==1 else "道别","DatingCharacterEvent":"同游见闻"}[name])
            if not l.get(v.get("Name")):label += f" · {v['Id']}"
            field=next((f for f in ("Desc1","Desc2","Desc3","Option1","Option2") if v.get(f) in l),None)
            if field is None:continue
            group="／".join(people or places or ["共用场景"])+" · 邀约"
            more=" ".join(l.get(v.get(f),"") for f in ("Desc1","Desc2","Desc3","Memory","Option1","Option2","Option3","Option4","Option5"))
            r,body=entry(name,v,field,label,"邀约",group,v["Id"],people+["魔王"],more)
            r.update(places=places,mode="可重复邀约",reason="认识同行者后按地点选读。每次出游会抽取或选择片段。",
                     time="一次邀约中的相对场景；没有固定剧情日期。",evidence=f"邀约配置 {v['Id']}，"+("限定地点为"+"、".join(places)+"。" if places else "按相约对象安排。"),
                     risk="高" if "尘沙（源初）" in people or any(z.startswith("菲兰尼斯") or z=="因苏拉" for z in places) else "低",route=1360)
    for v in t.rows("StarTowerTalk").values():
        l=t.lang("StarTowerTalk"); npc=l[v["Name"]]
        r,body=entry("StarTowerTalk",v,"Content",f"{npc} · 塔内交谈 {v['Id']}","星塔交谈",npc+" · 塔内交谈",v["Id"],[npc])
        r.update(reason="读过该 NPC 的好感剧情后可按默契区间查阅日常台词。",time="一次攀塔中；默契门槛随玩家进度变化。",
                 unlock="默契区间 "+"–".join(map(str,v.get("Affinity",[]))),mode="重复交谈",risk="低",route=1380)
    opts=defaultdict(list)
    for v in t.rows("StarTowerEventOptionAction").values():
        opts[v["Group"],v["OptionId"]//100].append(v)
    names={9133:"波西亚",9172:"贝缇丽",9173:"珀尔娜",9174:"维嘉尔"}
    for v in t.rows("StarTowerEventAction").values():
        eid=v["EventId"]; npc=names.get(v["Group"],str(v["Group"]))
        title=t.rows("StarTowerEvent")[str(eid)]["Desc"]
        r,body=entry("StarTowerEventAction",v,"Desc",f"{npc} · {title}","星塔事件",npc+" · 塔内事件",eid,[npc])
        r.update(reason="同一种交易或塔中事件有不同 NPC 演出，展开来源可对照相应选项。",time="随机攀塔事件；游玩中的触发次序可变。",
                 mode="可选事件",risk="低",route=1385)
        for o in opts.get((v["Group"],eid),[]):
            r["sources"].append(dict(label=f"回应选项 {o['OptionId']}",url=t.url("StarTowerEventOptionAction",o["Desc"])))
            r["keywords"]=uniq(r["keywords"]+tags(t.lang("StarTowerEventOptionAction").get(o["Desc"],"")))
    opening=next(mdid(p) for p in pages if p["family"]=="soldier" and p["id"]=="ST_sys_soldier_intro")
    for v in t.rows("SoldierStoryType").values():
        title=t.lang("SoldierStoryType")[v["Title"]]
        r,body=entry("SoldierStoryType",v,"Desc",title,"尖兵陷阵事件","尖兵陷阵 · 遭遇",v["Id"])
        r.update(route=966,mode="可选事件",requires=[opening],risk="中",time="联合调查行动中的一次随机遭遇。",phase="仅有相对先后",grade="C",
                 reason="在模式开场之后、终局之前选读。多次遭遇没有固定日期。")
    # Some outcomes/choices are identical fallbacks; group only verbatim-identical records.
    for name,field,typ in (("SoldierOptionType","OptionTitle","尖兵陷阵选项"),("SoldierStoryResult","ResultText","尖兵陷阵结果")):
        rows=t.rows(name);lang=t.lang(name);grouped=defaultdict(list)
        for v in rows.values():
            first=next((val for val in v.values() if isinstance(val,str) and val in lang),None)
            if first:grouped[lang[first]].append((v,first))
        for val,variants in grouped.items():
            v,key=variants[0]
            r=base_record(f"mirror/{name}/{v['Id']}",clean(val)[:19]+("…" if len(clean(val))>19 else ""),typ,"尖兵陷阵 · 分歧文本",v["Id"],t.url(name,key))
            r.update(route=967,mode="条件文本",risk="高",requires=[opening],time="随局内选择或结算出现；不同结局独立。",
                     reason="对照遭遇场景选读。相同文本的配置另列于来源。",evidence=f"同文配置 {len(variants)} 条。",keywords=tags(val),
                     sources=[dict(label=f"编号 {vv['Id']}",url=t.url(name,kk)) for vv,kk in variants])
            results.append(r)
    gacha=f"https://github.com/MakoStar/ss-lua/blob/{t.lua}/Lua/Game/UI/Avg/_cn/Config/GD_gacha.lua"
    r=base_record("upstream/GD_gacha","GD_gacha · 招募出发演出","招募演出","散佚演出",0,gacha)
    r.update(route=1380,cast=["尘沙","琥珀","鸢尾"],risk="低",evidence="四次 SetTalk 中，三位旅人商量开车去星塔、找同行伙伴。",
             time="招募演出未找到关卡挂载。",reason="认识旅行车上的三人后即可选读。",mode="系统演出",availability="上游有文")
    results.append(r)
    return results
