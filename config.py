import json

__all__ = ["get_config"]

__config: dict | None = None


def get_config(reload: bool = False) -> dict:
    global __config
    if reload or __config is None:
        with open("config.json", "rt") as fh:
            __config = json.load(fh)
            return __config  # type: ignore

    return __config
