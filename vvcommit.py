#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil
import urllib.request
from enum import Enum

# CONSTANTS WITH CONSOLE COLORS
RED = "\033[31m"
GREEN = "\033[32m"
GREY = "\033[90m"
RESET = "\033[0m"

# OTHER CONSTANTS
BRANCH_TYPES = {
        "f": "feature",
        "h": "hotfix",
        "e": "empty",
        "b": "bugfix",
        }

class AuthMethodType(Enum):
    HTTPS = 1
    SSH = 2

# ----- IMPLEMENTATIONS ------
# UPDATE FUNCTION
# With this function you can get newest version of script from github with only 1 command
# also it has --no-backup flag if you dont want to save backup with older version
def update(flag: str) -> None:
    url = "https://raw.githubusercontent.com/Vadim-Seleznov/vvcommit/main/vvcommit.py"
    script_path = os.path.realpath(sys.argv[0])
    backup_path = script_path + ".bak"

    print("Starting update...")

    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")

        if flag == "backup":
            shutil.copy2(script_path, backup_path)
            print(f"{GREY}Backup created at: {backup_path}{RESET}")

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(data)

        print(f"{GREEN}Update completed successfully!{RESET}")
    except Exception as e:
        print(f"{RED}ERROR Update failed {RESET}: {e}")
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, script_path)
            print(f"{GREEN}Restored backup version.{RESET}")
        sys.exit(1)

    sys.exit(0)

# HELP FUNCTION TO PRINT TUTORIAL FOR REQUESTS IN TERMINAL
def help() -> None:
    print(f"{GREY}--------------------VV HELP----------{RESET}")
    print(f"{RED}Request options:{RESET}")
    print(f"{GREEN}curr - git commit and push into current branch{RESET}")
    print(f"{GREEN}switch - switches current git auth method HTTPS->SSH and SSH->HTTPS{RESET}")
    print(f"{GREEN}comm - git commit into current branch without pushing{RESET}")
    print(f"{GREEN}cbranch - git commit and push into specific branch{RESET}")
    print(f"{GREEN}pull - git pull or git pull origin \"branch-name\" if you provide an argument (python ./vvcommit.py pull (optional branch name)){RESET}")
    print(f"{GREEN}ignore \"elements\"- adding files into .gitignore {RESET}")
    print(f"{GREEN}ignore -\"elements\" --restore - to restore files from .gitignore{RESET}")
    print(f"{GREEN}branch-create - to create and switch into new branch{RESET}")
    print(f"{GREEN}branch-end - merge stuff from specific branch and (optional) delete it{RESET}")
    print(f"{GREEN}init - to init github repo in current directory from scratch with github-login and repo-name{RESET}")
    print(f"{GREEN}push-ex - pushing stuff into existing github repo using github-login and repo-name{RESET}")
    print(f"{GREEN}update - for getting newest version of tool from github! (--no-backup for not creating .bak file){RESET}")
    print(f"{GREEN}If you use branch request you should give extra argument with branch name{RESET}")
    print(f"{GREEN}EXAMPLE:{RESET} python ./vvcommit.py branch \"main\" \"small fix\"")
    sys.exit(0)

# THIS FUNCTION IS FOR PRINTING USAGE OF ANY REQUEST
def usage(message: str) -> None:
    print(f'{RED}ERROR{RESET}: {GREY}usage: python ./vvcommit.py {message}{RESET}')
    sys.exit(1)

# ADD AND COMMIT + PUSH STUFF INTO CURRENT BRANCH WITH SIMPLE COMMAND
def commit_curr(commit_message: str) -> None:
    subprocess.run(["git", "add", "."])

    result = subprocess.run(["git", "commit", "-m", commit_message])
    if result.returncode != 0:
        print(f"{RED}Commit failed!{RESET}")
        sys.exit(1)
    subprocess.run(["git", "push"])

    print(f'{GREEN}Successful commit{RESET}: {commit_message}')

    sys.exit(0)

# ADD + COMMIT + PUSH STUFF INTO SPECIFIC BRANCH
def commit_branch(branch: str, commit_message) -> None:
    subprocess.run(["git", "add", "."])

    result = subprocess.run(["git", "commit", "-m", commit_message])
    if result.returncode != 0:
        print(f"{RED}Commit failed!{RESET}")
        sys.exit(1)

    subprocess.run(["git", "push", "origin", branch])

    print(f'{GREEN}Successful commit: {commit_message} into branch: {branch}{RESET}')

    sys.exit(0)

# ADD + COMMIT INTO CURRENT BRANCH WITHOUT PUSH
def commit(commit_message: str) -> None:
    subprocess.run(["git", "add", "."])

    result = subprocess.run(["git", "commit", "-m", commit_message])
    if result.returncode != 0:
        print(f"{RED}Commit failed!{RESET}")
        sys.exit(1)

    print(f'{GREEN}Successful commit: {commit_message}{RESET}')

    sys.exit(0)

# PULL STUFF FROM CURRENT OR SPECIFIC BRANCH
def pull(branch: str = "none") -> None:
    if branch == "none":
        subprocess.run(["git", "pull"])
    else:
        subprocess.run(["git", "pull", "origin", branch])

    sys.exit(0)

