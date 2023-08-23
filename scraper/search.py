import requests
from bs4 import BeautifulSoup
import json

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_search_data(anime_name):
    base_url = "https://www5.gogoanimes.fi"
    search_url = f"{base_url}/search.html?keyword={anime_name}"
    soup = get_soup(search_url)
    
    pagination_div = soup.find('ul', class_='pagination-list')
    anime_data = []

    if pagination_div:
        pages = pagination_div.find_all('li')
        num_pages = len(pages)
        
        for page_num in range(1, num_pages + 1):
            page_url = f"{base_url}/search.html?keyword={anime_name}&page={page_num}"
            page_soup = get_soup(page_url)
            
            anime_container = page_soup.find("div", class_="last_episodes")
            for title_div, image_div, card in zip(anime_container.find_all('p', class_="name"),
                                      anime_container.find_all('div', class_="img"),
                                      anime_container.find_all('div', class_="img")):
                name = title_div.find('a').text.strip()
                image_src = image_div.find("img")["src"]
                card_link = card.find('a')["href"].replace("/category", '')
                anime_data.append({"name": name, "image": image_src, "link": card_link})
    else:
        anime_container = soup.find("div", class_="last_episodes")

        for title_div, image_div, card in zip(anime_container.find_all('p', class_="name"),
                                  anime_container.find_all('div', class_="img"),
                                  anime_container.find_all('div', class_="img")):
            name = title_div.find('a').text.strip()
            image_src = image_div.find("img")["src"]
            card_link = card.find('a')["href"].replace("/category", '')
            anime_data.append({"name": name, "image": image_src, "link": card_link})

    return anime_data
