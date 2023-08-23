
import json
from my_site.json_validator import remove_duplicates_and_update
def load_home_data(limit=20):
    try:
        with open("cached_data/home.json", "r") as file:
            data = json.load(file)
            if limit is not None:
                return data[:limit]
            else:
                return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None

def load_trending_data(limit=20):
    try:
        with open("cached_data/trending.json", "r") as file:
            data = json.load(file)
            if limit is not None:
                return data[:limit]
            else:
                return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None
    
def load_detail_data(title):
    try:
        with open("cached_data/detail.json", "r") as file:
            data = json.load(file)
            
            matching_data = [item for item in data if item.get("anime_name", "").strip() == title]
            print("Matching data:", matching_data)
            print("serving data from file")
            return matching_data
    except FileNotFoundError:
        print("File not found. Creating a new file.")
        with open("cached_data/detail.json", "w") as file:
            json.dump([], file)
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None
    except EOFError:
        print("File is empty.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def save_detail_data(new_data, title):
    try:
        with open("cached_data/detail.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    found = False
    for item in data:
        if item.get("anime_name", "").strip() == title.strip():
            found = True
            break

    if not found:
        data.append(new_data)
        json_file_path = "cached_data/detail.json"
        remove_duplicates_and_update(json_file_path)

    with open("cached_data/detail.json", "w") as f:
        json.dump(data, f, indent=4)
# ///////////////////////////////////////////////////