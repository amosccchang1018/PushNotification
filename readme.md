# PushNotification

A Python-based automation pipeline that **fetches weather information from websites and pushes formatted notifications to Telegram**, executed daily via **GitHub Actions**.

This project is designed to be:

- Modular (easy to add new data sources)
- Deterministic (reproducible with locked dependencies)
- CI-friendly (runs fully on GitHub Actions using Linux + Playwright)

---

## Tech Stack

- **Language**: Python 3.12+ (recommended for CI stability)
- **Dependency Management**: [`uv`](https://github.com/astral-sh/uv)
- **Web Automation / Scraping**: Playwright (Chromium)
- **CI/CD**: GitHub Actions (cron-based scheduling)
- **Notification Channel**: Telegram Bot API

---

## Python Version

The project pins the Python version using `.python-version`.

Recommended:

Python 3.12.x

GitHub Actions will automatically install the pinned version via `uv`.

---

## Dependency Management (uv)

This project uses **uv** instead of pip/poetry.

Key files:

- `pyproject.toml` — dependency definitions
- `uv.lock` — locked, reproducible dependency versions

### Local setup

```bash
uv venv
uv sync
```

CI usage (GitHub Actions)

```bash
uv sync --frozen
```

---

Repository Structure
High-level

```css
PushNotification/
  src/
    push_notification/
      __init__.py
      main.py
  pyproject.toml
  uv.lock
  README.md
  .github/
    workflows/
      daily_telegram_push.yml
```

Detailed Structure

```css
src/
  push_notification/
    __init__.py
    main.py                    # Orchestrates the full pipeline
    models.py                  # Shared dataclasses (e.g. Forecast)
    http.py                    # Shared HTTP utilities (headers, retry, timeout)

    sources/                   # Website-specific data extractors
      __init__.py
      base.py                  # BaseSource interface
      weeronline.py            # Weeronline extractor (Playwright-based)
      knmi.py                  # (Planned) KNMI extractor

    formatters/
      __init__.py
      base.py                  # Formatter interface
      default.py               # Default Telegram text formatter

    notifiers/
      __init__.py
      telegram.py              # Telegram sender implementation

configs/
  sources.yaml                 # Enabled sources and parameters
```

---

Pipeline Overview

```scss
Website(s)
   ↓
Source extractor (Playwright / HTTP)
   ↓
Normalized data model (Forecast)
   ↓
Formatter (Telegram message text)
   ↓
Telegram Bot API
```

Each layer is isolated:

* Adding a new website = add a new file under sources/

* Changing message format = modify or add a formatter

* Notification channel is abstracted (Telegram now, others later)

---

### Configuring Data Sources

Data sources are defined in:
```bash
configs/sources.yaml
```
Example (conceptual):
```yaml
sources:
  - name: weeronline
    enabled: true
    url: https://www.weeronline.nl/weerbericht-nederland
```

Each enabled source must have a corresponding extractor class in `src/push_notification/sources/`.

---
### Telegram Setup
#### Required Secrets

The pipeline sends messages via a Telegram bot. You must configure two secrets in GitHub:
| Secret Name  | Name	Description |
| ------------- |:-------------:|
|`TG_BOT_TOKEN`|Telegram Bot API token|
|`TG_CHAT_ID`|Chat ID (group or private)|

⚠️ Do not wrap values in quotes.
Store raw values only.

###Local testing
```bash
export TG_BOT_TOKEN=123456:ABC...
export TG_CHAT_ID=-1001234567890

uv run python -m push_notification.main
```
---
### GitHub Actions (Daily Run)
#### Workflow Location
```bash
.github/workflows/daily_telegram_push.yml
```

GitHub Actions **only reads workflows from this directory.**

---

### Scheduling Logic (Netherlands Time)

#### GitHub Actions cron uses UTC only, so this project uses a dual-cron + runtime gate strategy:

```yaml
schedule:
  - cron: "0 6 * * *" # 08:00 CEST
  - cron: "0 7 * * *" # 08:00 CET
```
At runtime, the job checks:

```python
Europe/Amsterdam local time == 08:00
```


This ensures:

* Exactly **one execution per day**

* Automatic handling of **daylight saving time**

---

### Playwright Requirement (Important)

Because this project uses Playwright on Linux runners, the workflow must install browser dependencies:

```bash
uv run playwright install --with-deps chromium
```

This step is mandatory on GitHub Actions.

---

### Running the Workflow
#### Manual run (recommended for testing)

1. GitHub → Actions

2. Select Daily Telegram Push

3. Click Run workflow

4. Choose branch: `master`

#### Scheduled run

* Runs automatically every day at **08:00 (Europe/Amsterdam)**

* No UI interaction required

---

### Branching & Safety

* Only the default branch (`master`) is scheduled

* Other branches do not trigger workflows

* Secrets are injected only at runtime via GitHub Actions

---

### Notes

* `.github/workflows/*.yml` files are authoritative; deleting a workflow file immediately stops its schedule

* `uv.lock` must be committed for reproducible CI runs

* Linux runners are case-sensitive (`README.md` ≠ `readme.md`)

## Author

**ChiChun Chang**

- LinkedIn: https://www.linkedin.com/in/ccchang1018/
- GitHub: https://github.com/amosccchang1018


## License

This project is licensed under the **MIT License**.

Copyright (c) 2025 ChiChun Chang

See the [LICENSE](LICENSE) file for details.
