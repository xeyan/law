# pip install -U ckiptagger
# Tensorflow限定版本
# pip install tensorflow==1.13.1
# pip install gdown
# coding=utf-8
# http://ckip.iis.sinica.edu.tw/data/ckiptagger/data.zip 下載中研院CKIP斷詞資料包並解壓縮

from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import os
import json
#
# 用OS設定避免報錯
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# 讀model
ws = WS('C:\\Users\\Big data\\PycharmProjects\\Final_test\\data')  # 斷詞
pos = POS('C:\\Users\\Big data\\PycharmProjects\\Final_test\\data')  # 詞性標注
ner = NER('C:\\Users\\Big data\\PycharmProjects\\Final_test\\data')  # 實體辨識

# 設定字典
# word_to_weight = {
#     "土地公": 1,
#     "土地婆": 1,
#     "公有": 2,
#     "": 1,
#     "來亂的": "啦",
#     "緯來體育台": 1,
# }
# dictionary = construct_dictionary(word_to_weight)
# # print(dictionary)
# # 設定自訂的字典

with open(r'./mydictionary.txt', 'r', encoding='utf8') as g:
    mydictionary = g.read()
# print(mydictionary)

word_to_weight = {}
for i in mydictionary.split('\n'):
    word_to_weight[i.split(': ')[0]] = 1
# print(word_to_weight)
    dictionary = construct_dictionary(word_to_weight)
# print(dictionary)


# 開啟json檔案
with open("C:/Users/Big data/PycharmProjects/Final_test/clean_data.json", "r+", encoding="utf8") as f:
    raw_data = json.load(f)
    for item in raw_data:
        content = str(item['judge_content'])
        content = content.replace(' ', '').replace('　', '').replace('台', '臺').split(',')

        # 引入CKIP斷詞
        word_s = ws(content,
                    sentence_segmentation=True,
                    segment_delimiter_set={",", "。", ":", "?", "!", ";"},
                    coerce_dictionary=dictionary)
        print(word_s)

        # word_sentence_list = ws(content,
        # sentence_segmentation = True, # To consider delimiters
        # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}, # This is the defualt set of delimiters
        # recommend_dictionary = dictionary, # words in this dictionary are encouraged
        # coerce_dictionary = dictionary  # words in this dictionary are forced
        # )

        #
        # # 詞性標注
        # word_p = pos(word_s)
        # print(word_p)
        #
        # # 實體辨識
        # word_n = ner(word_s, word_p)
        # print(word_n)

        # # 三個功能都合在一起
        # def combine_wandp(w_list, p_list):
        #     assert len(w_list) == len(p_list)
        #     for w, p in zip(w_list, p_list):
        #         print('{}({})'.format(w, p), end='\u3000')
        #
        #
        # for i, sentence in enumerate(content):
        #     print ("'{}'".format(sentence))
        #     combine_wandp(word_s[i], word_p[i])
        #     print ()
        #     for n in sorted(word_n[i]):
        #         print (n)
        #     print ('\n')