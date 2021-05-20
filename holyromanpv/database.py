import sqlite3
import pandas
import sqlalchemy
import datetime


class Database:
    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


class SQLiteDatabase(Database):
    
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.uri = 'sqlite:///{db_path}'.format(db_path=db_path)
        self.db_type = 'sqlite'
        self.engine = sqlalchemy.create_engine(self.uri)
        
        
    
class PostgresDatabase(Database):
    
    def __init__(self, config_file, config_name):
        self.user = None
        self.pwd = None
        self.connection = None
        self.cursor = None
        self.dict_cursor = None
        self.host = None
        self.db_name = None
        self.uri = None
        self.load_config(config_file, config_name)
        self.connect()
        self.db_type = 'postgres'
        self.placeholder = '%s'
        self.bool_function = 'BOOL'

    def load_config(self, config_file, config_name):
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(config_file)
        self.host = config[config_name]['host']
        self.user = config[config_name]['user']
        self.pwd = config[config_name]['pwd']
        self.db_name = config[config_name]['database']
        self.uri = 'postgresql+psycopg2://{user}:{pwd}@{host}/{db_name}'
        self.uri = self.uri.format(user=self.user, pwd=self.pwd, host=self.host, db_name=self.db_name)

    def connect(self):
        connection_str = "host='{}' dbname='{}' user='{}' password='{}'".format(self.host, self.db_name, self.user, self.pwd)
        self.connection = psycopg2.connect(connection_str)
        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def execute_query(self, query):
        self.cursor.execute(query)




class DBTable:
    
    def __init__(self, database, schema=None):
        self.database = database
        self.schema = schema

    def clear_tab(self):
        query = 'DELETE FROM {}'.format(self.table_name)
        self.database.cursor.execute(query)
        self.database.commit()

    def drop(self):
        query = 'DROP TABLE IF EXISTS {schema}.{table_name}'.format(schema=self.schema, table_name=self.table_name)
        self.database.cursor.execute(query)
        self.database.commit()

    def commit(self):
        self.database.commit()

    def to_dataframe(self):
        query = 'SELECT * FROM {table_name}'.format(table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri)
        return df

    def select_all(self):
        query = 'SELECT * FROM {table_name}'.format(table_name=self.table_name)
        self.database.cursor.execute(query)
        ret = self.database.cursor.fetchall()
        return ret

    def from_dataframe(self, df):        
        df.to_sql(name=self.table_name, con=self.database.engine, schema=self.schema, if_exists='replace', index=True)

    def drop_table(self):
        query = 'DROP TABLE IF EXISTS {schema}.{table_name}'
        query = query.format(schema=self.schema, table_name=self.table_name)
        self.database.cursor.execute(query)
        self.database.commit()

    def add_pkey(self):
        query = 'ALTER TABLE {schema}.{table_name} ADD CONSTRAINT {table_name}_pkey PRIMARY KEY(idx);'
        query = query.format(schema=self.schema, table_name=self.table_name)
        self.database.cursor.execute(query)
        self.database.commit()
        
    def get_value(self, query):
        self.database.cursor.execute(query)
        ret = self.database.cursor.fetchone()[0]
        return ret
    
    

