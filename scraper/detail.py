import requests
from bs4 import BeautifulSoup
# import json, os
from my_site.access import load_detail_data, save_detail_data


def scrape(title):
    # title_formatted = title.replace("-", " ").title()
    url = f"https://www5.gogoanimes.fi/category/{title}"
    # print(url)
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        anime_detail = soup.find("div", class_="anime_info_body_bg")

        img = anime_detail.find("img")["src"]
        anime_name = anime_detail.find("h1").text

        anime_details = anime_detail.find_all("p")
        Name = anime_details[1].find("a").text
        Plot = anime_details[2].text.replace("Plot Summary: ", "")
        Genre_list = anime_details[3].find_all("a")
        genre = []
        for item in Genre_list:
            genre.append(item["href"].replace("/genre/", ""))
        Released = anime_details[4].text.replace("Released: ", "")
        Status = anime_details[5].find("a").text
        Other_Name = anime_details[6].text.replace("Other name: ", "")

        # Extract last episode info
        episode_detail = soup.find("div", class_="anime_video_body")
        last_episode = episode_detail.find_all("li")

        ls_count = len(last_episode)
        # print(ls_count)
        last_item = last_episode[ls_count-1].find("a")["ep_end"]
        # print(last_item)
        last_episode_number = last_item
        # print(last_episode_number)
        card_link = img.replace("https://gogocdn.net/cover/", "").replace('.png', '').replace('.jpg', '').replace('https://gogocdn.net/images/anime/N/', '').replace("https://gogocdn.net/images/anime/", '')
        if card_link.rsplit('-', 1)[-1].isnumeric():
            card_link = card_link.rsplit('-', 1)[0]
        # verify_link = requests.get(f"https://www5.gogoanimes.fi/{card_link}")
        ep_url = card_link+"-episode-1"
        # ep_url = f"{anime_name}-episode-1".replace(" ", '-').replace(":", "").replace(".", "").replace("(", "").replace(")", "").replace(",", "").replace('"', "").replace("!", "").replace("☆", "").replace("---", "-").lower()
        # print(ep_url)
        anime_data = {
            "img": img,
            "anime_name": anime_name,
            "Name": Name,
            "Plot": Plot,
            "Genre": genre,
            "Released": Released,
            "Status": Status,
            "Other_Name": Other_Name,
            "Last_Episode_Number": last_episode_number,
            "ep_url":ep_url
            # "Last_Episode_URL": last_episode_href
        }

        return anime_data
    else:
        return None

def get_detail_data(card_link, title):
    data = load_detail_data(title)

    if not data:
        print("Data not found, scraping...")
        data = scrape(card_link)
        if data:
            print("Data scraped successfully.")
            save_detail_data(data, title)
            # update_existing_data(data)  # Call the function to update existing data
            return [data]
        else:
            print("Scraping failed.")
            return None
    else:
        print("Data found in cache.")
        return data
    
# def update_existing_data(scraped_data):
    # existing_data = load_detail_data("detail")  # Load existing data
    # for scraped_item in scraped_data:
    #     exists = False
    #     for i, existing_item in enumerate(existing_data):
    #         if scraped_item['anime_name'] == existing_item['anime_name']:
    #             exists = True
    #             break
    #     if not exists:
    #         existing_data.append(scraped_item)
    # save_detail_data(existing_data)  # Save updated data



# data = scrape_category_details("naruto")
# print(data)