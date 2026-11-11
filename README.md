# 诺瓦剧情手记

《星塔旅人》中文互动阅读指南。第一次玩可以沿着主线读到角色初遇，通关后也能回来查两段故事是否发生在同一天。第一版核查于 2026 年 11 月 12 日，采用 11 月 11 日的 Stella Sora Archive 快照。

**[在线打开《诺瓦剧情手记》](https://juvenile-a3.github.io/stella-sora-story-guide/)** · [直接查剧情目录](https://juvenile-a3.github.io/stella-sora-story-guide/#catalog) · [研究摘要（含剧透）](research-notes.md)

## 打开与使用

解压完整项目，双击 **index.html**。网页、图片、检索与阅读进度都可以离线使用。点击篇目的原文、游戏公告或资料镜像链接时需要联网。

从离线版转到在线版时，在原来的页面打开“管理阅读进度”导出备份，再在新页面导入。两个地址分别保存阅读状态。

1. 首页点“从序章开始”，再点“阅读本篇原文”。读完可以回到详情选“标为已读，读下一篇”。默认显示 559 个路线单元，包含主线、异闻、活动、个人剧情、秘闻、NPC 羁绊以及少量预告。勾选“显示可选补完”可以在相应人物或事件附近找到心链、逸闻、履历、演出等内容。进度总数包含所有 2,710 项。
2. “故事时间线”依诺瓦历和有依据的相对窗口分组。切换显示尺度、选择时期或人物即可缩小范围。有些篇目跨越多年，在详情里展开逐场时间与地点。标为分支未来的记录属于特定选择；只有同场或并行行动有证据时，才会明确并列。
3. 点首页“查找剧情”或按 `/` 进入检索，可以搜 `#12`、篇名和关键词。手机可在搜索框下展开筛选；当前筛选可复制网址分享。首页四位旅人的头像直达各自羁绊，“查看全部”可选其他旅人。剧透保护默认开启，允许查找公开归属的个人故事，并隐藏未读篇目的客串、关键标题和考据。可直接打开本篇原文，或单篇揭示考据。
4. “人物关系”可从人物、组织、历史事件或剧情依赖进入，点击节点即可打开篇目。人物的“推荐路线首次出现”与“正文所见的初遇”各有标记。匿名身份和跨年代形态仅在有文本依据时关联。
5. 用篇目右侧选择未读、在读、已读。批量操作前可查看所选范围。顶部书本图标打开进度面板，可导出备份、合并导入或恢复整份备份。阅读状态保存在当前浏览器，换浏览器、清理浏览数据、移动离线目录前可先导出。

## 资料与维护

| 文件 | 用途 |
|---|---|
| [研究摘要](research-notes.md) | 覆盖口径、重要证据、未决之处与资料来源 |
| [主线与活动](research/main-events.md) · [异闻、羁绊与秘闻](research/side-stories.md) | 分章分组研究，含剧透 |
| [阅读条目](data/story-data.json) | 每个阅读单元的稳定进度键、证据等级、原文、理由、窗口和关系 |
| [人物](data/characters.json) · [时间线](data/timeline.json) | 出场索引、确认初遇、组织关系、推荐顺序、故事时间及有类型的边 |
| [版本与计数](data/metadata.json) | 上游两份镜像版本、各类条目与等级分布 |
| [本版验收记录](research/verification.md) | 档案对账、定位精度、实际浏览器的检索与进度测试 |
| [构建程序](build/build_guide.py) · [校验程序](build/validate.py) | 从快照重建网页数据、核验覆盖和前置 |
| [来源与署名](NOTICE.md) | 资料和本地图片来源、改编说明 |

网页通过 `data/guide.js` 载入与三个 JSON 文件相同的数据，兼容浏览器直接打开本地文件。更改内容后重新构建即可同时更新两种格式。

公开站点由 GitHub Pages 从 `main` 分支的根目录发布。更新并提交构建产物后，Pages 会重新部署。站内导航使用 URL 片段，可直接分享某一篇或某一页的地址。

### 重建此版

需要 Python 3.10 或更高版本和 Git。首次取得档案库和固定版本的中文配置表需要联网。以下命令在解压后的项目根目录运行。只想阅读时无需执行。

```powershell
git clone --depth 1 --filter=blob:none --sparse https://github.com/419bw/stellasora-archive.git source-archive
git -C source-archive fetch --depth 1 origin f3209414ab301a552755781487b560a1bbcda72f
git -C source-archive checkout --detach f3209414ab301a552755781487b560a1bbcda72f
git -C source-archive sparse-checkout set story_docs
python -B -X utf8 build/build_guide.py source-archive --cache source-cache
python -B -X utf8 build/validate.py source-archive
```

原始表缓存以镜像提交号分目录。取得此版来源后，再次构建可离线进行。已生成的交付物也可独立执行 `python -B -X utf8 build/validate.py` 校验数据包。

### 收进新版本

1. 在另一份检出目录更新档案库，对比 `story_docs/_data/sections.json`、`chapters.json`、`_chat/_index.md` 及 `.upstream_sync_state.json`。以 family 和游戏 ID 对账，检查只有关卡、没有文本的节点及新增的未挂载文本。
2. 用 `python -B -X utf8 build/refresh_main_tables.py source-archive` 刷新活动回顾和图连接的副本。从同版各语言 StorySetChapter 表复核 `build/nova-locales.json`。官方开放时间、延期与服务器时区要分别核实。
3. 主线与活动结论维护在 `main_events.py`、`main_event_notes.py`。异闻、羁绊、秘闻和秘纹独立散文有逐条考据表。扩展来源在 `supplement.py`，旅人长篇档案的逐条互证在 `profile_review.py`，穿插阅读与跨类连接在 `build_guide.py`。写入明确年代或关系前，保留对应的场记、原文链接或官方配置依据。
4. 复核正式公开后是否可以移除旧预告、改订前置或旧别名。替换已开放内容时保留原进度键。新篇若缺少依据，给出未定位原因和阅读窗口。
5. 重跑构建和校验，双击网页核对新增篇目的显示、分支、剧透保护及旧备份导入。网页的资料版本取自实际快照；本版研究笔记里的日期和结论应在复审后更新。

### 数据字段

`route` 是编辑读序的排序值。`phase` 表示时间线展示区间，`timeWindow` 保留原考据窗口，`calendar` 的空日、空月保留为空。`time` 说明剧中时间，`dateScope` 和 `sceneLabels` 用来拆解多镜头或跨期叙述。`grade` 对应定位依据强度，`positionStatus` 表示定位精度，`availability` 表示资料或开放状态。`optional` 控制首读路线的默认显示。

`requires` 表示内容前置，`readAfter` 是编辑阅读建议，`unlockRequires` 是系统解锁。`topologyParents` 保留关卡来路，`alternativeParents` 表示有多条可到达的来路。`related` 只表示值得对读。`id` 用于篇目链接，`progressKey` 优先采用家族和游戏 ID。每个条目的初始阅读状态为未读，读者自己的状态独立保存在浏览器或导出文件里。
