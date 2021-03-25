import requests
from bs4 import BeautifulSoup
#import ssl
import os
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
url = 'https://www.ptt.cc/bbs/Beauty/index.html'

ss = requests.session()
ss.cookies['over18'] = '1'

path = r'./beauty'
if not os.path.exists(path):
    os.mkdir(path)

#res = ss.get(url, headers=headers)
#soup = BeautifulSoup(res.text, 'html.parser')

for i in range(0, 50):
    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.select('div[class="title"] a')

    for each_title in title:
        print(each_title.text)
        try:
            article_url = 'https://www.ptt.cc' + each_title['href']
            print(article_url)
            res_article = ss.get(article_url, headers=headers)
            article_soup = BeautifulSoup(res_article.text, 'html.parser')
            tem_str = article_soup.select('div[id="main-content"]')[0].text.split('--')[0]

            tag_up = 0
            tag_down = 0
            score = 0
            auth = ''
            article_name = each_title.text
            article_data = ''

            #算噓的數量
            for tag in article_soup.select('span[class ="f1 hl push-tag"]'):
                if '噓 ' in tag:
                    tag_down +=1

            #算推的數量
            for tag in article_soup.select('span[lass ="hl push-tag" ]'):
                if '推 ' in tag:
                    tag_up += 1
            score = tag_up - tag_down

            #設定作者
            article_data = article_soup.select('span[class = "article-meta-value"]')[3].text

            tem_str += '\n---split---\n'
            tem_str += '推 : %s\n'%(tag_up)
            tem_str += '噓 : %s\n'%(tag_down)
            tem_str += '分數 : %s\n'%(score)
            tem_str += '作者 : %s\n'%(auth)
            tem_str += '標題 : %s\n'%(article_name)
            tem_str += '時間 : %s'%(article_data)

            with open(path + '/' + each_title.text + '.txt', 'w', encoding = 'utf8') as f:
                f.write(tem_str)
        except KeyError as e:
            print(e.args)
        except:
             print(each_title.text)
        print()
    url_list = soup.select('div[class="btn-group btn-group-paging"] a[class="btn wide"]')
    url = 'https://www.ptt.cc' + url_list[1]['href']

#title = soup.select('')