import requests
from bs4 import BeautifulSoup
from my_site.access import load_detail_data, save_detail_data


def scrape(title):
    url = f"https://www5.gogoanimes.fi/category/{title}"
    
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

        episode_detail = soup.find("div", class_="anime_video_body")
        last_episode = episode_detail.find_all("li")

        ls_count = len(last_episode)
        last_item = last_episode[ls_count-1].find("a")["ep_end"]
        last_episode_number = last_item
        card_link = img.replace("https://gogocdn.net/cover/", "").replace('.png', '').replace('.jpg', '').replace('https://gogocdn.net/images/anime/N/', '').replace("https://gogocdn.net/images/anime/", '')
        if card_link.rsplit('-', 1)[-1].isnumeric():
            card_link = card_link.rsplit('-', 1)[0]
        ep_url = card_link+"-episode-1"
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
            return [data]
        else:
            print("Scraping failed.")
            return None
    else:
        print("Data found in cache.")
        return data