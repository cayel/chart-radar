import os
import sqlite3
from datetime import datetime
import shutil

def create_database(database_path):
    # Create data directory if it does not exist
    data_directory = os.path.dirname(database_path)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)      
    # Create the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS album (id INTEGER PRIMARY KEY, artist TEXT, title TEXT, year INTEGER, id_discogs INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS discogs (id INTEGER PRIMARY KEY, artist TEXT, title TEXT, year INTEGER, image TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS ranking (id INTEGER PRIMARY KEY, id_album INTEGER, position INTEGER, date TEXT)")
    connection.commit()
    connection.close()
    
def drop_database(database_path):
    # Drop the SQLite database
    os.remove(database_path)
    return 0
    
def backup_database(database_path):
    # Backup the SQLite database
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = database_path.replace(".db", f"_{date_str}_backup.db")
    try:
        shutil.copy(database_path, backup_path)
        print(f"La base de données {database_path} a été sauvegardée sous {backup_path}.")
        return 0
    except IOError as e:
        print(f"Impossible de copier le fichier. {e}")
        return -1
    except:
        print("Une erreur inattendue est survenue lors de la copie du fichier.")
        return -1