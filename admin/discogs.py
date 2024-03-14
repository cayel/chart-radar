import requests
from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    return os.getenv('TOKEN')

class DiscogsInfo:
    def __init__(self, artist, title):
        self.id = None
        self.artist = artist
        self.title = title
        self.year = None
        self.image = None   
        self.reference = None
        self.token = load_env()
    
    def __str__(self):
        return f"Artiste : {self.artist} - Titre : {self.title}"

    def _get_discogs_data(self, url, params):
        response = requests.get(url, params=params)
        return response.json()
    
    def _search_and_get_master_id(self, artist, title):        
        url = "https://api.discogs.com/database/search"
        params = {
            "release_title": title,
            "artist": artist,
            "type": "master",
            "token": self.token
        }
        data = self._get_discogs_data(url, params)
        if 'results' in data and data['results']:
            return data['results'][0]['master_id']
        else:
            return None
    
    def _search_and_get_release_id(self, artist, title):
        url = "https://api.discogs.com/database/search"
        params = {
            "release_title": title,
            "artist": artist,
            "type": "release",
            "token": self.token
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data is not None and data['results'] != []:
            return data['results'][0]['id']
        else:
            return None
        
    def _search(self):
        self.id = self._search_and_get_master_id(self.artist, self.title)
        if self.id is None:
            self.id = self._search_and_get_release_id(self.artist, self.title)
            self.reference = 'release'
            return self.id
        else:
            self.reference = 'master'
            return self.id
    
    def get_info(self):
        if self._search() is not None:  
            if self.reference == 'master':
                url = f"https://api.discogs.com/masters/{self.id}"
            else:
                url = f"https://api.discogs.com/releases/{self.id}"
            params = {
                "token": self.token
            }
            data = self._get_discogs_data(url, params)
            self.artist = data['artists'][0]['name']
            self.title = data['title']
            self.year = data['year']
            self.image = data['images'][0]['uri'] if 'images' in data and data['images'] else None
            return 0
        else:   
            return -1
        
class Discogs:
    def __init__(self):
        self.token = load_env()

    def get_discogs_data(self, url, params):
        print(params)
        response = requests.get(url, params=params)
        return response.json()

    def search_and_get_master_id(self, artist, title):        
        url = "https://api.discogs.com/database/search"
        params = {
            "release_title": title,
            "artist": artist,
            "type": "master",
            "token": self.token
        }
        data = self.get_discogs_data(url, params)
        if 'results' in data and data['results']:
            return data['results'][0]['master_id']
        else:
            return None
        
    def search_and_get_release_id(self, artist, title):
        url = "https://api.discogs.com/database/search"
        params = {
            "release_title": title,
            "artist": artist,
            "type": "release",
            "token": self.token
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data is not None and data['results'] != []:
            return data['results'][0]['id']
        else:
            return None
    
    def get_info_master(self, id_discogs):
        url = f"https://api.discogs.com/masters/{id_discogs}"
        params = {
            "token": self.token
        }
        data = self.get_discogs_data(url, params)
        return data
    
    def get_info_release(self, id_discogs):
        url = f"https://api.discogs.com/releases/{id_discogs}"
        params = {
            "token": self.token
        }
        data = self.get_discogs_data(url, params)
        return data