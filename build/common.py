"""Shared helpers for the editorial index. No game or archive build code is run."""
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

ARCHIVE = "https://github.com/419bw/stellasora-archive"
MIRROR = "https://github.com/AutumnVN/StellaSoraData"
SITE = "https://stellasora-archive.pages.dev/"
OUT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def revision(root):
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def mdid(page):
    return page["page_md"].removesuffix(".md")


def permalink(commit, relative, line=None):
    return f"{ARCHIVE}/blob/{commit}/story_docs/{quote(relative)}" + (f"#L{line}" if line else "")


def clean(text):
    text = re.sub(r"<[^>]*>|\*\*|==DATING_CHARACTER==|==PLAYER_NAME==", "", text or "")
    return " ".join(text.split()).strip(" 「」")


def uniq(values):
    return list(dict.fromkeys(x for x in values if x))


PLACES = "埃摩 千塔之城 千塔城 苍梧 松川 达尔茜亚 菲莱 菲兰尼斯 塞尔斯泰 米拉什 弗拉维奥 角斗场 水道桥 灰城区 银城区 金城区 灰城孤儿院 怀璟食府 大图书馆 移动工坊 学院 便利店 星塔 港口 沙滩 剧院".split()
TOPICS = "初遇 初次 委托 救援 试用期 回忆 小时候 小时候 童年 祖父 父亲 母亲 弟弟 妹妹 毕业 生日 生病 花束 礼物 手机 猫猫 名片 记忆 失忆 身份 手册 照片 调查 诊断 报告 研究 比赛 庆典 会议 祈愿 许愿箱 图书馆 星之铃 布丁 旅团 新春 月亮 沙漠 温泉 演出 魔王派 兔子派 研究所 雪愿节 雪愿树 冰钓 春节 拍卖 猎火 圣女 守夜人 坟墓 学园 咖啡 帐篷 钓鱼 搬家 猪排饭 音乐盒 面具 恩赐意志 摩金会 灰风俱乐部 联合种业 地理协会 白泽公署 帝国卫队 万送屋 小黑 试验田 行李箱 绯瞳传讯 永夜联合 战争 裂隙 角斗士 退休 针筒 短信 特训 电影 剧团 采访 舞台 师父 航海 海盗 失踪 故乡 玉米 留影盒 绘画 旅行车 布兰迪 地下市场 神器 红茶 甜枣 机甲 孤儿院 鸟笼 猪排 蛋糕 饼干 小猫 探险 登山 魔法师 失控 童话 传说 极光 商店 种子 打工 封印 能量沛沛 告别 雪山 影戏 船长 黑足猫 处刑 虚界 星骸 悬赏".split()


def tags(body):
    return uniq(k for k in TOPICS + PLACES if k in body)


def base_record(sid, title, story_type, group, order, source):
    return dict(id=sid, title=title, type=story_type, group=group, order=order, source=source,
                grade="U", phase="未知", time="正文没有可对齐主线的日历坐标。",
                route=1300, cast=[], places=[], requires=[], related=[], risk="中",
                reason="", evidence="", mode="日常", optional=True)
