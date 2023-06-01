try:
    from bs4 import BeautifulSoup
    import requests
    import bs4
    import os
    import json
    import traceback
except Exception as e:
    print('Caught exception while importing: {}'.format(e))

def make_dir(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
def write_json(filename, data):
    with open(filename, 'w', encoding='utf8') as f:

        json.dump(data, f, indent=4, ensure_ascii=False)

def read_json(filename):
    try:
        with open(filename, 'r', encoding="utf8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print('Error loading {}'.format(filename), e)
        traceback.print_exc()
        return []
def find_json(filename):
    current_path=__file__.replace(__file__.split("/")[-1], filename)
    return current_path
def request_url(url):
    session= requests.Session()
    header ={"User-Agent" : 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "Accept" : "text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,image/apng,*/*;q=0.8"}
    response = session.get(url, headers=header)
    soup=BeautifulSoup(response.text,"html.parser")
    return soup
class FilmScraper:
    def __init__(self, config):
        self.config = config
    def film_extract(self,start=1):
        url=self.config.SEARCH_URL
        save_dir=self.config.save_dir
        save_file=self.config.save_file
        base_url = self.config.BASE_URL
        print(base_url)
        make_dir(save_dir)
        url=url.format((start-1)*50 + 1)
        print(url)
        soup=request_url(url)
        elements=soup.select('span.lister-item-header')
        data=[]
        for ele in elements:
            try:
                
                a_tag = ele.select('span')[1].select('a')[0]
                
                # link=ele.select("img")[0]
                # # print(link)
                link = a_tag['href']
                # print(link)
                name = a_tag.getText()
                # print(name)
                film_link = base_url + link
                review_link = film_link.replace("?ref_=adv_li_tt","reviews?ref_=tt_urv")
                ele_data={
                    'film': name,
                    'film_link': film_link,
                    'review_link': review_link,
                    'page': start
                }
                data.append(ele_data)
            except Exception as e:
                print("Error: ", e)
                traceback.print_exc()
        filename = save_file + '_page_{}.json'.format(start)
        write_json(save_dir + '/'+filename,data)
    @property
    def film_crawler(self):
        start=self.config.start
        number=self.config.number
        for i in range(start,start+number):
            self.film_extract(start=i)
    
    
class ReviewCrawler:
    def __init__(self,config):
        self.config = config
    
    # def read_review(self,start=1):
    #     review_link = []
    #     datas = read_json(self.base_dir.format(start))
    #     for data in datas:
    #         review_link.append(data["review_link"])
    #         film = film.append(data["film"])
    #     return review_link, film
    
    def access_review(self, review_ele):
        soup = request_url(review_ele)
        elements = soup.select("div.show-more__control")
        data = []
        for ele in elements:
            text_div = ele.getText()
            if len(text_div) > 4:
                data.append(text_div)
                
        # print(data)    
        return data
        
    
    def crawl_review(self, start = 1):
        base = self.config.save_dir + "/review_page_{}.json"
        # print(base)
        save = self.config.base_dir
        datas = read_json(base.format(start))
        num_reviews = 0
        # print(datas)
        for i, data in enumerate(datas):
            review_link = data["review_link"]
            
            film = data["film"]
            
            texts = self.access_review(review_link)
            # print(texts)
            ele = {
                "film": film,
                "num_reviews": len(texts),
                "list_reviews": texts
            }
            num_reviews += len(texts)
            filename = 'film_{}.json'.format((start-1)*50+i)
            write_json(save + '/'+filename,ele)
        return num_reviews
        
    def start_crawl(self):
        make_dir(self.config.base_dir)
        start=self.config.start
        number=self.config.number
        num_reviews = 0
        no_comment = 0
        for i in range(start,start + number):
            num = self.crawl_review(start=i)
            num_reviews += num
            if (num == 0):
                no_comment += 1
            print("Crawl page {} has done".format(i+1))
            print("----------------------")
        # print("Number of reviews: ", num_reviews)
        element = {
            "num_of_reviews": num_reviews,
            "num_of_films": number*50,
            "num_of_no_comment": no_comment 
        }
        write_json(self.config.base_dir[:-7] +'/summary.json',element)