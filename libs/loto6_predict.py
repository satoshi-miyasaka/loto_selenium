#!/bin/python3
# 全体から最近出現率の低いボールをｎ個
# 最近出現率が低いボールをｍ個
# 選ぶボール数がｌ個として
# l - (n + m) = o で計算し、
# 最近出現率の高いボールをｏ個選ぶ
# ｎとｍのボールに重複がある場合、重複したボール数分ｏが増える

import MySQLdb
import pandas
import loto_selenium

class LotoPredict:
    all_select = 2
    new_select = 4
    total_select = 6
    last_select = 0

    def __init__(self, config):
        conn = sqlite3.connect(config.database)
        df = pandas.read_sql(f'SELECT * FROM {config.table}', conn)
        conn.close()

        self.loto_shukei = LotoShukei(df, config.ball_count)

    def predict(self):

        # STEP 1
        # total
        ball_count = self.config.ball_count

        marge_list = list(get_worst(top=n))

        # STEP 2
        # recently
        list = [i +1 for i in range(ball_count)]

        max_row = len(df)
        i = 1
        while (new_select < list.size()):
            temp_list = [n for n in list \
                    if df.iloc[max_row -i].values.tolist() not in n]
            list = temp_list
            i += 1

        marge_list = set(marge_list.extend(list))

        # STEP 3

        self.conn.commit()
    
    def get_column_list(self):
        primary_key = self.config['primary_key']
        return [key for key in self.config['columns'] if key <> primary_key]

    def get_table_all(self):
        table = self.config['table']
        primary_key = self.config['primary_key']
        columns = ','.join(get_column_list())

        return pandas.read_sql(f'SELECT {columns} FROM {table}', self.conn)

    def big_select(self, df: Dataframe, ball_count: int):
        dict = {str(i +1):0 for i in range(ball_count)}
        for row in data:
            for col in row:
                dict[str(col)] += 1

        sort_list = [int(n) for n, m in sorted(dict.items(), key=lambda x:x[1])]
        return [n for n in sort_list in 0 < n]
        
    def __del__(self):
        self.conn.close()

