from auth import AuthMethodType
from pathlib import Path
import os

# CONSTANTS WITH CONSOLE COLORS
RED = "\033[31m"
GREEN = "\033[32m"
GREY = "\033[90m"
RESET = "\033[0m"


class Settings:
    def __init__(self, login="", method=AuthMethodType.HTTPS):
        self._login = login
        self._method = method


    # update user settings in file settings.vvcommit
    def update(self, login, method):
        m = ""
        if method == "s":
            m = "SSH"
        elif method == "h":
            m = "HTTPS"
        else:
            print(f'{RED}ERROR: Unrecognized method: {method}{RESET}')
            sys.exit(1)

        self._login = login
        self._method = method
        script_dir = Path(__file__).resolve().parent
        path = os.path.join(script_dir, "settings.vvcommit")
        with open(path, "w") as f:
            f.write(f"login: {login}\nmethod: {m}\n# THIS FILE IS GENERETED AUTOMATICALLY DO NOT CHANGE IT URSELF!\n#COMMAND TO CHANGE SETTINGS PROPERLY: vvcommit settings <login> <s/h> (stands for SSH or HTTPS)\n#TO RESTORE SETTINGS TO AN EMPTY STATE USE: vvcommit settings-remove")
        print(f'{GREEN}INFO: Successfully updated settins with name: {login}, and method {method}{RESET}')
    

        
    # reset settings to an empty state
    def reset(self):
        script_dir = Path(__file__).resolve().parent
        path = os.path.join(script_dir, "settings.vvcommit")
        with open(path, "w") as f:
            f.write(f"login: \nmethod: \n# THIS FILE IS GENERETED AUTOMATICALLY DO NOT CHANGE IT URSELF!\n#COMMAND TO CHANGE SETTINGS PROPERLY: vvcommit settings <login> <s/h> (stands for SSH or HTTPS)\n#TO RESTORE SETTINGS TO AN EMPTY STATE USE: vvcommit settings-remove")
            print(f"{GREEN}SETTINGS WERE SUCCESSFULY RESTORED!{RESET}")
    
    @property
    def method(self):
        return self._method

    @property
    def login(self):
        if self._login == "":
            return ""
        return self._login

    @login.setter
    def login(self, value):
        value = value.strip()
        self._login = value

    @method.setter
    def method(self, value: AuthMethodType):
        self._method = value
