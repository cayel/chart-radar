import os
import sqlite3
from datetime import datetime
import shutil

def execute_sql(connection, query):
    """Execute a SQL query."""
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def create_table_ranking(connection):
    """Create the ranking table."""
    execute_sql(connection, "CREATE TABLE IF NOT EXISTS ranking ( id TEXT PRIMARY KEY, name TEXT, description TEXT, url TEXT, style TEXT, year INTEGER, date DATE, language TEXT, created_date TIMESTAMP, active BOOLEAN DEFAULT 0)")

def create_table_album(connection):
    """Create the album table."""
    execute_sql(connection, "CREATE TABLE IF NOT EXISTS album (id INTEGER PRIMARY KEY AUTOINCREMENT, id_ranking TEXT, rank INTEGER, artist TEXT, title TEXT, year INTEGER, id_discogs INTEGER, reference TEXT)")

def create_table_discogs(connection):
    """Create the discogs table."""
    execute_sql(connection, "CREATE TABLE IF NOT EXISTS discogs (id INTEGER PRIMARY KEY, artist TEXT, title TEXT, year INTEGER, image TEXT)")

def populate_database(connection):
    # Insert fake ranking
    execute_sql(connection, "INSERT INTO ranking (id, name, description, url, style, year, date, language, created_date, active) VALUES ('628cf492-5001-4e6c-9c3a-4db5d531f33a','Mes Tops', 'Mes 10 meilleurs albums de tous les temps', '', '',0,'2021-01-01','fr','2024-03-14', 1)")
    # Insert fake album without discogs id
    execute_sql(connection, "INSERT INTO album (id_ranking, rank, artist, title, year, id_discogs, reference) VALUES ( '628cf492-5001-4e6c-9c3a-4db5d531f33a', 1, 'The Cure', 'Disintegration', 1989, NULL, NULL)")    
    execute_sql(connection, "INSERT INTO album (id_ranking, rank, artist, title, year, id_discogs, reference) VALUES ( '628cf492-5001-4e6c-9c3a-4db5d531f33a', 2, 'Joy Division', 'Closer', 1980, NULL, NULL)")    
    execute_sql(connection, "INSERT INTO album (id_ranking, rank, artist, title, year, id_discogs, reference) VALUES ( '628cf492-5001-4e6c-9c3a-4db5d531f33a', 3, 'Nirvana', 'Nevermind', 0, NULL, NULL)")    
        
def create_database(database_path):
    # Create data directory if it does not exist
    data_directory = os.path.dirname(database_path)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)      
    # Create the SQLite database
    connection = sqlite3.connect(database_path)
    create_table_ranking(connection)
    create_table_album(connection)
    create_table_discogs(connection)
    connection.commit()
    connection.close()
    
def create_test_database(database_path):
    if os.path.exists(database_path):
        drop_database(database_path)
    create_database(database_path)
    connection = sqlite3.connect(database_path)
    populate_database(connection)
    connection.close()
    return 0
       
def drop_database(database_path):
    # Check if the database exists
    if not os.path.exists(database_path):
        return -1

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