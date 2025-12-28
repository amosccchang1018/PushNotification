from pathlib import Path
import yaml


def load_sources_config(path: str | Path) -> list[dict]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "sources" not in data:
        raise ValueError("Invalid sources.yaml: missing 'sources' key")

    return data["sources"]
