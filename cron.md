*/61 * * * * /home/griessbaum/duckdns/duck.sh

*/5 * * * * /home/griessbaum/holyromanpv/bin/get_realtime.py           # Every 5 minutes
*/15 * * * * /home/griessbaum/holyromanpv/bin/update_website.sh        # Every 15 minutes
1 23 * * *  /home/griessbaum/holyromanpv/bin/get_daystats.py           # Every day at 23:01 hours
1 2 * * *   /home/griessbaum/holyromanpv/bin/get_monthstats.py         # Every day at 2:01 AM
1 3 * * *   /home/griessbaum/holyromanpv/bin/upload_dropbox.py         # Every day at 3:01 AM

1 16 * * * /home/griessbaum/holyromanpv/bin/get_sce_page.sh           # Every day at 16:01 hours
5 4 * * *  /home/griessbaum/holyromanpv/bin/get_sce_page.sh           # Every day at 04:05 hours
