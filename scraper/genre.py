import os
import requests
from bs4 import BeautifulSoup
import re, json

def scrape(genre):
    url = f"https://www5.gogoanimes.fi/genre/{genre}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find('ul', class_="items")
    data_list = []
    
    try:
        for li in items.find_all('li'):
            data = {}  # Create a new dictionary for each item
            
            # Extracting image URL
            image_div = li.find('div', class_="img")
            images = image_div.find('img')['src']
            data.update({"image": images})
            
            # Extracting title
            title = li.find('p', class_="name").text
            data.update({"title": title})
            
            # Extracting card link
            anchor = li.find('a', href=True)  # Find anchor tag with href attribute
            href = anchor['href']
            # Use regex to extract the desired part from the href
            card_link = re.search(r'/category/(.+)', href).group(1)
            data.update({"card_link": card_link})
            
            data_list.append(data)
    except AttributeError:
        pass  # Skip this genre if no data is returned
    
    return data_list

def get_genre_data(genres):
    data = []  # Initialize an empty list to hold genre data
    
    # Directory to store cached data
    cache_directory = "cached_data/genre"
    
    # Make sure the cache directory exists
    os.makedirs(cache_directory, exist_ok=True)
    
    for genre in genres:
        # Check if the cache file exists
        cache_file_path = os.path.join(cache_directory, f"{genre}.json")
        if os.path.exists(cache_file_path):
            # If cache file exists, read data from it
            with open(cache_file_path, "r") as cache_file:
                cached_data = json.load(cache_file)
                data.extend(cached_data)
        else:
            # If cache file doesn't exist, scrape data and create cache file
            scraped_data = scrape(genre)
            with open(cache_file_path, "w") as cache_file:
                json.dump(scraped_data, cache_file, indent=4)
            data.extend(scraped_data)
    return data

res = get_genre_data(["action", "comedy"])
print(res)
