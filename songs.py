import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests as rq
load_dotenv()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('ID'),
                                               client_secret=os.getenv('ID_SECRET'),
                                               redirect_uri=os.getenv('URI'),
                                               scope="playlist-modify-private")
)

URL = 'https://www.billboard.com/charts/hot-100/'
        

def get_bilboard()->list:
    """
    Finds current top 100 songs on Bilboard, returns a list of dictionaries
    that are formatted {'name':song title, 'artist':artist name}
    """
    response = rq.get(URL)
    website = response.text

    soup = BeautifulSoup(website, "html.parser")
    result = soup.find_all('div', class_='o-chart-results-list-row-container')
    top_100 = [
                {'name':res.find('h3').text.strip(),
                  'artist': res.find('h3').find_next('span').text.strip()
                }
                  for res in result
                ]

    return top_100


def get_artist():
    pass

def get_album():
    pass

def get_year():
    pass