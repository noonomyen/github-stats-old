from os import system, chdir, mkdir, getcwd, listdir, rmdir
from os.path import isdir, isfile
from datetime import datetime
from subprocess import run
from shutil import rmtree

class init:
    def __init__(self, user, token, name, email):
        self.user = user
        self.token = token
        self.name = name
        self.email = email
        self.url = f"https://{self.token}@github.com/{self.user}/{self.user}.git"
        self.dir = f"tmp/repos/{user}"
        self.working_dir = getcwd()
        self.file_list = []
        if not isdir("tmp"):
            mkdir("tmp")
        if not isdir("tmp/repos"):
            mkdir("tmp/repos")
        if not isdir(f"tmp/repos/{self.user}"):
            chdir(f"tmp/repos")
            system(f"git clone {self.url}")
            chdir(self.working_dir)

    def pull(self, name=None):
        if not name:
            name = self.user
        chdir(f"tmp/repos/{name}")
        system("git pull")
        chdir(self.working_dir)

    def push(self):
        chdir(self.dir)
        dt = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        system(f"git config user.name \"{self.name}\"")
        system(f"git config user.email \"{self.email}\"")
        system("git add .")
        system(f"git commit -m \"{dt}\"")
        system(f"git push")
        chdir(self.working_dir)

    def git_ls_file(self, dir=None):
        chdir(self.dir)
        self.git_lsfile = run(["git", "ls-files"], capture_output=True).stdout.decode("utf-8").split("\n")[:-1]
        chdir(self.working_dir)

    def get_size_by_author(self, file, uid, sha_commits):
        output = run(["git", "blame", file], capture_output=True).stdout.decode("utf-8").split("\n")[:-1]
        size = 0
        file_size = 0
        for line in output:
            state = 0
            line = line.split(" ")
            if line[0][0] == "^":
                sha = line[0][1:]
            else:
                sha = line[0]
            len_sha = len(sha)
            is_author = False
            for _ in sha_commits:
                if _[:len_sha] == sha:
                    is_author = True
                    break
            for _ in line:
                if state == 1:
                    len_ = len(_)
                    file_size += len_
                    if is_author:
                        size += len_
                elif state == 0 and len(_) != 0 and _[-1] == ")":
                    state = 1
        return size, file_size

    def get_repos_by_list(self, repos_list):
        chdir("tmp/repos")
        tmp = [[], [], []]
        for name in repos_list:
            if not isdir(name):
                tmp[0].append(name)
        removed = []
        for local_repos in listdir():
            if local_repos == self.user:
                continue
            for name in repos_list:
                if local_repos == name:
                    tmp[1].append(name)
                    break
            else:
                tmp[2].append(local_repos)
                rmtree(local_repos)
        for name in tmp[0]:
            system(f"git clone https://github.com/{self.user}/{name}")
        chdir(self.working_dir)
        return tmp

