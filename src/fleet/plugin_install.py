"""A /fleet:* plugin telepítése az ágens fiókjába, a claude saját CLI-jével.

A `fleet join` a repó settings.json-jába csak deklarálja a marketplace-t; a
tényleges telepítés itt történik, nem-interaktívan, hogy egy hiba szövegesen
látszódjon (és ne egy TUI-ablak álljon a pane-ben). Nem blokkol: a plugin
kényelmi réteg, az ágens nélküle is fut — a hiba egy érthető megjegyzés.
"""
from __future__ import annotations
from pathlib import Path

from fleet import claude_auth
from fleet.plugin_source import PLUGIN_KEY, parse

_PRIVATE_HINTS = ("not found", "authentication", "could not read username", "permission denied",
                  "repository not found", "403", "401")


def _ok(r) -> bool:
    text = ((r.stdout or "") + (r.stderr or "")).lower()
    return r.returncode == 0 or "already" in text


def _why(r, repo: str) -> str:
    text = ((r.stdout or "") + (r.stderr or "")).strip()
    last = text.splitlines()[-1] if text else f"kód {r.returncode}"
    if any(h in text.lower() for h in _PRIVATE_HINTS):
        return (f"a {repo} nem érhető el ({last}) — privát repó? Ezen a gépen git-hitelesítés kell "
                f"hozzá (`gh auth login` + `gh auth setup-git`), vagy FLEET_MARKETPLACE_REPO=<fork>")
    return last


def install_plugin(entry: dict, *, claude_bin: Path, home: Path, run=claude_auth.run_env,
                   plugin_source: str | None = None) -> dict:
    """{"ok": bool, "note": str} — sosem dob."""
    env = claude_auth.unit_env(entry, home)
    repo = parse(plugin_source).add_arg
    r = run([str(claude_bin), "plugin", "marketplace", "add", repo], env)
    if not _ok(r):
        return {"ok": False, "note": f"plugin: NEM települt — {_why(r, repo)}; az ágens enélkül is fut"}
    r = run([str(claude_bin), "plugin", "install", PLUGIN_KEY], env)
    if not _ok(r):
        return {"ok": False, "note": f"plugin: NEM települt ({PLUGIN_KEY}) — {_why(r, repo)}; az ágens enélkül is fut"}
    return {"ok": True, "note": f"plugin: {PLUGIN_KEY} telepítve ({repo})"}
