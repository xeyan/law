from sklearn.externals import joblib #jbolib模組
import pandas as pd
import numpy as np
import csv

entering = '''女生因男生外遇而且不拿錢回家想離婚,男生卻不想離但女生沒錢請律師或徵信社之類的構成離婚要件一定要請警察捉姦在床嗎?
還是有其他因素也可以訴請離婚呢?女生該如何主張訴請離婚呢?謝謝'''

reason_path = "C:/Users/Big data/PycharmProjects/Final_test/reason.csv"


def find_factor(enter_str):
    data = {
        "input": enter_str,
        "foreigner": 0,
        "proof": 0,
        "noshow": 0,
        "lawyer_both": 0,
        "lawyer_plaintiff": 0,
        "lawyer_defendant": 0,
        "lawyer_none": 1,
        "judge_court_地方法院": 1,
        'judge_court_高等法院': 0,
        'judge_court_最高法院': 0,
        'judge_court_少年及家事法院': 0
    }
    reason_keyword = {}
    reasons = []
    # 開啟reason檔案
    with open(reason_path, newline='') as c1:
        reason_list = csv.reader(c1)
        for label in reason_list:
            keyword = label[0]
            tag_type = label[1]
            tag = label[2]

            # 判斷是否含有關鍵字，有就寫1，沒有忽略
            if keyword in enter_str:
                data[tag] = 1
                data[tag_type] = 1
                reason_keyword[tag] = keyword
                # reason_keyword[tag_type]= keyword
                reasons.append(tag)

    reasons = sorted(set(reasons), key=reasons.index)
    return data, reason_keyword, reasons


def main():
    data, reason_keyword, reasons = find_factor(entering)
    df = pd.DataFrame(data, index=[0]).drop(['input'], axis=1)

    #  載入model
    for keyreason in reasons:
        lr = joblib.load('save/s_lr_%s.pkl' % keyreason)
        put_in = df[[keyreason, 'foreigner', 'proof', 'noshow', 'lawyer_both', 'lawyer_plaintiff', 'lawyer_defendant',
                     'lawyer_none', 'judge_court_地方法院', 'judge_court_高等法院', 'judge_court_最高法院', 'judge_court_少年及家事法院']]
        # 模擬不同情況(證據,律師)
        put_in_p = [[1, put_in.at[0, 'foreigner'], 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]]
        put_in_p_b = [[1, put_in.at[0, 'foreigner'], 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]]
        put_in_p_p = [[1, put_in.at[0, 'foreigner'], 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]]
        put_in_p_d = [[1, put_in.at[0, 'foreigner'], 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]]
        put_in_p_n = [[1, put_in.at[0, 'foreigner'], 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]]

        # print('離婚理由是',reason_keyword[keyreason], '時，當沒有證據，雙方都不請律師時，您的可能勝率為', round(prob[0][1] * 100, 1), '%')
        prob0 = np.round(lr.predict_proba(put_in_p), 3)
        prob_p = np.round(lr.predict_proba(put_in_p), 3)
        prob_p_b = np.round(lr.predict_proba(put_in_p_b), 3)
        prob_p_p = np.round(lr.predict_proba(put_in_p_p), 3)
        prob_p_d = np.round(lr.predict_proba(put_in_p_d), 3)

        aa = [prob0[0][-1], prob_p[0][-1], prob_p_b[0][-1], prob_p_p[0][-1], prob_p_d[0][-1]]
        bb = ['沒證據都沒請律師','有證據都沒請律師', '有證據雙方都請律師', '有證據請律師,對方沒有請律師', '有證據,只有對方請律師']

        print('當離婚理由為', reason_keyword[keyreason], bb[aa.index(max(aa))], '時有', round(max(aa) * 100, 1), '% 的機率成功離婚')


if __name__ == '__main__':
    main()


#
# pd.DataFrame.from_dict(data)
# # 讀取Model
# lr0 = joblib.load('save/lr_abandon_t.pkl')
#
# #  預測新一筆資料
# # x = df[['abandon', 'foreigner', 'proof', 'lawyer_plaintiff', 'lawyer_no_lawyer', 'lawyer_both', 'lawyer_defendant',
# #         'judge_court_county', 'noshow', 'judge_court_high', 'judge_court_supreme']]
# put_in = [[1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]]
# prob = np.round(lr0.predict_proba(put_in), 3)
# print('模型預測雙方都不請律師時，您的可能勝率為', round(prob[0][1]*100, 1), '%')
#
# put_in = [[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0]]
# prob = np.round(lr0.predict_proba(put_in), 3)
# print('模型預測只有您請律師可能勝率為', round(prob[0][1]*100, 1), '%')
#
# put_in = [[1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]]
# prob = np.round(lr0.predict_proba(put_in), 3)
# print('模型預測雙方都請律師時，您的可能勝率為', round(prob[0][1]*100, 1), '%')
#
# put_in = [[1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]]
# prob = np.round(lr0.predict_proba(put_in), 3)
# print('模型預測只有對方請律師時，您的可能勝率為', round(prob[0][1]*100, 1), '%')
