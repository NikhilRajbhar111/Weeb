import requests
from bs4 import BeautifulSoup
import json, os
import re  # Import the 're' module for regular expressions

def scrape(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any request errors
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find('ul', class_="items")
        data_list = []  # List to store information about all the items

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
            
            data_list.append(data)  # Add the current item's data to the list

        return json.dumps(data_list)  # Return the list of items as JSON string
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
        all_data.extend(json.loads(data))  # Append the data from each page to the list
        
        # Write data to JSON file
    data_file_path = os.path.join(os.path.dirname(__file__), '..', 'cached_data', 'trending.json')
    with open(data_file_path, 'w') as f:
        json.dump(all_data, f, indent=4)
    return all_data

# def get_carousel_data():
#     data_file_path = os.path.join(os.path.dirname(__file__), '..', 'cached_data', 'home.json')
#     with open(data_file_path, 'w') as f:
#         json.dump(all_data, f, indent=4)
#     return carousel_data

if __name__ == "__main__":
    all_data_json = get_trending_data(50)
    # print(all_data_json)
