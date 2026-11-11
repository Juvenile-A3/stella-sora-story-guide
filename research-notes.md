# 《星塔旅人》剧情时间线考据摘要

以下笔记含剧透。首次阅读可直接打开 [受剧透保护的指南](index.html)。考据截至 **2026 年 11 月 12 日**，游戏数据固定于档案库 11 月 11 日的提交 `f3209414`。[资料快照](https://github.com/419bw/stellasora-archive/tree/f3209414ab301a552755781487b560a1bbcda72f) · [上游镜像版本](https://github.com/419bw/stellasora-archive/blob/f3209414ab301a552755781487b560a1bbcda72f/.upstream_sync_state.json)

## 读序为什么会分开

**从哪里认识空白旅团。** 序章先给出沙漠、许愿箱和失忆者。异闻 #02 开头把四人同行的一次爬塔放在获救以后、抵达埃摩以前，末话补全便利店与欢迎会。这使它在故事内排到第一章前。首读路线把它放在第二章后，给主线车窗前醒来、进城和追问身份的开场保留悬念。波西亚的《二次入职》又从店员的视角回看了同一段经历，应在知道猪排饭为何重要之后阅读。[序章](https://stellasora-archive.pages.dev/prologue/STm00_01.html) · [第一章开场](https://stellasora-archive.pages.dev/main/ch01/STm01_01.html) · [异闻 #02 其三](https://stellasora-archive.pages.dev/storysets/1002/100203.html) · [波西亚第二话](https://stellasora-archive.pages.dev/npc/9133/913302.html)

**千都世的过去与一个可以对到分的场面。** #01 其一写到修行与受赠食物，其三进入水道桥营救。只有其中一场与第二章 03A 同在埃摩金城区水道桥走廊，场记都是雨月 2 日 04:15。这个分钟数不能覆盖千都世整段往事。另一处交接是 #08 末幕的 08:28 与二章 05 的 08:30；两分钟的间隔也保留在各自条目中。[异闻 #01 其三](https://stellasora-archive.pages.dev/storysets/1001/100103.html) · [第二章 03A](https://stellasora-archive.pages.dev/main/ch02/STm02_03_a.html) · [异闻 #08 其三](https://stellasora-archive.pages.dev/storysets/1008/100803.html) · [第二章 05](https://stellasora-archive.pages.dev/main/ch02/STm02_05.html)

**初遇会改变角色故事的读法。** #12 其一写地理协会安排空白旅团与格芮同行，第四话让人看见她的一段往事。推荐先读完这个委托，再打开格芮的羁绊、秘闻与通讯。人物图分别记录正文所见的初遇和沿推荐路线首次出场。另一个直接的跨异闻前置来自 #17 重提 #11 里的购车价格、留车期限和攒钱约定。[异闻 #12](https://stellasora-archive.pages.dev/storysets/1012/101201.html) · [异闻 #11](https://stellasora-archive.pages.dev/storysets/1011/101103.html) · [异闻 #17](https://stellasora-archive.pages.dev/storysets/1017/101701.html)

**#18 有三种日期。** 开篇场记为星塔历 996 年谷月 24 日 10:00，正接第六章达尔茜亚事件。运营开放时间为现实的 2026 年 10 月 13 日，本版推荐在第九章之后阅读，保留尘沙身世线的揭示。繁中公告使用《眠於秋分之際》，地方化配置另见《眠於秋分之日》。编号和正文匹配同一篇。[异闻 #18 第一话](https://stellasora-archive.pages.dev/storysets/1018/101801.html) · [繁中服 9 月 29 日公告](https://stellasora.stargazer-games.com/news/4768)

**活动回顾提供了游戏内月份。** 《枪林弹雨覆黄沙》落在 996 年谷月，《闪耀的使者与圣夜的精灵》落在同年霜月，《敬启，致珍重的你》和《心跳！柔光狂想曲》同属 997 年雨月。两篇同月不会自动取得彼此的先后。到了 997 年热月，才有两支队伍分别写到同一次海上救援，可在网页中并列对读。[游戏内回顾年月表](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/language/zh_CN/ActivityStoryChapter.json) · [《拨云见日》](https://stellasora-archive.pages.dev/events/20103/201030209.html) · [《空白旅团漂流记》](https://stellasora-archive.pages.dev/events/10110/101100203.html)

**两个特别篇和多个结局。** 《谜影的序曲》承接第六章，通向第七章。周年特别篇《完璧之庭·微尘破晓》进入前星塔历 4 年，主角的主观经历却承接第九章《窄门》。繁中同一特别篇作《遺塵之庭 銀沙黎明》。在第九章，《点燃》会随此前看过的结局改写对话；《窄门》回顾三次尝试。外界的分歧与魔王保有的记忆各自有序，网页保留关卡来路和阅读前置。特别篇后半经延期，截至本版仍属于待开放。[主线拓扑](https://stellasora-archive.pages.dev/main/) · [《点燃》](https://stellasora-archive.pages.dev/main/ch09/STm09_00_b.html) · [繁中周年公告](https://stellasora.stargazer-games.com/news/4972) · [延期公告](https://stellasora.yostar.cn/news/5001)

## 全量清点

清点先从 Git 完整文件树、12 类正文的 `sections.json` 和主线 `chapters.json` 开始，再把 694 个 Markdown 正文逐一对应到 694 个结构化剧本。仓库另外提供 73 个心链 Markdown 文件。两份上游对账说明、心链目录页以及冻结的旧版 `docs/` 用于核查来源。它们与正文分开计数。[全量正文与分支](https://github.com/419bw/stellasora-archive/tree/f3209414ab301a552755781487b560a1bbcda72f/story_docs) · [仓库结构与生成流程](https://github.com/419bw/stellasora-archive/tree/f3209414ab301a552755781487b560a1bbcda72f#readme)

| 范围 | 第一版实际口径 |
|---|---|
| 序章、主线、特别篇 | 序章 2 节。其余为九章、两个特别篇，共 220 个关卡节点，有 204 份独立正文。保留无对白战斗与后半预留节点。 |
| 诺瓦异闻 | 已收录 #01–#18 共 56 话，另有 #19 官方预告。编号、地区题名、组内顺序、现实开放时间分别登记。 |
| 活动 | 11 组、124 关。105 关有独立正文，其余 19 关按原配置留在活动拓扑中。另设 1 条后续活动预告。 |
| 旅人羁绊 | 41 个角色／形态条目，各有 3 话，共 123 话。限定形态独立建组。 |
| 秘闻与独立秘纹散文 | 档案库“秘闻”栏目 25 篇，剧本及所附散文合页对读。上游另有 79 份无独立 AVG 演出的秘纹散文，逐篇标为另一类型。 |
| NPC 与逸闻 | 4 位 NPC 的 8 话好感剧情。45 个逸闻笔记合页拆成 135 则可标记单元，保留原来的合页及获取条件。 |
| 心链 | 41 个联系人／形态、73 个剧本、600 段，按本版总索引有 11,519 条短信、353 组抉择。以“段”为进度单位。同一段的互斥回复留在有分支标记的原文里。 |
| 其他档案正文 | 113 段委托演出、9 份存目战斗气泡、1 篇回归、3 份尖兵陷阵开场与终局。 |
| 上游增补 | 旅人履历及条件改订、邀约、塔内交谈和事件选项、尖兵陷阵遭遇与结果，以及档案库覆盖表列出的招募演出 `GD_gacha`。同文结果聚合，保留全部配置编号。 |

**2,710** 是可以各自标记的阅读单元数，包含扩展资料、战斗节点和预告。**559** 是首读路线默认显示的单元数。原文页、聊天剧本、短信条数和关卡数各有分母。精确的逐类数量、证据分布与位置精度可在随项目交付的元数据中核查。[机器计数](data/metadata.json) · [心链总索引](https://github.com/419bw/stellasora-archive/blob/f3209414ab301a552755781487b560a1bbcda72f/story_docs/_chat/_index.md) · [战斗对账](https://github.com/419bw/stellasora-archive/blob/f3209414ab301a552755781487b560a1bbcda72f/story_docs/_battle_reconciliation.md)

## 如何判断与复核

- **证据等级标在实际主张上。** A 可成立于“下一话明确提到上一次治疗”，这一结论仍可能没有年份。B 需要跨文本互证。C 保留从人物状态、季节、地点推论的余地。D 用于仅有外部读序或发布线索的判断。U 表示与整条时间线的关系仍不足以定位。阅读建议另用文字说明。
- **日期的精度独立保存。** 用年月标整场活动、用场记标单个镜头、用“数周前”记录插叙；年份遮盖的票据照原样处理。在璟麟的两份代理店长日记中，994 年的具体日期可以落轴。在风影的枪械档案中，987 年指武器首次出现，墓园里的谈话只能置于其后。[璟麟、风影的原始履历表](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/language/zh_CN/CharacterArchiveContent.json)
- **系统条件与情节因果分别核实。** 心链读取真实的 Chat ID 和前置聊天字段。两段都借同一条起始短信解锁时，不连成连续两天。羁绊的好感门槛也只约束阅读。个人履历还可能在读过指定主线或好感故事后改订，因此原档与改订文本分开记录。[聊天配置](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/Chat.json) · [履历改订配置](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/CharacterArchiveContent.json)
- **短对白逐类核对。** 序章的六个未挂载战斗气泡提供了三人在沙暴中失散、联络和趋近许愿箱的旁证。委托结算则按编队与权重抽取。首读主线不会把 113 段结算串成 113 次连续委托。采矿配置的 8 次剧情调用沿用已有角色羁绊，避免重复入册。[序章战斗现场](https://stellasora-archive.pages.dev/battles/BBm00_01.html) · [委托档案](https://stellasora-archive.pages.dev/dispatch/) · [采矿剧情调用](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/MiningStory.json)

## 外部资料如何影响判断

Reddit 的第一部读序把 #01、#02、#12 放在第二章后，#18 放在第九章后；本版采用其中保留悬念的思路。此前一份时间线曾根据贝修莉娜实习期移动 #05，本版以转正台词为可证下界。日文开服实录也注意到 #02 早于 #01。不同社区的共同读法只用来检验是否好读。[Reddit 第一部读序](https://www.reddit.com/r/StellaSora/comments/1xdz8mn/reading_guide_for_stella_sora_arc_1/) · [早期时间线修订](https://www.reddit.com/r/StellaSora/comments/1rwrw1d/stella_sora_timeline_map_post_haste_event_ver/) · [日文开服记录](https://room-shiki.hatenablog.com/entry/2025/10/23/100000)

活动回顾的玩家实录提供了查找月份字段的线索。实际入库的是固定快照的中文回顾表。繁中剧情笔记用来对照月日名，大陆实机回放用来核实邀约、短信和演出确有不同入口。韩文活动资料特别区分服务器开关卡时间及关卡内容；这些现实时间单列核对。异闻的简繁日英韩地区标题按同一 StorySetChapter ID 对齐。[活动回顾实录](https://www.reddit.com/r/StellaSora/comments/1xavrjz/thank_you_event_review/) · [繁中剧情笔记](https://home.gamer.com.tw/artwork.php?sn=6380264) · [大陆服实机回放](https://www.bilibili.com/video/BV1VkWSz3Ej1/) · [韩文活动记录](https://gagether.wiki/ko/games/stellasora/browse) · [地区标题对照](build/nova-locales.json)

## 未决问题与覆盖边界

1. 大量短讯、委托、随机邀约、塔内交易及人物侧写只有人际状态或游戏触发条件。网页保留它们的原文入口、建议补读位置和 U 级。选择具体人物或篇目时，可以继续沿链接核实。相对索引里没有上下界的不同组无法互相排序，同一月份下也不表示同日。
2. 档案首页、README 及旧版维护说明中的个别快照数字不同。本版以锁定提交的文件对账。心链诊断登记 40 个没有聊天表记录的段，其中 1 个空段在提取时跳过。最终可读的 600 段中，561 段有聊天表记录，另 39 段有正文但未挂载。网页保留这 39 段，并标明状态。[心链诊断](https://github.com/419bw/stellasora-archive/blob/f3209414ab301a552755781487b560a1bbcda72f/story_docs/_chat/_diagnostics.json)
3. 只有影像、没有台词或字幕的 CG 缺少可抽取正文。角色语音表中仅列音频编号或功能名的记录没有据此编写剧情。匿名说话人、面具、怪谈、梦与戏中戏也不自动合并成真实身份。图谱里的说话人标签包含许多小配角，不能用作可玩角色人数。[档案收录说明](https://github.com/419bw/stellasora-archive#阅读提示与剧透预警)
4. 截至核查日，《完璧之庭》后半只有预留关卡。《执笔展卷，勾勒未名之境》已有版本预告，#19《比“宝石”更耀眼的》公告计划于 11 月 27 日 12:00 开放。保留预告与条件引用，待公开文本到达再校订。读序攻略提到的“第十章”等未在快照内形成独立正文的项目没有虚构关卡。[延期公告](https://stellasora.yostar.cn/news/5001) · [版本前瞻](https://stellasora.yostar.cn/news/5077)

完整的逐章、逐活动、逐异闻核查记录另附在 [主线与活动考据](research/main-events.md) 和 [异闻、羁绊与秘闻考据](research/side-stories.md)。网页详情和 [结构化阅读数据](data/story-data.json) 保存每个阅读单元的结论与原文入口。
