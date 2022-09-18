import json
from os import chdir, getcwd
from os.path import isfile
from subprocess import run

def get(repo_name, GIT, lang, lang_stats, uid, sha_commits):
    wd = getcwd()
    chdir(f"tmp/repos/{repo_name}")
    gl = json.loads(str(run(["github-linguist", "--breakdown", "--json"], capture_output=True).stdout.decode("utf-8")))
    for l in gl:
        if not l in lang_stats:
            lang_stats[l] = {
                "size": 0,
                "full_size": 0,
                "percent": 0,
                "color": lang[l]["color"]
            }
        for file in gl[l]["files"]:
            _ = GIT.get_size_by_author(file, uid, sha_commits)
            lang_stats[l]["size"] += _[0]
            lang_stats[l]["full_size"] += _[1]
        lang_stats[l]["percent"] = (lang_stats[l]["size"] / lang_stats[l]["full_size"]) * 100
    chdir(wd)

    return lang_stats

def load_fls():
    if not isfile("tmp/lang_stats"):
        save_fls({})
        return {}
    else:
        return json.loads(open("tmp/lang_stats", "r", encoding="utf-8").read())

def save_fls(lang_stats):
    open("tmp/lang_stats", "w", encoding="utf-8").write(json.dumps(lang_stats, indent=4))

