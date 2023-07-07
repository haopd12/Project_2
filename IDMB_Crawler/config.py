try:
    import urllib
except Exception as e:
    print('Caught exception while importing: {}'.format(e))


class Config:
    SEARCH_URL = 'https://www.imdb.com/search/title/?title_type=feature&languages=en&view=simple&start={}'
    BASE_URL = 'https://www.imdb.com'

    def __init__(self, base_dir="", save_dir="", save_file="", start=1, number=8):
        self.save_dir = save_dir
        self.save_file = save_file
        self.start = start
        self.number = number
        self.base_dir = base_dir
    
    #image search url
    @property
    def search_url(self):
        return self.SEARCH_URL
    
    @property
    def base_url(self):
        return self.BASE_URL

    @property
    def image_data(self):
        return '{"option":{"save_dir":"' + self.save_dir + '","save_file":"' + self.save_file  + '"}'
    