class SceTable(DBTable):
    table_name = 'sce'

    def upsert_dataframe(self, df):
        for row in df.iterrows():            
            timestamp = row[0]
            power = row[1]['power']
            self.upsert_record(timestamp, power)
        self.commit()

    def upsert_record(self, timestamp, power):
        self.delete_by_timestamp(timestamp)
        self.insert_record(timestamp, power)

    def delete_by_timestamp(self, timestamp):
        query = 'DELETE FROM {table_name} ' \
                'WHERE timestamp = ?'
        query = query.format(table_name=self.table_name)
        timestamp = str(timestamp)
        self.database.cursor.execute(query, (timestamp,))

    def insert_record(self, timestamp, power):
        timestamp = str(timestamp)
        query = 'INSERT INTO {table_name} (timestamp, power) VALUES (?,?)'
        query = query.format(table_name=self.table_name)
        self.database.cursor.execute(query, (timestamp, power))

    def latest_entry(self):
        query = 'SELECT timestamp FROM {table_name} ORDER BY timestamp DESC LIMIT 1'
        query = query.format(table_name=self.table_name)
        self.database.cursor.execute(query)
        ret = self.database.cursor.fetchone()
        latest_entry = datetime.datetime.strptime(ret[0], '%Y-%m-%d %H:%M:%S')
        return latest_entry
    
    def earliest_entry(self):
        query = 'SELECT timestamp FROM {table_name} ORDER BY timestamp ASC LIMIT 1'
        query = query.format(table_name=self.table_name)
        self.database.cursor.execute(query)
        ret = self.database.cursor.fetchone()
        latest_entry = datetime.datetime.strptime(ret[0], '%Y-%m-%d %H:%M:%S')
        return latest_entry
    
    def avg_daily(self, start, end):
        query = """SELECT avg(p)*24 as daily, sum(p) as total FROM
                (SELECT avg(power) as p FROM sce 
                WHERE timestamp >= '{start}'
                AND timestamp <= '{end}'
                GROUP BY STRFTIME('%Y%m%d%H', timestamp))"""
        query = query.format(start=start, end=end)        
        self.database.cursor.execute(query)
        ret = self.database.cursor.fetchone()        
        avg = ret[0]
        tot = ret[1]
        return avg, tot
            

    def to_dataframe(self, max_date=None, min_date=None):
        if max_date is None:
            max_date = self.latest_entry()
        if min_date is None:
            min_date = self.earliest_entry()
        query = 'SELECT * FROM {table_name} ' \
                'WHERE timestamp >= "{min_date}" ' \
                'AND timestamp <= "{max_date}" ' \
                'ORDER BY timestamp'
        query = query.format(table_name=self.table_name, min_date=min_date, max_date=max_date)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='timestamp', parse_dates=['timestamp'])
        return df

    def to_daily_dataframe(self, max_date=None, min_date=None):
        if max_date is None:
            max_date = self.latest_entry()
        if min_date is None:
            min_date = self.earliest_entry()
        query = 'SELECT date(timestamp) as date , sum(power) as power ' \
                'FROM {table_name} ' \
                'WHERE timestamp >= "{min_date}" ' \
                'AND timestamp <= "{max_date}" ' \
                'GROUP BY date(timestamp) ' \
                'ORDER BY date(timestamp) '
        query = query.format(max_date=max_date, min_date=min_date, table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='date', parse_dates=['date'])
        return df

    def to_weekly_dataframe(self, max_date=None, min_date=None):
        if max_date is None:
            max_date = self.latest_entry()
        if min_date is None:
            min_date = self.earliest_entry()
        query = 'SELECT STRFTIME(\'%Y\', timestamp) || \'-\' || STRFTIME(\'%W\', timestamp) AS week, sum(power) as power ' \
                'FROM {table_name} ' \
                'WHERE timestamp >= "{min_date}" ' \
                'AND timestamp <= "{max_date}" ' \
                'GROUP BY STRFTIME(\'%Y\', timestamp)  || \'-\' || STRFTIME(\'%W\', timestamp) ' \
                'ORDER BY STRFTIME(\'%Y\', timestamp)  || \'-\' || STRFTIME(\'%W\', timestamp) '
        query = query.format(max_date=max_date, min_date=min_date, table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='week')
        return df
      
    def to_week_dataframe(self, year, week):
        query = 'SELECT ' \
                'date(timestamp) as date, ' \
                'sum(power) as power ' \
                'FROM {table_name} ' \
                'WHERE STRFTIME(\'%W\', timestamp) = "{week}" ' \
                'AND STRFTIME(\'%Y\', timestamp) = "{year}" ' \
                'GROUP BY date(timestamp) ' \
                'ORDER BY date(timestamp) '
        query = query.format(year=year, week=week, table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='date')
        return df
      
    def to_day_dataframe(self, date):
        query = 'SELECT ' \
                'STRFTIME(\'%H\', timestamp) as hour, ' \
                'power ' \
                'FROM {table_name} ' \
                'WHERE date(timestamp) = "{date}" ' \
                'ORDER BY timestamp '
        query = query.format(date=date, table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='hour')
        return df
          
    def to_monthly_dataframe(self, max_date=None, min_date=None):
        if max_date is None:
            max_date = self.latest_entry()
        if min_date is None:
            min_date = self.earliest_entry()
        query = 'SELECT STRFTIME(\'%Y\', timestamp) || \'-\' || STRFTIME(\'%m\', timestamp) AS month, sum(power) as power ' \
                'FROM {table_name} ' \
                'WHERE timestamp >= "{min_date}" ' \
                'AND timestamp <= "{max_date}" ' \
                'GROUP BY STRFTIME(\'%Y\', timestamp)  || \'-\' || STRFTIME(\'%m\', timestamp) ' \
                'ORDER BY STRFTIME(\'%Y\', timestamp)  || \'-\' || STRFTIME(\'%m\', timestamp) '
        query = query.format(max_date=max_date, min_date=min_date, table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='month')
        return df

    def to_weekday_dataframe(self):
        query = 'SELECT STRFTIME(\'%w\', timestamp) AS day, SUM(power) AS power ' \
                'FROM {table_name} ' \
                'GROUP BY strftime(\'%w\', timestamp) ' \
                'ORDER BY strftime(\'%w\', timestamp)'
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='day', table_name=self.table_name)
        df['daystring'] = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
        return df

    def to_hour_dataframe(self, max_date=None, min_date=None):
        if max_date is None:
            max_date = self.latest_entry()
        if min_date is None:
            min_date = self.earliest_entry()
        query = 'SELECT STRFTIME(\'%H\', timestamp) AS hour, SUM(power) AS power ' \
                'FROM {table_name} ' \
                'WHERE timestamp >= "{min_date}" ' \
                'AND timestamp <= "{max_date}" ' \
                'GROUP BY STRFTIME(\'%H\', timestamp) ' \
                'ORDER BY STRFTIME(\'%H\', timestamp) '
        query = query.format(max_date=max_date, min_date=min_date, table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='hour')
        return df

    def to_quarterhour_dataframe(self, min_date=None, max_date=None):
        if max_date is None:
            max_date = self.latest_entry()
        if min_date is None:
            min_date = self.earliest_entry()
        query = 'SELECT STRFTIME(\'%H:%M\', timestamp) AS quarterhour, '\
                '       SUM(power)/COUNT(power) AS power ' \
                'FROM {table_name} ' \
                'WHERE timestamp >= "{min_date}" ' \
                'AND timestamp <= "{max_date}" ' \
                'GROUP BY quarterhour ' \
                'ORDER BY quarterhour '
        query = query.format(max_date=max_date, min_date=min_date, table_name=self.table_name)
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='quarterhour')
        df.sort_index(inplace=True)
        return df
    
    def baseload(self):
        query = """SELECT min(power) FROM SCE WHERE POWER > 0
                    AND timestamp > '2020-02-01'AND 
                    (strftime('%H', timestamp) >'20'OR strftime('%H', timestamp) <'06')"""
        return self.get_value(query)


