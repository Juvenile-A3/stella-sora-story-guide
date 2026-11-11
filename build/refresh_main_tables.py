"""Import the small game tables that the Archive reads at website build time.

Run with the Archive checkout as the first argument. Only public, pinned tables
are fetched. The generated supplement is sufficient for subsequently offline builds.
"""
import json
import sys
import urllib.request
from pathlib import Path


def collect(revision, read):
    stories = read("bin/ActivityStory")
    chapter_defs = read("bin/ActivityStoryChapter")
    labels = read("language/zh_CN/ActivityStoryChapter")
    titles = read("language/zh_CN/ActivityStory")
    conditions = read("bin/ActivityStoryCondition")
    main_conditions = read("bin/StoryCondition")
    return {
        "upstreamCommit": revision,
        "eventPeriods": {
            str(r["ChapterId"]): {
                "time": labels.get(r.get("StoryTime"), ""),
                "title": labels.get(r.get("Title"), ""),
                "key": r.get("StoryTime"),
                "unlockChapterTableId": r.get("PrevChapterId"),
            }
            for r in chapter_defs.values()
        },
        "eventNodes": [
            {
                "id": r["Id"], "group": r["ChapterId"],
                "code": titles.get(r.get("Index"), ""),
                "title": titles.get(r.get("Title"), ""),
                "script": bool(r.get("AvgLuaName")),
                "parents": [*cond.get("ActivityStoryId_a", []), *cond.get("ActivityStoryId_b", [])],
            }
            for r in stories.values()
            for cond in [conditions.get(str(r.get("ConditionId",r["Id"])), {})]
        ],
        "mainConditions": {
            r["ConditionId"]: {
                "parents": [*r.get("StoryId_a", []), *r.get("StoryId_b", [])],
                "evidence": [*r.get("EvIds_a", []), *r.get("EvIds_b", [])],
            }
            for r in main_conditions.values() if r.get("ConditionId")
        },
    }


def refresh(root):
    revision = json.loads((root/".upstream_sync_state.json").read_text(encoding="utf-8"))["stella_sora_data_commit"]
    def read(name):
        url = f"https://raw.githubusercontent.com/AutumnVN/StellaSoraData/{revision}/CN/{name}.json"
        with urllib.request.urlopen(url, timeout=45) as response:
            return json.load(response)
    out = Path(__file__).with_name("main-event-tables.json")
    out.write_text(json.dumps(collect(revision, read), ensure_ascii=False, indent=1)+"\n",encoding="utf-8")


if __name__ == "__main__":
    refresh(Path(sys.argv[1]))
