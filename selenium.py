from selenium import webdriver
from selenium.webdriver.support.ui import Select
from random import randint
import time
import csv
import os

url = 'https://law.judicial.gov.tw/FJUD/default_AD.aspx'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument('user-agent=%s' % user_agent)

# 搜尋條件
court = 'TPD'
year = 108
reason = '離婚'

if os.path.isfile('./lawjudicial_%s_%s.csv' %(court, reason)):
    os.remove('lawjudicial_%s_%s.csv' %(court, reason))
    print('File deleted')

for year in range(89, year+1):
    for month in range(1, 13):
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        cookie = browser.get_cookies()

        Select(browser.find_element_by_name('jud_court')).select_by_value('%s' % court)
        browser.find_element_by_name('dy1').send_keys('%d' % year)
        browser.find_element_by_name('dy2').send_keys('%d' % year)

        browser.find_element_by_name('dm1').send_keys('%d' % month)
        browser.find_element_by_name('dm2').send_keys('%d' % month)
        browser.find_element_by_name('jud_title').send_keys('%s' % reason)
        browser.find_element_by_name('ctl00$cp_content$btnQry').click()
        print('民國 %d 年 %d 月' % (year, month))
        try:
            browser.switch_to.frame(browser.find_element_by_id('iframe-data'))
            browser.find_elements_by_id('hlTitle')[0].click()

            # 總資料量
            total_number = int(browser.find_element_by_id('plPager').text.split()[3])

            each_judgment_list = []
            each_law_list = []

            for i in range(total_number):
                time.sleep(randint(1, 3))

                # 找判決書內容
                judge_id = browser.find_elements_by_class_name('col-td')[0].text
                judge_date = browser.find_elements_by_class_name('col-td')[1].text
                judge_reason = browser.find_elements_by_class_name('col-td')[2].text
                judge_content = ' '.join(browser.find_elements_by_xpath('//div[@class="text-pre text-pre-in"]')[0].text.split())

                find_targets = browser.find_elements_by_css_selector('div.panel-body ul li')
                find_laws = browser.find_elements_by_css_selector('ul.rela-law li')

                # print("Judgments amount: ", len(find_targets)-len(find_laws))
                # print("Laws amount: ", len(find_laws))

                for index in range(len(find_targets)):
                    # 找歷審裁判
                    if index < len(find_targets) - len(find_laws):
                        each_judgment_list.append(find_targets[index].text)
                    # 找相關法條
                    else:
                        each_law_list.append(find_targets[index].text)

                # 寫入csv
                with open('lawjudicial_%s_%s.csv' %(court, reason), 'a', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([judge_id, judge_date, judge_reason, judge_content, each_judgment_list, each_law_list])

                each_judgment_list.clear()
                each_law_list.clear()

                print('已完成第 %d / %d 筆' % (i + 1, total_number))

                # 換頁
                try:
                    browser.find_element_by_id('hlNext').click()
                except:
                    print('This is the last page')
                    print('Completed!!')
                    print('')
                    pass
        except:
            print('查無資料')
            print('')
            pass

        browser.close()