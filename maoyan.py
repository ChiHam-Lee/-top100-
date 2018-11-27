import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException


def one_page_code(url):
    try:
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        page = requests.get(url,headers = header)
        if page.status_code == 200:
            return page.text
        print("Failed\n状态码为%d"%(page.status_code))
    except RequestException:
        print("Exception")

def parse_page(page_code):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)<.*?<a href.*?title="(.*?)".*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?"integer">(.*?)<.*?"fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,page_code)
    for item in items:
        yield{
            'index':item[0],
            'name':item[1],
            'actor':item[2].strip()[3:],
            'time':item[3].strip()[5:],
            'score':item[4]+item[5]
        }

def set_file(content):
    with open('movie.doc','a',encoding = 'utf-8')as f:
        f.write(json.dumps(content,ensure_ascii = False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    page_code = one_page_code(url)
    #parse_page(page_code)
    for item in parse_page(page_code):
        print(item)
        set_file(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])