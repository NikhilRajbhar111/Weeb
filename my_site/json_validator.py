import json

def remove_duplicates_and_update(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return

    unique_data = []
    anime_names_seen = set()

    for item in data:
        anime_name = item.get("anime_name")
        if anime_name and anime_name not in anime_names_seen:
            unique_data.append(item)
            anime_names_seen.add(anime_name)

    with open(file_path, "w") as file:
        json.dump(unique_data, file, indent=4)

# Specify the path to your JSON file
json_file_path = "cached_data/detail.json"
remove_duplicates_and_update(json_file_path)
print("Duplicates removed and file updated.")
