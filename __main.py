import configparser
import pandas
from urllib.parse import urljoin

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

url = config['download']['loto6']
encoding = config['download']['encoding']

df = pandas.read_csv(url, encoding=encoding)