# INIT GIT REPO ABSOLUTELY FROM SCRATCH
# to use it just go to github website create new repo
# then use init command with yours username + repo-name
def init(login: str, repo: str) -> None:
    subprocess.run(["git", "init", "."])
    subprocess.run(["git", "add", "."])
    result = subprocess.run(["git", "commit", "-m", "Initial commit"])
    if result.returncode != 0:
        print(f"{RED}Commit failed!{RESET}")
        sys.exit(1)
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "remote", "add", "origin", f'https://github.com/{login}/{repo}.git'])
    subprocess.run(["git", "push", "-u", "origin", "main"])

    sys.exit(0)

# PUSH STUFF INTO EXISTING GITHUB REPO (also using username and repo-name)
def push_ex(login: str, repo: str) -> None:
    subprocess.run(["git", "remote", "add", "origin", f'https://github.com/{login}/{repo}.git'])
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "push", "-u", "origin", "main"])

    sys.exit(0)

# IGNORE SOME FILES/DIRS 
def ignore(paths: str) -> None:
    print(f"{GREY}Ignoring: {paths}{RESET}")

    try:
        path = './.gitignore'
        elements: list = paths.split(" ")
        
        with open(path, "a") as f:
            for el in elements:
                f.write(f'{el}\n')
        
        for el in elements:
            if os.path.isdir(el):
                subprocess.run(["git", "rm", "-r", "--cached", el])
            else:
                subprocess.run(["git", "rm", "--cached", el])
        
        print(f"{GREEN}Added {elements} to .gitignore successfully!{RESET}")
        print(f"{GREEN}Now committing and pushing...{RESET}")
        
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Ignored: {', '.join(elements)}"])
        subprocess.run(["git", "push"])
        
        sys.exit(0)
    except Exception as e:
        print(f"{RED}ERROR:{RESET} {e}")
        sys.exit(1)

# BACKUP FUNCTION FOR ignore()
def restore_ignore(paths: str) -> None:
    try:
        print(f"{GREY}Restore script started successfully{RESET}")
        path = "./.gitignore"
        elements: list = paths.split(" ")
        
        with open(path, "r") as f:
            print(f"{GREY}Reading from .gitignore{RESET}")
            lines = f.readlines()
        
        with open(path, "w") as new_file:
            for line in lines:
                if line.strip() not in elements:
                    new_file.write(line)
        
        print(f"{GREEN}Successfully removed from .gitignore: {elements}!{RESET}")
        print(f"{GREY}Trying to add files...{RESET}")
        
        for el in elements:
            subprocess.run(["git", "add", "-f", el])
        
        subprocess.run(["git", "add", ".gitignore"])
        print(f"{GREEN}Successfully added! Now committing and pushing...{RESET}")
        
        subprocess.run(["git", "commit", "-m", f"Restored: {', '.join(elements)}"])
        subprocess.run(["git", "push"])
        
        sys.exit(0)
    except Exception as e:
        print(f"{RED}ERROR:{RESET} {e}")
        sys.exit(1)

# FUNCTION FOR CREATING A NEW BRANCH AND SWITCHING INTO
def branch_create(name: str, branch_type: str, user_option: str = "") -> None:
    if branch_type == "c":
        if not user_option:
            usage("branch-create c option-name branch-name")
        option = user_option
    else:
        if branch_type not in BRANCH_TYPES:
            print(f'{RED}ERROR:{RESET} there is no such branch type option: {branch_type}')
            usage("branch-create (f, h, b or c) name")

        option = BRANCH_TYPES[branch_type]
    if option != "empty":
        full_name = f"{option}/{name}"
    else:
        full_name = name

    subprocess.run(["git", "switch", "main"])
    subprocess.run(["git", "pull"])
    subprocess.run(["git", "switch", "-c", full_name])

    print(f'{GREEN}SUCCESSFULLY CREATED AND SWITCHED INTO: {full_name}{RESET}')
    sys.exit(0)

# FUNCTION TO MERGE ALL STUFF FROM SPECIFIC BRANCH INTO MAIN AND (OPTIONAL) DELETE THIS BRANCH
def branch_end(name: str, delete: bool = False, remote: bool = False)-> None:
    print(f'{GREY}Trying to find branch: {name}{RESET}')
    result = subprocess.run(["git", "branch"], capture_output=True, text=True)
    branches = result.stdout.splitlines()

    branches = [b.strip().lstrip("* ").strip() for b in branches]

    target_branch = next((b for b in branches if b.endswith(name)), None)

    if not target_branch:
        print(f'{RED}ERROR:{RESET} there is no such branch!: {name}')
        sys.exit(1)

    print(f"{GREEN}BRANCH: {target_branch} was found{RESET}")
    subprocess.run(["git", "add", "."])

    subprocess.run(["git", "commit", "-m", f'end up with branch: {name}'])

    subprocess.run(["git", "switch", "main"])
    subprocess.run(["git", "pull"])

    subprocess.run(["git", "merge", target_branch])

    if delete:
        subprocess.run(["git", "branch", "-d", target_branch])
    
        if remote:
            subprocess.run(["git", "push", "origin", "--delete", target_branch])

    subprocess.run(["git", "push"])

    sys.exit(0)

