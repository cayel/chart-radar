import streamlit as st
import sqlite3
import pandas as pd
import os
from database_utils import create_database, drop_database, backup_database
from discogs_utils import update_discogs_links

def load_ranking(connection):
    df_ranking = pd.read_sql_query("SELECT * FROM ranking", connection)
    return df_ranking

def load_album(connection):
    df_album = pd.read_sql_query("SELECT * FROM album LEFT JOIN discogs on id_discogs=discogs.id", connection)
    # Rename columns
    df_album.rename(columns={'artist': 'artist_old'}, inplace=True)
    df_album.rename(columns={'title': 'title_old'}, inplace=True)
    return df_album

# Create a connection to the SQLite database
database_path = "../data/database.db"

# Define the sidebar selectbox
menu = st.sidebar.selectbox(
    "Menu",
    ("Tableau de bord", "Administration")
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

        # Close the database connection
        connection.close()

        count_albums = df_album.shape[0]        
        count_albums_with_image = df_album[df_album['image'].notnull()].shape[0]
        count_albums_without_image = df_album[df_album['image'].isnull()].shape[0]        

        st.header('Statistiques générales', divider='blue')        
        col1, col2, col3 = st.columns(3)
        col1.metric("Nombres d'albums", count_albums)
        col3.metric("Nombre d'albums avec pochette", count_albums_with_image, f"{100*count_albums_with_image/count_albums:.0f}%")
        
        st.header('Liens avec discogs', divider='blue')        
        col1, col2, col3 = st.columns(3)
        count_albums_with_discogs = df_album[df_album['id_discogs'] > 0].shape[0]
        count_albums_with_discogs_not_found = df_album[df_album['id_discogs'] == 0].shape[0]
        percentage_albums_with_discogs = 100*(count_albums_with_discogs / count_albums) 
        col1.metric("Nombre d'albums avec référence", count_albums_with_discogs, f"{percentage_albums_with_discogs:.0f}%")
        col2.metric("Nombres d'albums avec référence discogs non trouvée", count_albums_with_discogs_not_found, f"{100*count_albums_with_discogs_not_found/count_albums:.0f}%")

        print(df_album)
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
            update_discogs_links()
            st.success("Les liens discogs ont été mis à jour.")
            
                
            
            
            

        


