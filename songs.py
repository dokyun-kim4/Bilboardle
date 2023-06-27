import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests as rq
import datetime
load_dotenv()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('ID'),
                                               client_secret=os.getenv('ID_SECRET'),
                                               redirect_uri=os.getenv('URI'),
                                               scope="playlist-modify-private")
)

URL = 'https://www.billboard.com/charts/hot-100/'
      

class song:
    def __init__(self,title:str,artist:str,release_date:str,duration:int,explicit:bool,ranking:int):
        """
        Song object constructor
        """
        self._title = title
        self._artist=artist
        self._release_date = datetime.datetime(
                                int(release_date.split('-')[0]),
                                int(release_date.split('-')[1]),
                                int(release_date.split('-')[2])
                                )
        self._duration= duration
        self._is_explicit = explicit
        self._ranking = ranking

    @property
    def title(self)->str:
        return self._title
    
    @property
    def artist(self)->str:
        return self._artist
    
    @property
    def release_date(self)->datetime:
        return self._release_date
    
    @property
    def duration(self)->int:
        return self._duration
    
    @property
    def is_explicit(self)->bool:
        return self._is_explicit
    
    @property
    def ranking(self):
        return self._ranking  


def get_bilboard()->list:
    """
    Scrape current top 100 songs on bilboard.com, returns a list of dictionaries
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