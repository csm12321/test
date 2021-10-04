import pymysql
import requests
import re
from lxml import etree
import redis
from pymongo import MongoClient


class conectmysql(object):

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  database='news',
                                  user='root',
                                  password='123456',
                                  charset='utf8')
        # 创建游标指针
        self.cursor = self.db.cursor()

    def insert(self, data):
        sql = '''
            insert into news_detail (detail_url)values(%s)
            '''
        self.cursor.execute(sql, data)
        self.db.commit()  # 提交操作


class conectmongodb(object):
    def __init__(self):
        """初始化"""
        self.client = MongoClient('mongodb://127.0.0.1:27017')
        self.data = self.client['news']['news_detail']

    def __del__(self):
        # 关闭数据库连接
        self.client.close()

    def insert(self, data):
        self.data.insert_one({'url': data})


class conectredis(object):
    def __init__(self, host='127.0.0.1', port='6379'):
        self.db = redis.StrictRedis(host=host, port=port,db=0)

    def insert(self, data):
        self.db.rpush('news_url',data)


def parse_url(url):
    resp = requests.get(url)
    html = etree.HTML(resp.text)
    model_urls = html.xpath('//*[@id="blk_cNav2_01"]/div/a/@href')
    return model_urls


def parse_every_model(url):
    key = str(url).split('cn/')[1].split('/')[0]
    session = requests.session()
    resp = session.get(url)
    html = etree.HTML(resp.text)
    if key == 'china':
        detail_urls = html.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/a/@href')
        return detail_urls
    elif key == 'world':
        detail_urls = html.xpath('/html/body/div[5]/div[1]/div[1]/div[1]/div[2]//h2/a/@href')
        return detail_urls
    else:
        pass


def parse_data(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    html = etree.HTML(resp.text)
    title = html.xpath('/html/body/div[2]/h1/text()')
    content = html.xpath('//*[@id="article"]//text()')
    title = re.sub(r'[\':\s ,]*', '', str(title)).replace('\\u200b', '')
    content = re.sub(r'[\':\s ,*\\ntxa]*', '', str(content)).replace('u3000', '  ')
    return title, content


def save_redis(data):
    data = ''.join(data)
    database = conectredis()
    database.insert(data)

def save_mongo(data):
    database = conectmongodb()
    database.insert(data)


def save_mysql(data):
    database = conectmysql()
    database.insert(data)


if __name__ == '__main__':
    start_url = 'https://news.sina.com.cn/'
    model_urls = parse_url(start_url)
    a = [3, 4]
    detail_urls = []
    for i in a:
        m_url = model_urls[i]
        detail_urls.append(parse_every_model(m_url))
    urls = []
    for d_urls in detail_urls:
        for d_url in d_urls:
            urls.append(d_url)
            save_redis(d_url)

            # save_mongo(d_url)
            # save_mysql(d_url)
            # parse_data(d_url)
            print('OK')
