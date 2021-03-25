import jieba
from pathlib import Path
import json

def stopwordslist(filepath):#載入停用字路徑
    stopwords = [line.strip() for line in open("C:/Users/Big data/PycharmProjects/project/data/test/stopword.txt", 'r', encoding='utf-8').readlines()]
    return stopwords
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('C:/Users/Big data/PycharmProjects/project/data/test/stopword.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr
def search_result(court, reason):

    analysis_root_dir = "C:/Users/Big data/PycharmProjects/project/data/司法院法學資料庫"#指定要讀入的資料夾
    path = Path(analysis_root_dir)
    all_json_file = list(path.glob('**/*.json'))#選擇全部要讀入的json檔

    lib = {}
    for json_file in all_json_file:
        print(json_file)
        file = open(r'%s'% json_file, 'r', encoding='utf-8-sig',errors='ignore')#指定json開啟格式
        title = str(json_file)[59:-5]#指定檔名
        papers = []
        #將json拆成一行行並分別寫入dic
        for line in file.readlines():
            dic = json.loads(line)
            papers.append(dic)
            lib.update({title: papers})
            line_seg = seg_sentence(line)  # 这里的返回值是字符串
            outputs = open(r'C:/Users/Big data/PycharmProjects/project/data/after/%s.json' % title, 'a',encoding='utf-8')
            outputs.write(line_seg + '\n')
            outputs.close()
            file.close()
def main():

    courtlist = ['*']#指定search_resule的命名方式
    reasonlist = ['*']
    for court in courtlist:
        for reason in reasonlist:
            search_result(court, reason)


if __name__ == '__main__':
    main()