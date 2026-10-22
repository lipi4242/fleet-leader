"""Őr: a tesztfutás nem ír a valódi HOME `.config/fleet` alá.

A `zz` előtag miatt a `unittest discover` utolsónak futtatja, így a teljes
futás alatti változást látja. A `_hermetic` nélkül (vagy ha egy útvonal
importkor a valódi HOME-ból számolódik) piros."""
from __future__ import annotations
import _hermetic  # noqa: F401  (az első import: HOME → tmp)
import sys
import unittest
from pathlib import Path

import pytest  # noqa: F401  (repo konvenció: unittest és pytest alatt is fut)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import fleet  # noqa: E402


def _under(p: Path, root: Path) -> bool:
    p = Path(p).resolve()
    return p == root or root in p.parents


class TestHermeticGuard(unittest.TestCase):
    def test_real_home_config_fleet_unchanged(self):
        after = _hermetic.snapshot(_hermetic.GUARDED)
        changed = sorted(k for k in set(after) | set(_hermetic.BEFORE)
                         if after.get(k) != _hermetic.BEFORE.get(k))
        self.assertEqual(changed, [], f"a futás írt ide: {_hermetic.GUARDED}")

    def test_paths_do_not_point_into_real_home(self):
        real = _hermetic.REAL_HOME
        for name, p in [("registry_pointer_file()", fleet.registry_pointer_file()),
                        ("CONFIG_DIR", fleet.CONFIG_DIR)]:
            self.assertFalse(_under(p, real), f"{name} a valódi HOME alá mutat: {p}")


if __name__ == "__main__":
    unittest.main()
