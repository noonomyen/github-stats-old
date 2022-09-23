import json
from os.path import isfile

def get_top_lang(lang_stats):
    top = []
    total = 0
    for lang in lang_stats:
        total += lang_stats[lang]["size"]
        top.append([lang, lang_stats[lang]["size"]])
    top = sorted(top, key=lambda x: x[1], reverse=True)
    for i in range(len(top)):
        top[i].append((top[i][1] / total) * 100)
    return top

def load():
    if not isfile("tmp/stats"):
        tmp = {
            "top_lang": [],
            "lang_stats": {},
            "total_stars_earned": 0,
            "total_commits": 0,
            "total_issues": 0,
            "total_forks_earned": 0,
            "total_repos": 0,
            "total_forks_repos": 0,
            "pull_request": {
                "open": 0,
                "merged": 0,
                "closed": 0
            }
        }
        save(tmp)
        return tmp
    else:
        return json.loads(open("tmp/stats", "r", encoding="utf-8").read())

def save(stats):
    open("tmp/stats", "w", encoding="utf-8").write(json.dumps(stats, indent=4))

