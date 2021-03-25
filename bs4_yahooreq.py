import requests
from bs4 import BeautifulSoup
import time
import re
import json
import os
from selenium import webdriver

# 建立Mongo collection
# client = MongoClient('192.168.156.101:27017') # python連mongodb
# db = client["yahoo_QA"]  # 資料庫名稱
# collect = db["Devorce_QA"]  # collection名稱 

reasonlist = ['夫妻共同財產', '離婚', '監護權']

for reason in reasonlist:
     headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
     url = 'https://tw.answers.yahoo.com/'
     user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

     options = webdriver.ChromeOptions()
     options.add_argument('user-agent=%s' % user_agent)
     browser = webdriver.Chrome(chrome_options=options)
     browser.get(url)
     cookie = browser.get_cookies()

     time.sleep(1)
     browser.find_element_by_xpath('//*[@id="searchbarContainer"]/form/input').send_keys('%s' % reason)
     browser.find_element_by_xpath('//*[@id="searchbarContainer"]/form/button').click()


     url = browser.current_url
          

     for page_number in range(1, 51):
          # 對第一頁離婚提出請求
          r = requests.get(url, headers=headers)
          soup = BeautifulSoup(r.text, 'html.parser')
          # print(soup.prettify())
          question_title_html = soup.select('a[class="fz-m ac-1st"]')
          # print(question_title_html)
          for each_question in question_title_html:
               try:
                    print()
                    time.sleep(1)
                    each_question_title = each_question.text
                    print(each_question_title) # 印出各問題標題
                    # 問題網址
                    question_url = each_question['href']
                    # 對問題網址提出請求
                    question_res = requests.get(question_url, headers = headers)
                    question_soup = BeautifulSoup(question_res.text, 'html.parser')

                    # 用 script 這個標籤來找新的網址
                    question_soup_script = question_soup.select('script')
                    string_question = str(question_soup_script)
                    question_replace_url = re.split('\"', string_question)[1] # 用正規表示法切出新網址
                    print(question_replace_url)
                    if question_replace_url == 'https://consent.cmp.oath.com/cmpStub.min.js':
                         # 直接抓出javascript內之內容
                         jsQuestion_title = re.split(r'\"', string_question)[75] # 包在javascript的標題
                         # print(jsQuestion_title)
                         jsQuestion_content = re.split(r'\"', string_question)[79] # 包在js的內容還沒處理乾淨
                         jsQuestion_clean = re.split(r'[a-z]', jsQuestion_content)
                         jsqwithlines =''.join(jsQuestion_clean)
                         jsQuestion_Cleanlines = re.split(r'\\', jsqwithlines)
                         jsQuestionwithspace = ''.join(jsQuestion_Cleanlines)
                         jsQuestion_cleanspace = re.split(r'\s', jsQuestionwithspace)
                         jsQuestion_Cleancontent = ''.join(jsQuestion_cleanspace) # 處理乾淨的JS問題內容
                         print(jsQuestion_Cleancontent)
                         dataJ = {'title' : jsQuestion_title, 
                                  'content' : jsQuestion_Cleancontent,
                                  }
                    
                    # 對新文章網址提出請求
                    question_res_new = requests.get(question_replace_url, headers = headers)
                    question_soup_new = BeautifulSoup(question_res_new.text, 'html.parser')
                    # 文章內容字串變數
                    question_contentPlus = question_soup_new.select('div[class="Question__contentWrapper___3EDuq"]')
                    for each_question_content in question_contentPlus:
                         time.sleep(1)
                         every_question_content = each_question_content.text
                         print(every_question_content) #印出問題內容

                         dataN = {'title' : each_question_title, 
                                  'content' : every_question_content,
                                  }

 
                    # 寫入json
                    with open('yahooQA_%s.json' %reason, 'a', encoding='utf-8') as f:
                         if question_replace_url != 'https://consent.cmp.oath.com/cmpStub.min.js':
                              f.write(json.dumps(dataN, ensure_ascii=False) + '\n')
                         else:
                              f.write(json.dumps(dataJ, ensure_ascii=False) + '\n')
                                             
                                  
                    print()
                    print()


               
               except AttributeError as e:
                    print('============')
                    print(each_question)
                    print(e.args)
                    print('============')
          try:
               next_page_url = soup.select('div[class="compPagination"]')[0] \
                              .select('a')[4]['href']
               url = next_page_url

               
               print('========================')
               print('已完成第 %d 頁' %(page_number))
               print('========================')
               print()
               page_number += 1
          except:
               print('This is the last page')
               pass
     browser.close()
     time.sleep(3)