class SolarTable(SceTable):
    table_name = 'power'
    
    def to_quarterhour_dataframe(self, min_date=None, max_date=None):
        query = ''' SELECT 
                        strftime('%H:%M', datetime(quarterhour)) as minutes,
                        avg(solar_power) as power, 
                        avg(voltage) as voltage, 
                        avg(current) as current 
                    FROM solar_quarterhour
                    GROUP BY minutes
                    ORDER BY minutes'''
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='minutes')
        df.sort_index(inplace=True)
        return df
    
    def self_consumption_rate(self):
        query = """ SELECT sum(self_cons)/sum(solar) FROM 
                    (SELECT 
                        solar, 
                        CASE sce 
                            WHEN 0 THEN 0.04 
                            ELSE solar
                        END AS self_cons
                    FROM merged_quarterhour)"""
        return self.get_value(query)
        
    def latest(self):
        query = 'SELECT timestamp, power FROM {table_name} ORDER BY timestamp DESC LIMIT 1'
        query = query.format(table_name=self.table_name)
        self.database.cursor.execute(query)
        ret = self.database.cursor.fetchone()        
        return ret
    
    def weekly(self):
        query = 'SELECT * FROM weekly'
        df = pandas.read_sql(sql=query, con=self.database.uri, index_col='minutes')
        df.sort_index(inplace=True)
        return df
