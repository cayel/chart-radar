class Album:
    def __init__(self, id_ranking, rank, artist, title, year, id_discogs, reference):
        self.id_ranking = id_ranking
        self.rank = rank
        self.artist = artist
        self.title = title
        self.year = year
        self.id_discogs = id_discogs
        self.reference = reference

    def __str__(self):
        return f'Album({self.id_ranking}, {self.rank}, {self.artist}, {self.title}, {self.year}, {self.id_discogs}, {self.reference})'
    
    def update_discogs_id(self, id_discogs, reference):
        self.id_discogs = id_discogs
        self.reference = reference
        return 0