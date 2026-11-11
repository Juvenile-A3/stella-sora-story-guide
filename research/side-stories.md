# 异闻、旅人羁绊与秘纹的时间依据

基于 2026 年 11 月 11 日的档案快照。核对对象共 56 话诺瓦异闻、41 个旅人条目的 123 话羁绊、25 组剧本与附文合页，以及 79 篇另有散文但没有独立 AVG 演出的秘纹。预告异闻 #19 单列，尚无分话。每个小节和每篇散文的判断随网页数据交付。下面的情节说明含剧透。

## 收录口径

档案库用「故事集支线」收纳诺瓦异闻，四个栏目为旅途随笔、荒野快讯、职场热线、风情杂记。「诺瓦异闻」是运营公告用名。「秘闻」是档案库栏目，收录能播放的秘纹剧情及同页附文。官方招募与物品公告称「秘纹」。25 个带 AVG 的 DiscIP 条目与 79 个仅有 StoryDesc 的条目合计 104 个；同一条目的脚本和附文可从不同年代、人物视角叙事。网页按源条目记录阅读进度，详情区交代双层叙时。[档案库说明](https://github.com/419bw/stellasora-archive/blob/f3209414ab301a552755781487b560a1bbcda72f/README.md) · [官方招募与秘纹名称](https://stellasora.yostar.cn/news/4887) · [DiscIP 表](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/DiscIP.json)

羁绊以角色编号分组，好感等级从正文元数据逐话读取。菈露（圣夜）、科洛妮丝（新春）、薇洛（盛夏）、尘沙（源初）各保留自己的三话；没有其他形态正文的角色不会被补造三话。关系列表中的「上／中／下」是连读顺序；下篇若写了一周后，内时会另行标注。角色名、发言者和出场角色并非完全等价，选择回应里的魔王、回忆中的孩子或未具名的医生有时并未在说话人栏署名。

## 异闻编号与开放时间

国服 StorySetChapter 的 Title 固定映射 #01 至 #18，StorySetSection 通过 ChapterId 归入各篇。18 篇中 #02、#12 各四话，其余三话。#01、#02 没有单独的 OpenTime；其他编号的配置开放时间在这一快照中不递减。#03 与 #04 等多组同批，不能把编号差当作事件相隔时间。下表是北京时间的开放配置，供版本维护；每一行的时间判断来自故事文本。[章节配置](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/StorySetChapter.json) · [简中篇号与标题](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/language/zh_CN/StorySetChapter.json) · [小节归属](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/bin/StorySetSection.json)

|篇号及正文入口|国服配置开放时间|故事内窗口|
|---|---|---|
|[#01《刀尖之寒，掌心之暖》](https://stellasora-archive.pages.dev/storysets/1001/100101.html)|配置未设独立时间|行前修行未标日；受赠食物场景接星塔历996年花月26日12:40之后|
|[#02《仍未知晓，你的名字》](https://stellasora-archive.pages.dev/storysets/1002/100201.html)|配置未设独立时间|从沙漠获救后、抵达埃摩前，四人首次共同登塔|
|[#03《夜放花千树》](https://stellasora-archive.pages.dev/storysets/1003/100301.html)|2025-11-11 04:00|苍梧游鱼节，三人童年之后；年份未给出|
|[#04《抹茶梦语》](https://stellasora-archive.pages.dev/storysets/1004/100401.html)|2025-11-11 04:00|花原带领菲莱家政分部，师父最后一次吃蛋糕已是许久前|
|[#05《老油条与新员工》](https://stellasora-archive.pages.dev/storysets/1005/100501.html)|2025-12-02 12:00|第二章尾声的转正之后，贝修莉娜仍处于刚转正的时期|
|[#06《卫队之魂，骑士之心》](https://stellasora-archive.pages.dev/storysets/1006/100601.html)|2025-12-02 12:00|帝国卫队第一季宣传片拍摄至上映；第二季之前|
|[#07《雪愿的回响》](https://stellasora-archive.pages.dev/storysets/1007/100701.html)|2025-12-30 12:00|万送屋成立后首个雪愿节。很可能与996年霜月的圣夜活动同届；前夜、派件当日与团聚按话次区分。|
|[#08《真理的囚徒》](https://stellasora-archive.pages.dev/storysets/1008/100801.html)|2026-01-27 12:00|服刑期间，早于地下诊所行医；月份未知|
|[#09《临时搭档》](https://stellasora-archive.pages.dev/storysets/1009/100901.html)|2026-02-17 12:00|雾语与魔王建立通讯后；潜入与通知卫队跨数日|
|[#10《丰收日》](https://stellasora-archive.pages.dev/storysets/1010/101001.html)|2026-02-17 12:00|岭川管理菲莱温室时期，尚无可定年的收成记录|
|[#11《晨间溜走的信使》](https://stellasora-archive.pages.dev/storysets/1011/101101.html)|2026-03-10 12:00|万送屋三人结伴后，为共同出远门筹钱的阶段|
|[#12《眼眸中的彼此》](https://stellasora-archive.pages.dev/storysets/1012/101201.html)|2026-03-10 12:00|埃摩，与格芮初遇；第一章揭示身份之后|
|[#13《大小姐与俏女仆》](https://stellasora-archive.pages.dev/storysets/1013/101301.html)|2026-03-31 12:00|第四章三大委托解决后、《谜影的序曲》忆及花原名片前，亦早于修炼手册茶会|
|[#14《跨越星声的对话》](https://stellasora-archive.pages.dev/storysets/1014/101401.html)|2026-04-30 12:00|焦糖尚未了解尊者；塔内幻境先于地理协会联合讨伐|
|[#15《可爱依赖症候群》](https://stellasora-archive.pages.dev/storysets/1015/101501.html)|2026-05-26 12:00|第一季宣传片播出后，第二季数周后公开|
|[#16《此间日常》](https://stellasora-archive.pages.dev/storysets/1016/101601.html)|2026-07-14 12:00|协会造船计划因经费搁置以后；千塔分部忙碌的一天延续到次晨|
|[#17《最珍贵的宝物》](https://stellasora-archive.pages.dev/storysets/1017/101701.html)|2026-09-01 12:00|#11三人约好一起存钱后、三轮车仍在预留期内；第三话回到数周前|
|[#18《眠于秋分之日》](https://stellasora-archive.pages.dev/storysets/1018/101801.html)|2026-10-13 12:00|星塔历996年谷月24日，达尔茜亚风波平息后的菲莱|

11 月的运营长图已公布第十九篇《比“宝石”更耀眼的》，安排于 2026 年 11 月 27 日 12:00 常驻。11 月 12 日仍属预告，故未猜测分话或主人公。[版本公告](https://stellasora.yostar.cn/news/5077) · [正式篇名在长图末栏](https://webusstatic.yo-star.com/web-cms-test/upload/content/2026/11/09/OvmfWJ_5.jpg)

另按同一 ChapterId 逐项比对上游繁中、日文、韩文与英语的 18 个标题，已纳入关键词。繁中镜像为 #18《眠於秋分之日》，GameKee 保存的繁中公告标题为《眠於秋分之際》，国服官方为《眠于秋分之日》。篇号、更新批次和内容主题相合，作为同一条目的异写。现实公告使用各区当地时间。[繁中表](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/TW/language/zh_TW/StorySetChapter.json) · [繁中公告存档](https://www.gamekee.com/stellasora/722580.html) · [国服官方公告](https://stellasora.yostar.cn/news/4757)

## 能够交叉核验的位置

1. **两笔食物，一条从第一章延伸到第二章的线。** #02 的开头把首次登塔放在沙漠获救与抵达埃摩之间，末话才邀请魔王加入。#01 不是整体早于序章的前传。其一在修行回忆之后，千都世吃到的面包和鱼可对应一章04花月26日12:40在桥上留下的食物。其三与二章03A共享雨月2日04:15的水道桥走廊场记。她自己的早年、赠饭和出刀应分成三层。 [仍未知晓，你的名字 其一](https://stellasora-archive.pages.dev/storysets/1002/100201.html)、[仍未知晓，你的名字 其四](https://stellasora-archive.pages.dev/storysets/1002/100204.html)、[桥洞下](https://stellasora-archive.pages.dev/main/ch01/STm01_04.html)、[刀尖之寒，掌心之暖 其一](https://stellasora-archive.pages.dev/storysets/1001/100101.html)、[暗夜中的视线](https://stellasora-archive.pages.dev/main/ch02/STm02_03_a.html)、[刀尖之寒，掌心之暖 其三](https://stellasora-archive.pages.dev/storysets/1001/100103.html)

2. **同一间诊所，两分钟的视角差。** #08其二回到入狱两个月前；其三从假死离开监狱、开诊所、代班，才推进到雨月兜帽日08:28。密涅瓦送来的病人和对话与二章05开头雨月2日08:30相合。完整异闻的建议位置随菲莱篇推进，避免预先泄露医生的义眼与过去。 [真理的囚徒 其二](https://stellasora-archive.pages.dev/storysets/1008/100802.html)、[真理的囚徒 其三](https://stellasora-archive.pages.dev/storysets/1008/100803.html)、[仁义与刀](https://stellasora-archive.pages.dev/main/ch02/STm02_05.html)

3. **从实习生到新人。** 二章07贝修莉娜仍以实习生接待顾客，到尾声才向魔王报告转正。#05开头与次话明确是刚转正的新人；给她办理采购业务有时段下界。另一篇散文《沐光祷告》中她还在实习，发生顺序正相反。 [特许经营](https://stellasora-archive.pages.dev/main/ch02/STm02_07.html)、[新的起点](https://stellasora-archive.pages.dev/main/ch02/STm02_11.html)、[老油条与新员工 其一](https://stellasora-archive.pages.dev/storysets/1005/100501.html)、[老油条与新员工 其二](https://stellasora-archive.pages.dev/storysets/1005/100502.html)

4. **两次初见的对象不同。** #12 是格芮向魔王初次自报姓名；魔王已自称魔王协议执行官，一章末尾解释了这个身份。格芮羁绊下篇再次问起第一次触碰绳索，故应在异闻后阅读。#13 中埃莉诺是重逢，花原则初次介绍自己。第四章末已结束三大委托，谜影03回忆前段时间收到的名片，逐句重现 #13末话递名片场面。修炼手册再回忆这次救援；羁绊下篇的共舞，又被《飞吧，笼中鸟》点名追忆。 [眼眸中的彼此 其一](https://stellasora-archive.pages.dev/storysets/1012/101201.html)、[项圈与绳索 下](https://stellasora-archive.pages.dev/characters/149/14903.html)、[在星塔下](https://stellasora-archive.pages.dev/main/ch04/STm04_10.html)、[大小姐与俏女仆 其一](https://stellasora-archive.pages.dev/storysets/1013/101301.html)、[大小姐与俏女仆 其三](https://stellasora-archive.pages.dev/storysets/1013/101303.html)、[合作共赢](https://stellasora-archive.pages.dev/main/chsp7/STm06x5_03.html)、[大小姐们的茶会](https://stellasora-archive.pages.dev/events/10111/101110201.html)、[后辈的烦恼日 下](https://stellasora-archive.pages.dev/characters/137/13703.html)、[飞吧，笼中鸟](https://stellasora-archive.pages.dev/discs/214059.html)

5. **两季宣传片。** #06结尾邀拍续作，#15末话写着第二季公开。两篇主要拍摄场景都含戏中戏。角色在剧中相斗的镜头不构成她们在现实阵营敌对的证据。 [卫队之魂，骑士之心 其三](https://stellasora-archive.pages.dev/storysets/1006/100603.html)、[可爱依赖症候群 其三](https://stellasora-archive.pages.dev/storysets/1015/101503.html)

6. **埃摩派件的制服。** #07说明这是万送屋成立以来的首个雪愿节。两份独立剧本都写到恩赐意志请信使去埃摩、却只寄来一套合苍兰身材的使者服，故很可能对应圣夜活动同届；当年霜月25日属于跨篇互证。#07首话还在准备，确切日另留空。 [雪愿的回响 其一](https://stellasora-archive.pages.dev/storysets/1007/100701.html)、[雪愿的回响 其二](https://stellasora-archive.pages.dev/storysets/1007/100702.html)、[雪愿节的使者](https://stellasora-archive.pages.dev/events/20101/201010201.html)、[漫雪的蓝调](https://stellasora-archive.pages.dev/events/20101/201010206.html)

7. **菲莱的次日放到九章后读。** 六章末场记为谷月23日。#18开头标出谷月24日10:00、菲莱郊外，并明确说明距达尔茜亚引起的风波已过去。各文本里「亚／娅」写法不一。放在九章后有助于理解尘沙的异常记忆。 [未知的明天](https://stellasora-archive.pages.dev/main/ch06/STm06_13.html)、[眠于秋分之日 其一](https://stellasora-archive.pages.dev/storysets/1018/101801.html)、[眠于秋分之日 其三](https://stellasora-archive.pages.dev/storysets/1018/101803.html)、[窄门](https://stellasora-archive.pages.dev/main/ch09/STm09_01_d.html)

8. **一辆车的预留期串起万送屋的两篇异闻。** #17其一重现 #11其二三百万朵拉与预留三个月的交易话语；#17其三，多娜又提醒特丽莎曾约好要三个人一起存钱，对应 #11末尾。寻宝当日因此在 #11 筹钱约定之后，尚未买下预留的车。 [晨间溜走的信使 其二](https://stellasora-archive.pages.dev/storysets/1011/101102.html)、[晨间溜走的信使 其三](https://stellasora-archive.pages.dev/storysets/1011/101103.html)、[最珍贵的宝物 其一](https://stellasora-archive.pages.dev/storysets/1017/101701.html)、[最珍贵的宝物 其三](https://stellasora-archive.pages.dev/storysets/1017/101703.html)

9. **两场演讲。** 《初雪来时》下篇是冬香首次完成营地演讲；《花火》她准备在规模更大的丰收祭演讲，主动回顾先前的营地经验。此处有明确先后，但报道与发售时间都没有给出故事中的绝对年份。 [初雪来时 下](https://stellasora-archive.pages.dev/characters/134/13403.html)、[花火](https://stellasora-archive.pages.dev/discs/214017.html)

10. **出生日期与纪年分开。** 花原明说今天是生日，档案列4月20日；花铃生日当天收到冲浪板，档案列9月1日。两者同属月日线索，尚未从剧情找到对应年份。 [女仆的秘密任务 下](https://stellasora-archive.pages.dev/characters/119/11903.html)、[伴我航行](https://stellasora-archive.pages.dev/discs/214057.html) · [CharacterArchiveBaseInfo 地区原表](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/language/zh_CN/CharacterArchiveBaseInfo.json)

11. **79篇独立散文也有可对表的事件。** 《酒暖灯明时》在苍梧走私案结案后聚餐，《冬夜后的黎明》在北境委托的余波中，《夏日栖息地》回顾刚解决的奶奶风波，《夏日进行曲》提到花铃隐形眼镜在星塔中的意外，《荣誉时刻》是埃莉诺与活动08同场的颁奖感受。《革新的萌芽》则同时记录菲莱动荡平息后和幼年两个阶段。 [人间万象更新时](https://stellasora-archive.pages.dev/events/10104/101040211.html)、[告别风雪](https://stellasora-archive.pages.dev/events/10105/101050212.html)、[漫无止境的夏天](https://stellasora-archive.pages.dev/events/11100/111000211.html)、[镜框里的海](https://stellasora-archive.pages.dev/events/10110/101100208.html)、[荣誉之夜](https://stellasora-archive.pages.dev/events/10111/101110210.html)、[未知的明天](https://stellasora-archive.pages.dev/main/ch06/STm06_13.html) · [散文原表，可查对应 ID](https://github.com/AutumnVN/StellaSoraData/blob/a7ba98f95592b13c1290613b305a6b6a688f5fd0/CN/language/zh_CN/DiscIP.json)

## 社区读序与未决事项

Reddit 的一周目路线建议二章后补 #01、#02、#12，九章后补 #18，符合保护揭示的需要。本指南独立以正文定位 #02 在第一章前、#18 在第六章后。日本玩家实录亦观察到按故事时间 #02 早于 #01。韩语资料把 #01 笼统写在二章04与05之间，其三确实接近该处，但一章赠饭和二章03A的场记提示整篇跨度更长。繁中玩家就诺瓦前史及角色身分还有多种推测，未作历年硬锚。[Reddit 玩家读法](https://www.reddit.com/r/StellaSora/comments/1xdz8mn/reading_guide_for_stella_sora_arc_1/) · [日本玩家阅读实录](https://room-shiki.hatenablog.com/entry/2025/10/23/100000) · [韩语分篇整理](https://www.namu.moe/w/스텔라%20소라/스토리/노바%20기담) · [繁中主线考据讨论](https://forum.gamer.com.tw/Co.php?bPage=0&bsn=81566&sn=4183&subbsn=9)

仍待更精确定位的典型情况包括 #03 游鱼节是哪一年、#04 的宴会与其他工作委托相距多久、#10 的温室收成与菲莱丰收祭是否有关，以及万送屋寻宝与《敬启》委托的相对位置。没有用发售日期或角色编号补齐这些空格。对于《白日花园》的附文，角色自己亦不能证实记忆，应保留文本的不确定性。特别篇相关的《指引前路的启明星》与《永恒的闪耀》可提早取得，但其内容触及后段揭示，初读建议推迟至特别篇读完。

维护时按小节 ID 核对上游，把已开放正文与预告占位匹配；若分支或标题发生更动，仍以剧本标识及同一段动作、引述或场记重新验证。四份编辑表按篇组及小节记录人审判断，独立散文另表保存每篇性质与依据。
