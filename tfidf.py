from pathlib import Path
import os
import jieba
import jieba.posseg as pseg
import sys
import string
from openpyxl import load_workbook, Workbook
import xlwt
import json
import time
import operator
from sklearn import feature_extraction
from operator import itemgetter, attrgetter
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
side = "C:/Users/Big data/PycharmProjects/project/data/after/"
path = Path(side)
all_file = list(path.glob('**/*.json'))
parse = []
lib = {}

sFilePath = './tfidf'
if not os.path.exists(sFilePath):
    os.mkdir(sFilePath)

sFilePath_1 = './tfidffile'
if not os.path.exists(sFilePath_1):
    os.mkdir(sFilePath_1)

data = {}

for files in all_file:
    title = str(files)[59:-4]
    # print(files)
    files_1 = open(r'%s'%files,'r',encoding='utf-8',errors='ignore').read()
    # print(files_1)
    corpus = [files_1]
    # print(corpus)
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()  # 所有文件的關鍵字
    weight = tfidf.toarray()  # 對應的tfidf矩陣
    # print(tfidf)
    # print(len(word))
    # print(tfidf)
#   將每份文件的TF-IDF寫入tfidffile資料夾中保存
    for i in range(len(weight)):
        i = str(i)
        print(u"Writing all the tf-idf in the", i, u" file into ", sFilePath+'/'+str.zfill(i, 5)+'.json')
        with open(sFilePath + '/' + str.zfill(i, 5) + '.json', 'a+', encoding='utf-8', errors='ignore') as json_file:
            for j in range(len(word)):
                i = int(i)
                j = int(j)
                j_1 = str(weight[i][j])
                data[str(word[j])] = float(j_1)
                data_order = {k: v for k, v in sorted(data.items(), key=lambda x: x[1], reverse=True)}
                print(data_order)
                # data = {str(word[j]), float(j_1)}
                json_file.write(json.dumps(data_order, ensure_ascii=False))
            # json_file.close()


# print(data_order)
#                 # [[word,score],[],[],[]]
