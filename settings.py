
from auth import AuthMethodType
from pathlib import Path
import os
import sys

# CONSTANTS FOR CONSOLE COLORS
RED = "\033[31m"
GREEN = "\033[32m"
GREY = "\033[90m"
RESET = "\033[0m"

class Settings:
    def __init__(self, login="", method=AuthMethodType.HTTPS):
        self._login = login
        self._method = method
    
    def update(self, login, method):
        if isinstance(method, str):
            if method == "s":
                method = AuthMethodType.SSH
            elif method == "h":
                method = AuthMethodType.HTTPS
            else:
                raise ValueError(f"Unrecognized method: {method}")

        if not isinstance(method, AuthMethodType):
            raise TypeError("method must be AuthMethodType")

        self._login = login
        self._method = method

        script_dir = Path(__file__).resolve().parent
        path = script_dir / "settings.vvcommit"

        with open(path, "w", encoding="utf-8") as f:
            f.write(
                f"login: {login}\n"
                f"method: {method.name}\n"
                "# THIS FILE IS GENERATED AUTOMATICALLY (change it only with vvcommit settings <login> <method>)\n"
            )

        print(
            f"{GREEN}INFO: Successfully updated settings "
            f"with name: {login}, and method {method.name}{RESET}"
        )


    # reset settings to an empty state
    def reset(self):
        script_dir = Path(__file__).resolve().parent
        path = os.path.join(script_dir, "settings.vvcommit")
        with open(path, "w") as f:
            f.write(
                    f"login: \nmethod: \n"
                    "# THIS FILE IS GENERATED AUTOMATICALLY (change it only with vvcommit settings <login> <method>)\n"
                    )
            print(f"{GREEN}SETTINGS WERE SUCCESSFULY RESTORED!{RESET}")

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value: AuthMethodType):
        self._method = value

    @property
    def login(self):
        if self._login == "":
            return ""
        return self._login

    @login.setter
    def login(self, value):
        value = value.strip()
        self._login = value
