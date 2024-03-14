import unittest
from album import Album

class TestAlbum(unittest.TestCase):
    def setUp(self):
        self.album = Album(1, 1, 'Artist', 'Title', 2000, '1234', 'ref1')

    def test_init(self):
        self.assertEqual(self.album.id_ranking, 1)
        self.assertEqual(self.album.rank, 1)
        self.assertEqual(self.album.artist, 'Artist')
        self.assertEqual(self.album.title, 'Title')
        self.assertEqual(self.album.year, 2000)
        self.assertEqual(self.album.id_discogs, '1234')
        self.assertEqual(self.album.reference, 'ref1')

    def test_str(self):
        expected_str = 'Album(1, 1, Artist, Title, 2000, 1234, ref1)'
        self.assertEqual(str(self.album), expected_str)

    def test_update_discogs_id(self):
        self.album.update_discogs_id('5678', 'ref2')
        self.assertEqual(self.album.id_discogs, '5678')
        self.assertEqual(self.album.reference, 'ref2')

if __name__ == '__main__':
    unittest.main()