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

    def __repr__(self) -> str:
        return f"title: {self._title} | artist: {self._artist} | release date: {self._release_date} | duration: {self._duration} | explicit: {self._is_explicit} | ranking: {self._ranking}"

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


def compile_songinfo(songs_and_artists):
    """
    Takes list of {'name':song title, 'artist':artist name}, and creates a 
    list of `song` objects with more info about the song
    """
    songList=[]

    def search_song(title,artist):
        """
        Search a song by title and artist using Spotify API, returns dictionary
        of information about the song
        """
        #Possible fix for long artist names due to featuring messing up search
        if len(artist) > 14:
          artist=artist[:14]

        query = spotify.search(
                          q=title+" "+artist,
                          type='track',
                          market='US',
                          limit=1)
        song_info = query['tracks']['items'][0]
        return song_info
    
    for idx, pair in enumerate(songs_and_artists):
        title = pair['name']
        artist = pair['artist']
        curr_song = search_song(title=title,artist=artist)
        songList.append(
                        song(
                              title=curr_song['name'],
                              artist=curr_song['album']['artists'][0]['name'],
                              release_date=curr_song['album']['release_date'],
                              duration=curr_song['duration_ms'],
                              explicit=curr_song['explicit'],
                              ranking=idx+1
                        )
                      )
    return songList


def compare_song(guess:song,answer:song):
    """
    Compares two songs and returns a list that includes variables describing
    which traits are the same/different.
    """

    title_same = guess.title == answer.title #Boolean
    artist_same = guess.artist == answer.artist #Boolean

    date_updown = guess.release_date == answer.release_date #True if same
    if guess.release_date > answer.release_date:
        date_updown = "down"
    if guess.release_date < answer.release_date:
        date_updown = "up"

    duration_updown = guess.duration == answer.duration #True if same
    if guess.duration > answer.duration:
        duration_updown = "down"
    if guess.duration < answer.duration:
        duration_updown = "up"
    
    explicit_same = guess.is_explicit == answer.is_explicit #Boolean

    ranking_updown = guess.ranking == answer.ranking #Boolean
    if guess.ranking > answer.ranking:
        ranking_updown = "up"
    if guess.ranking < answer.ranking:
        ranking_updown = "down"

    compared = {
                'title':title_same,
                'artist':artist_same,
                'release_date':date_updown,
                'duration':duration_updown,
                'explicit':explicit_same,
                'ranking':ranking_updown
    }
    return compared