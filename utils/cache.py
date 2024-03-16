import json
from typing import Optional

def get_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

cache_path = "utils/cached_responses.json"

def update_cache(key: str, value: str) -> None:
    cache = get_json(cache_path)

    cache[key] = value

    with open(cache_path, 'w') as f:
        json.dump(cache, f)



def get_from_cache(key: str) -> Optional[str]:
    cache = get_json(cache_path)

    value = cache.get(key)
    return value