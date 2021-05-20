#!/usr/bin/python3

import database
import pandas
import glob
import config

config_file = config.get_config()
db_path = config_file['sqlite']['dbpath']

db = database.SQLiteDatabase(db_path)
power_table = database.SceTable(db)


def upsert_csv(filename):
    df = pandas.read_csv(filename, 
                         skiprows=13,
                         header=0,
                         names=['date', 'elec', 'quality'])
    df[['start','stop']] = df['date'].str.split('to', expand=True)
    df.drop(columns=['date', 'stop', 'quality'], inplace=True)
    df.elec = pandas.to_numeric(df.elec, errors='coerce')
    df.dropna(inplace=True)
    df.start = pandas.to_datetime(df.start)
    df['power'] = df.elec*4
    df.drop(columns=['elec'], inplace=True)
    df.set_index('start', inplace=True)
    power_table.upsert_dataframe(df)


if __name__ == '__main__':
    filename = 'sce_data/SCE_Usage_3-050-3487-45_02-01-20_to_02-06-20.csv'
    csvs = glob.glob('sce_data/*csv')
    for csv in csvs:
        print(csv)
        upsert_csv(csv)
