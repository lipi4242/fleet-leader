# Changelog

Every release also ships a machine-readable `release.json` at the root of its
tag.

## 0.3.1

Released together with the Mentat brain 0.3.1 and anytime-engine 0.3.1.

- **The identity gate as a plugin hook**: every agent on the box gets the same check before your
  e-mail address leaves for a third party: asked in an interactive session, denied headless.
  <!-- cap: fleet-identity-gate -->
- **doctor checks every agent's guard**: `fleet doctor` shows red when an agent's guard or its
  Claude Code version is not up to date with 0.3.1. Nothing is rewritten. <!-- cap: doctor-fail-open -->
- **New agents come up cleanly**: `fleet validate` also finds a runbook relative to the
  registry repo's root; the session-id hook reads `FLEET_AGENT` and the older `THUFIR_AGENT`, and
  `seed_settings` replaces an older hook entry instead of adding a second one.
  <!-- cap: fleet-setup-fixes -->
- **Safer defaults on the server**: fewer elevated rights on the box, and no menu questions for an
  agent that runs unattended. <!-- cap: fleet-hardening -->
- **The capability tree across the fleet**: `fleet capabilities collect` gathers each agent's
  exported capabilities on this box (filtered, outside the repos); `fleet capabilities find --as
  <agent>` searches them with the right visibility. <!-- cap: fleet-capabilities -->

## 0.3.0

First public release of the fleet runner for always-on agents.

- **Setup in one command** - `fleet setup` provisions a box and an agent end to
  end; `fleet init` writes the registry entry from a repository, `fleet wait-up`
  blocks until an agent reports healthy.
- **One controller** - `fleet reconcile` (5-minute timer) enforces the desired
  state: OOM protection, tick re-arm, duplicate alerts. `reconcile-fast`
  brings a dead agent process back in about a minute. Installs are
  transactional and finish on a green postcheck.
- **Bridge 2.0.1** - Telegram-to-tmux bridge with webhook output, delivery
  receipts, chunked output, a token lock and strict argument parsing.
- **Drift and rollback** - `fleet bridge status` reports sha256 drift of the
  installed bridge; `fleet bridge rollback` restores the previous one.
- **mentat.json synergies** - `fleet join` / `upgrade` read the Mentat
  manifest and warn when the brain is not loaded by `CLAUDE.md`.
- **Claude plugin** - skills `roster`, `doctor`, `new-agent`, `runtime` and a
  SessionStart hook (plugin version 1.2.0).
- **Templates** - systemd units and timers, rule file, a separate
  `claude-auth.env` for the agent's Claude token.
