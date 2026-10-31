"""A titok-kapu kód- és környezet-szabályai (titok_olvas.py használja).

    code(text, cwd, lel)   értelmezőnek adott kód (-c, -e, heredoc): környezet-kiírás, vagy titokra
                           mutató szövegliterál (út, vagy kulcsfájl-név mint ".env")
    envdump(name, args)    a parancs kiírja-e a környezetet: bare env, printenv, set, export -p,
                           ps e/eww, systemctl … show-environment
"""
import os
import re

from titok_minta import name_hit, secret
from vedett_ut import STRINGS

PROC = re.compile(r"/proc/[^\s'\"]*/environ")
ENVDUMP = re.compile(r"/proc/[^\s'\"]*/environ|\bprint\(\s*(dict\()?os\.environ\s*\)?\)|"
                     r"json\.dumps\(\s*(dict\()?os\.environ|JSON\.stringify\(\s*process\.env\s*\)|"
                     r"console\.log\(\s*process\.env\s*\)|os\.environ\.items\(\)")


def code(text, cwd, lel):
    """Értelmezőnek adott kód: környezet-kiírás, vagy titokra mutató szövegliterál."""
    if ENVDUMP.search(text):
        return "környezet kiírása"
    for m in STRINGS.finditer(text):
        lit = next(g for g in m.groups() if g is not None)
        if "\n" in lit or not lit.strip():
            continue
        if "/" in lit or lit.startswith("~"):
            why = secret(lit, cwd, lel)
            if why:
                return why
        elif name_hit(os.path.basename(lit)):
            return "kulcsfájl-név a kódban"
    return None


def envdump(name, args):
    if name == "env":
        rest, skip = [], False
        for a in args:
            if skip:
                skip = False
            elif a in ("-u", "--unset", "-C", "--chdir", "-S"):
                skip = True
            elif not (a.startswith("-") or re.match(r"^\w+=", a)):
                rest.append(a)
        return None if rest else "környezet kiírása (env)"
    if name == "printenv" or (name == "set" and not args) or (name in ("export", "declare") and
                                                            (not args or "-p" in args or "-x" in args)):
        return "környezet kiírása (%s)" % name
    if name == "ps" and any(not a.startswith("-") and "e" in a for a in args):
        return "környezet kiírása (ps e)"
    if name in ("systemctl", "launchctl") and any("environment" in a.lower() for a in args):
        return "környezet kiírása (%s)" % name
    return None
