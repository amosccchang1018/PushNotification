
##  Using uv to manage libs

##  repos structure
```
PushNotification/
  src/
    push_notification/
      __init__.py
      telegram.py
      main.py
  pyproject.toml
  README.md
  .github/
    workflows/
      daily_push.yml
```

### Detail
```
src/
  push_notification/
    __init__.py
    main.py                    # pipeline: fetch -> format -> push
    models.py                  # dataclasses: Forecast, SourceResult...
    http.py                    # shared HTTP client (headers, retry, timeout)
    sources/                   # each website extractor lives here
      __init__.py
      base.py                  # BaseSource interface
      weeronline.py            # Weeronline extractor
      knmi.py                  # later
    formatters/
      __init__.py
      base.py                  # Formatter interface
      default.py               # simple formatter
    notifiers/
      __init__.py
      telegram.py              # sender
configs/
  sources.yaml                 # which sources enabled + params
```


When run the command in GitHub Action, remember
```
uv run playwright install --with-deps chromium
```