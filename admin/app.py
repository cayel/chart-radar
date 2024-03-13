import streamlit as st
import sqlite3
import pandas as pd
import os
from database_utils import create_database, drop_database, backup_database
from discogs_utils import update_discogs_id_multiple, get_info_discogs
import logging

logging.basicConfig(level=logging.INFO)

def load_ranking(connection):
    df_ranking = pd.read_sql_query("SELECT * FROM ranking", connection)
    return df_ranking

def load_album(connection):
    df_album = pd.read_sql_query("SELECT album.id_ranking,album.rank,album.id_discogs, discogs.artist, discogs.title, discogs.year, discogs.image FROM album LEFT JOIN discogs on album.id_discogs=discogs.id", connection)
    return df_album

def load_discogs(connection):
    df_discogs = pd.read_sql_query("SELECT * FROM discogs", connection)
    return df_discogs

# Create a connection to the SQLite database
database_path = "../data/database.db"

# Define the sidebar selectbox
menu = st.sidebar.selectbox(
    "Menu",
    ("Tableau de bord", "Classement", "Administration")
)

# Depending on the selection, display the corresponding page
if menu == "Tableau de bord":
    st.header("Tableau de bord")
    if not os.path.exists(database_path):
        st.error("La base de données n'existe pas à l'emplacement spécifié.")
    else:
        connection = sqlite3.connect(database_path)

        # Load the ranking data from the database
        df_ranking = load_ranking(connection)
        df_album = load_album(connection)
        df_discogs = load_discogs(connection)

        # Close the database connection
        connection.close()

        count_albums = df_album.shape[0]        
        count_albums_with_image = df_album[df_album['image'].notnull()].shape[0]
        count_albums_without_image = df_album[df_album['image'].isnull()].shape[0]        

        st.header('Statistiques générales', divider='blue')        
        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de classements", df_album['id_ranking'].nunique())
        col2.metric("Nombres d'albums", count_albums)

        st.header('Liens avec discogs', divider='blue')        
        col1, col2, col3 = st.columns(3)
        count_albums_with_discogs = df_album[df_album['id_discogs'] > 0].shape[0]
        count_albums_with_discogs_not_found = df_album[df_album['id_discogs'] == 0].shape[0]
        percentage_albums_with_discogs = 100*(count_albums_with_discogs / count_albums) 
        col1.metric("Référence Discogs", count_albums_with_discogs, f"{percentage_albums_with_discogs:.0f}%")
        col2.metric("Référence Discogs non trouvée", count_albums_with_discogs_not_found, f"{100*count_albums_with_discogs_not_found/count_albums:.0f}%")
        col3.metric("Nombre d'albums avec pochette", count_albums_with_image, f"{100*count_albums_with_image/count_albums:.0f}%")
        
        # Top 10 of most represented artists
        st.header('Top 10 des artistes', divider='blue')
        top_10_artists = df_discogs['artist'].value_counts().head(10)
        top_10_artists = top_10_artists.sort_values(ascending=False)
        # Display list in a datatable
        st.dataframe(top_10_artists)
        # Top 10 of moste represented years
        st.header('Top 10 des années', divider='blue')
        top_10_years = df_discogs['year'].value_counts().head(10)
        top_10_years = top_10_years.sort_values(ascending=False)
        # Display list in a bar chart   
        st.bar_chart(top_10_years)


        
elif menu == "Administration":
    st.header("Administration")
    if not os.path.exists(database_path):
        if st.button("Créer la base de données"):
            create_database(database_path)
            st.success(f"La base de données {database_path} a été créée.")
    else:
        if st.button("Supprimer la base de données"):
            if (drop_database(database_path) == 0) :
                st.success(f"La base de données {database_path} a été supprimée.")
            else:
                st.error(f"Une erreur est survenue lors de la suppression de la base de données.")
        if st.button("Sauvegarder la base de données"):
            if (backup_database(database_path) == 0) :
                st.success(f"La base de données {database_path} a été sauvegardée.")
            else:
                st.error(f"Une erreur est survenue lors de la sauvegarde de la base de données.")  
        if st.button("Mettre à jour les liens discogs"):
            update_discogs_id_multiple(sqlite3.connect(database_path),20)
            st.success("Les liens discogs ont été mis à jour.")
        if st.button("Mettre à jour les infos discogs"):
            get_info_discogs()
            st.success("Les infos discogs ont été mis à jour.")
elif menu == "Classement":
    st.header("Classement")
    connection = sqlite3.connect(database_path)
    df_ranking = load_ranking(connection)
    df_album = load_album(connection)
    connection.close()
    # select a ranking from the list
    ranking = st.selectbox("Classement", df_ranking['description'].unique())
    # filter the albums by ranking
    df_album_filtered = df_album[df_album['id_ranking'] == df_ranking[df_ranking['description'] == ranking].iloc[0]['id']]
    # convert year to string with no decimal
    df_album_filtered['year'] = df_album_filtered['year'].fillna(0).astype(int).astype(str)
    # display the albums in a datatable (artist, title, year) sorted by rank
    st.dataframe(df_album_filtered[['rank', 'artist', 'title', 'year']].sort_values(by='rank'),hide_index=True)


                
            
            
            

        


