from jsonlines import jsonlines

courtlist = ['TPS', 'TPH', 'TCH', 'TNH','KSH','HLH','TPD', 'SLD', 'PCD', 'ILD','KLD', 'TYD', 'SCD', 'MLD','TCD','CHD', 'NTD', 'ULD', 'CYD', 'TND', 'KSD', 'CTD','HLD', 'TTD', 'PTD', 'PHD',
'KMH', 'LCD', 'KSY']


for i in range(len(courtlist)):
    court = courtlist[i]

    # 開啟多個json檔案(判決書)
    with open("lawjudicial_%s_tags.json" % court, "r+", encoding="utf8") as f:
        for item in jsonlines.Reader(f):
            if 'court' not in item['reason_type']: #如果不知道勝敗也沒有中性的待議判決就人工檢查是否有遺漏的關鍵字，不然就丟掉
                print(item['reason_type'], item['judge_content'])
            elif len(item['reason_type']) < 2: #如果只知道結果，沒有特徵，就人工檢查是否有遺漏的關鍵字，不然就丟掉，無法建模
                print(item['reason_type'], item['judge_content'])
            else:
                pass
