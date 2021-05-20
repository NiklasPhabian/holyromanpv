HOST=holyromanpv.duckdns.org
#HOST=192.168.2.106
PORT=8023
USER=griessbaum

# Syncing project (mind the trailing slashes)
LOCAL=../
REMOTE=/home/griessbaum/holyromanpv

scp -P $PORT $LOCAL/sce_data/* $USER@$HOST:$REMOTE/sce_data
ssh $USER@$HOST -p $PORT "cd $REMOTE && ./get_sce_csvs.py"
ssh $USER@$HOST -p $PORT "rm $REMOTE/sce_data/*"
