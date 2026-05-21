---
name: github-review-coach
description: Route general GitHub review requests to the right specialized skill. Use when the user asks broadly for help with code review, pull request review, PR readiness, or review follow-up and the exact workflow has not been chosen yet.
---

# GitHub Review Coach

## Overview

Use this skill as a lightweight dispatcher. Classify the request quickly, then switch to the matching specialized skill instead of keeping broad review instructions in scope.

## Workflow Decision

Choose one path early and say so explicitly:

- `make my code ready for a PR`: Use [pr-readiness-review](D:\Users\CChang\Documents\Codex\2026-05-21\github-plugin-github-openai-curated-inspect\pr-readiness-review\SKILL.md).
- `review someone else's PR`: Use [external-pr-review](D:\Users\CChang\Documents\Codex\2026-05-21\github-plugin-github-openai-curated-inspect\external-pr-review\SKILL.md).
- `help me respond to review comments on my PR`: Use [pr-review-follow-up](D:\Users\CChang\Documents\Codex\2026-05-21\github-plugin-github-openai-curated-inspect\pr-review-follow-up\SKILL.md).

If the task is still broad, begin with a short brainstorming pass:

1. Identify the target repo, PR, branch, or issue.
2. Identify whether the main risk is correctness, CI stability, maintainability, or review clarity.
3. Choose the specialized skill.
4. Gather only the context needed for that skill.

## Example Triggers

- "Use $github-review-coach to make this branch ready for a PR."
- "Use $github-review-coach to review PR #42."
- "Use $github-review-coach to help me address the latest review comments on my PR."
