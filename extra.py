from jsonlines import jsonlines
import csv
import json

# 移除list中的重複值


def del_Duplicat(list):
    return sorted(set(list), key=list.index)
    return list(set(list))


# 自動化法院及搜尋條件
courtlist = ['TPS', 'TPH', 'TCH', 'TNH','KSH','HLH','TPD', 'SLD', 'PCD', 'ILD','KLD', 'TYD', 'SCD', 'MLD','TCD','CHD', 'NTD', 'ULD', 'CYD', 'TND', 'KSD', 'CTD','HLD', 'TTD', 'PTD', 'PHD',
'KMH', 'LCD', 'KSY']


for i in range(len(courtlist)):
    court = courtlist[i]

    # 開啟多個json檔案(判決書)
    with open("lawjudicial_%s.json" % court, "r+", encoding="utf8") as f:
        for item in jsonlines.Reader(f):
            # 取json檔案的某一個項目
            content = item['judge_content']
            # 去除空格
            content = content.replace(' ', '').replace('　', '').split(',')

            # 新字典以存入新json
            case = dict()
            case['judge_id'] = item['judge_id']
            case['judge_date'] = item['judge_date']
            case['judge_reason'] = item['judge_reason']
            case['judge_content'] = item['judge_content']
            case['each_judgment_list'] = item['each_judgment_list']
            case['each_law_list'] = item['each_law_list']


            # 新list放理由分類
            reason_type_list = []
            # 開啟 CSV 檔案(特徵清單)
            with open('tags_1.csv', newline='') as csvfile:
                # 讀取 CSV 檔案內容
                taglist_1 = csv.reader(csvfile)

                # 以迴圈輸出每一個特徵
                for tag in taglist_1:
                    # print(tag)
                    keyword = tag[0]
                    reason_type = tag[1]
                    reason_name = tag[2]

                    # 判斷是否含有關鍵字，有就寫1，沒有忽略
                    if keyword in str(content):
                        reason_type_list.append(reason_type)
                        case[reason_name] = 1

                    else:
                        pass

            with open('tags_0.csv', newline='') as csvfile:
                # 讀取 CSV 檔案內容(填 0的特徵清單)
                taglist_0 = csv.reader(csvfile)

                # 以迴圈輸出每一列
                for tag in taglist_0:
                    # print(tag)
                    keyword = tag[0]
                    reason_type = tag[1]
                    reason_name = tag[2]

                    # 判斷是否含有關鍵字，有就寫0，沒有忽略
                    if keyword in str(content):
                        reason_type_list.append(reason_type)
                        case[reason_name] = 0

                    else:
                        pass

            # 產生移除重複值之後的大項清單
            case['reason_type'] = del_Duplicat(reason_type_list)

            # 寫入新的json
            with open("lawjudicial_%s_tags.json" % court, 'a', encoding='utf-8') as json_file:

                json_file.write(json.dumps(case, ensure_ascii=False) + '\n')
