/* No HTTP requests are needed to open this guide. data/guide.js is generated from the same JSON files used for research. */
"use strict";
(() => {
  const guide = window.GUIDE;
  const $ = (selector) => document.querySelector(selector);
  if (!guide || !Array.isArray(guide.stories)) {
    $("#workspace").innerHTML =
      '<div class="empty"><h2>未载入剧情数据</h2><p>请保留完整项目目录，确认 data/guide.js 与网页位于同一份解压目录。</p></div>';
    $("#hero").hidden = true;
    return;
  }
  const paths = {
    route:
      '<path d="M4 18V8a3 3 0 0 1 3-3h10m-3-3 3 3-3 3M4 13h10m-3-3 3 3-3 3"/><circle cx="4" cy="19" r="2"/>',
    time: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/>',
    catalog:
      '<rect x="3" y="4" width="7" height="7" rx="1"/><rect x="14" y="4" width="7" height="7" rx="1"/><rect x="3" y="15" width="7" height="6" rx="1"/><rect x="14" y="15" width="7" height="6" rx="1"/>',
    graph:
      '<circle cx="5" cy="12" r="2.5"/><circle cx="17" cy="5" r="2.5"/><circle cx="17" cy="19" r="2.5"/><path d="m7 11 8-5m-8 7 8 5"/>',
    book: '<path d="M3 5c3-1 6-1 9 1 3-2 6-2 9-1v14c-4-1-6-1-9 1-3-2-5-2-9-1zM12 6v14"/>',
    shield:
      '<path d="m12 2 8 3v6c0 5-3.5 8-8 11-4.5-3-8-6-8-11V5z"/><path d="m8.5 11.5 2.4 2.5 4.7-5"/>',
    eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="2.5"/>',
    next: '<path d="m9 5 7 7-7 7"/>',
    prev: '<path d="m15 5-7 7 7 7"/>',
    arrow: '<path d="M4 12h15m-6-6 6 6-6 6"/>',
    mark: '<path d="M6 3h12v18l-6-4-6 4z"/>',
    list: '<path d="M8 6h12M8 12h12M8 18h12M4 6h0m0 6h0m0 6h0"/>',
    search: '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
    play: '<circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z"/>',
    close: '<path d="M5 5l14 14M19 5 5 19"/>',
    ext: '<path d="M13 4h7v7m0-7L10 14M10 5H5v14h14v-5"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5m0-9v.1"/>',
    lock: '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 1 1 8 0v3"/>',
    check: '<path d="m4 12 5 6L20 6"/>',
    select:
      '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="m7 12 3 3 7-7"/>',
    sparkle:
      '<path d="M12 2c1.4 6.2 3.8 8.6 10 10-6.2 1.4-8.6 3.8-10 10C10.6 15.8 8.2 13.4 2 12c6.2-1.4 8.6-3.8 10-10Z"/>',
    up: '<path d="M12 16V3m-5 5 5-5 5 5M4 15v5h16v-5"/>',
    down: '<path d="M12 3v13m-5-5 5 5 5-5M4 16v4h16v-4"/>',
    group:
      '<circle cx="9" cy="9" r="3"/><path d="M3 20a6 6 0 0 1 12 0M15 6a3 3 0 0 1 0 6m2 3a5 5 0 0 1 4 5"/>',
  };
  const icon = (name) =>
    '<svg aria-hidden="true" class="icon" viewBox="0 0 24 24">' +
    (paths[name] || paths.sparkle) +
    "</svg>";
  const esc = (v) =>
    String(v ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const list = (value) => (Array.isArray(value) ? value : value ? [value] : []);
  const unique = (values) => Array.from(new Set(values.filter(Boolean)));
  const cmp = (a, b) =>
    String(a ?? "").localeCompare(String(b ?? ""), "zh-CN", { numeric: true });
  const number = (value) =>
    Number.isFinite(Number(value)) ? Number(value) : 999999;
  const fmt = (value) => Number(value).toLocaleString("zh-CN");
  const by = (items, pick) => {
    const out = new Map();
    for (const item of items) {
      const key = pick(item);
      if (!out.has(key)) out.set(key, []);
      out.get(key).push(item);
    }
    return out;
  };
  const safeUrl = (u) => (/^https?:\/\//i.test(String(u)) ? esc(u) : "");
  const external = (u, label) =>
    safeUrl(u)
      ? '<a href="' +
        safeUrl(u) +
        '" target="_blank" rel="noopener noreferrer">' +
        esc(label) +
        " " +
        icon("ext") +
        "</a>"
      : "";
  const button = (action, label, classes = "btn", attrs = "") =>
    '<button type="button" class="' +
    classes +
    '" data-act="' +
    action +
    '" ' +
    attrs +
    ">" +
    label +
    "</button>";
  const options = (pairs, selected) =>
    pairs
      .map(
        ([key, label]) =>
          '<option value="' +
          esc(key) +
          '"' +
          (String(key) === String(selected) ? " selected" : "") +
          ">" +
          esc(label) +
          "</option>",
      )
      .join("");
  const tabNames = {
    route: "推荐路线",
    time: "故事时间线",
    catalog: "剧情目录",
    graph: "人物关系",
  };
  const typeTexts = {
    main: "主线 / 序章",
    side: "诺瓦异闻",
    event: "活动",
    person: "人物故事",
    secret: "秘闻",
    extra: "补完",
  };
  const typesOf = (t) =>
    /主线|序章|特别篇/.test(t)
      ? "main"
      : /异闻|故事集/.test(t)
        ? "side"
        : /活动/.test(t)
          ? "event"
          : /羁绊|好感|个人/.test(t)
            ? "person"
            : /秘闻/.test(t)
              ? "secret"
              : "extra";
  const gradeText = {
    A: "正文或官方明确",
    B: "多处文本互证",
    C: "场景、人物或季节推定",
    D: "仅有发布或玩家读序线索",
    U: "尚无跨篇定位依据",
  };
  const stateText = { unread: "未读", reading: "在读", read: "已读" };
  const graphTabs = {
    people: "人物",
    orgs: "组织",
    history: "历史事件",
    deps: "剧情依赖",
  };
  const all = guide.stories,
    people = list(guide.characters),
    timeline = guide.timeline || {},
    meta = guide.meta || {};
  const stories = new Map(all.map((s) => [s.id, s])),
    personByName = new Map(people.map((p) => [p.name, p]));
  const edges = list(timeline.edges),
    outgoing = by(edges, (e) => e.from),
    incoming = by(edges, (e) => e.to);
  const orgs = list(timeline.organizations),
    histories = list(timeline.history),
    periods = list(timeline.periods);
  const periodMeta = new Map(periods.map((p) => [p.id, p])),
    phases = unique([
      ...periods.map((p) => p.id),
      ...all.map((s) => s.phase || "未知"),
    ]);
  const sortedTypes = unique(all.map((s) => s.type));
  const routeStories = [...all].sort(
    (a, b) =>
      number(a.route) - number(b.route) ||
      cmp(a.group, b.group) ||
      number(a.order) - number(b.order) ||
      cmp(a.id, b.id),
  );
  const indexes = new Map(routeStories.map((s, index) => [s.id, index]));
  const storageKey = "stella-sora-reading-guide.v1";
  let saveMessage = "",
    saved;
  try {
    saved = JSON.parse(localStorage.getItem(storageKey) || "{}") || {};
  } catch {
    saved = {};
    saveMessage = "当前浏览器无法读取本地进度。可在阅读进度中导出备份。";
  }
  const stableKey = (id) => stories.get(id)?.progressKey || id;
  const knownProgressKeys = new Set(all.map((s) => stableKey(s.id)));
  const validStates = (obj) => {
    const clean = Object.create(null),
      entries = Object.entries(obj || {});
    for (const [id, value] of entries)
      if (["reading", "read"].includes(value) && !knownProgressKeys.has(id))
        clean[stableKey(id)] = value;
    for (const [id, value] of entries)
      if (["reading", "read"].includes(value) && knownProgressKeys.has(id))
        clean[id] = value;
    return clean;
  };
  let progress = validStates(saved.progress),
    guard = saved.guard !== false;
  const revealed = new Set(),
    selected = new Set();
  let view = "route",
    currentList = [],
    pageNo = 1,
    bulk = false,
    modal = "",
    modalId = "",
    lastFocus = null,
    returnFocusSelector = "",
    toastTimer;
  const pageSize = 24;
  let stage = "*",
    phase = "*",
    zoom = "篇目",
    timePerson = "",
    graphMode = "people",
    graphKey = "",
    graphQuery = "";
  const defaultFilter = () => ({
    q: "",
    type: "",
    person: "",
    phase: "",
    grade: "",
    status: "",
    position: "",
  });
  let filters = defaultFilter();
  let catalogFiltersOpen = false;
  const status = (s) => progress[stableKey(s.id)] || "unread";
  const visible = (s) =>
    !!s && (!guard || status(s) === "read" || revealed.has(s.id));
  const high = (s) =>
    /高/.test(s.risk) || /结局|终局|身份揭晓/.test(s.title || "");
  const repeatedTitles = by(all, (s) => s.group + "\n" + s.title);
  function safeTitle(s) {
    if (visible(s) || !high(s)) {
      const duplicates = repeatedTitles.get(s.group + "\n" + s.title) || [];
      return (
        (s.title || s.id) +
        (duplicates.length > 1
          ? "（" + (duplicates.indexOf(s) + 1) + "/" + duplicates.length + "）"
          : "")
      );
    }
    const code =
      s.code ||
      String(s.title || "").match(
        /^((?:#[0-9]+[.、\s-]*)?[0-9]{1,3}[A-Da-d]?)\s*[.、·—]/,
      )?.[1];
    const no = Number.isFinite(s.order) ? "第 " + s.order + " 项" : "";
    return (code || no || "未读篇目") + " · 标题已遮蔽";
  }
  const speakablePhase = (s) =>
    !guard ||
    availablePhases.has(s) ||
    /^(?:前?星塔历\s*\d+\s*年(?:[\s·]*(?:[雪旅鸣清花雨雷热谷猎雾霜\d]+月|月日未定|月份未定))?|未知|待考|待开放|未定位|序章|序章前|序章后|第[一二三四五六七八九十\d]+章(?:之前|之后|此前|以后|前|后|期间)?(?:（范围）)?|历史时期|年代不明|时间不明)$/.test(
      s,
    );
  const phaseLabel = (s) =>
    speakablePhase(s)
      ? periodMeta.get(s)?.label || s
      : (String(s).match(/^(前?星塔历(?:\s*\d+\s*年)?)/)?.[1] || "") +
        " 时段 " +
        (phases.indexOf(s) + 1) +
        "（含未读线索）";
  const safeGroup = (s) =>
    visible(s) || !high(s)
      ? s.group
      : String(s.group || "").match(
          /^(序章|特别篇|第[一二三四五六七八九十\d]+章|#\s*\d+)/,
        )?.[1] || "";
  const namedArchives = new Set(["角色羁绊", "心链", "邀约", "NPC羁绊", "旅人档案"]);
  const archiveOwner = (s) => namedArchives.has(s.type) ? s.group.split(" · ")[0] : "";
  const featuredTravelers = [["赤霞","chixia"], ["科洛妮丝","coronis"], ["璟麟","jinglin"], ["师渺","shimiao"]];
  const chapterNames = [
    "序章",
    "第一章",
    "第二章",
    "第三章",
    "第四章",
    "第五章",
    "第六章",
    "第七章",
    "第八章",
    "第九章",
    "后期补读（一）",
    "后期补读（二）",
  ];
  const stageKey = (s) =>
    s.route < 0
      ? "before"
      : Number.isFinite(Number(s.route)) && Number(s.route) < 1200
        ? "c" + Math.floor(Number(s.route) / 100)
        : "extra:" + s.type;
  const stageLabel = (key) =>
    key === "before"
      ? "序章前导读"
      : key.startsWith("c")
        ? chapterNames[+key.slice(1)] || "主线阶段"
        : "补完 · " + key.slice(6);
  const routeBuckets = by(routeStories, stageKey),
    timeBuckets = by(all, (s) => s.phase || "未知");
  const canonicalPhases = phases
    .filter((p) => timeBuckets.has(p))
    .sort(
      (a, b) =>
        number(periodMeta.get(a)?.order) - number(periodMeta.get(b)?.order) ||
        phases.indexOf(a) - phases.indexOf(b),
    );
  const getValue = (item) =>
    typeof item === "string" ? item : item?.label || item?.name || "";
  const series = (xs) => list(xs).map(getValue).filter(Boolean).join("、");
  const strip = (string) => String(string ?? "").toLocaleLowerCase();
  const showNotice = (message) => {
    const box = $("#notice");
    box.textContent = message;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (box.textContent = ""), 4200);
  };
  function store() {
    try {
      localStorage.setItem(
        storageKey,
        JSON.stringify({ version: 1, guard, progress }),
      );
      saveMessage = "";
    } catch {
      saveMessage = "浏览器未能保存本次更改，请从阅读进度导出备份。";
      showNotice(saveMessage);
    }
  }
  function writeStatus(id, value) {
    const key = stableKey(id);
    if (value === "unread") delete progress[key];
    else if (Object.hasOwn(stateText, value)) progress[key] = value;
  }
  function stat() {
    const counts = { read: 0, reading: 0, unread: 0 };
    all.forEach((s) => counts[status(s)]++);
    return counts;
  }
  function routePosition(s) {
    if (s.routeLabel) return s.routeLabel;
    const n = Number(s.route),
      key = stageKey(s);
    if (key.startsWith("extra:")) return "主线后按主题补完";
    if (key === "before") return "序章前导读";
    if (!Number.isFinite(n)) return "待考补完";
    if (n >= 1000) return stageLabel(key);
    const frac = n % 100;
    if (frac >= 40) return stageLabel(key) + "后";
    return stageLabel(key) + "阶段";
  }
  function routeTitle() {
    return stage === "*" ? (includeOptional ? "完整阅读路线" : "首读路线") : stageLabel(stage);
  }
  function storyHref(id) {
    const params = new URLSearchParams({story:id});
    if (view === "catalog")
      for (const [key, value] of Object.entries(filters)) if (value) params.set(key, value);
    return "#" + view + "?" + params.toString();
  }
  function catalogHash() {
    const params = new URLSearchParams(Object.entries(filters).filter(([, value]) => value));
    return params.size ? "#catalog?" + params : "#catalog";
  }
  function syncCatalogAddress() {
    if (view === "catalog" && !sheet.open) history.replaceState(null, "", catalogHash());
  }
  function focusSearch() {
    if (view !== "catalog") {
      filters = defaultFilter();
      location.hash = "catalog";
      window.addEventListener("hashchange", focusSearch, {once:true});
      return;
    }
    const input = $("#query");
    if (input) {
      input.focus({preventScroll:true});
      input.scrollIntoView({block:"center"});
    }
  }
  function titleBlock(title, subtitle, controls = "") {
    return (
      '<div class="view-heading"><div><h2>' +
      esc(title) +
      "</h2>" +
      (subtitle ? "<p>" + esc(subtitle) + "</p>" : "") +
      "</div>" +
      controls +
      "</div>"
    );
  }
  function selectState(s) {
    return (
      '<select aria-label="设置此篇阅读状态" class="state-select ' +
      status(s) +
      '" data-status="' +
      esc(s.id) +
      '">' +
      options(Object.entries(stateText), status(s)) +
      "</select>"
    );
  }
  function badge(s) {
    const gr = s.grade || "U",
      risk = s.risk || "未分级",
      cl = /高/.test(risk) ? "high" : /中/.test(risk) ? "mid" : "low";
    return (
      '<span class="badge e-grade" title="' +
      esc(gradeText[gr] || "") +
      '">证据 ' +
      esc(gr) +
      '</span><span class="badge risk-' +
      cl +
      '">' +
      esc(String(risk).replace(/剧透/g, "")) +
      "剧透</span>"
    );
  }
  function topologyMark(s) {
    const count = list(s.branches).length;
    let label = "";
    if (list(s.parallelNext).length > 1)
      label = "分头行动 · " + s.parallelNext.length + " 个并行视角";
    else if (count > 1) label = "分歧点 · " + count + " 条可选路线";
    else if (/终局|结局/.test(s.mode || "")) label = "独立路线终局";
    else if (list(s.alternativeParents).length > 1) label = "路线汇合";
    return label
      ? '<span class="branch-mark">' + icon("graph") + " " + label + "</span>"
      : "";
  }
  function row(s, opts = {}) {
    const g = safeGroup(s),
      info = opts.timeline
        ? visible(s)
          ? s.dateLabel || s.time
          : "时间线索已遮蔽"
        : routePosition(s);
    const title = safeTitle(s),
      visiblyGrouped = g && g !== title;
    const timeHint = opts.timeline
      ? ""
      : visible(s)
        ? s.dateLabel || s.time || "时段待考"
        : s.grade === "U"
          ? "时间待考"
          : "故事时间受保护";
    return (
      '<article class="story-row" data-kind="' +
      typesOf(s.type) +
      '">' +
      (bulk
        ? '<input class="pick" type="checkbox" aria-label="选择本篇" data-pick="' +
          esc(s.id) +
          '"' +
          (selected.has(s.id) ? " checked" : "") +
          ">"
        : "") +
      '<a href="' +
      esc(storyHref(s.id)) +
      '" class="row-open"><strong>' +
      esc(title) +
      '</strong><span class="row-sub"><span class="pin-type">' +
      esc(s.type) +
      "</span>" +
      (visiblyGrouped ? "<span>" + esc(g) + "</span>" : "") +
      "<span>" +
      esc(info) +
      "</span>" +
      (timeHint ? '<span class="time-hint">' + esc(timeHint) + "</span>" : "") +
      topologyMark(s) +
      badge(s) +
      "</span></a>" +
      '<div class="row-actions">' +
      selectState(s) +
      '<a class="row-chevron" aria-label="打开此篇详情" href="' +
      esc(storyHref(s.id)) +
      '">' +
      icon("next") +
      "</a></div></article>"
    );
  }
  function pager(total, count = Math.ceil(total / pageSize)) {
    return count < 2
      ? ""
      : '<div class="pager">' +
          button(
            "prev",
            icon("prev") + " 上一页",
            "btn",
            pageNo === 1 ? "disabled" : "",
          ) +
          "<span>" +
          pageNo +
          " / " +
          count +
          "</span>" +
          button(
            "next",
            "下一页 " + icon("next"),
            "btn",
            pageNo === count ? "disabled" : "",
          ) +
          "</div>";
  }
  function sliceStories(items) {
    currentList = items;
    pageNo = Math.max(
      1,
      Math.min(pageNo, Math.ceil(items.length / pageSize) || 1),
    );
    return items.slice((pageNo - 1) * pageSize, pageNo * pageSize);
  }
  function bulkControls() {
    if (!bulk) return "";
    return (
      '<div class="bulk">' +
      button("pick-page", "选本页", "tiny-btn") +
      button(
        "pick-all",
        "选全部 " + fmt(currentList.length) + " 篇",
        "tiny-btn",
      ) +
      button("clear-picks", "清除选择", "tiny-btn") +
      "<span>已选 " +
      fmt(selected.size) +
      ' 篇</span><select aria-label="批量更改后的状态" id="bulk-value">' +
      options(Object.entries(stateText), "read") +
      "</select>" +
      button("set-many", "应用", "tiny-btn", !selected.size ? "disabled" : "") +
      "</div>"
    );
  }
  const bulkBtn = () =>
    button("bulk", icon("select") + (bulk ? "结束批选" : "批量标记"), "btn");
  function empty(text) {
    return '<div class="empty"><p>' + esc(text) + "</p></div>";
  }
  function splitRows(chunk, pick, label, opts = {}) {
    return [...by(chunk, pick)]
      .map(
        ([key, items]) =>
          '<section class="reader-section"><div class="group-heading"><span class="stage-symbol">' +
          icon(opts.timeline ? "time" : "mark") +
          "</span><h3>" +
          esc(label(key)) +
          "</h3></div>" +
          items.map((s) => row(s, opts)).join("") +
          "</section>",
      )
      .join("");
  }
  function renderNav() {
    $("#nav").innerHTML = Object.entries(tabNames)
      .map(
        ([key, value]) =>
          '<a href="#' +
          key +
          '" class="navlink ' +
          (view === key ? "active" : "") +
          '"' +
          (view === key ? ' aria-current="page"' : "") +
          ">" +
          icon(key) +
          value +
          "</a>",
      )
      .join("");
    const sb = $("#spoiler");
    sb.innerHTML =
      icon(guard ? "shield" : "eye") + (guard ? "剧透保护" : "显示剧透");
    sb.setAttribute("aria-pressed", String(guard));
    sb.title = guard ? "点击显示所有篇目的剧透" : "点击保护未读篇目";
    $("#book").innerHTML = icon("book") + "<span>进度</span>";
    const hero = $("#hero");
    hero.className = view === "route" ? "hero" : "hero sub";
    const titles = {
      route: "诺瓦剧情手记",
      time: "故事内时间线",
      catalog: "全部剧情目录",
      graph: "人物与剧情关系图",
    };
    const intros = {
      route: "跟着主线遇见每一位旅人。读过之后，再回时间线拼起同一天的故事。",
      time: "在相对时期与可考日期之间，追踪人物经历。",
      catalog: "按篇目、所属故事、人物或证据等级查找档案。",
      graph: "从一次初遇、一场事件或一个分歧点，找到相连的篇目。",
    };
    const hasHistory = all.some((s) => status(s) !== "unread");
    hero.innerHTML =
      '<div class="hero-inner"><div class="hero-kicker">星塔旅人 · ' +
      (view === "route" ? "非官方剧情阅读指南" : tabNames[view]) +
      '</div><h1 id="hero-title">' +
      titles[view] +
      "</h1><p>" +
      intros[view] +
      "</p>" +
      (view === "route"
        ? '<div class="hero-actions">' +
          button(
            "resume",
            icon("book") + (hasHistory ? "继续阅读" : "从序章开始"),
            "hero-cta",
          ) +
          button("search", icon("search") + " 查找剧情", "hero-secondary",
            'aria-label="查找剧情，快捷键斜杠"') +
          '<a href="intro.html" class="hero-film">' + icon("play") + ' 介绍短片</a></div>'
        : "") +
      "</div>";
    const travelerIndex = $("#traveller-index");
    travelerIndex.hidden = view !== "route";
    if (!travelerIndex.hidden && !travelerIndex.childElementCount) {
      travelerIndex.innerHTML = '<div class="traveller-caption"><h2>旅人羁绊</h2><a href="#catalog?type=' +
        encodeURIComponent("角色羁绊") + '">查看全部 ' + icon("next") + '</a></div><div class="traveller-shortcuts">' +
        featuredTravelers.map(([name, image]) => '<a href="#catalog?' +
          new URLSearchParams({type:"角色羁绊",person:name}).toString().replace(/&/g,"&amp;") +
          '"><img src="assets/characters/' + image + '.webp" width="52" height="52" alt=""/><span>' +
          name + '</span>' + icon("next") + '</a>').join("") + '</div>';
    }
  }
  function sideOptions() {
    if (view === "route")
      return {
        title: "跳到阅读阶段",
        current: stage,
        action: "stage",
        allText: "全部阶段",
        entries: [...routeBuckets].map(([key, ss]) => [
          key,
          stageLabel(key),
          includeOptional ? ss.length : ss.filter((s) => !s.optional).length,
        ]).filter((row) => row[2] || row[0] === stage),
      };
    if (view === "time")
      return {
        title: "故事时期",
        current: phase,
        action: "phase",
        allText: "全部时期",
        entries: canonicalPhases.map((key) => [
          key,
          phaseLabel(key),
          timeBuckets.get(key).length,
        ]),
      };
    if (view === "catalog")
      return {
        title: "剧情分类",
        current: filters.type || "*",
        action: "side-type",
        allText: "全部分类",
        entries: sortedTypes.map((t) => [
          t,
          t,
          all.filter((s) => s.type === t).length,
        ]),
      };
    return {
      title: "关系索引",
      current: graphMode,
      action: "graph-mode",
      entries: Object.entries(graphTabs).map(([k, v]) => [k, v, ""]),
    };
  }
  function side() {
    const stats = stat(),
      pct = all.length ? Math.round((stats.read / all.length) * 100) : 0,
      menu = sideOptions(),
      params = menu.allText
        ? [["*", menu.allText, menu.entries.reduce((total, row) => total + Number(row[2]), 0)], ...menu.entries]
        : menu.entries;
    return (
      '<aside class="sidebar"><div class="progress-card">' +
      button("progress", icon("book") + " 我的阅读进度", "") +
      '<div class="progress-stat"><strong>' +
      fmt(stats.read) +
      "</strong><small>/ " +
      fmt(all.length) +
      ' 篇已读</small></div><div class="track"><i style="width:' +
      pct +
      '%"></i></div><div class="progress-tail"><span>' +
      fmt(stats.reading) +
      " 篇在读</span><span>" +
      pct +
      "%</span></div></div>" +
      '<div class="side-box"><div class="side-head">' +
      menu.title +
      icon("list") +
      '</div><div class="side-list">' +
      params
        .map(([key, label, count]) =>
          button(
            menu.action,
            icon(key === "*" ? "list" : view === "graph" ? "graph" : "mark") +
              "<span>" +
              esc(label) +
              "</span><small>" +
              esc(count) +
              "</small>",
            "side-item " + (menu.current === key ? "active" : ""),
            'data-key="' +
              esc(key) +
              '"' +
              (menu.current === key ? ' aria-current="true"' : ""),
          ),
        )
        .join("") +
      "</div></div>" +
      '<div class="side-foot">' +
      button("about", icon("info") + " 证据等级与资料来源", "") +
      '</div><label class="mobile-jump">' +
      menu.title +
      '<select data-menu="' +
      menu.action +
      '">' +
      options(
        params.map(([k, l, n]) => [k, l + (n !== "" ? " · " + fmt(n) : "")]),
        menu.current,
      ) +
      "</select></label></aside>"
    );
  }
  function renderRoute() {
    const pool = stage === "*" ? routeStories : routeBuckets.get(stage) || [],
      items = includeOptional ? pool : pool.filter((s) => !s.optional),
      chunk = sliceStories(items);
    return (
      titleBlock(
        routeTitle(),
        "按顺序点开篇目即可读原文。回忆和初遇已穿插在对应的主线阶段。",
        bulkBtn(),
      ) +
      '<div class="filter-meta"><span>' +
      fmt(items.length) +
      " 篇" +
      '</span><label class="toggle-extra"><input type="checkbox" id="optional"' +
      (includeOptional ? " checked" : "") +
      " >显示可选补完（" +
      fmt(pool.filter((s) => s.optional).length) +
      "）</label>" +
      button("about", "证据等级 " + icon("info"), "link-btn") +
      "</div>" +
      bulkControls() +
      (chunk.length
        ? splitRows(chunk, stageKey, stageLabel)
        : empty("这个阶段尚未收录篇目。")) +
      pager(items.length)
    );
  }
  function catalogMatches(s) {
    if (
      (filters.type && filters.type !== s.type) ||
      (filters.phase && filters.phase !== (s.phase || "未知")) ||
      (filters.grade && filters.grade !== (s.grade || "U")) ||
      (filters.status && filters.status !== status(s))
    )
      return false;
    if (filters.position && filters.position !== s.positionStatus) return false;
    if (
      filters.person &&
      archiveOwner(s) !== filters.person && (!visible(s) || !list(s.cast).includes(filters.person))
    )
      return false;
    if (!filters.q.trim()) return true;
    const fields = [
      safeTitle(s),
      safeGroup(s),
      archiveOwner(s),
      s.type,
      routePosition(s),
      phaseLabel(s.phase || "未知"),
    ];
    if (visible(s))
      fields.push(
        s.summary,
        s.time,
        s.dateLabel,
        s.reason,
        s.evidence,
        series(s.cast),
        series(s.places),
        series(s.keywords),
        series(s.aliases),
        s.id,
      );
    const haystack = strip(fields.join(" "));
    return strip(filters.q.trim())
      .split(/\s+/)
      .every((q) => haystack.includes(q));
  }
  function field(label, id, values, choice, emptyText) {
    return (
      '<label class="field">' +
      esc(label) +
      '<select data-filter="' +
      id +
      '">' +
      options([["", emptyText], ...values], choice) +
      "</select></label>"
    );
  }
  const visibleCast = () =>
    unique(all.filter(visible).flatMap((s) => list(s.cast))).sort(cmp);
  function renderCatalog() {
    const items = routeStories.filter(catalogMatches),
      chunk = sliceStories(items);
    const hasFilters = Object.values(filters).some(Boolean);
    const activeCount = Object.entries(filters).filter(([key, value]) => key !== "q" && value).length;
    return (
      titleBlock(
        "检索与筛选",
        "可以直接搜异闻编号、篇名或关键词，再缩小范围。",
        bulkBtn(),
      ) +
      '<div class="filters"><label class="search-field">' +
      icon("search") +
      '<input id="query" type="search" value="' +
      esc(filters.q) +
      '" aria-label="搜索剧情" placeholder="搜篇名、关键词或异闻编号，如 #12"></label>' +
      button("catalog-filters", (catalogFiltersOpen ? "收起筛选" : "展开筛选") +
        (activeCount ? " · " + activeCount : ""), "filter-switch",
        'aria-controls="catalog-options" aria-expanded="' + catalogFiltersOpen + '"') +
      '<div id="catalog-options" class="selects' + (catalogFiltersOpen ? ' expanded' : '') + '">' +
      field(
        "剧情分类",
        "type",
        sortedTypes.map((v) => [v, v]),
        filters.type,
        "全部分类",
      ) +
      field(
        "出场人物",
        "person",
        unique([...all.map(archiveOwner), ...visibleCast()]).sort(cmp).map((v) => [v, v]),
        filters.person,
        "全部人物",
      ) +
      field(
        "故事时期",
        "phase",
        canonicalPhases.map((v) => [v, phaseLabel(v)]),
        filters.phase,
        "全部时期",
      ) +
      field(
        "定位状态",
        "position",
        unique(all.map((s) => s.positionStatus)).map((v) => [v, v]),
        filters.position,
        "全部定位",
      ) +
      field(
        "定位证据",
        "grade",
        Object.entries(gradeText).map(([v, l]) => [v, v + " · " + l]),
        filters.grade,
        "全部等级",
      ) +
      field(
        "阅读状态",
        "status",
        Object.entries(stateText),
        filters.status,
        "全部状态",
      ) +
      button(
        "reset-filters",
        "重置筛选",
        "link-btn",
        !hasFilters ? "disabled" : "",
      ) +
      "</div></div>" +
      (guard
        ? '<p class="section-note">' +
          icon("shield") +
          " 已开启剧透保护。可以查找旅人本人的故事；尚未揭示的客串和情节不会出现在搜索结果中。</p>"
        : "") +
      '<div class="filter-meta"><span>找到 <b>' +
      fmt(items.length) +
      "</b> 篇</span></div>" +
      bulkControls() +
      (chunk.length
        ? chunk.map((s) => row(s)).join("")
        : '<div class="empty"><p>没有找到符合条件的剧情。</p>' +
          button("reset-filters", "清除条件，查看全部剧情", "btn") + '</div>') +
      pager(items.length)
    );
  }
  function timeSort(a, b) {
    const pa = canonicalPhases.indexOf(a.phase || "未知"),
      pb = canonicalPhases.indexOf(b.phase || "未知");
    if (pa !== pb) return pa - pb;
    if (a.chronoSort != null || b.chronoSort != null) {
      const at = a.chronoSort == null ? Infinity : Number(a.chronoSort),
        bt = b.chronoSort == null ? Infinity : Number(b.chronoSort);
      return (
        at - bt ||
        cmp(a.group, b.group) ||
        number(a.order) - number(b.order) ||
        cmp(a.id, b.id)
      );
    }
    return (
      cmp(a.group, b.group) ||
      number(a.order) - number(b.order) ||
      cmp(a.id, b.id)
    );
  }
  function timePages(items) {
    // Keep a shared scene at its first participant's position without collecting
    // unrelated rows into a group. Paginate complete groups, even at page breaks.
    const units = by(items, (s) =>
      s.parallelKey && visible(s)
        ? JSON.stringify(["parallel", s.phase, s.parallelKey])
        : JSON.stringify(["single", s.id]),
    );
    const pages = [];
    let page = [],
      size = 0;
    for (const group of units.values()) {
      if (size && size + group.length > pageSize) {
        pages.push(page);
        page = [];
        size = 0;
      }
      page.push(group);
      size += group.length;
    }
    if (page.length) pages.push(page);
    return pages;
  }
  function timeGroup(units) {
    let html = "";
    for (const [period, groups] of by(
      units,
      (group) => group[0].phase || "未知",
    )) {
      html +=
        '<section class="reader-section calendar"><div class="group-heading"><h3>' +
        esc(phaseLabel(period)) +
        "</h3></div>";
      let previousDate = "";
      for (const group of groups) {
        const first = group[0];
        if (group.length > 1) {
          html +=
            '<div class="parallel-caption">并行视角 · ' +
            esc(first.parallelKey) +
            '</div><div class="parallel-grid">' +
            group.map((s) => row(s, { timeline: true })).join("") +
            "</div>";
          previousDate = "";
        } else {
          const date = visible(first)
            ? first.dateLabel || "日历日期未定"
            : "日期已遮蔽";
          if (zoom === "日期" && date !== previousDate)
            html += '<div class="date-line">' + esc(date) + "</div>";
          html += row(first, { timeline: true });
          previousDate = date;
        }
      }
      html += "</section>";
    }
    return html;
  }
  function renderTime() {
    const peopleList = visibleCast(),
      items = (phase === "*" ? all : timeBuckets.get(phase) || [])
        .filter(
          (s) =>
            !timePerson || (visible(s) && list(s.cast).includes(timePerson)),
        )
        .sort(timeSort);
    currentList = items;
    let body = "";
    if (zoom === "时期") {
      body = [...by(items, (s) => s.phase || "未知")]
        .map(([k, ss]) =>
          button(
            "expand-period",
            "<span>" +
              esc(phaseLabel(k)) +
              "</span><small>" +
              fmt(ss.length) +
              " 篇 " +
              icon("next") +
              "</small>",
            "overview-card",
            'data-key="' + esc(k) + '"',
          ),
        )
        .join("");
    } else {
      const pages = timePages(items);
      pageNo = Math.max(1, Math.min(pageNo, pages.length || 1));
      body =
        timeGroup(pages[pageNo - 1] || []) + pager(items.length, pages.length);
    }
    return (
      titleBlock(
        timePerson ? timePerson + "的出场轨迹" : "按故事时期浏览",
        "同一时间段可容纳多篇。缺少年月日时保留相对定位，同组展示顺序不代表先后。",
      ) +
      '<div class="filters"><div class="tool-row"><div class="segment" aria-label="时间线缩放">' +
      ["时期", "篇目", "日期"]
        .map((v) =>
          button(
            "zoom",
            esc(v),
            "choice " + (zoom === v ? "active" : ""),
            'data-key="' + v + '" aria-pressed="' + (zoom === v) + '"',
          ),
        )
        .join("") +
      '</div><label class="field">人物轨迹<select id="time-person">' +
      options(
        [["", "所有人物"], ...peopleList.map((n) => [n, n])],
        timePerson,
      ) +
      '</select></label></div><div class="legend">' +
      Object.entries(typeTexts)
        .map(
          ([k, v]) =>
            '<span><i class="type-dot" data-kind="' +
            k +
            '"></i>' +
            v +
            "</span>",
        )
        .join("") +
      "</div></div>" +
      (guard
        ? '<p class="section-note">' +
          icon("shield") +
          " 未读条目的详细时间及人物轨迹受保护。</p>"
        : "") +
      '<div class="filter-meta"><span>' +
      fmt(items.length) +
      " 篇" +
      (phase !== "*" ? " · " + esc(phaseLabel(phase)) : "") +
      "</span>" +
      (phase !== "*"
        ? button("phase", "所有时期", "link-btn", 'data-key="*"')
        : "") +
      "</div>" +
      (items.length ? body : empty("此时期没有符合条件的篇目。"))
    );
  }
  const edgeNames = {
    alternative: "可选来路",
    path: "关卡衔接",
    parallel: "并行视角",
    prerequisite: "故事前置",
    branch: "可选分支",
    related: "互相参照",
    unlock: "系统解锁",
    reading: "阅读前置",
  };
  function node(label, sub, action = "", key = "", css = "") {
    const inner =
      "<strong>" +
      esc(label) +
      "</strong>" +
      (sub ? "<span>" + esc(sub) + "</span>" : "");
    return action
      ? button(action, inner, "node " + css, 'data-key="' + esc(key) + '"')
      : '<div class="node ' + css + '">' + inner + "</div>";
  }
  const knownIds = (xs) => unique(list(xs)).filter((id) => stories.has(id));
  const evidenceVisible = (ids) =>
    !guard ||
    (knownIds(ids).length > 0 &&
      knownIds(ids).every((id) => visible(stories.get(id))));
  function firstNote(p) {
    const verified = knownIds(p.first);
    if (verified.length)
      return verified.filter((id) => visible(stories.get(id))).length
        ? "正文所见的初遇"
        : "初遇篇目受保护";
    return "与魔王初遇待考";
  }
  function graphOptions() {
    if (graphMode === "people")
      return people
        .filter(
          (p) =>
            !guard ||
            knownIds(p.stories).some((id) => visible(stories.get(id))),
        )
        .map((p) => [p.name, p.name]);
    if (graphMode === "orgs")
      return orgs
        .filter(
          (o) =>
            !guard ||
            knownIds(o.stories).some((id) => visible(stories.get(id))),
        )
        .map((o) => [o.name, o.name]);
    if (graphMode === "history")
      return histories
        .filter((h) => evidenceVisible(h.stories))
        .map((h) => [h.label, h.label]);
    return routeStories
      .filter(
        (s) =>
          visible(s) &&
          ((incoming.get(s.id) || []).length +
            (outgoing.get(s.id) || []).length ||
            knownIds([
              ...list(s.requires),
              ...list(s.related),
              ...list(s.branches),
              ...list(s.parallelNext),
              ...list(s.readAfter),
              ...list(s.unlockRequires),
            ]).length),
      )
      .map((s) => [s.id, s.title + " · " + s.group]);
  }
  function relationItems(s) {
    const nodes = [];
    const add = (id, label, dir) => {
      if (
        stories.has(id) &&
        id !== s.id &&
        !nodes.some((n) => n.id === id && n.label === label && n.dir === dir)
      )
        nodes.push({ id, label, dir });
    };
    list(incoming.get(s.id)).forEach((e) =>
      add(e.from, edgeNames[e.type] || e.label || "相关", "in"),
    );
    list(outgoing.get(s.id)).forEach((e) =>
      add(e.to, edgeNames[e.type] || e.label || "相关", "out"),
    );
    for (const [fieldName, label, dir] of [
      ["requires", "故事前置", "in"],
      ["readAfter", "阅读前置", "in"],
      ["unlockRequires", "系统解锁", "in"],
      ["alternativeParents", "可选来路", "in"],
      ["branches", "可选分支", "out"],
      ["parallelNext", "并行视角", "out"],
      ["related", "互相参照", "out"],
    ])
      knownIds(s[fieldName]).forEach((id) => add(id, label, dir));
    return nodes;
  }
  function graphData() {
    const left = [],
      right = [],
      associations = new Map();
    let ids = [],
      label = graphKey,
      center = "",
      caption = "",
      note = "";
    const storyNode = (id, tag) => {
      const s = stories.get(id);
      return node(s.title, tag || s.type, "open", id);
    };
    if (graphMode === "people") {
      const p = personByName.get(graphKey);
      if (!p) return null;
      ids = knownIds(p.stories);
      center = "人物";
      caption = firstNote(p);
      const first = knownIds(p.first).filter((id) => visible(stories.get(id)));
      first.slice(0, 3).forEach((id) => left.push(storyNode(id, "与魔王初遇")));
      const earliest = knownIds(p.firstIndexed).find((id) =>
        visible(stories.get(id)),
      );
      if (earliest && !first.includes(earliest))
        left.push(storyNode(earliest, "推荐路线首次出现"));
      const groups = orgs.filter(
        (o) => list(o.members).includes(p.name) && evidenceVisible(o.stories),
      );
      groups
        .slice(0, 3)
        .forEach((o) =>
          left.push(node(o.name, "所属组织", "graph-org", o.name)),
        );
      if (!groups.length && p.organization && !guard)
        left.push(node(series(p.organization), "资料所列组织"));
      first.forEach((id) => associations.set(id, "与魔王初遇"));
      if (earliest && !associations.has(earliest))
        associations.set(earliest, "推荐路线首次出现");
    } else if (graphMode === "orgs") {
      const o = orgs.find((x) => x.name === graphKey);
      if (!o) return null;
      ids = knownIds(o.stories);
      center = "组织";
      caption = "成员与组织出场";
      const members = list(o.members).filter(
        (n) =>
          personByName.has(n) &&
          (!guard ||
            knownIds(personByName.get(n).stories).some((id) =>
              visible(stories.get(id)),
            )),
      );
      if (evidenceVisible(o.stories))
        members.forEach((n) => left.push(node(n, "成员", "graph-person", n)));
      list(o.links)
        .filter((l) => !guard || visible(stories.get(l.story)))
        .forEach((l) => {
          if (orgs.some((o) => o.name === l.to))
            left.push(node(l.to, l.label || "关联组织", "graph-org", l.to));
          if (stories.has(l.story)) {
            ids.push(l.story);
            associations.set(l.story, l.label || "组织关系依据");
          }
        });
      ids = unique(ids);
    } else if (graphMode === "history") {
      const h = histories.find((x) => x.label === graphKey);
      if (!h) return null;
      ids = knownIds(h.stories);
      center = "历史事件";
      caption = "正文回溯与相关篇目";
      if (h.source && typeof h.source === "string" && safeUrl(h.source))
        note = external(h.source, "核对事件来源");
      const names = unique(
        ids
          .filter((id) => visible(stories.get(id)))
          .flatMap((id) => list(stories.get(id).cast)),
      ).filter((n) => personByName.has(n));
      names
        .slice(0, 4)
        .forEach((n) =>
          left.push(node(n, "相关篇目的出场人物", "graph-person", n)),
        );
    } else {
      const s = stories.get(graphKey);
      if (!s || !visible(s)) return null;
      label = s.title;
      center = s.type;
      caption = "剧情节点";
      note = "可选分支表示不同后继，系统解锁只说明开放条件。";
      const connections = relationItems(s).filter((n) =>
        visible(stories.get(n.id)),
      );
      connections
        .filter((n) => n.dir === "in")
        .slice(0, 5)
        .forEach((n) => left.push(storyNode(n.id, n.label)));
      connections
        .filter((n) => n.dir === "out")
        .slice(0, 5)
        .forEach((n) => right.push(storyNode(n.id, n.label)));
      connections.forEach((n) => associations.set(n.id, n.label));
      ids = unique(connections.map((n) => n.id));
    }
    const hiddenCount = ids.filter((id) => !visible(stories.get(id))).length;
    const shown = ids
      .filter((id) => visible(stories.get(id)))
      .map((id) => stories.get(id))
      .sort((a, b) => indexes.get(a.id) - indexes.get(b.id));
    if (graphMode !== "deps")
      shown
        .filter((s) => graphMode !== "people" || !associations.has(s.id))
        .slice(0, 5)
        .forEach((s) =>
          right.push(storyNode(s.id, associations.get(s.id) || s.type)),
        );
    return { left, right, shown, hiddenCount, label, center, caption, note };
  }
  function renderGraph() {
    const opts = graphOptions().filter(([, label]) =>
      strip(label).includes(strip(graphQuery.trim())),
    );
    if (!opts.some(([key]) => key === graphKey)) graphKey = opts[0]?.[0] || "";
    const d = graphData(),
      tabs =
        '<div class="graph-tabs">' +
        Object.entries(graphTabs)
          .map(([k, v]) =>
            button(
              "graph-mode",
              v,
              "choice " + (graphMode === k ? "active" : ""),
              'data-key="' + k + '" aria-pressed="' + (graphMode === k) + '"',
            ),
          )
          .join("") +
        "</div>";
    const tools =
      '<div class="graph-tools"><label class="field">检索' +
      graphTabs[graphMode] +
      '<input id="graph-query" type="search" value="' +
      esc(graphQuery) +
      '" placeholder="输入名称或标题"></label><label class="field">中心节点<select id="graph-pick">' +
      options(opts.length ? opts : [["", "无可显示的节点"]], graphKey) +
      "</select></label></div>";
    const head =
      titleBlock(
        "关系索引",
        "点击图中的人物、组织或篇目，可沿关系查阅原始证据。",
      ) +
      tabs +
      tools;
    if (!d) {
      currentList = [];
      return (
        head +
        '<div class="notice-box">' +
        (guard
          ? "为保护未读剧情，关系网只展示已读和已揭示的联系。 " +
            button("guard", "显示剧透并查看关系", "link-btn")
          : esc(
              graphQuery
                ? "没有匹配的节点，可尝试其他名称。"
                : "本版尚无这一类经核实的关系。",
            )) +
        "</div>"
      );
    }
    const col = (ns) => '<div class="net-col">' + ns.join("") + "</div>";
    const c = node(
      d.label,
      d.center + (d.caption ? " · " + d.caption : ""),
      graphMode === "deps" ? "open" : "",
      graphKey,
      "current",
    );
    const chunk = sliceStories(d.shown);
    return (
      head +
      '<div class="graph-panel"><svg aria-hidden="true" class="graph-lines"></svg><div class="net">' +
      col(d.left) +
      col([c]) +
      col(d.right) +
      '</div></div><p class="graph-foot">' +
      (d.note || "图中展示部分关联节点，相关篇目见下方列表。") +
      (d.hiddenCount ? " 另有未读关联受保护。" : "") +
      "</p>" +
      '<div class="group-heading"><h3>关联篇目</h3><span class="group-count">' +
      fmt(d.shown.length) +
      "</span></div>" +
      (chunk.length
        ? chunk.map((s) => row(s)).join("")
        : empty("尚无可显示的关联篇目。")) +
      pager(d.shown.length)
    );
  }
  function drawEdges() {
    const panel = $(".graph-panel"),
      root = $(".net");
    if (!panel || !root) return;
    const svg = panel.querySelector("svg"),
      box = panel.getBoundingClientRect(),
      cols = root.children,
      center = cols[1]?.firstElementChild?.getBoundingClientRect();
    if (!center) return;
    const line = (x, y, tx, ty) =>
      '<path d="M' +
      x.toFixed(1) +
      " " +
      y.toFixed(1) +
      " C " +
      ((x + tx) / 2).toFixed(1) +
      " " +
      y.toFixed(1) +
      " " +
      ((x + tx) / 2).toFixed(1) +
      " " +
      ty.toFixed(1) +
      " " +
      tx.toFixed(1) +
      " " +
      ty.toFixed(1) +
      '" fill="none" stroke="currentColor" stroke-width="1.4"/>';
    const cy = center.top + center.height / 2 - box.top;
    let html = "";
    for (const idx of [0, 2])
      for (const n of cols[idx].children) {
        const b = n.getBoundingClientRect();
        html += line(
          (idx ? center.right : center.left) - box.left,
          cy,
          (idx ? b.left : b.right) - box.left,
          b.top + b.height / 2 - box.top,
        );
      }
    svg.setAttribute("viewBox", "0 0 " + box.width + " " + box.height);
    svg.innerHTML = html;
  }
  window.addEventListener("resize", () => {
    if (view === "graph") requestAnimationFrame(drawEdges);
  });
  function refs(ids, label) {
    const sids = knownIds(ids);
    if (!sids.length) return "";
    const accessible = sids.filter((id) => visible(stories.get(id)));
    const links = accessible
      .map((id) =>
        button(
          "open",
          esc(stories.get(id).title),
          "",
          'data-key="' + esc(id) + '"',
        ),
      )
      .join("");
    const hiddenIds = sids.filter((id) => !visible(stories.get(id)));
    const hiddenLinks = hiddenIds
      .map((id, i) =>
        button(
          "open",
          icon("lock") +
            " 未读关联 " +
            (i + 1) +
            (stories.get(id).code ? " · " + esc(stories.get(id).code) : ""),
          "",
          'data-key="' + esc(id) + '"',
        ),
      )
      .join("");
    return (
      '<section class="dialog-section"><h3>' +
      esc(label) +
      '</h3><div class="ref-list">' +
      links +
      hiddenLinks +
      "</div></section>"
    );
  }
  function dialogHead(title, subtitle = "") {
    return (
      '<div class="dialog-head"><div>' +
      (subtitle ? '<span class="quiet">' + esc(subtitle) + "</span>" : "") +
      '<h2 id="sheet-title">' +
      esc(title) +
      "</h2></div>" +
      button("close", icon("close"), "icon-button", 'aria-label="关闭弹窗"') +
      "</div>"
    );
  }
  const para = (label, val) =>
    val
      ? '<section class="dialog-section"><h3>' +
        esc(label) +
        "</h3><p>" +
        esc(val) +
        "</p></section>"
      : "";
  const sheet = $("#sheet");
  document.addEventListener("keydown", (event) => {
    if (event.key !== "/" || event.altKey || event.ctrlKey || event.metaKey || event.isComposing ||
        sheet.open || event.target.closest("input,textarea,select,[contenteditable=true]")) return;
    event.preventDefault();
    focusSearch();
  });
  function showModal(type, body, id = "") {
    if (!sheet.open) {
      lastFocus = document.activeElement;
      const trigger = lastFocus?.closest("a[href], button[data-act]");
      returnFocusSelector = trigger?.matches("a") ? 'a[href="' + CSS.escape(trigger.getAttribute("href")) + '"]' :
        trigger?.dataset.act ? 'button[data-act="' + CSS.escape(trigger.dataset.act) + '"]' : "";
      sheet.showModal();
    }
    modal = type;
    modalId = id;
    $("#sheet-body").innerHTML = body;
  }
  function storyModal(s, keepScroll = false) {
    if (!s) return;
    const offset = sheet.scrollTop,
      shown = visible(s);
    let body =
      dialogHead(
        safeTitle(s),
        s.type + (safeGroup(s) ? " · " + safeGroup(s) : ""),
      ) +
      '<div class="tag-row">' +
      badge(s) +
      '<span class="quiet">' +
      esc(routePosition(s)) +
      "</span>" +
      (s.positionStatus
        ? '<span class="badge e-grade">定位 · ' +
          esc(s.positionStatus) +
          "</span>"
        : "") +
      (s.availability
        ? '<span class="badge e-grade">' + esc(s.availability) + "</span>"
        : "") +
      "</div>";
    const mainLinkLabel = s.released === false ? "查看开放资料" :
      s.availability === "无独立对白" ? "查看关卡资料" : "阅读本篇原文";
    body += '<div class="primary-source">' + external(s.source, mainLinkLabel) + '</div>';
    const branches = knownIds(s.branches);
    if (branches.length) {
      body += '<section class="dialog-section"><h3>可选分支（依所选路线进入）</h3>' +
        '<p>从这里可走 ' + branches.length + ' 条路线。选一条继续，另外的可以留到回看时读。</p><div class="ref-list">' +
        branches.map((id, i) => {
          const next = stories.get(id);
          const label = visible(next) ? next.title : "路线 " + (i+1) + (next.code ? " · " + next.code : "");
          return button("open", esc(label), "", 'data-key="' + esc(id) + '"');
        }).join("") + "</div></section>";
    }
    if (!shown) {
      body +=
        '<div class="access-note"><div>' +
        icon("shield") +
        " 可先读原文，回来再核对时间和人物。下方考据含本篇剧透。</div>" +
        button("reveal", "仅揭示本篇", "btn", 'data-key="' + esc(s.id) + '"') +
        "</div>";
    } else {
      body +=
        para("推荐阅读位置", s.reason || routePosition(s)) +
        para("故事内时间", unique([s.dateLabel, s.time]).join(" · ")) +
        para("叙事方式", s.mode);
      const details = [];
      if (list(s.places).length) details.push("地点　" + series(s.places));
      if (list(s.cast).length) details.push("出场　" + series(s.cast));
      body += para("场景与人物", details.join("\n"));
      const sceneRows = list(s.sceneLabels).length
        ? list(s.sceneLabels)
        : list(s.scenes)
            .map((x) =>
              [
                x.year != null
                  ? (Number(x.year) < 0
                      ? "前星塔历" + Math.abs(x.year)
                      : "星塔历" + x.year) + "年"
                  : "",
                x.date,
                x.time,
                x.place,
              ]
                .filter(Boolean)
                .join(" · "),
            )
            .filter(Boolean);
      if (sceneRows.length)
        body +=
          '<details class="scene-details"><summary>逐场时间与地点（' +
          sceneRows.length +
          "）</summary><ol>" +
          sceneRows.map((x) => "<li>" + esc(x) + "</li>").join("") +
          "</ol></details>";
      body += para("时间范围说明", s.dateScope || s.periodNote);
      if (s.summary) body += para("剧情概要", s.summary);
      if (s.evidence)
        body +=
          '<section class="dialog-section"><h3>定位依据 · ' +
          esc(s.grade || "U") +
          "</h3><blockquote>" +
          esc(s.evidence) +
          "</blockquote></section>";
      if (s.unlock) body += para("解锁条件", s.unlock);
      if (s.aliases?.length) body += para("地区名与别称", series(s.aliases));
      const relations = relationItems(s).filter((relation) => !branches.includes(relation.id)),
        relGroups = by(
          relations,
          (n) => n.label + " · " + (n.dir === "in" ? "上游节点" : "关联后继"),
        );
      for (const [key, ns] of relGroups)
        body += refs(
          ns.map((n) => n.id),
          key
            .replace("互相参照 · 关联后继", "其他参照篇目")
            .replace("互相参照 · 上游节点", "其他参照篇目")
            .replace("并行视角 · 关联后继", "分头行动的并行视角")
            .replace("并行视角 · 上游节点", "分头行动的共同起点")
            .replace("可选分支 · 关联后继", "可选分支（依所选路线进入）"),
        );
      const sources = unique([
        s.source,
        ...list(s.sources).map((x) => (typeof x === "string" ? x : x.url)),
        ...list(s.evidenceSources).map((x) =>
          typeof x === "string" ? x : x.url,
        ),
      ]).filter(safeUrl);
      if (sources.length)
        body +=
          '<section class="dialog-section"><h3>原文与资料</h3><div class="source-links">' +
          sources
            .map((u, i) => {
              const x = [...list(s.sources), ...list(s.evidenceSources)].find(
                (x) => x?.url === u,
              );
              return (
                "<p>" +
                external(
                  u,
                  guard && i > 0
                    ? "查阅对照资料 " + i
                    : x?.label || (i === 0 ? "打开本篇原文" : "查阅参考资料"),
                ) +
                "</p>"
              );
            })
            .join("") +
          "</div></section>";
    }
    body +=
      '<div class="dialog-actions"><label class="quiet">阅读状态　' +
      selectState(s) +
      '</label><div class="inline-actions">' +
      (shown && guard && status(s) !== "read"
        ? button(
            "hide-one",
            icon("lock") + " 隐藏本篇",
            "link-btn",
            'data-key="' + esc(s.id) + '"',
          )
        : "") +
      (view === "route" && s.released !== false && !list(s.branches).length &&
        routeStories.slice(indexes.get(s.id) + 1).some((item) => item.released !== false && (includeOptional || !item.optional))
        ? button("read-next", status(s) === "read" ? "推荐路线下一篇" : "标为已读，读下一篇", "btn primary") : "") +
      button("close", "返回列表", "btn") +
      "</div></div>";
    showModal("story", body, s.id);
    sheet.scrollTop = keepScroll ? offset : 0;
  }
  function progressModal(note = "") {
    const counts = stat(),
      body =
        dialogHead("我的阅读进度") +
        '<section class="dialog-section stat-grid">' +
        Object.entries(stateText)
          .map(
            ([k, l]) =>
              "<div><strong>" +
              fmt(counts[k]) +
              "</strong><span>" +
              l +
              "</span></div>",
          )
          .join("") +
        "</section>" +
        para(
          "保存位置",
          "进度会保存在当前浏览器。移动项目、换浏览器或清理浏览器数据前，可导出 JSON 备份。",
        ) +
        para(
          "恢复记录",
          "合并会保留本机独有的标记。选择整份恢复后，进度会还原为备份中的状态。",
        ) +
        '<label class="field">导入方式<select id="import-method"><option value="merge">合并备份与本机标记</option><option value="restore">用备份恢复整份进度</option></select></label>' +
        (note ? '<div class="notice-box">' + esc(note) + "</div>" : "") +
        (saveMessage
          ? '<div class="notice-box">' + esc(saveMessage) + "</div>"
          : "") +
        '<div class="dialog-actions">' +
        button("export", icon("down") + " 导出进度", "btn") +
        button("import", icon("up") + " 导入备份", "btn primary") +
        "</div>";
    showModal("progress", body);
  }
  function aboutModal() {
    const snapshot = String(meta.snapshot || "").slice(0, 12);
    showModal(
      "about",
      dialogHead("证据等级与资料来源") +
        para(
          "两条路线",
          "推荐路线兼顾初遇与信息揭示。故事时间线只呈现正文支持的日期、范围或局部先后。分支与结局按路线分别查看。",
        ) +
        '<dl class="grade-list">' +
        Object.entries(gradeText)
          .map(([k, v]) => "<dt>" + k + "</dt><dd>" + v + "</dd>")
          .join("") +
        "</dl>" +
        para(
          "资料版本",
          [
            meta.date && "资料日期 " + meta.date,
            snapshot && "档案快照 " + snapshot,
            fmt(all.length) + " 个可标记阅读单元",
          ]
            .filter(Boolean)
            .join("　"),
        ) +
        '<section class="dialog-section"><h3>资料入口</h3><p>' +
        external(
          meta.archiveUrl || "https://stellasora-archive.pages.dev/",
          "Stella Sora Archive",
        ) +
        "</p><p>" +
        external(
          "https://github.com/419bw/stellasora-archive",
          "档案库 GitHub 仓库",
        ) +
        '</p><p><a href="' + (location.hostname === "juvenile-a3.github.io" ?
          "https://github.com/Juvenile-A3/stella-sora-story-guide/blob/main/research-notes.md" : "research-notes.md") +
          '" target="_blank" rel="noopener">详细考据与未决问题</a></p></section>' +
        '<section class="dialog-section"><h3>美术与模型</h3><p>城市和塔楼为本指南生成的幻想插画。旅人头像使用官方模型自行渲染。Model: Stella Sora / 久远丶酱。原作角色与模型 © Yostar。</p><p>' +
        external("https://stellasora.global/news/2545", "官方模型与使用说明") +
        "</p></section>",
    );
  }
  let availablePhases = new Set();
  let includeOptional = false;
  function render(focusId = "") {
    const focusInput = focusId ? $("#" + focusId) : null;
    const start = focusInput?.selectionStart,
      end = focusInput?.selectionEnd;
    availablePhases = new Set(
      all.filter(visible).map((s) => s.phase || "未知"),
    );
    renderNav();
    const renderers = {
      route: renderRoute,
      time: renderTime,
      catalog: renderCatalog,
      graph: renderGraph,
    };
    $("#workspace").innerHTML =
      side() +
      '<div class="view-main" id="view-main">' +
      renderers[view]() +
      "</div>";
    if (focusId) {
      const el = $("#" + focusId);
      if (el) {
        el.focus({ preventScroll: true });
        if (typeof start === "number" && el.setSelectionRange)
          el.setSelectionRange(start, end);
      }
    }
    if (view === "graph") requestAnimationFrame(drawEdges);
  }
  function resetPage() {
    pageNo = 1;
    selected.clear();
  }
  function applyMenu(action, key) {
    if (action === "stage") {
      stage = key;
      if (
        key.startsWith("extra:") ||
        (key !== "*" && routeBuckets.get(key)?.every((s) => s.optional))
      )
        includeOptional = true;
    }
    if (action === "phase") phase = key;
    if (action === "side-type") filters.type = key === "*" ? "" : key;
    if (action === "graph-mode") {
      graphMode = key;
      graphQuery = "";
      graphKey = "";
    }
    resetPage();
    render();
    if (action === "side-type") syncCatalogAddress();
  }
  function closeDialog() {
    if (modal === "story") {
      history.replaceState(null, "", view === "catalog" ? catalogHash() : "#" + view);
    }
    sheet.close();
  }
  sheet.addEventListener("cancel", (ev) => {
    ev.preventDefault();
    closeDialog();
  });
  sheet.addEventListener("close", () => {
    if (sheet.open) return;
    modal = "";
    modalId = "";
    const origin = lastFocus?.isConnected ? lastFocus : returnFocusSelector && $(returnFocusSelector);
    if (origin) origin.focus({ preventScroll: true });
  });
  sheet.addEventListener("click", (ev) => {
    if (ev.target === sheet) {
      const b = sheet.getBoundingClientRect();
      if (
        ev.clientX < b.left ||
        ev.clientX > b.right ||
        ev.clientY < b.top ||
        ev.clientY > b.bottom
      )
        closeDialog();
    }
  });
  function openStory(id) {
    if (!stories.has(id)) return;
    if (location.hash === storyHref(id)) storyModal(stories.get(id));
    else location.hash = storyHref(id);
  }
  function readHash(initial = false) {
    const parts = location.hash.slice(1).split("?"),
      next = Object.hasOwn(tabNames, parts[0]) ? parts[0] : "route",
      params = new URLSearchParams(parts[1] || ""),
      id = params.get("story");
    let changedFilters = false;
    if (next === "catalog" && Object.keys(defaultFilter()).some((key) => params.has(key))) {
      const fromUrl = defaultFilter();
      for (const key of Object.keys(fromUrl)) fromUrl[key] = params.get(key) || "";
      changedFilters = Object.keys(fromUrl).some((key) => filters[key] !== fromUrl[key]);
      filters = fromUrl;
    }
    if (view !== next || initial || changedFilters) {
      view = next;
      resetPage();
      bulk = false;
      if (sheet.open) sheet.close();
      render();
      if (!initial) window.scrollTo({ top: 0, behavior: "instant" });
    }
    if (id && stories.has(id)) storyModal(stories.get(id));
    else if (sheet.open && modal === "story") sheet.close();
    if (id && !stories.has(id)) showNotice("这个篇目未收入当前资料版本。");
    if (!id) syncCatalogAddress();
    document.title = tabNames[view] + " · 诺瓦剧情手记";
  }
  window.addEventListener("hashchange", () => readHash());
  window.addEventListener("storage", (ev) => {
    if (ev.key !== storageKey) return;
    try {
      const next = JSON.parse(ev.newValue || "{}");
      progress = validStates(next.progress);
      guard = next.guard !== false;
      revealed.clear();
      render();
      if (modal === "story") storyModal(stories.get(modalId), true);
      if (modal === "progress") progressModal();
    } catch {
      /* Preserve the current tab when an external write is incomplete. */
    }
  });
  function focusGraph(mode, key) {
    graphMode = mode;
    graphQuery = "";
    graphKey = key;
    resetPage();
    render();
  }
  function changeGuard() {
    guard = !guard;
    revealed.clear();
    filters.person = "";
    timePerson = "";
    graphKey = "";
    resetPage();
    store();
    render();
    if (modal === "story") storyModal(stories.get(modalId), true);
    showNotice(
      guard
        ? "未读篇目的剧透保护已开启。"
        : "已显示剧情信息。可再次点击顶栏恢复保护。",
    );
  }
  function downloadProgress() {
    const file = new Blob(
      [
        JSON.stringify(
          {
            format: "stella-sora-reading-progress",
            version: 1,
            exported: new Date().toISOString(),
            snapshot: meta.snapshot,
            progress,
          },
          null,
          2,
        ),
      ],
      { type: "application/json;charset=utf-8" },
    );
    const link = document.createElement("a"),
      url = URL.createObjectURL(file);
    link.href = url;
    link.download =
      "stella-sora-progress-" + new Date().toISOString().slice(0, 10) + ".json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1200);
  }
  async function importProgress(file) {
    if (!file) return;
    try {
      if (file.size > 8 * 1024 * 1024)
        throw new Error("文件超过 8 MB，请选择进度备份。");
      const json = JSON.parse((await file.text()).replace(/^\uFEFF/, ""));
      if (
        json.format !== "stella-sora-reading-progress" ||
        json.version !== 1 ||
        !json.progress ||
        typeof json.progress !== "object" ||
        Array.isArray(json.progress)
      )
        throw new Error("请选择本指南导出的第一版进度 JSON 文件。");
      const entries = Object.entries(json.progress);
      if (
        entries.some(
          ([id, st]) =>
            !id || id.length > 1600 || !Object.hasOwn(stateText, st),
        )
      )
        throw new Error("备份包含无效状态，现有进度未改动。");
      const restore = $("#import-method")?.value === "restore";
      if (restore) progress = Object.create(null);
      let known = 0;
      for (const [id, st] of entries) {
        if (stories.has(id) || knownProgressKeys.has(id)) known++;
        writeStatus(id, st);
      }
      store();
      render();
      progressModal(
        (restore ? "已恢复 " : "已合并 ") +
          fmt(known) +
          " 个当前篇目的记录。" +
          (entries.length > known
            ? "另保留 " + fmt(entries.length - known) + " 个其他版本的标记。"
            : ""),
      );
    } catch (e) {
      progressModal(
        e instanceof SyntaxError
          ? "文件不是有效的 JSON，现有进度未改动。"
          : String(e.message),
      );
    } finally {
      $("#import").value = "";
    }
  }
  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-act]");
    if (!b || b.disabled) return;
    const { act, key } = b.dataset;
    switch (act) {
      case "guard":
        changeGuard();
        break;
      case "progress":
        progressModal();
        break;
      case "search":
        focusSearch();
        break;
      case "catalog-filters":
        catalogFiltersOpen = !catalogFiltersOpen;
        render();
        $('[data-act="catalog-filters"]').focus({preventScroll:true});
        break;
      case "read-next": {
        const nextStory = routeStories.slice(indexes.get(modalId) + 1)
          .find((item) => item.released !== false && (includeOptional || !item.optional));
        if (!nextStory || !modalId) break;
        writeStatus(modalId, "read");
        store();
        render();
        openStory(nextStory.id);
        showNotice("上一篇已标为已读。");
        break;
      }
      case "about":
        aboutModal();
        break;
      case "close":
        closeDialog();
        break;
      case "open":
        openStory(key);
        break;
      case "resume": {
        const s =
          routeStories.find((s) => s.released !== false && status(s) === "reading") ||
          routeStories.find((s) => s.released !== false && !s.optional && status(s) === "unread") ||
          routeStories.find((s) => s.released !== false && status(s) === "unread") ||
          routeStories[0];
        if (s) openStory(s.id);
        break;
      }
      case "reveal":
        revealed.add(key);
        render();
        storyModal(stories.get(key));
        break;
      case "hide-one":
        revealed.delete(key);
        render();
        storyModal(stories.get(key));
        break;
      case "stage":
      case "phase":
      case "side-type":
      case "graph-mode":
        applyMenu(act, key);
        break;
      case "prev":
      case "next":
        pageNo += act === "prev" ? -1 : 1;
        render();
        $("#view-main").scrollIntoView({ block: "start" });
        break;
      case "bulk":
        bulk = !bulk;
        selected.clear();
        render();
        break;
      case "pick-page":
        currentList
          .slice((pageNo - 1) * pageSize, pageNo * pageSize)
          .forEach((s) => selected.add(s.id));
        render();
        break;
      case "pick-all":
        currentList.forEach((s) => selected.add(s.id));
        render();
        break;
      case "clear-picks":
        selected.clear();
        render();
        break;
      case "set-many": {
        const v = $("#bulk-value").value,
          n = selected.size;
        selected.forEach((id) => writeStatus(id, v));
        selected.clear();
        store();
        render();
        showNotice("已将 " + fmt(n) + " 篇标为" + stateText[v] + "。");
        break;
      }
      case "reset-filters":
        filters = defaultFilter();
        resetPage();
        render();
        syncCatalogAddress();
        break;
      case "expand-period":
        phase = key;
        zoom = "篇目";
        resetPage();
        render();
        break;
      case "zoom":
        zoom = key;
        resetPage();
        render();
        break;
      case "graph-org":
        focusGraph("orgs", key);
        break;
      case "graph-person":
        focusGraph("people", key);
        break;
      case "export":
        downloadProgress();
        break;
      case "import":
        $("#import").click();
        break;
    }
  });
  document.addEventListener("change", (ev) => {
    const el = ev.target;
    if (el.dataset.status) {
      writeStatus(el.dataset.status, el.value);
      store();
      render();
      if (modal === "story") storyModal(stories.get(modalId), true);
      return;
    }
    if (el.dataset.menu) {
      applyMenu(el.dataset.menu, el.value);
      return;
    }
    if (el.dataset.pick) {
      if (el.checked) selected.add(el.dataset.pick);
      else selected.delete(el.dataset.pick);
      const box = $(".bulk");
      if (box) box.outerHTML = bulkControls();
      return;
    }
    if (el.dataset.filter) {
      filters[el.dataset.filter] = el.value;
      resetPage();
      render();
      syncCatalogAddress();
      return;
    }
    if (el.id === "time-person") {
      timePerson = el.value;
      resetPage();
      render();
    }
    if (el.id === "graph-pick") {
      graphKey = el.value;
      resetPage();
      render();
    }
    if (el.id === "optional") {
      includeOptional = el.checked;
      if (!includeOptional && stage !== "*" && routeBuckets.get(stage)?.every((s) => s.optional)) stage = "*";
      resetPage();
      render();
    }
    if (el.id === "import") importProgress(el.files?.[0]);
  });
  document.addEventListener("compositionend", (ev) => {
    if (["query", "graph-query"].includes(ev.target.id))
      ev.target.dispatchEvent(new Event("input", { bubbles: true }));
  });
  document.addEventListener("input", (ev) => {
    if (ev.isComposing) return;
    if (ev.target.id === "query") {
      filters.q = ev.target.value;
      resetPage();
      render("query");
      syncCatalogAddress();
    }
    if (ev.target.id === "graph-query") {
      graphQuery = ev.target.value;
      resetPage();
      render("graph-query");
    }
  });
  readHash(true);
  if (saveMessage) showNotice(saveMessage);
})();
