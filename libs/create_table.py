import sqlite3
import yaml
import pandas

def create_database(config):
    conn = sqlite3.connect(config['common']['database'])
    cur = conn.cursor()
    return conn, cur

def create_table(cur, config):
    primary_key = config['primary_key']
    table = config['table']
    columns = ','.join([x + ' INTEGER' for x in config['columns'].keys()])

    sql = f'CREATE TABLE {table} ({columns}, PRIMARY KEY({primary_key}))'
    cur.execute(sql)

def insert_data(cur, config):
    table = config['table']
    questions = ','.join(['?' for x in range(len(config['columns'].keys()))])

    df = pandas.read_csv(config['csv'], header=None, index_col=0)
    insert = f'INSERT INTO {table} VALUES({questions})'

    for row in df.itertuples(name=None):
        cur.execute(insert, row)

    conn.commit()

def close():
    conn.close()

with open('config.yml', 'r') as yml:
    config = yaml.safe_load(yml)

conn, cur = create_database(config)

create_table(cur, config['loto6'])
insert_data(cur, config['loto6'])

create_table(cur, config['loto7'])
insert_data(cur, config['loto7'])

close()

