*/5 * * * * /home/griessbaum/smartplug/update_realtime.sh      # Every 5 minutes
1 16 * * * /home/griessbaum/smartplug/get_sce_page.py          # Every day at 16:01 hours
1 4 * * * /home/griessbaum/smartplug/get_sce_page.py           # Every day at 04:01 hours
1 1 * * * /home/griessbaum/smartplug/kill_chrome.sh            # Every day at 01:01 hours
1 23 * * * /home/griessbaum/smartplug/get_daystats.py          # Every day at 23:01 hours
1 2 * * * /home/griessbaum/smartplug/get_monthstats.py         # Every day at 2:01 AM
1 3 * * * /home/griessbaum/smartplug/upload_dropbox.py         # Every day at 3:01 AM
