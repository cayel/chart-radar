import requests
from dotenv import load_dotenv
import os
import pandas as pd
import sqlite3
from database_utils import execute_sql
import streamlit as st

database_path = "../data/database.db"

def load_env():
    load_dotenv()
    return os.getenv('TOKEN')

def get_discogs_data(url, params):
    response = requests.get(url, params=params)
    return response.json()

def search_and_get_master_id(artist, title):        
    token = load_env()
    
    url = "https://api.discogs.com/database/search"
    params = {
        "release_title": title,
        "artist": artist,
        "type": "master",
        "token": token
    }
    data = get_discogs_data(url, params)
    if 'results' in data and data['results']:
        return data['results'][0]['master_id']
    else:
        return None
    
def load_album(connection):
    df_album = pd.read_sql_query("SELECT * FROM album WHERE id_discogs IS NULL LIMIT 20", connection)
    return df_album

def update_album_link(connection, id_album, id_discogs):
    execute_sql(connection, f"UPDATE album SET id_discogs = {id_discogs} WHERE id = {id_album}")
    
def update_discogs_links():
    # Create a progress bar
    progress_bar = st.progress(0)
    # Connect to the database
    connection = sqlite3.connect(database_path)

    # Load the album data from the database
    df_album = load_album(connection)

    # Update the discogs links
    for index, row in df_album.iterrows():
        progress_bar.progress((index + 1) / 20)
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
    # Clear the progress bar
    progress_bar.empty()

def get_info_album(id_discogs):
    load_dotenv()
    token = os.getenv('TOKEN')
    
    url = f"https://api.discogs.com/masters/{id_discogs}"
    params = {
        "token": token
    }
    data = get_discogs_data(url, params)
    return data

def get_info_discogs():
    # Create a progress bar
    progress_bar = st.progress(0)
    # Connect to the database
    connection = sqlite3.connect(database_path)

    # Load the album data where the discogs id is not null and the discogs info is not already in the discogs table
    df_album = pd.read_sql_query("SELECT * FROM album WHERE id_discogs IS NOT NULL AND id_discogs>0 AND id_discogs NOT IN (SELECT id FROM discogs) LIMIT 20", connection)
    # For each album, get the discogs info and insert it into the discogs table
    for index, row in df_album.iterrows():
        # Update the progress bar
        progress_bar.progress((index + 1) / 20)
        discogs_info = get_info_album(row['id_discogs'])
        artist = discogs_info['artists'][0]['name'].replace("'", "''")
        title = discogs_info['title'].replace("'", "''")
        year = discogs_info['year']
        image = discogs_info['images'][0]['uri'] if 'images' in discogs_info and discogs_info['images'] else None
        execute_sql(connection, f"INSERT INTO discogs (id, artist, title, year, image) VALUES ({row['id_discogs']}, '{artist}', '{title}', {year}, '{image}')")
    # Close the database connection
    connection.close()
    # Clear the progress bar
    progress_bar.empty()
    