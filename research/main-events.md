# 主线、特别篇与活动考据

2026-11-12 核查，正文基线为档案库 11 月 11 日快照。先清点 `_data/sections.json` 全部原文页和 `chapters.json` 所有关卡，再把 11 部活动的原始关卡表、回顾时间表和解锁表按 ID 交叉匹配。主线另外逐镜读取了 490 条场景牌。网页的“原文”通往具体节点，生成数据的 `textSource` 保留固定版本；以下笔记包含剧透。[档案快照](https://github.com/419bw/stellasora-archive/tree/f3209414ab301a552755781487b560a1bbcda72f/story_docs) · [上游版本记录](https://github.com/419bw/stellasora-archive/blob/f3209414ab301a552755781487b560a1bbcda72f/.upstream_sync_state.json)

## 数量与开放状态

| 范围 | 节点 | 其中有独立对白或叙事文本 | 差额 |
|---|---:|---:|---|
| 序章 | 2 | 2 | 注册流程单独调用两份同名文本 |
| 主线九章与两个特别篇 | 220 | 204 | 《谜影》有2个无独立对白的战斗，另一特别篇有12个待开剧情编号、2个待开战斗编号 |
| 11个已收录活动 | 124 | 105 | 19个战斗节点有标题和前后关卡，未挂独立AVG |
| 已预告活动《执笔展卷，勾勒未名之境》 | 1项预告 | 0 | 只有版本前瞻，独立列示 |

两种统计口径的分母不同。档案首页统计文本页，主线地图与游戏回顾还列出无台词或预留节点。另核实上游 `ActivityAvgLevel` 的11条复挂《幽灵船》的同一批剧本；`MiningStory` 的8条复挂琥珀、缇莉娅、卡西米拉、翡冷翠的好感文本。对这两份表采用同剧本去重。[游戏活动关卡表](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/ActivityStory.json) · [活动地图](https://stellasora-archive.pages.dev/events/) · [MiningStory](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/MiningStory.json)

《谜影的序曲》位于表内第7组，对应第六章与第七章之间的特别篇。表内第8、9、10组依次对应实机编号七、八、九章。第11组属于另一条官方年代线。《完璧之庭·微尘破晓》与繁中《遺塵之庭 銀沙黎明》、日文《暁天を破る、創生の光》均为同一周年主线特别篇。两地同期周年公告的活动、角色及玩法一致，且同期日服另有专门的延期说明。繁中官方标题以空格分隔，中点拼法保留为搜索别名。[简中版本公告](https://stellasora.yostar.cn/news/4887) · [繁中活动公告](https://stellasora.stargazer-games.com/news/4972) · [日文延期公告](https://stellasora.jp/news/4999)

10月28日运营公告把后半段从10月30日延期到11月13日，临时提前体验入口另延至12月4日。截至查核日，后半段仍以预留行登记。特别篇节点1117、1122的档案框架能生成“战斗已开放”的网页，但二者在锁闭续段内、标题仍为“敬请期待”、无本地台词，不能据此算作读得完的剧情。对尚无表内编号的第十章不编造章节标题和事件。[简中延期原文](https://stellasora.yostar.cn/news/5001) · [11月版本前瞻](https://stellasora.yostar.cn/news/5077) · [韩语社区对更新的转述](https://m.inven.co.kr/board/party/6553/389)

## 年月、场记与回忆

活动能定位到月份的直接依据是游戏回顾配置。取 `ActivityStoryChapter.StoryTime` 指定的本地化键。现实开服时间、活动分栏、读序排序权重和回顾解锁条件分别保存，均不能替代这个字段。十二个月名顺序还可由同角色同键的中日生日对应验证，正月雪月（卡娜丝）、二月旅月（特丽莎）、三月鸣月（埃莉诺）、四月清月（花原）、五月花月（鸢尾）、六月雨月（尘沙）、七月雷月（师渺）、八月热月（琥珀）、九月谷月（苍兰）、十月猎月（日文“狩月”，卡西米拉）、十一月雾月（翡冷翠）、十二月霜月（风影）。本指南据此排序，不将某个星塔历日期换算为现实公历日期。[活动回顾定义](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/ActivityStoryChapter.json) · [回顾年月](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/language/zh_CN/ActivityStoryChapter.json) · [中服生日](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/language/zh_CN/CharacterArchiveBaseInfo.json) · [日服生日](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/JP/language/ja_JP/CharacterArchiveBaseInfo.json)

| 篇章 | 节点 | 可复核的时点及叙事位置 |
|---|---:|---|
| [第一章](https://stellasora-archive.pages.dev/main/ch01/) | 13 | 996年花月26日至雨月1日。序章的开箱在此之前；08的不同解法分流，部分节点汇回09。 |
| [第二章](https://stellasora-archive.pages.dev/main/ch02/) | 17 | 雨月1日下午承接第一章尾声。05的诊所场景使桥下赠食与千都世的报恩接通。 |
| [第三章](https://stellasora-archive.pages.dev/main/ch03/) | 17 | 雨月9日幕间开始，推进到27日。04先回到两个月前清月6日，再回雨月16日。 |
| [第四章](https://stellasora-archive.pages.dev/main/ch04/) | 17 | 承第三章雨月27日的遇袭。02的清月6日11:10续第三章的11:00；09梦内日期为问号。 |
| [第五章](https://stellasora-archive.pages.dev/main/ch05/) | 19 | 雷月21日至谷月5日凌晨。各部门调查是同一任务不同视角；05复盘的994年不应覆盖眼前的996年。 |
| [第六章](https://stellasora-archive.pages.dev/main/ch06/) | 22 | 幕间横跨翡冷翠童年、992年庭审、995年调职与996年谷月5日。主路尾声到谷月23日；《天下静谧》独立延伸到1000年。 |
| [谜影的序曲](https://stellasora-archive.pages.dev/main/chsp7/) | 12 | 996年猎月2日晚到7日。第六章尾声解锁本篇，本篇10解锁第七章。解锁条件中可以复原第06、07之后各自的战斗。 |
| [第七章](https://stellasora-archive.pages.dev/main/ch07/) | 25 | 猎月8日接晚宴后果。14日11:35的缆车行动与筹款行动是并行视角。05B贷款后约两年的分歧历史通向三个备选终局。 |
| [第八章](https://stellasora-archive.pages.dev/main/ch08/) | 28 | 996年猎月23日至雾月18日的主路中嵌入追忆。《生日快乐》涉及981、986、987、988年；鸢尾求学的追忆涉及994、995年。B线另抵997、998年。 |
| [第九章](https://stellasora-archive.pages.dev/main/ch09/) | 26 | 雾月18日有A、B、C三次尝试和真终局。01A先倒回雾月8日；A线04发生在03稍早之前。真终局保留魔王的多次尝试记忆。 |
| [完璧之庭·微尘破晓](https://stellasora-archive.pages.dev/main/chsp11/) | 24 | 故事场景属于前星塔历4年，但从魔王的记忆看，进入本篇须读过《窄门》。05至08有5月26日场记；09讲角斗士约一年前的往事。 |

只有章节年份的战斗不自动继承相邻节点的分钟。主线关卡图中“同一列”的场景可能在两个不同时间，也可能跨年份，本版优先使用逐句剧本的各次换景与年份字幕。比如第六章幕间的第一张场记是雾月16日，但紧贴该场记的字幕是992年；套用996年章节标题会整整错四年。[《忠诚与背叛》](https://stellasora-archive.pages.dev/main/ch06/STm06_00.html) · [《天下静谧》](https://stellasora-archive.pages.dev/main/ch06/STm06_05_a.html) · [《空白的正解 中》](https://stellasora-archive.pages.dev/main/ch08/STm08_08.html)

第九章《点燃》的四路在世界内相互排斥，但魔王经历了多轮尝试。A线之后的B线开口就谈上一次撤退；《点燃》会随A、A+B、A+B+C的阅读记录改变发言；《窄门》主角亲自回顾三次回到过去。本版把三个结局分别保留在各自支路，并将它们设为《窄门》的**阅读前置**。表内向《窄门》连线的仍是《点燃》，第四个选择对应证据标记 E1004。跨章进入周年篇的登记前置则确实是《窄门》。[《点燃》](https://stellasora-archive.pages.dev/main/ch09/STm09_00_b.html) · [《未卜先知》](https://stellasora-archive.pages.dev/main/ch09/STm09_01_b.html) · [《窄门》](https://stellasora-archive.pages.dev/main/ch09/STm09_01_d.html) · [正式剧情条件表](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/StoryCondition.json)

## 十一部活动的故事顺序

表中年月是官方标注的全篇时段，等级A。斜线两侧分别是总关卡和有剧本的节点。具体节点的回忆、时间跳跃和解锁选项在网页单独说明。活动《烟火绚丽寻春意》在活动组用“绚”，回顾标题用“绮”，两者共享 10104。

| 全篇时段 | 活动 | 节点 | 可以验证的交点 |
|---|---|---:|---|
| 996 谷月 | [枪林弹雨覆黄沙](https://stellasora-archive.pages.dev/events/10109/101090201.html) | 10/8 | 01在米拉什，02回到几个月前的苍梧，03再述不久前的千塔。这两段回忆不全在谷月。先读完六章再认识白猫，符合进入后续米拉什故事的需要。 |
| 996 霜月 | [闪耀的使者与圣夜的精灵](https://stellasora-archive.pages.dev/events/20101/201010201.html) | 14/13 | 01解释节日定在二十五日；尾声说当天工作完毕，当前送礼、找照片、入塔等行动均围绕同一日。06开始回述，07主体在童年，08又回到现时；童年是哪一年没有日期。 |
| 997 雪月 | [烟火绚丽寻春意](https://stellasora-archive.pages.dev/events/10104/101040211.html) | 11/9 | 同伴失联后搜救，结尾从除夕晚餐写到零点。这里过的是龙裔春节，月份由回顾给出，没有足够材料从现实春节推对应日。 |
| 997 鸣月 | [穿透心壁的取景框](https://stellasora-archive.pages.dev/events/10107/101070201.html) | 11/9 | 01里魔王明确认出去年雪愿节的火垂。04的实验室经过由卡娜丝回忆，约早一年。 |
| 997 清月 | [冬夜镇魂曲与破晓扳机](https://stellasora-archive.pages.dev/events/10105/101050212.html) | 12/10 | 北境委托写在清月，常年风雪不足以把它改判成霜月。风影的童年、古代壁画、幻境及埃妲求学插段要另读；尊者线可接异闻 #14。 |
| 997 清月 | [奋斗吧！大小姐的旅人修炼手册！](https://stellasora-archive.pages.dev/events/10111/101110201.html) | 11/9 | 埃莉诺明确复述前辈与花原解决绑架，对应异闻 #13。03开头跨过一个月，表彰另过五日，不能把所有关卡限制在这一个清月。 |
| 997 雨月 | [惊奇冒险！渊海幽灵船传说！](https://stellasora-archive.pages.dev/events/11100/111000202.html) | 11/11 | 魔王刚被两位陌生兔耳少女救起；六角鲸岛上的寻宝者留下后续辨认线索。 |
| 997 雨月 | [敬启，致珍重的你](https://stellasora-archive.pages.dev/events/10106/101060206.html) | 12/10 | 04里魔王认出在六角鲸岛见过的寻宝旅人，直接锁定在《幽灵船》之后。02A/B/C是查收件人的替代途径，各含万送屋成员的往事。 |
| 997 雨月 | [心跳！柔光狂想曲](https://stellasora-archive.pages.dev/events/10108/101080201.html) | 10/8 | 第一节能源短缺是委托的直接原因；02明示两天后。与另两部雨月故事之间没有同样具体的日级连接。 |
| 997 热月 | [晴风碧海·悠哉盛夏依然打卡~](https://stellasora-archive.pages.dev/events/20103/201030209.html) | 11/9 | 由薇洛视角写度假、触礁和荒岛脱困。08的援船与另一篇03的援船是同一场救援。 |
| 997 热月 | [欢歌劲浪·闪耀假日惊涛探险！](https://stellasora-archive.pages.dev/events/10110/101100203.html) | 11/9 | 01回顾几个月前的海上绿光。03交代救援队从何而来，04接上《晴风碧海》结尾所见的海中星塔。两篇开篇有重叠，推荐连读以保留救援者身份与续篇悬念。 |

跨支线证据中，雪愿节的一套制服尤其容易复核。异闻 #07 第一话写发给万送屋的制服只有一套，尺码正合苍兰；活动04C由苍兰向菈露追问礼物派送时为什么少发制服。委托方、城邦、任务、制服件数与穿着者五点相合，可以把这两段作为同届节庆的两种视角，等级B。节目内追查照片的04C本身是一种选读路径。[异闻 #07 第一话](https://stellasora-archive.pages.dev/storysets/1007/100701.html) · [活动04C](https://stellasora-archive.pages.dev/events/20101/201010206.html)

## 来源取舍与未解决问题

- 玩家读序多建议先读主线，再补较早发生的异闻，还建议在第八章的米拉什事件前先认识猫眼。这里采用能保护身份揭示的建议，同时用谷月回顾确认《枪林弹雨》的发生期。关于“大部分活动在第一部之后”的日语整理，与文本表中9个997年月以及996年霜月这一个晚于主线雾月的事件基本一致；大范围概括不能代替每一部的原始字段。[Reddit 第一部读序](https://www.reddit.com/r/StellaSora/comments/1xdz8mn/reading_guide_for_stella_sora_arc_1/) · [日语玩家对幽灵船的逐段复盘](https://pomzero.hatenablog.com/entry/2025/10/30/201856) · [繁中玩家的月份笔记](https://home.gamer.com.tw/artwork.php?sn=6380264)
- 原文能确定枪林发生在谷月，不能把全篇钉在第六章尾声谷月23日之后；本版在第六章后插读。两部清月故事的日序未明。《幽灵船》先于《敬启》有正文证据，但《心跳》的雨月委托在两者之前、之间或之后仍可成立。
- 真结局的角色经验、世界线是否持续与系统阅读条件分字段登记。分头行动也不必等同互斥，例如第七章同一时间的缆车组及筹款组。纯战斗的坐标有时只能限定到邻接关卡；主线 BT01《远方的心》的气泡仅能证明通讯内容，发话者的地点未写。
- 核验过所有与无正文、预留或预告相关的28个不同链接。19个活动战斗页和4个主线战斗页均有与表对应的独立页面标题；两个周年篇战斗页明确只显示“敬请期待”。同名标题不会导致阅读进度合并。
