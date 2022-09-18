import time
import datetime
import json
import sys
import os
import shutil
import yaml

import api
import git
import svg_card
import lang_counter
import stats

if len(sys.argv) > 1 and sys.argv[1] == "--reset" and os.path.isdir("tmp"):
    shutil.rmtree("tmp")
    exit()
elif len(sys.argv) > 2 and sys.argv[1] == "--config":
    config_file = sys.argv[2]
else:
    config_file = "config.json"

_print = print
def print(output):
    _print(datetime.datetime.now().strftime("[%Y%m%d %H:%M:%S] ") + str(output))

with open("linguist/lib/linguist/languages.yml", "r", encoding="utf-8") as stream:
    lang = yaml.safe_load(stream)

if __name__ == "__main__":
    config = json.loads(open(config_file, "r", encoding="utf-8").read())
    GIT = git.init(config["user"], config["auth"]["token"], config["auth"]["name"], config["auth"]["email"])
    API = api.init(config["user"], config["auth"]["token"])
    API.get_users()
    while True:
        print(f"pulling : {GIT.user}/{GIT.user}")
        GIT.pull()
        print("getting list of repository")
        API.get_repos()
        print("getting last commits")
        API.get_lastcommit()
        print("getting repository")
        repos_update = GIT.get_repos_by_list(API.repos_list)
        print("load last commits history")
        API.load_flc()
        print(f"new repos    : {repos_update[0]}")
        print(f"already have : {repos_update[1]}")
        print(f"deleted      : {repos_update[2]}")
        for r in repos_update[2]:
            del API.flc[r]
        for r in repos_update[0]:
            API.flc[r] = API.last_commits[r]
        update = repos_update[0]
        for r in repos_update[1]:
            if API.is_newcommits(r):
                update.append(r)
        print(f"update : {update}")
        print("save last commits history")
        lang_stats = lang_counter.load_fls()
        for r in update:
            print(f"pulling : {GIT.user}/{r}")
            GIT.pull(r)
            uid = API.users["id"]
            sha_commits = []
            print(f"getting commits log of {API.user}/{r}")
            for commit in API.commits_json[r]:
                if commit["author"]["id"] == uid:
                    sha_commits.append(commit["sha"])
            print(f"commits by ID:{uid} : {len(sha_commits)}")
            print(f"counting : {API.user}/{r}")
            lang_stats = lang_counter.get(r, GIT, lang, lang_stats, uid, sha_commits)
        print("getting total pull request")
        API.get_total_prs()
        API.get_total_commits()
        stats_old = stats.load()
        is_update = len(update) > 0
        is_update = (API.prs["open"] != stats_old["pull_requrest"]["open"]) or is_update
        is_update = (API.prs["merged"] != stats_old["pull_requrest"]["merged"]) or is_update
        is_update = (API.prs["closed"] != stats_old["pull_requrest"]["closed"]) or is_update
        is_update = (API.repos != stats_old["total_repos"]) or is_update
        is_update = (API.fork_repos != stats_old["total_fork_repos"]) or is_update
        is_update = (API.stars != stats_old["total_stars_earned"]) or is_update
        is_update = (API.forks != stats_old["total_forks_earned"]) or is_update
        is_update = (API.issues != stats_old["total_issues"]) or is_update
        is_update = (API.commits != stats_old["total_commits"]) or is_update
        if is_update:
            print("have update !")
            tmp = {
                "top_lang": stats.get_top_lang(lang_stats),
                "lang_stats": lang_stats,
                "total_stars_earned": API.stars,
                "total_commits": API.commits,
                "total_issues": API.issues,
                "total_forks_earned": API.forks,
                "total_repos": API.repos,
                "total_fork_repos": API.fork_repos,
                "pull_requrest": {
                    "open": API.prs["open"],
                    "merged": API.prs["merged"],
                    "closed": API.prs["closed"]
                }
            }
            stats.save(tmp)
            GIT.push()
        else:
            print("no update !")
        shutil.copyfile("tmp/stats", f"tmp/repos/{API.user}/{config['stats']}")
        lang_counter.save_fls(lang_stats)
        API.save_flc()
        print(f"sleeping : {config['delay']}sec")

        time.sleep(config["delay"])