# find github login + repo name from: git remote -v
# Your_Name/awesome_repo.git
def find_base(url: str) -> str:
    url = url.strip()
    
    if url.startswith("https://github.com/"):
        base = url[len("https://github.com/"):]
    elif url.startswith("git@github.com:"):
        base = url[len("git@github.com:"):]
    else:
        raise ValueError(f"Unknown GitHub URL format: {url}")

    return base

# helper function for switch_methods
def switch(url: str, method: AuthMethodType):
    BASE = find_base(url)

    if method == AuthMethodType.HTTPS:
        full = f"git@github.com:{BASE}"
    else:
        full = f"https://github.com/{BASE}"

    subprocess.run(["git", "remote", "set-url", "origin", full])

# FUNCTION THAT SWITCHES AUTH METHODS: SSH->HTTPS and reversed
def switch_methods() -> None:
    print(f'{GREY}Detecting current method..{RESET}')
    
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True
    )
    
    url = result.stdout.strip()

    if url.startswith("https"):
        print(f'{GREEN}METHOD IS: HTTPS{RESET}')
        switch(url, AuthMethodType.HTTPS)
        print(f"{GREEN}SUCCESS! Now auth method is: SSH{RESET}")
        
    elif url.startswith("git@"):
        print(f'{GREEN}METHOD IS: SSH{RESET}')
        switch(url, AuthMethodType.SSH)
        print(f"{GREEN}SUCCESS! Now auth method is: HTTPS{RESET}")
        
    else:
        print(f'{RED}ERROR: Unrecognized method for: {url}{RESET}')

    sys.exit(0)


# ---- HANDLERS -----
def handle_switch():
    switch_methods()

def handle_com():
    if len(sys.argv) != 3:
        usage("com commit-message")
    commit(sys.argv[2])

def handle_curr():
    if len(sys.argv) < 3:
        usage("curr commit-message")
    commit_curr(sys.argv[2])

def handle_cbranch():
    if len(sys.argv) < 4:
        usage("cbranch branch-name commit-message")
    commit_branch(sys.argv[2], sys.argv[3])

def handle_pull():
    if len(sys.argv) >= 3:
        pull(sys.argv[2])
    else:
        pull()

def handle_init():
    if len(sys.argv) != 4:
        usage("init github-login repo-name")
    init(sys.argv[2], sys.argv[3])

def handle_push_ex():
    if len(sys.argv) != 4:
        usage("push-ex github-login repo-name")
    push_ex(sys.argv[2], sys.argv[3])

def handle_ignore():
    if len(sys.argv) == 3:
        ignore(sys.argv[2])
    elif len(sys.argv) == 4:
        if sys.argv[3] == "--restore":
            restore_ignore(sys.argv[2])
        else:
            help()
    else:
        print(f'Wrong command: {sys.argv}')
        help()

def handle_update():
    if len(sys.argv) >= 3:
        if sys.argv[2] == "--no-backup":
            update("no-backup")
        else:
            print(f'There is no such flag: {sys.argv[2]}')
            help()
    update("with-backup")

def handle_branch_create():
    if len(sys.argv) < 4:
        usage("branch-create (f, b, h or c) name")
    if sys.argv[2] == "c":
        if len(sys.argv) != 5:
            usage("branch-create c option-name branch-name")
        branch_create(sys.argv[4], "c", sys.argv[3])
    else:
        branch_create(sys.argv[3], sys.argv[2])

def handle_branch_end():
    if len(sys.argv) < 3:
        usage("branch-end (delete optional) (remote optional) name (without prefix)")
    if "delete" in sys.argv and "remote" in sys.argv:
        if len(sys.argv) != 5:
            usage("branch-end delete remote name (without prefix)")
        branch_end(sys.argv[4], True, True)
    elif "delete" in sys.argv:
        if len(sys.argv) != 4:
            usage("branch-end delete name (without prefix)")
        branch_end(sys.argv[3], True, False)
    else:
        if len(sys.argv) != 3:
            usage("branch-end name (without prefix)")
        branch_end(sys.argv[2], False, False)


# REQUESTS MAP
REQUESTS = {
    "switch":        handle_switch,
    "com":           handle_com,
    "curr":          handle_curr,
    "cbranch":       handle_cbranch,
    "pull":          handle_pull,
    "init":          handle_init,
    "push-ex":       handle_push_ex,
    "ignore":        handle_ignore,
    "update":        handle_update,
    "branch-create": handle_branch_create,
    "branch-end":    handle_branch_end,
    "help":          help,
}

# MAIN FUNCTION
def main() -> None:
    print(f"{GREEN}Welcome from vvcommit!{RESET}")

    if len(sys.argv) < 2:
        usage("request")

    request = sys.argv[1]

    handler = REQUESTS.get(request)
    if handler:
        handler()
    else:
        print(f"{RED}ERROR:{RESET} no such request!")
        help()

if __name__ == "__main__":
    main()