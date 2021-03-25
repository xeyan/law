import pandas as pd
import numpy as np
import csv

minsize = 5
ref_path = "C:/Users/Big data/PycharmProjects/Final_test/indexword_%s.csv" % minsize
links_path = "C:/Users/Big data/PycharmProjects/Final_test/links_%s.csv" % minsize
reason_path = "C:/Users/Big data/PycharmProjects/Final_test/reason.csv"
reasonplus_path = "C:/Users/Big data/PycharmProjects/Final_test/reasonplus_%s.csv" % minsize
reasonplusinrow_path = "C:/Users/Big data/PycharmProjects/Final_test/reasonplusinrow_%s.csv" % minsize
reasonpluspick_path = "C:/Users/Big data/PycharmProjects/Final_test/reasonpluspick_%s.csv" % minsize

# 字典{編號:文字}
def find_word(r_path):
    word = {}
    with open(r_path, newline='', encoding='utf-8') as c1:
        word_list = csv.reader(c1)
        for label in word_list:
            word[label[0]] = label[1]
    print(word)
    return word


# word_list = [編號,編號] dict = {編號:字}
def links(path, dict):
    wordlink = []
    with open(path, newline='') as c1:
        word_list = csv.reader(c1)
        try:
            for label in word_list:
                link = dict[label[0]], dict[label[1]], label[2]
                wordlink.append(link)
        except KeyError:
            pass

    return wordlink


# 原本的csvlabel [字, tagtype, tag] wordlink i [[字, 字, 相關性]]


def main():
    ref = find_word(ref_path)
    words = links(links_path, ref)
    keytag = []
    wordslink = []
    with open(reason_path, newline='', encoding='utf-8') as r1:
        word_list = csv.reader(r1)
        for label in word_list:
            print('I am label', label[0])
            keytag.append(label[0])
    for i in range(len(words)):
        if words[i][0].replace(',', '') in keytag:
            wordslink.append(words[i])
        elif words[i][1].replace(',', '') in keytag:
            wordslink.append(words[i])


    with open(reasonplus_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in words:
            writer.writerow(row)

    with open(reasonpluspick_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in wordslink:
            writer.writerow(row)


if __name__ == '__main__':
    main()



#
#
# with open('output.csv', 'w', newline='') as csvfile:
#   # 定義欄位
#   fieldnames = ['姓名', '身高', '體重']
#
#   # 將 dictionary 寫入 CSV 檔
#   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#   # 寫入第一列的欄位名稱
#   writer.writeheader()
#
#   # 寫入資料
#   writer.writerow({'姓名': '令狐沖', '身高': 175, '體重': 60})
#   writer.writerow({'姓名': '岳靈珊', '身高': 165, '體重': 57})
