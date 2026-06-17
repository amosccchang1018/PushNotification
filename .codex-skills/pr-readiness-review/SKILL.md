---
name: pr-readiness-review
description: Prepare local code changes or a branch for pull request review. Use when Codex should inspect unreviewed code, reduce likely reviewer feedback, fix obvious PR blockers, tighten scope, add missing validation, or draft a clear PR summary before the pull request is opened.
---

# PR Readiness Review

## Overview

Use this skill when the user wants "make my code ready for a PR." Focus on pre-review quality: reduce likely reviewer objections, improve validation, and leave the branch easier to review.

## Workflow

1. Inspect the changed files and infer the intended behavior.
2. Brainstorm likely reviewer questions:
   - What could break?
   - What assumptions changed?
   - What tests prove this?
   - What rollout or config detail is easy to miss?
3. Check for readiness:
   - narrow scope
   - clear naming
   - dead code or debug leftovers
   - docs or config updates
   - tests or manual verification notes
   - CI compatibility
4. Fix issues when the task calls for action. Otherwise return a prioritized readiness list.
5. End with a concise PR description draft when helpful.

## Review Focus

Prioritize:

- correctness before polish
- missing tests or verification
- configuration and migration gaps
- CI and deployment assumptions
- PR scope clarity and reviewer ergonomics

## Python Standard

For Python changes, also review against the Google Python Style Guide:

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

Apply the highest-signal parts during PR-readiness work:

- prefer clear module imports and avoid ambiguous local-import patterns
- use explicit exceptions and avoid broad `except:` handling
- keep names, comments, and docstrings clear and conventional
- preserve readable function size and structure
- keep type annotations consistent where the codebase already uses them
- treat lint and formatter cleanliness as part of review readiness

## Output

Return:

- a short readiness assessment
- the highest-priority fixes or blockers
- verification performed and gaps that remain
- a PR summary draft when useful
