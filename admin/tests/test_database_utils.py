import unittest
import os
import database_utils as db_utils
from  datetime import datetime
import sqlite3

class TestDatabaseUtils(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database for testing."""
        self.database_path = "test/test.db"
        db_utils.create_database(self.database_path)

    def tearDown(self):
        """Remove the temporary database after testing."""
        db_utils.drop_database(self.database_path)
        os.rmdir("test")

    # def test_create_database(self):
    #     """Test that create_database creates a database file."""
    #     db_utils.create_database(self.database_path)
    #     self.assertTrue(os.path.exists(self.database_path))
    
    # def test_execute_sql(self):
    #     """Test that execute_sql runs without errors."""
    #     connection = sqlite3.connect(self.database_path)
    #     try:
    #         db_utils.execute_sql(connection, "SELECT * FROM ranking")
    #         db_utils.execute_sql(connection, "SELECT * FROM album")
    #         db_utils.execute_sql(connection, "SELECT * FROM discogs")
    #     except sqlite3.Error as e:
    #         self.fail(f"execute_sql raised sqlite3.Error unexpectedly: {e}")
    #     finally:
    #         connection.close()
            
    # def test_drop_database(self):
    #     """Test that drop_database removes the database file."""
    #     db_utils.drop_database(self.database_path)
    #     self.assertFalse(os.path.exists(self.database_path))

    # def test_backup_database(self):
    #     """Test that backup_database creates a backup of the database."""
    #     result = db_utils.backup_database(self.database_path)
    #     self.assertEqual(result, 0)
    #     backup_path = self.database_path.replace(".db", f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}_backup.db")
    #     self.assertTrue(os.path.exists(backup_path))
    #     os.remove(backup_path)  # Clean up the backup file

if __name__ == "__main__":
    unittest.main()