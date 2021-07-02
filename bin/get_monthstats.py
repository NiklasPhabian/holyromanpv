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

#engine = sqlalchemy.create_engine('sqlite:///' + db_path)
db = holyromanpv.database.PostgresDatabase(config_loc, 'postgres')

interface = holyromanpv.Interface(ip=ip, port=port)

year = datetime.datetime.now().year

df = interface.get_monthstats(year=year)
print(df)
df_db = pandas.read_sql('pv_monthly', con=db.engine)
df = df.append(df_db, sort=False)
df = df[~df.duplicated(subset='timestamp')]
df.to_sql(name='pv_monthly', con=db.engine, if_exists='replace', index=False)

