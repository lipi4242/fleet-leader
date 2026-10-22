import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { writeHealth } from "../lib/health.mjs";

test("writeHealth merges fields and never throws", () => {
  const p = join(mkdtempSync(join(tmpdir(), "se-")), "health.json");
  writeHealth(p, { last_poll_ok: 100 });
  writeHealth(p, { last_delivered: 200 });
  const h = JSON.parse(readFileSync(p, "utf8"));
  assert.equal(h.last_poll_ok, 100);
  assert.equal(h.last_delivered, 200);
  assert.ok(h.written_at > 0);

  // Truly uncreatable path: a regular FILE used as a directory component.
  // mkdirSync(dirname(...), { recursive: true }) will fail with ENOTDIR here,
  // so this genuinely exercises the swallow path (not just an auto-created dir).
  const dir = mkdtempSync(join(tmpdir(), "se-"));
  const fileAsDir = join(dir, "not-a-dir");
  writeFileSync(fileAsDir, "x");
  assert.doesNotThrow(() => writeHealth(join(fileAsDir, "health.json"), { a: 1 }));
});
