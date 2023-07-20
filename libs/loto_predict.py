#!/bin/python3
# 全体から最近出現率の低いボールをｎ個
# 最近出現率が低いボールをｍ個
# 選ぶボール数がｌ個として
# l - (n + m) = o で計算し、
# 最近出現率の高いボールをｏ個選ぶ
# ｎとｍのボールに重複がある場合、重複したボール数分ｏが増える

from . import loto_shukei
import pandas
import sqlite3
import yaml

class LotoPredict:
    loto = 'None'

    def __init__(self, config):
        self.config = config[self.loto]
        conn = sqlite3.connect(config['common']['database'])
        df = pandas.read_sql(f'SELECT * FROM {self.config["table"]}', conn)
        conn.close()

        self.loto_shukei = loto_shukei.LotoShukei(df, self.config['ball_count'])

    def predict(self):

        # STEP 1
        # total
        ball_count = self.config['ball_count']

        marge_list = list(self.loto_shukei.get_worst(top=self.config['low_count']))

        # STEP 2
        # recently
        marge_list = list(set(marge_list + list(self.loto_shukei.get_worst_4_top(top=self.config['hi_count']))))

        # STEP 3
        temp_list = []
        limit_up = self.config['select_count'] - len(marge_list)
        while True:
            temp_list = list(self.loto_shukei.get_best_4_top(limit=limit_up))
            if self.config['select_count'] <= len(set(marge_list + temp_list)): break
            limit_up += 1

        temp_list = [x for x in temp_list if not (x in marge_list)]

        return marge_list + temp_list[:self.config['select_count'] - len(marge_list)]

class Loto6Predict(LotoPredict):
    loto = 'loto6'

class Loto7Predict(LotoPredict):
    loto = 'loto7'

if __name__ == '__main__':
    with open('config.yml', 'r') as yml:
        config = yaml.safe_load(yml)

    predict = Loto7Predict(config)
    print(predict.predict())
