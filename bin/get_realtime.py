#!/usr/bin/env python3


import holyromanpv
import sqlalchemy
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

df = interface.get_realtime()
print(df)
df.to_sql(name='pv_realtime', con=db.engine, if_exists='append', index=False)
