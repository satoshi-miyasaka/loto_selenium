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

        cur = self.conn.cursor()
        cur.execute(f'SELECT MAX({primary_key}) FROM {table}')
        max_number = cur.fetchall()[0][0]

        columns=[name for name in self.config['columns'].keys()]
        df = pandas.read_csv(url, encoding=self.encoding)
        df = df[[name for name in self.config['columns'].values()]]
        df = df.set_axis(columns, axis='columns')
        df = df.replace(r'第(\d+)回', r'\1', regex=True)
        df = df.astype(int)
        df = df[df[primary_key] > max_number]

        df.to_sql(table, con=self.conn, if_exists='append', index=False)

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
