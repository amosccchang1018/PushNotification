---
name: pr-review-follow-up
description: Address review comments on your own pull request. Use when Codex should gather review feedback, turn comments into action items, propose or implement fixes, draft responses, and summarize how each requested change was handled.
---

# PR Review Follow-Up

## Overview

Use this skill when the user wants "help me respond to review comments on my PR." Focus on turning feedback into a concrete response plan and minimal effective fixes.

## Workflow

1. Collect review comments, unresolved threads, and the relevant diff context.
2. Normalize feedback into action items:
   - must-fix
   - likely follow-up
   - optional disagreement or clarification
3. Separate correctness comments from preference comments.
4. For each actionable item, propose the smallest reasonable code or doc change.
5. If comments conflict, pause and explain the tradeoff instead of guessing.
6. After edits, summarize how each comment was addressed.

## Review Focus

Prioritize:

- direct response to reviewer concerns
- smallest safe fix for each actionable comment
- explicit handling of unresolved or conflicting feedback
- concise communication back to reviewers

## Python Standard

For Python review comments, use the Google Python Style Guide when deciding whether feedback reflects a real cleanup item or only a preference:

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

Use it to guide follow-up on:

- imports and module structure
- exception behavior and error handling
- naming clarity
- comments and docstrings
- function size and readability
- type-annotation consistency

## Output

Return:

- the action plan
- the implemented fixes or proposed changes
- draft reviewer responses when useful
- any comments that still need human clarification
