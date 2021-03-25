import os
import ssl
import requests
from bs4 import BeautifulSoup

resource_path = r'./project'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
head_html_law = 'https://law.judicial.gov.tw/FJUD/default.aspx'
res = requests.get(head_Html_lotto, timeout=30)
ss = requests.session()

url = 'https://law.judicial.gov.tw/fonts/fontawesome-webfont.woff2?v=4.7.0'
src = "qryresultlst.aspx?ty=JUDBOOK&q=97e441703582fb2057a1003531b8baa8"
n = 10
for i in range(0,n):
    res = ss.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    article_title_html = soup.select('div[class="title"]')

    url = 'https://law.judicial.gov.tw/fonts/fontawesome-webfont.woff2?v=4.7.0' + url_list[1]['href']