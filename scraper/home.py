import requests
from bs4 import BeautifulSoup
import json
import os

def scrape(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        anime_items = soup.select(".last_episodes > ul.items > li")
        data = []

        for anime_item in anime_items:
            title = anime_item.select_one(".name a")["title"]
            image_link = anime_item.select_one("img")["src"]

            watch_anchor = anime_item.select_one(".img a")
            watch_link = watch_anchor["href"]
            watch_link = "-".join(watch_link.split("-")[:-2])
            watch_link = watch_link.replace("/", '')

            card_link = image_link.replace("https://gogocdn.net/cover/", "").replace('.png', '').replace('.jpg', '').replace('https://gogocdn.net/images/anime/N/', '').replace("https://gogocdn.net/images/anime/", '')
            if card_link.rsplit('-', 1)[-1].isnumeric():
                card_link = card_link.rsplit('-', 1)[0]

            anime_data = {"title": title, "image": image_link, "card_link": card_link, "watch_link": watch_link}
            data.append(anime_data)

        return data
    else:
        return None

def get_home_data(pages=2):
    base_url = "https://www5.gogoanimes.fi/?page="
    all_data = []

    for page_number in range(1, pages + 1):
        page_url = base_url + str(page_number)
        data = scrape(page_url)
        all_data.extend(data)

    # Write data to JSON file
    data_file_path = os.path.join(os.path.dirname(__file__), '..', 'cached_data', 'home.json')
    with open(data_file_path, 'w') as f:
        json.dump(all_data, f, indent=4)

    return all_data

if __name__ == '__main__':
    data = get_home_data(pages=50)
    print(json.dumps(data, indent=4))
