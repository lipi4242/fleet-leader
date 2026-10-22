"""Honnan jön a /fleet:* plugin — EGY hely, egy sorban cserélhető.

A commitolt `.claude/settings.json` mindig a publikus GitHub-repót nevezi meg,
gépfüggő útvonalat soha. Helyi forrás (pl. egy checkout) csak explicit
`--plugin-source local:<út>` kapcsolóval jöhet, és akkor is csak a nem
commitolt `.claude/settings.local.json`-ba kerül (azt a Claude Code olvassa).
"""
from __future__ import annotations
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

PUBLIC_REPO = "lipi4242/fleet-leader"   # the public repo the plugin is installed from
MARKETPLACE_NAME = "fleet-leader"       # a marketplace.json "name" mezője
PLUGIN_KEY = f"fleet@{MARKETPLACE_NAME}"

_SLUG = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def public_repo(env=None) -> str:
    """Fork/tükör: FLEET_MARKETPLACE_REPO=<owner>/<repo>. Útvonalat nem fogad el."""
    v = (os.environ if env is None else env).get("FLEET_MARKETPLACE_REPO") or ""
    return v if _SLUG.match(v) else PUBLIC_REPO


@dataclass(frozen=True)
class Source:
    committed: dict      # ami a commitolt settings.json-ba mehet (mindig github)
    local: dict | None   # ami csak a settings.local.json-ba (directory) — vagy None
    add_arg: str         # a `claude plugin marketplace add` argumentuma


def parse(spec: str | None) -> Source:
    repo = public_repo()
    committed = {"source": "github", "repo": repo}
    if not spec:
        return Source(committed, None, repo)
    if not spec.startswith("local:"):
        raise ValueError(f"ismeretlen --plugin-source: {spec!r} (csak `local:<út>`)")
    path = Path(spec[len("local:"):]).expanduser()
    if not (path / ".claude-plugin" / "marketplace.json").is_file():
        raise ValueError(f"a local forrásban nincs .claude-plugin/marketplace.json: {path}")
    p = str(path.resolve())
    return Source(committed, {"source": "directory", "path": p}, p)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text() or "{}") if path.exists() else {}


def merge_local(existing: dict, source: dict) -> dict:
    """A nem commitolt helyi beállítás: csak akkor veszünk fel forrást, ha a
    felhasználónak még nincs sajátja ehhez a marketplace-hez — azt nem írjuk felül."""
    out = json.loads(json.dumps(existing))
    out.setdefault("extraKnownMarketplaces", {}).setdefault(MARKETPLACE_NAME, {"source": source})
    return out
