import os
import bs4
import os
import json
import pandas as pd
import traceback
def make_dir(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
def write_json(filename, data):
    with open(filename, 'w', encoding='utf8') as f:

        json.dump(data, f, ensure_ascii=False)

def read_json(filename):
    try:
        with open(filename, 'r', encoding = 'utf8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print('Error loading {}'.format(filename), e)
        traceback.print_exc()
        return []
def find_json(filename):
    current_path=__file__.replace(__file__.split("/")[-1], filename)
    return current_path

class Text2Csv:
    def __init__(self,base_dir):
        self.base_dir = base_dir
    def read_review(self,path):
        data = read_json(path)
        # print(type(data))
        list_reviews = data["list_reviews"]
        csv = []
        for i, row in enumerate(list_reviews):
            csv.append(
                {
                    "film": path[-11:-5],
                    "raw_review": row
                }
            )
        # print(csv)
        return csv
    def write_csv_pineline(self):
        path = self.base_dir + "/review/film_{}.json"
        print(path)
        csv = []
        for i in range(0,499):
            print(path.format(i))
            data = self.read_review(path.format(i))
            csv = csv +data
            print("done i")
            print("------------------------")
        df = pd.DataFrame(csv)
        df.to_csv("./final.csv", index=False)




