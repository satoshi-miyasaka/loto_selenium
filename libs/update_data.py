import sqlite3
import yaml
import pandas
import re
from urllib.parse import urljoin

class UpdateData:
    loto = 'none'

    def __init__(self, config):
        self.config = config[self.loto]
        self.conn = sqlite3.connect(config['common']['database'])
        self.encoding = config['download']['encoding']

    def update(self):
        url = self.config['url']
        table = self.config['table']
        primary_key = self.config['primary_key']
        questions = ','.join(['?' for x in range(len(self.config['columns'].keys()))])

        max_sql = f'SELECT MAX({primary_key}) FROM {table}'
        insert_sql = f'INSERT INTO {table} VALUES({questions})'

        df = pandas.read_csv(url, encoding=self.encoding)
        cur = self.conn.cursor()
        cur.execute(max_sql)
        max_number = cur.fetchall()[0][0]
        for index, row in df.iterrows():
            key = row[self.config['columns'][primary_key]]
            key = int(re.search(r'\d+', key)[0])
            if key <= max_number:
                continue

            data = [re.search(r'\d+', str(row[csv_key]))[0]
                    for csv_key in self.config['columns'].values()]

            cur.execute(insert_sql, data)

        self.conn.commit()

    def __del__(self):
        self.conn.close()

class UpdateDataLoto6(UpdateData):
    loto = 'loto6'

class UpdateDataLoto7(UpdateData):
    loto = 'loto7'

with open('config.yml', 'r') as yml:
    config = yaml.safe_load(yml)

update_data = UpdateDataLoto6(config)
update_data.update()
update_data = UpdateDataLoto7(config)
update_data.update()
