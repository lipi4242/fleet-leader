# Security policy

## Supported versions

Security fixes go into the latest 0.3.x release.

## Reporting a vulnerability

Please do not open a public issue. Report it privately through GitHub
Security Advisories: on the repository page choose **Security**, then
**Report a vulnerability**.

Include what you found, how to reproduce it, and which version you tested.
This is a small project maintained on a best-effort basis; reports are read
and answered as soon as possible, and a fix is released before the details
are made public.

## Scope

`fleet` runs on your own server and talks to the Telegram Bot API with a token
you provide. Things that matter here: leaking that token, running commands
for someone who is not on the bridge's allowlist, or writing outside the
agent's own files. Keep tokens out of the registry and out of git.
