import json

import pymongo
import requests
from requests import RequestException
from pyquery import PyQuery


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None


def parse_one_page(html):
    doc = PyQuery(html)
    index_list = doc('dd>i').text().split()
    image_list = list(doc('dd .board-img').items())
    name_list = doc('dd .name').text().split()
    actor_list = doc('dd .star').text().split()
    time_list = doc('.releasetime').text().split()
    score_list = doc('.score').text().split()
    for index,image,name,actor,time,score in zip(index_list,image_list,name_list,actor_list,time_list,score_list):
        yield {
            'index':index,
            'image':image.attr('data-src'),
            'name':name,
            'actor':actor[3:],
            'time':time[5:],
            'score':score
        }
MONGO_URL = 'localhost'
MONGO_DB = 'maoyan'
MONGO_COLLECTION = 'movies'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def save_to_mongo(item):
    try:
        db[MONGO_COLLECTION].insert_one(item)
        print('存储到Mongo成功')
    except Exception:
        print('存储到Mongo失败')


# def write_to_file(item):
#     with open('movie.txt','a',encoding='utf-8') as fa:
#         fa.write(json.dumps(item,ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        save_to_mongo(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    