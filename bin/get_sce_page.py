#!/usr/bin/python3

import holyromanpv
import datetime
import os

home = os.path.expanduser("~")
config_loc = home + '/holyromanpv/data/config.ini'
config_file = holyromanpv.config.get_config(config_loc)

db_path = config_file['sqlite']['dbpath']

#db = holyromanpv.database.SQLiteDatabase(db_path)
db = holyromanpv.database.PostgresDatabase(config_loc, 'postgres')
sce_table = holyromanpv.database.SceTable(db)

username = config_file['SCE']['username']
password = config_file['SCE']['password']
account = config_file['SCE']['account']
contract = config_file['SCE']['contract']

if __name__ == '__main__':
    session = holyromanpv.SCESession(username=username,
                                     password=password,
                                     account=account,
                                     contract=contract)
    print('stared driver')
    logged_in = session.login()

    if not logged_in:
        print('failed login; incorrect password?')
        quit()
    else:
        print('logged in')

    session.make_requests_session()

    date = sce_table.latest_entry().date()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    n_tries = 0

    while date < yesterday:
        try:
            print('downloading {}'.format(date))
            df = session.download(str(date))
            print(df)
            sce_table.upsert_dataframe(df)
            date = date + datetime.timedelta(days=1)
        except Exception as e:
            print('download failed. Retrying')
            print(e)
            n_tries += 1
        if n_tries > 5:
            print('Tried 5 times. Giving up')
            break

    session.logout()
    session.quit()
    del session
