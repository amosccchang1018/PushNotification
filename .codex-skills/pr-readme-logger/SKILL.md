---
name: pr-readme-logger
description: Record each newly created pull request in `D:\Repositories\PushNotification\PRhistory.md`. Use when Codex creates a new PR, opens a draft PR, or is asked to log PR history there using the format "<PR name> - <create date>: <description> - <User name>".
---

# PR README Logger

## Overview

Use this skill whenever a new pull request is created and the repository should keep a simple PR history in [PRhistory.md](D:\Repositories\PushNotification\PRhistory.md).

## Workflow

1. Confirm the PR has actually been created.
2. Collect the PR title, creation date, and short description.
3. Open [PRhistory.md](D:\Repositories\PushNotification\PRhistory.md).
4. Append one new log line in this format:
   `<PR name> - <create date>: <description> - <User name>`
5. Do not rewrite older log entries unless the user explicitly asks.
6. If the file does not exist yet, create it and start appending entries there.

## Formatting Rules

- Use the PR title as `<PR name>`.
- Use the PR creation date in ISO style when possible, for example `2026-05-21`.
- Keep `<description>` short and human-readable.
- Use the PR author as `<User name>`.
- Add exactly one line per PR.
- Avoid duplicate entries for the same PR.

## Output

Return:

- whether the PR was logged
- the `PRhistory.md` location updated
- the exact line that was added
