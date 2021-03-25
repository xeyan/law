import jieba.analyse
from wordcloud import WordCloud

import os
import json
from pathlib import Path
import jieba.posseg as pseg
import csv
import math
from multiprocessing import Pool,cpu_count,Queue,Manager
import pandas as pd
import sys
import time
import multiprocessing as mp
import codecs

data_file = "C:/Users/Big data/PycharmProjects/project/data/clean_data/clean_raw.txt"
clean_data_path = "C:/Users/Big data/PycharmProjects/project/data/clean_data/clean_final_data.txt"
jieba.load_userdict(r'C:/Users/Big data/PycharmProjects/project/data/old/dic.txt')
jieba.analyse.set_stop_words(r'C:/Users/Big data/PycharmProjects/project/data/old/stopword.txt')

# with open("C:/Users/Big data/PycharmProjects/project/data/clean_data/clean_raw.txt", 'r', encoding='utf-8', errors='ignore') as f:
    # for libs in iter(lambda: f.read(1024), ''):
    # lib = f.readlines()
# print(lib)
# print(type(lib))
# analysis_root_dir = "C:/Users/Big data/PycharmProjects/project/data/old"
# path = Path(analysis_root_dir)
# all_json_file = list(path.glob('**/*.json'))
# parse_result = []
# clean_data = {}
# for json_file in all_json_file:
#     name = str(json_file)[51:-5]
#     # print(data_path)
#     file = open(json_file, 'r', encoding='utf-8',errors='ignore')
#     papers = []
#     for line in file.readlines():
#         dic = json.loads(line)
#         papers.append(dic)
#         clean_data.update({name: papers})
#         # print(line)
#         # clean_data = str(clean_data)
#         # print(dic)
#         # print(papers)
#         print(clean_data)
# clean_data = str(clean_data)
# clean_data_path = "C:/Users/Big data/PycharmProjects/project/data/raw_data.json"
# with open(clean_data_path, encoding='utf-8') as c:
#     while True:
#         for block in c.readlines():
#             clean_data = json.loads(block)
#             if not clean_data:
#                 break
# with open(clean_data_path, encoding='utf-8') as c:
#     clean_data = json.loads(c.read())
# clean_data = open("C:/Users/Big data/PycharmProjects/project/data/clean_data/clean_raw.txt",'r', encoding='utf-8', errors='ignore').read()
# print(clean_data)
# for i in lib:

# lib = []

# def jieb(raw_data):
# with open(raw_data_path, encoding='utf-8', errors='ignore') as r:
#     raw_data = r.readlines()
#         # 將"judge_date"民國時間轉換成西元時間
#     for item in raw_data:
#         lib.append(item)
#         # print(lib)
#         # print(item)
#     # return lib
#
#
# # def wordc(jieb):
#
#
# #     print(lib)
#
#     # dates = list(jieba.cut_for_search(lib))
#     # print(dates)
#
#
#
#
# # clean_data = str(lib)
# # clean_data = str(lib)
# # text = []
# # stopwords = []
# #         print(lib)
# #     wordcl = []
#     # print(jieb)
#     #     print(lib)
#     #     print(type(lib))
#     str_load = jieba.cut_for_search(lib)
#         # str_load_1 = str(''.join(str_load))
#         # print(str_load)
#
#         # print('/'.join(s.decode('utf-8', 'ignore') for s in str_load))
#     # key_word_1 = jieba.analyse.extract_tags(str_load,topK=20, withWeight=False, allowPOS=())
#     # data_1 = jieba.cut(lib, cut_all=True)
# # word_freq = {}
# #     total = len(list(jieba.cut_for_search(lib)))
# #     get_cut = math.ceil(total*0.1)
#     tags = jieba.analyse.extract_tags(lib,topK=50, withWeight=False, allowPOS=())
#     # print(tags)
#     #     key_word_1 = str(tags)
#     # print(key_word_1)
# # print(tags)
# # print('load_userdict後:'+"".join(str_load))
# # print(key_word_1)
#     print('load_cut後:'+"".join(str_load))
#     print('關鍵詞:'+"/".join(tags))
#     for tag,weights in tags:
#         print(tag+","+str(int(weights * 1000)))
#         # pcd_p = WordCloud(font_path='mingliu.ttc').generate(key_word_1)
#         # pcd_p.to_file('C:/Users/Big data/PycharmProjects/project/data/clean_data/clean_data.png')
#         weights = str(weights)
#         with open(r'C:/Users/Big data/PycharmProjects/project/data/clean_data/word.csv', 'a', encoding='utf-8', errors='ignore', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['%s' % tag, '%s' % weights])
#     # wordcl.append(''.join(str_load))
#     # print(wordcl)
# #     return lib

def extract_keyword(input_string):
    print("Do task by process {proc}".format(proc=os.getpid()))
    tags = jieba.analyse.extract_tags(input_string, topK=100)
    tfid = jieba.analyse.TFIDF(idf_path=None)
    print("key words:{kw}".format(kw=" ".join(tags)))
    print('TFIDF:'+"/".join(tfid))

    return tags
#def parallel_extract_keyword(input_string,out_file):
def parallel_extract_keyword(input_string):
    print("Do task by process {proc}".format(proc=os.getpid()))
    tags = jieba.analyse.extract_tags(input_string, topK=100)

    #time.sleep(random.random())
    print("key words:{kw}".format(kw=" ".join(tags)))
    o_f = open(clean_data_path,'w', encoding='utf-8')
    o_f.write(" ".join(tags)+"\n")
    return tags

# def main():
    # 載入Raw data
    # with open(raw_data_path, encoding='utf-8', errors='ignore') as r:
    #     raw_data = r.readlines()
    # trans_data = jieb(raw_data)
    # print(len(trans_data))


    # 輸出檔案
    # final_data = []
    # for i in trans_data:
    #     # if len(i['reason_type']) >= 2:
    #     if 'win_lose' in dict.keys(i):
    #         final_data.append(i)
    #
    # print(len(final_data))
    # json.dump(final_data, open(clean_data_path, 'w',encoding='utf-8'), ensure_ascii=False)
    # print('檔案輸出成功')
#
#
if __name__ == '__main__':
    # main()

    data_file = sys.argv[0]
    with codecs.open(r"C:/Users/Big data/PycharmProjects/project/data/old/final_data.txt", 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        f.close()

    out_put = data_file.split('.')[0] +"_tags.txt"
    t0 = time.time()
    for line in lines:
        parallel_extract_keyword(line)
        #parallel_extract_keyword(line,out_put)
        #extract_keyword(line)
    print("序列處理花費時間{t}".format(t=time.time()-t0))

    pool = Pool(processes=int(mp.cpu_count()*0.7))
    t1 = time.time()
    #for line in lines:
        #pool.apply_async(parallel_extract_keyword,(line,out_put))
    #儲存處理的結果，可以方便輸出到檔案
    res = pool.map(parallel_extract_keyword,lines)
    print("Print keywords:")
    for tag in res:
        print(" ".join(tag))
    pool.close()
    pool.join()
    print("並行處理花費時間{t}s".format(t=time.time()-t1))

    with open(r"C:/Users/Big data/PycharmProjects/project/data/old/clean_data.txt", 'w', encoding='utf-8', errors='ignore') as h:
        h.writelines()
