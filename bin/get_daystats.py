#!/usr/bin/python3

import holyromanpv
import sqlalchemy
import pandas
import datetime
import os 

home = os.path.expanduser("~")
config_loc = home + '/holyromanpv/data/config.ini'
config_file = holyromanpv.config.get_config(config_loc)

db_path = config_file['sqlite']['dbpath']
ip = config_file['smartplug']['ip']
port = int(config_file['smartplug']['port'])

engine = sqlalchemy.create_engine('sqlite:///' + db_path)
interface = holyromanpv.Interface(ip=ip, port=port)

year = datetime.datetime.now().year
month = datetime.datetime.now().month

df = interface.get_daystats(year=year, month=month)
print(df)
df_db = pandas.read_sql('day', con=engine)
df = df.append(df_db, sort=False)
df = df[~df.duplicated(subset='timestamp')]
df.to_sql(name='day', con=engine, if_exists='replace', index=False)
