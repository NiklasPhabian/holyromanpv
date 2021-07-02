#!/usr/bin/python3

import holyromanpv
import os


home = os.path.expanduser("~")
config_loc = home + '/holyromanpv/data/config.ini'
config_file = holyromanpv.config.get_config(config_loc)
db_path = config_file['sqlite']['dbpath']
www_folder = config_file['www']['folder']

#db = holyromanpv.database.SQLiteDatabase(db_path)
db = holyromanpv.database.PostgresDatabase(config_loc, 'postgres')
solar_table = holyromanpv.database.SolarTable(db)
sce_table = holyromanpv.database.SceTable(db)

timestamp, power = solar_table.latest()
sce_timestamp = sce_table.latest_entry()

power = round(power*10)/10
day_tab = holyromanpv.database.DBTable(db)
avg_day_prod = day_tab.get_value('SELECT avg(energy) FROM pv_daily')
avg_day_prod = round(avg_day_prod * 100)/100

avg_day_cons_before = sce_table.avg_daily('2019-04-01', '2020-02-01')[0]
avg_day_cons_before = round(avg_day_cons_before *100)/100
avg_day_cons_after = sce_table.avg_daily('2020-02-01', '2025-02-01')[0]
avg_day_cons_after= round(avg_day_cons_after*100)/100

self_cons = solar_table.self_consumption_rate()
self_cons = round(self_cons*1000)/10

with open(www_folder  + 'index_template.html', 'r') as template:
    html = template.read()

html = html.format(power=power,
                   timestamp=timestamp,
                   avg_day_prod=avg_day_prod,
                   avg_day_cons_before=avg_day_cons_before,
                   avg_day_cons_after=avg_day_cons_after,
                   self_cons=self_cons,
                   sce_timestamp=sce_timestamp)

with open(www_folder + 'index.html', 'w') as index:
    index.write(html)
