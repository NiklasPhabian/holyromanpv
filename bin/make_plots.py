#!/usr/bin/python3

import pandas
import datetime
import holyromanpv
import plots
import os

pandas.plotting.register_matplotlib_converters()

home = os.path.expanduser("~")
config_loc = home + '/holyromanpv/data/config.ini'
config_file = holyromanpv.config.get_config(config_loc)
db_path = config_file['sqlite']['dbpath']
www_folder = config_file['www']['folder']

db = holyromanpv.database.SQLiteDatabase(db_path)
solar_table = holyromanpv.database.SolarTable(db)
sce_table = holyromanpv.database.SceTable(db)

now = datetime.datetime.now()
today = datetime.datetime.now().date()


def prod_plot(n_days=7):
    start = now - datetime.timedelta(days=n_days)
    query = ''' SELECT timestamp, power FROM power 
            WHERE timestamp > '{start}'
            ORDER BY timestamp'''
    query = query.format(start=start)
    solar_power = pandas.read_sql(sql=query, con=db.engine, parse_dates='timestamp', index_col='timestamp')    
    plot = plots.Plot()
    plot.plot_pandas(solar_power['power'])
    plot.y_label('Power \n in W')
    plot.save_fig(www_folder + 'production.svg')


def day_plot(n_days=7):
    plot = plots.Plot()
    sql = 'SELECT * FROM day ORDER BY timestamp;'
    days = pandas.read_sql(sql=sql, con=db.engine, 
                           parse_dates='timestamp',
                           index_col='timestamp')        
    plot.plot_pandas(days['energy'])

    plot.y_label('Energy \n in kWh')
    plot.set_monthly_ticks()
    plot.rotate_ticks(90)
    plot.save_fig(www_folder + 'days.svg')
    
def month_plot():
    plot = plots.Plot()
    query = 'SELECT timestamp, energy FROM month;'
    months = pandas.read_sql(sql=query, con=db.uri, 
                         parse_dates='timestamp',
                         index_col='timestamp')
    months.index = months.index.to_period('M')
    plot.plot_pandas_series(months['energy'], kind='bar')
    plot.y_label('Energy \n in kWh')    
    plot.save_fig(www_folder + 'months.svg')
    
def month_comparison():    
    query = ''' SELECT minute, power 
                FROM solar_avg_15minute 
                WHERE month="{month}"'''
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    s = []
    for month in months:
        s.append(pandas.read_sql(sql=query.format(month=month), con=db.engine, index_col='minute'))
    df = pandas.concat(s, axis=1)
    df.columns = months
    # We go UTC and then fixed 8 hours off of it
    df['ts'] = (pandas.to_datetime(df.index)-datetime.timedelta(hours=8)).strftime('%H:%M')
    df.set_index('ts', inplace=True)
    df.sort_index(inplace=True)
    
    plot = plots.Plot()    
    plot.plot_pandas_df(df, colormap='Paired')
    plot.y_label('Average \n Power  in W')
    plot.x_label('Hour of the day (fixed: UTC-8)')
    plot.save_fig(www_folder + 'months_comparison.svg')

def prodcons_plot(n_days=7):    
    start = now - datetime.timedelta(days=7)
    query = ''' SELECT timestamp, power/1000 as solar 
                FROM power 
                WHERE timestamp > '{start}'
                ORDER BY timestamp'''
    query = query.format(start=start)
    solar = pandas.read_sql(sql=query, con=db.engine, 
                            parse_dates='timestamp',
                            index_col='timestamp')
    
    query = ''' SELECT timestamp, power as sce
                FROM sce
                WHERE timestamp > '{start}' 
                ORDER BY timestamp'''
    query = query.format(start=start)
    sce = pandas.read_sql(sql=query, con=db.engine, 
                          parse_dates='timestamp',
                          index_col='timestamp')
               
    plot = plots.Plot()
    plot.plot_pandas(sce['sce'])
    plot.plot_pandas(solar['solar'])
    plot.y_label('Power \n in W')
    plot.set_daily_ticks()    
    plot.ax.xaxis.grid(True)
    plot.save_fig(www_folder + 'prodcons.svg')
    
    
def avg_prodcons_plot():    
    query = ''' SELECT STRFTIME(\'%H:%M\', timestamp) AS quarterhour, 
                    avg(solar) AS solar, 
                    avg(sce) AS sce
            FROM merged_quarterhour
            WHERE timestamp >= "{min_date}" 
            AND timestamp <= "{max_date}" 
            GROUP BY quarterhour 
            ORDER BY quarterhour '''

    sql = query.format(min_date='2019-04-01', max_date='2025-02-01')
    merged = pandas.read_sql(sql=sql, con=db.engine)    
    before_pv = sce_table.to_quarterhour_dataframe(min_date='2019-04-01', max_date='2020-02-01')
    
    plot = plots.Plot()
    plot.y_label('Power \n in kW')
    plot.plot_pandas(before_pv['power'], series_name='before pv')
    plot.plot_pandas(merged['sce'], series_name='after pv')
    plot.plot_pandas(merged['solar'], series_name='pv')
    plot.set_xlim(0, 24*4)
    plot.ax.set_xticks(range(0,24*4,4))
    plot.rotate_ticks(90)
    plot.save_fig(www_folder + 'avg_prodcons.svg')
    

def consumption_plot():
    query = ''' SELECT strftime('%Y-%m-%d', timestamp) AS week,
                AVG(power)*168 AS weekly
                FROM sce
                GROUP BY strftime('%Y-%W', timestamp)'''

    week_avg = pandas.read_sql(sql=query, con=db.engine,                         
                               index_col='week',
                               parse_dates='week')
    
    query = ''' SELECT min(strftime('%Y-%m-%d', timestamp)) AS month,
                AVG(power)*168 AS monthly
                FROM sce
                GROUP BY strftime('%Y-%m', timestamp)'''
                
    month_avg = pandas.read_sql(sql=query, con=db.engine,                         
                                index_col='month',
                                parse_dates='month')
    plot = plots.Plot()
    plot.y_label('Weekly energy \n in kWh')
    plot.plot_pandas(week_avg['weekly'], marker='.')
    plot.plot_pandas(month_avg['monthly'], marker='o', linewidth=3)
    plot.make_legend()
    plot.x_label('')
    plot.save_fig(www_folder + 'consumption.svg')
    
    
if __name__ == '__main__':
    prod_plot()
    day_plot()
    month_plot()
    month_comparison()
    prodcons_plot()
    avg_prodcons_plot()
    consumption_plot()
