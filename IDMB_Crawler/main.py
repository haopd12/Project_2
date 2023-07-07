try:
    import os
    import argparse
    from FilmScraper import FilmScraper, ReviewCrawler 
    from config import Config
    from FilmScraper import read_json
except Exception as e:
    print("Caught exception while importing: {}".format(e))
    
if __name__ == '__main__':
    parser= argparse.ArgumentParser(description="")
    parser.add_argument('--dir', help='output dir', default='Output', type=str)
    parser.add_argument('--file', help='output file', default='review', type=str)
    parser.add_argument('-st', '--start', help="the start page for search", default=1, type=int)
    parser.add_argument('-np', '--number-of-pages', help='number of pages for search', default=8, type=int )
    args = parser.parse_args()
    print("Start crawling...")
    print(args)
    
    current_path = os.getcwd()
    save_dir = current_path + '/' + args.dir
    base_dir = current_path + '/review'
    configs = Config(base_dir = base_dir,save_dir= save_dir, save_file= args.file,start=args.start, number=args.number_of_pages)
    crawler = FilmScraper(configs)
    crawler.film_crawler
    
    r_crawler = ReviewCrawler(configs)
    # print(base_dir[:-7])
    # r_crawler.access_review('https://www.imdb.com/title/tt6791350/reviews?ref_=tt_urv')
    # r_crawler.start_crawl()