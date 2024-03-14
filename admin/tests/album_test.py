import unittest
from album import Album
from discogs import Discogs, DiscogsInfo


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

class TestDiscogsInfo(unittest.TestCase):
    def setUp(self):
        self.discogs_info = DiscogsInfo('The Beatles', 'Abbey Road')

    def test_init(self):
        self.assertEqual(self.discogs_info.artist, 'The Beatles')
        self.assertEqual(self.discogs_info.title, 'Abbey Road')

    def test_get_info(self):
        self.assertEqual(self.discogs_info.get_info(), 0)
        self.assertEqual(self.discogs_info.reference, 'master')
        self.assertEqual(self.discogs_info.artist, 'The Beatles')
        self.assertEqual(self.discogs_info.title, 'Abbey Road')
        self.assertEqual(self.discogs_info.year, 1969)

    def test_get_info_not_found(self):
        discogs_info = DiscogsInfo('The Beatles', 'Abbey Road 123')
        self.assertEqual(discogs_info.get_info(), -1)
    
    def test_get_info_is_release(self):
        discogs_info = DiscogsInfo('Laura Veirs', 'Phone Orphans')
        self.assertEqual(discogs_info.get_info(), 0)
        self.assertEqual(discogs_info.reference, 'release')
        self.assertEqual(discogs_info.artist, 'Laura Veirs')
        self.assertEqual(discogs_info.title, 'Phone Orphans')
        self.assertEqual(discogs_info.year, 2023)

if __name__ == '__main__':
    unittest.main()