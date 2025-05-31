import os
import json
import requests

# Dictionary of data files with their corresponding URLs
DATA_FILES = {
    "ability_cards": "https://deadlock.wiki/Data:AbilityCards.json?action=raw",
    "item_data": "https://deadlock.wiki/Data:ItemData.json?action=raw",
    "hero_data": "https://deadlock.wiki/Data:HeroData.json?action=raw",
    "soul_unlock_data": "https://deadlock.wiki/Data:SoulUnlockData.json?action=raw",
    "generic_data": "https://deadlock.wiki/Data:GenericData.json?action=raw",
    "lang_en": "https://deadlock.wiki/Data:Lang_en.json?action=raw"
}

# Local cache directory
CACHE_DIR = "cache"


def fetch_data(name, url, force_refresh=False):
    """
    Fetches data from the Deadlock wiki or loads it from a local cache.

    :param name: Name of the data file (used for caching).
    :param url: URL to fetch the data from.
    :param force_refresh: If True, force a fresh download even if cached file exists.
    :return: Parsed JSON data (as Python dict or list)
    """
    # Ensure the cache directory exists
    os.makedirs(CACHE_DIR, exist_ok=True)

    cache_file = os.path.join(CACHE_DIR, f"{name}.json")

    if not force_refresh and os.path.exists(cache_file):
        print(f"Loading {name} from cache...")
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    print(f"Fetching {name} from Deadlock wiki...")
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed

    data = json.loads(response.text)

    # Save to cache
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return data


# Example usage
if __name__ == "__main__":
    for _name, _url in DATA_FILES.items():
        data = fetch_data(_name, _url)
        # You can now process 'data' as needed
        print(f"{_name} data fetched and cached.")
