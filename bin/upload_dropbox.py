#!/usr/bin/python3

import dropbox
import holyromanpv
import os

home = os.path.expanduser("~")
config_loc = home + '/holyromanpv/data/config.ini'
config_file = holyromanpv.config.get_config(config_loc)


token = config_file['dropbox']['token']
db_path = config_file['sqlite']['dbpath']
dbx = dropbox.Dropbox(token)


def upload_file(filename):
    remotefilename = filename.split('/')[-1]
    remote_path = path = '/' + remotefilename
    with open(filename, 'rb') as f:
        path = '/' + remotefilename
        dbx.files_upload(f=f.read(), path=path, mode=dropbox.files.WriteMode.overwrite)
 

if __name__ == '__main__':
    upload_file(db_path)
