import sqlite3
import yaml
import pandas

def create_database(config):
    return sqlite3.connect(config['common']['database'])

def create_table(conn, config):
    primary_key = config['primary_key']
    table = config['table']
    columns = ','.join([x + ' INTEGER' for x in config['columns'].keys()])

    sql = f'CREATE TABLE {table} ({columns}, PRIMARY KEY({primary_key}))'
    conn.execute(sql)

def insert_data(conn, config):
    columns=[name for name in config['columns'].keys()]
    df = pandas.read_csv(config['csv'], header=None)
    df2 = df.set_axis(columns, axis='columns')
    df2.to_sql(config['table'], con=conn, if_exists='append', index=False)

def close(conn):
    conn.close()

with open('config.yml', 'r') as yml:
    config = yaml.safe_load(yml)

conn = create_database(config)

create_table(conn, config['loto6'])
insert_data(conn, config['loto6'])

create_table(conn, config['loto7'])
insert_data(conn, config['loto7'])

close(conn)

