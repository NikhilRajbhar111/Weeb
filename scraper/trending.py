import requests
from bs4 import BeautifulSoup
import json, os
import re

def scrape(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find('ul', class_="items")
        data_list = []

        for li in items.find_all('li'):
            data = {}
            
            image_div = li.find('div', class_="img")
            images = image_div.find('img')['src']
            data.update({"image": images})
            
            title = li.find('p', class_="name").text
            data.update({"title": title})
            
            anchor = li.find('a', href=True)
            href = anchor['href']
            card_link = re.search(r'/category/(.+)', href).group(1)
            data.update({"card_link": card_link})
            
            data_list.append(data)

        return json.dumps(data_list)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "[]"

def get_trending_data(pages=2):
    all_data = []
    base_url = "https://www5.gogoanimes.fi/popular.html"
    for i in range(1, pages + 1):
        url = f"{base_url}?page={i}"
        print(f"Scraping data from page {i}")
        data = scrape(url)
        all_data.extend(json.loads(data))
        
    data_file_path = os.path.join(os.path.dirname(__file__), '..', 'cached_data', 'trending.json')
    with open(data_file_path, 'w') as f:
        json.dump(all_data, f, indent=4)
    return all_data
