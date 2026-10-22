"""Hermetikus tesztfutás: a valódi HOME nem írható célpont.

Minden tesztmodul ELSŐ importja (a `fleet` előtt), mert a `fleet` több
útvonala importkor számolódik (`CONFIG_DIR`, `install.UNIT_DIR`,
`reconcile.STATE_DIR`, …). Az első import a teljes futásra tmp-re állítja a
HOME-ot és az XDG_CONFIG_HOME-ot, és lefényképezi a valódi (indulás előtti)
HOME `.config/fleet` fáját — a `test_zz_hermetic_guard` ezzel veti össze.

2026-10-18: a Mac valódi `~/.config/fleet/registry`-je egy tesztből jött
létre, egy tmp `registry.d`-re mutatva.
"""
from __future__ import annotations
import atexit
import os
import shutil
import tempfile
from pathlib import Path

REAL_HOME = Path(os.environ.get("_FLEET_TEST_REAL_HOME") or os.path.expanduser("~")).resolve()
os.environ["_FLEET_TEST_REAL_HOME"] = str(REAL_HOME)


def snapshot(root: Path) -> dict[str, tuple[int, int]]:
    """Útvonal → (méret, mtime_ns) a `root` alatt; csak olvas."""
    out = {}
    for p in sorted(root.rglob("*")) if root.is_dir() else []:
        try:
            st = p.lstat()
        except OSError:
            continue
        out[str(p.relative_to(root))] = (st.st_size, st.st_mtime_ns)
    return out


GUARDED = REAL_HOME / ".config" / "fleet"
BEFORE = snapshot(GUARDED)

if not os.environ.get("_FLEET_TEST_HOME"):
    _tmp = tempfile.mkdtemp(prefix="fleet-test-home-")
    atexit.register(shutil.rmtree, _tmp, True)
    os.environ["_FLEET_TEST_HOME"] = _tmp
TEST_HOME = Path(os.environ["_FLEET_TEST_HOME"]).resolve()
os.environ["HOME"] = str(TEST_HOME)
os.environ["XDG_CONFIG_HOME"] = str(TEST_HOME / ".config")
