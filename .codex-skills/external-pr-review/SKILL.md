---
name: external-pr-review
description: Review someone else's pull request with a code-review mindset. Use when Codex should inspect a PR diff, identify bugs and regressions, assess tests and CI risk, and produce concise review findings with severity and evidence.
---

# External PR Review

## Overview

Use this skill when the user wants "review someone else's PR." Focus on finding real problems first, with brief summary only after findings.

## Workflow

1. Read the PR title, body, diff, and any available review context.
2. Infer the intended behavior and restate it in one sentence.
3. Use [pr-readme-logger](D:\Users\CChang\Documents\Codex\2026-05-21\github-plugin-github-openai-curated-inspect\pr-readme-logger\SKILL.md) to update [PRhistory.md](D:\Repositories\PushNotification\PRhistory.md) with the PR log entry unless the user explicitly asked for a dry run only.
4. Review the diff with a finding-first mindset.
5. Order findings by severity and include file or line references when available.
6. If the user asked to check or review the PR itself, and GitHub write tools are available, post the review back to the PR automatically unless the user explicitly asked for a dry run only.
7. Keep summary and praise brief after the findings.

## Review Focus

Prioritize:

- bugs and behavioral regressions
- missing tests
- CI and workflow hazards
- security and secret handling
- maintainability only when it affects future correctness or change safety

## Python Standard

For Python PRs, use the Google Python Style Guide as a secondary review lens after correctness:

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

Check especially for:

- import clarity and full-package readability
- exception handling that is too broad or hides failures
- misleading naming, comments, or missing docstrings where explanation is needed
- functions that have become too long or hard to reason about
- inconsistent typing patterns in typed code
- lint- or formatter-related regressions that make future review harder

## Output

If issues exist, list them first. If no issues are found, say that explicitly and mention any residual uncertainty such as missing tests, unavailable CI logs, or ambiguous requirements.

When posting back to GitHub:

- prefer a top-level PR review comment when the findings are diff-level but not tied to exact line coordinates
- use `REQUEST_CHANGES` only when the issues are clear blockers
- use `COMMENT` for normal review feedback
- summarize the highest-signal findings and keep the review concise

When updating the PR log:

- write through `pr-readme-logger`
- update [PRhistory.md](D:\Repositories\PushNotification\PRhistory.md)
- avoid duplicate entries for the same PR
- use the PR title, creation date, description, and user name in the required format
