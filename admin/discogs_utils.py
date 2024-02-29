import requests
from dotenv import load_dotenv
import os
import pandas as pd
import sqlite3
from database_utils import execute_sql

database_path = "../data/database.db"

def search_and_get_master_id(artist, title):        
    load_dotenv()
    token = os.getenv('TOKEN')
    
    url = "https://api.discogs.com/database/search"
    params = {
        "release_title": title,
        "artist": artist,
        "type": "master",
        "token": token
    }
    response = requests.get(url, params=params)
    data = response.json()
    if (data['results'] == []):
        return None
    else :
        return data['results'][0]['master_id']
    
def load_album(connection):
    df_album = pd.read_sql_query("SELECT * FROM album WHERE id_discogs IS NULL LIMIT 5", connection)
    return df_album

def update_album_link(connection, id_album, id_discogs):
    execute_sql(connection, f"UPDATE album SET id_discogs = {id_discogs} WHERE id = {id_album}")
    
def update_discogs_links():
    # Connect to the database
    connection = sqlite3.connect(database_path)

    # Load the album data from the database
    df_album = load_album(connection)

    # Update the discogs links
    for index, row in df_album.iterrows():
        if row['id_discogs'] is None:
            discogs_id = search_and_get_master_id(row['artist'], row['title'])
            if discogs_id is not None:
                # Album found on Discogs
                df_album.at[index, 'id_discogs'] = discogs_id   
                update_album_link(connection, row['id'], discogs_id)
            else:
                # Album not found on Discogs
                update_album_link(connection, row['id'], 0)
                
    # Close the database connection
    connection.close()