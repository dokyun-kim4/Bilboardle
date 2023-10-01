import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests as rq
import datetime
import time
load_dotenv()

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('ID'),
                                               client_secret=os.getenv('ID_SECRET'),
                                               redirect_uri=os.getenv('URI'),
                                               scope="playlist-modify-private")
)

today = datetime.datetime.today().strftime('%Y-%m-%d')
   

class song:
    def __init__(self,title:str,artist:str,release_date:str,duration:int,explicit:bool,ranking:int):
        """
        Song object constructor
        """
        self._title = title.replace('\"','\'')
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


def get_bilboard(date)->list:
    """
    Scrape current top 100 songs on bilboard.com, returns a list of dictionaries
    that are formatted {'name':song title, 'artist':artist name}

    Args: 
        date: string formatted 'YYYY-MM-DD'
    
    Returns:
        top_100: list of dictionaries containing song title and artist name
    """

    URL = f'https://www.billboard.com/charts/hot-100/{date}/' 
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


def compile_songinfo(songs_and_artists)->list:
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

        query = spotify.search(
                          q=title,
                          type='track',
                          market='US',
                          limit=1)
        song_info = query['tracks']['items'][0]
        return song_info
    
    print("Getting song information...")
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
    print("Done!")
    return songList


def song_from_name(query:str,songlist:list)->song:
    """
    Returns the song object in a list of songs based on title
    """

    names = [value.title for value in songlist]
    idx = None
    for i,name in enumerate(names):
        if name == query:
            idx=i
    
    return songlist[idx]


def save_songlist(songlist:list,date):
    """
    Given a list of song objects, save it as a json file
    """
    songs = [
        {
            "title":entry.title,
            "artist":entry.artist,
            #Convert datetime object back to string to jsonify
            "release_date":str(entry.release_date)[0:10],
            "duration":entry.duration,
            "explicit":entry.is_explicit,
            "ranking":entry.ranking         
         }
         for entry in songlist
    ]

    json_txt = json.dumps(songs,indent=4)

    with open(f"{date}.json","w") as file:
        file.write(json_txt)

def load_songlist()->list:
    """
    Read from today's songlist and convert to list of song objects
    If json doesn't exist, create one before converting
    Delete songlist from the day before
    """
    today_json = f"{today}.json"

    # Get today's bilboard chart json
    if os.path.exists(today_json):
        songs = json.load(open(today_json))
    # If first time playing today, make a json
    else:
        save_songlist(compile_songinfo(get_bilboard(today)),today)
        songs = json.load(open(today_json))

    # If today's chart is empty, go back until chart is not empty
    if songs == []:
        old_days = [today]
        delta_day = 1
        while True:
            old_day = (datetime.datetime.now() - datetime.timedelta(delta_day)).strftime('%Y-%m-%d')
            old_days.append(old_day)
            old_json = f"{old_day}.json"

            if os.path.exists(old_json):
                songs = json.load(open(old_json))
                break
            
            # Updater
            save_songlist(compile_songinfo(get_bilboard(old_day)),old_day)
            songs = json.load(open(old_json))
            if len(songs) != 0:
                break

            delta_day += 1
        # Cleanup
        for day in old_days[:len(old_days)-1]:
            os.remove(f'{day}.json')

    # Remove the json that was made before; could be many days off
    # else:
    #     delta_day = 1
    #     while True:
    #         old_day = (datetime.datetime.now() - datetime.timedelta(delta_day)).strftime('%Y-%m-%d')
    #         old_json = f"{old_day}.json"
    #         if os.path.exists(old_json):
    #             os.remove(old_json)
    #             break
    #         delta_day += 1


    songlist = [
                song(
                    title=entry['title'],
                    artist=entry['artist'],
                    #convert string back to datetime obj
                    release_date=entry['release_date'],
                    duration=entry['duration'],
                    explicit=entry['explicit'],
                    ranking=entry['ranking']
                )
        for entry in songs
    ]
    return songlist


def compare_song(guess:song,answer:song)->dict:
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

    minsec = str(datetime.timedelta(seconds=guess.duration//1000))[2:]
    ymd = (guess.release_date).strftime('%F')

    compared = {
                'title':[guess.title,title_same],
                'artist':[guess.artist,artist_same],
                'release_date':[ymd,date_updown],
                'duration':[minsec,duration_updown],
                'explicit':[guess.is_explicit,explicit_same],
                'ranking':[guess.ranking,ranking_updown]
    }
    return compared

#---------------- CUSTOM PLAYLIST MODE-----------------------#
def load_playlist(id)-> list:
    """
    Given a spotify playlist link, return a list of song objects 
    For playlist mode, the release date will be replaced by date added to playlist

    Args:
        id: Spotify playlist id
    
    Returns:
        List of song objects
    """
        
    playlist = spotify.playlist(playlist_id=id)
    playlist_songs = playlist['tracks']['items']

    songlist = []

    print("Loading playlist...")
    for entry in playlist_songs:
        songlist.append(
                        song(
                                title = entry['track']['name'],
                                artist = entry['track']['artists'][0]['name'],
                                # Using Date Added instead
                                release_date = entry['added_at'][:10],
                                duration = entry['track']['duration_ms'],
                                explicit = entry['track']['explicit'],    
                                ranking = 1                            
                        )
        )
    print("Done")
    
    return songlist



