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

def insert_fake_data(connection):
    """Insert fake data into the tables."""
    execute_sql(connection, "INSERT INTO ranking (id, name, description, url, style, year, date, language, created_date, active) VALUES ('test', 'Test', 'Test', 'http://test.com', 'Test', 2021, '2021-01-01', 'fr', '2021-01-01 00:00:00', 1)")
    execute_sql(connection, "INSERT INTO album (id_ranking, rank, artist, title, year, id_discogs) VALUES ('test', 1, 'Test', 'Test', 2021, 1)")
    execute_sql(connection, "INSERT INTO discogs (id, artist, title, year, image) VALUES (1, 'Test', 'Test', 2021, 'http://test.com')")

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
    insert_fake_data(connection)
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