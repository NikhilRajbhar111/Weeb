import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_stream_url(title):
    name = quote(title.replace(" ", '-').replace("(", '').replace(")", '').replace(":", ''))
    
    base_url = f"https://www5.gogoanimes.fi/{name}"
    response = requests.get(base_url)
    print(base_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ep_link = soup.find('iframe')['src']
        print(ep_link)
        return ep_link
    else:
        return None