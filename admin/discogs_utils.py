import requests
from dotenv import load_dotenv
import os
import pandas as pd
import sqlite3
from database_utils import execute_sql
import streamlit as st
import logging
from album import Album
from discogs import Discogs
    
database_path = "../data/database.db"
    
def update_album_link(connection, id_album, id_discogs, reference):
    execute_sql(connection, f"UPDATE album SET id_discogs = {id_discogs}, reference = '{reference}' WHERE id = {id_album}")
 
def get_first_album_without_discogs_id(connection):
    logging.info("Getting the first album without a Discogs ID...")
    row_album = pd.read_sql_query("SELECT * FROM album WHERE (id_discogs IS NULL OR (id_discogs=0 AND (reference IS NULL))) LIMIT 1", connection)
    logging.info(f"Retrieved album: {row_album}")
    return row_album

def get_discogs_id(row_album):
    discogs = Discogs()
    logging.info("Getting Discogs ID...")
    if row_album['id_discogs'].isnull().any() or ((row_album['id_discogs'] == 0).any() and row_album['reference'].isnull().any()):
        discogs_id = discogs.search_and_get_master_id(row_album['artist'], row_album['title'])
        if discogs_id is not None:
            # Album found on Discogs
            logging.info(f"Album found on Discogs with master ID: {discogs_id}")
            return discogs_id, 'master'
        else:
            # Album not found on Discogs
            discogs_id = discogs.search_and_get_release_id(row_album['artist'], row_album['title'])
            if discogs_id is not None:
                logging.info(f"Album found on Discogs with release ID: {discogs_id}")
                return discogs_id, 'release'
            else:
                # Album not found on Discogs
                logging.info("Album not found on Discogs.")
                return 0, ''
    logging.info(f"Returning existing Discogs ID: {row_album['id_discogs']}")
    return row_album['id_discogs'], row_album['reference']

def update_discogs_id(connection, id_album, id_discogs, reference):
    try:
        logging.info(f"Updating Discogs ID for album ID: {id_album}...")
        execute_sql(connection, f"UPDATE album SET id_discogs = {id_discogs}, reference = '{reference}' WHERE id = {id_album}")
        logging.info(f"Updated Discogs ID to {id_discogs} and reference to {reference} for album ID: {id_album}")
    except Exception as e:
        logging.error(f"An error occurred while updating Discogs ID for album ID: {id_album}: {e}")

def calculate_discogs_id(connection):
    # Create a progress bar
    progress_bar = st.progress(0)
    # Load the first album without discogs id
    row_album = get_first_album_without_discogs_id(connection)
    if not row_album.empty:        
        id_discogs, reference = get_discogs_id(row_album)
        update_discogs_id(connection, row_album['id'].iloc[0], id_discogs, reference)
    else:
        logging.info("No album without Discogs ID found.")
    # Clear the progress bar
    progress_bar.empty()

def update_discogs_id_multiple(connection, number_of_updates=10):
    # Create a progress bar
    progress_bar = st.progress(0)
    # Call 10 times the function update_discogs_id
    for i in range(number_of_updates):
        calculate_discogs_id(connection)
        progress_bar.progress((i + 1) / number_of_updates)
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
    