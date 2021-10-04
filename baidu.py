import requests
import re
from lxml import etree

global start_url
start_url = 'http://news.baidu.com'


def parse_url(url):
    session = requests.session()
    resp = session.get(url).text
    return resp


def parse_every_model(page_source):
    html = etree.HTML(page_source)
    a_list = html.xpath('//*[@id="channel-all"]/div/ul/li//a')
    m_data = []
    for a in a_list:
        m_url = start_url + a.xpath('./@href')[0]
        m_name = a.xpath('./text()')[0]
        m_data.append({m_name: m_url})
    return m_data


def parse_data(dict):
    print('正在解析：%s' % dict)
    url = list(dict.values())[0]
    session = requests.session()
    resp = session.get(url)

    html = etree.HTML(resp.text)
    # //div[contains(@class, 'demo') and contains(@class, 'other')]
    # urls = html.xpath(
    #     '//*[@id="col_focus"]//a/@href')
    # titles = html.xpath(
    #     '//*[@id="col_focus"]//a/text()')
    urls = html.xpath(
        '//*[@id="body"]//a/@href')
    titles = html.xpath(
        '//*[@id="body"]//a/text()')
    # print(urls,titles)

    keys = ['辟谣', '举报', '二维码', '收藏本站', '搜索', '用户反馈']
    for url, title in zip(urls, titles):
        # print(len(title))
        if 'http' in url and len(title) > 4:
            print(url, title)
    print('-----------------------------------------------------')


if __name__ == '__main__':
    html_page = parse_url(start_url)
    m_data = parse_every_model(html_page)
    for data in m_data:
        parse_data(data)
