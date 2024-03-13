import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sqlite3
import sys
sys.path.append('..')  # add the directory above to the path
import discogs_utils  # import the module

class TestDiscogsUtils(unittest.TestCase):
    @patch('pandas.read_sql_query')
    def test_get_first_album_without_discogs_id(self, mock_read_sql_query):
        # Arrange
        mock_df = pd.DataFrame({'id_discogs': [None, 0, 0], 'reference': [None, None, 'ref']})
        mock_read_sql_query.return_value = mock_df
        mock_connection = MagicMock(sqlite3.Connection)

        # Act
        result = discogs_utils.get_first_album_without_discogs_id(mock_connection)

        # Assert
        mock_read_sql_query.assert_called_once_with("SELECT * FROM album WHERE (id_discogs IS NULL OR (id_discogs=0 AND (reference IS NULL))) LIMIT 1", mock_connection)
        pd.testing.assert_frame_equal(result, mock_df)

if __name__ == '__main__':
    unittest.main()