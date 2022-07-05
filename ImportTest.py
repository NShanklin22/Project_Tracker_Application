import datetime
import sqlite3
import pandas as pd
import sqlalchemy
import datetime
import os
dirname = os.getcwd()
Database = os.path.join(dirname, 'data/tasks.db')

connection = sqlite3.connect(Database)
cursor = connection.cursor()
engine = sqlalchemy.create_engine(r'sqlite:///{}'.format(Database)).connect()
df = pd.read_sql_table('tasks', engine, index_col=1)

print(df.head())