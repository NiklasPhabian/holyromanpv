HOST=192.168.2.106
HOST=www.holyromanpv.duckdns.org
USER=griessbaum
PORT=8024


# Syncing project (mind the trailing slashes)
LOCAL=/home/griessbaum/Dropbox/holyromanpv
REMOTE=/home/griessbaum/holyromanpv

rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/database.py $USER@$HOST:$REMOTE/database.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/get_daystats.py $USER@$HOST:$REMOTE/get_daystats.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/get_monthstats.py $USER@$HOST:$REMOTE/get_monthstats.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/get_realtime.py $USER@$HOST:$REMOTE/get_realtime.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/get_sce_page.py $USER@$HOST:$REMOTE/get_sce_page.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/get_sce_csvs.py $USER@$HOST:$REMOTE/get_sce_csvs.py 
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/interface.py $USER@$HOST:$REMOTE/interface.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/sce_session.py $USER@$HOST:$REMOTE/sce_session.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" /home/griessbaum/Dropbox/python_libs/plots/plots.py $USER@$HOST:$REMOTE/plots.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/upload_dropbox.py $USER@$HOST:$REMOTE/upload_dropbox.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/make_plots.py $USER@$HOST:$REMOTE/make_plots.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/make_html.py $USER@$HOST:$REMOTE/make_html.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/template/index_template.html $USER@$HOST:$REMOTE/template/index_template.html
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/www/system_reduced.png $USER@$HOST:$REMOTE/www/system_reduced.png
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/update_website.sh $USER@$HOST:$REMOTE/update_website.sh 
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/config.ini $USER@$HOST:$REMOTE/config.ini
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/config.py $USER@$HOST:$REMOTE/config.py
rsync --verbose --recursive --update --rsh "ssh -p $PORT" $LOCAL/kill_chrome.sh $USER@$HOST:$REMOTE/kill_chrome.sh

ssh -p $PORT $USER@$HOST "sed -i -e 's#$LOCAL#$REMOTE#g' $REMOTE/config.ini"
