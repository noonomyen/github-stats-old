import json
from os import mkdir, rmdir
from os.path import isdir, isfile

from requests import get

class init:
    def __init__(self, user, token):
        self.user = user
        self.token = token
        self.headers = {"Authorization": "Bearer " + self.token}
        if not isdir("tmp"):
            mkdir("tmp")

    def get_users(self):
        res = get(f"https://api.github.com/users/{self.user}", headers=self.headers)
        if res.status_code == 200:
            self.request_fail = False
            self.users = res.json()
        else:
            self.request_fail = True

    def get_total_prs(self):
        res_open = get(f"https://api.github.com/search/issues?q=author:{self.user}%20type:pr%20is:open", headers=self.headers)
        res_closed = get(f"https://api.github.com/search/issues?q=author:{self.user}%20type:pr%20is:closed", headers=self.headers)
        res_merged = get(f"https://api.github.com/search/issues?q=author:{self.user}%20type:pr%20is:merged", headers=self.headers)
        if res_open.status_code == 200 and res_closed.status_code == 200 and res_merged.status_code == 200:
            self.request_fail = False
            self.prs = {
                "open": res_open.json()["total_count"],
                "merged": res_merged.json()["total_count"],
                "closed": res_closed.json()["total_count"]
            }
        else:
            self.request_fail = True

    def get_total_commits(self):
        res = get(f"https://api.github.com/search/commits?q=author:{self.user}", headers=self.headers)
        if res.status_code == 200:
            self.request_fail = False
            self.commits = res.json()["total_count"]
        else:
            self.request_fail = True

    def get_repos(self):
        res = get(f"https://api.github.com/users/{self.user}/repos", headers=self.headers)
        if res.status_code == 200:
            self.request_fail = False
            self.repos_json = res.json()
            self.repos = len(self.repos_json)
            self.forks_repos = 0
            self.stars = 0
            self.forks = 0
            self.issues = 0
            self.repos_list = []
            for i in range(self.repos):
                if self.repos_json[i]["fork"]:
                    self.forks_repos += 1
                if self.repos_json[i]["name"] != self.user:
                    self.repos_list.append(self.repos_json[i]["name"])
                self.stars += self.repos_json[i]["stargazers_count"]
                self.forks += self.repos_json[i]["forks"]
                self.issues += self.repos_json[i]["open_issues"]
        else:
            self.request_fail = True

    def get_lastcommit(self, page=2):
        self.last_commits = {}
        self.commits_json = {}
        tmp = []
        for name in self.repos_list:
            for i in range(page):
                res = get(f"https://api.github.com/repos/{self.user}/{name}/commits", headers=self.headers)
                if res.status_code == 200:
                    self.request_fail = False
                    res_json = res.json()
                    if len(res_json) != 0:
                        if i > 0:
                            self.commits_json[name] += res_json
                        else:
                            self.commits_json[name] = res_json
                            self.last_commits[name] = self.commits_json[name][0]["sha"]
                            tmp.append(name)
                    else:
                        break
                else:
                    self.request_fail = True
        self.repos_list = tmp

    def load_flc(self):
        if not isfile("tmp/last_commits"):
            open("tmp/last_commits", "w", encoding="utf-8").write("{}")
            self.flc = json.loads("{}")
        else:
            self.flc = json.loads(open("tmp/last_commits", "r", encoding="utf-8").read())

    def save_flc(self):
        open("tmp/last_commits", "w", encoding="utf-8").write(json.dumps(self.flc, indent=4))

    def is_newcommits(self, repo):
        try:
            if self.flc[repo] == self.last_commits[repo]:
                return False
            else:
                self.flc[repo] = self.last_commits[repo]
                return True
        except KeyError:
            self.flc[repo] = self.last_commits[repo]
            return True


