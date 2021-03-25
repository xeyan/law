import word2vec
import sklearn
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import json
from pathlib import Path
# import pandas as pd
# from jsonlines import jsonlines
import csv
import math
import winreg
# analysis_root_dir = "C:/Users/Big data/PycharmProjects/project/data/old"
# path = Path(analysis_root_dir)
# all_json_file = list(path.glob('**/*.json'))
# parse_result = []
data_path = "C:/Users/Big data/PycharmProjects/project/data/old/clean_data.json"
# print(data_path)
# lib = {}
# for json_file in all_json_file:
#     name = str(json_file)[51:-5]
#     print(data_path)
    # file = open(json_file, 'r', encoding='utf-8',errors='ignore')
    # papers = []
    # for line in file.readlines():
    #     dic = json.loads(line)
    #     papers.append(dic)
    # lib.update({name: papers})
# print(lib)
# with open("C:/Users/Big data/PycharmProjects/project/data/old/clean_data.json", "r+", encoding="utf-8") as f:
#     for item in jsonlines.Reader(f):
#         content = item['judge_content']
#         print(content)
# print(lib)
word2vec.word2vec(data_path,'corpusWord2Vec.bin', size=300, verbose=True, min_count=2)
model = word2vec.load('corpusWord2Vec.bin')
print(model.vectors)

k = 1
with open(r'C:/Users/Big data/PycharmProjects/project/data/tovec/model.csv', 'w', encoding='big5', newline='') as csvfile:
    mod = list(model.vocab)
    fieldname = ['Id', 'Label']
    writer = csv.DictWriter(csvfile, fieldname)
    writer.writeheader()
    for i in range(0,216):
        writer = csv.writer(csvfile)
        writer = writer.writerow(['%d'% k,'%s' % model.vocab[i]])
        k += 1

# vec.write(json.dumps(data,ensure_ascii=False))

index1,metrics1 = model.cosine(u'"離婚",')
index2,metrics2 = model.cosine(u"'民法")
index3,metrics3 = model.cosine(u'婚')

index01 = np.where(model.vocab == u'"離婚",')
index02 = np.where(model.vocab == u"'民法")
index03 = np.where(model.vocab == u'婚')

index001 = np.append(index1,index01)
index002 = np.append(index2,index02)
index003 = np.append(index3,index03)

rawWordVec = model.vectors
X_reduced = PCA(n_components=3).fit_transform(rawWordVec)
q = 1
with open(r'C:/Users/Big data/PycharmProjects/project/data/tovec/tovec.csv','w',encoding='big5', newline='') as csvfile:
    fieldname = ['source','target', 'value']
    writer = csv.DictWriter(csvfile, fieldname)
    writer.writeheader()
    for j in range(0,216):
        for l in range(0,10):
            index,metrics = model.cosine(model.vocab[j])
            writer = csv.writer(csvfile)
            writer = writer.writerow([q, index[l], metrics[l]])
        q += 1

zhfont = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/mingliu.ttc')

fig = plt.figure()
ax = fig.add_subplot(111)

for i in index001:
    ax.text(X_reduced[i][0], X_reduced[i][1], model.vocab[i], fontproperties=zhfont, color='C3')
for i in index002:
    ax.text(X_reduced[i][0], X_reduced[i][1], model.vocab[i], fontproperties=zhfont, color='C1')
for i in index003:
    ax.text(X_reduced[i][0], X_reduced[i][1], model.vocab[i], fontproperties=zhfont, color='C7')

ax.axis([0,0.5,-0.2,0.6])
plt.figure(figsize=(60,60))
plt.show()
