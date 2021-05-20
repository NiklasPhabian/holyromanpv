import database
import datetime


sl_db_name = '/home/griessbaum/{date}_pg_backup.sqlite'.format(date=str(datetime.date.today()))
sl_db = database.SQLiteDatabase(sl_db_name)
pg_db = database.PostgresDatabase('database.config', 'postgis')
pg_schema = 'public'


def vessels():
    pg_vessel_table = database.VesselTable(pg_db, schema=pg_schema)
    pg_vessel_table.select_all()
    sl_vessel_table = database.VesselTable(sl_db)
    sl_vessel_table.create()
    sl_vessel_table.batch_insert(pg_vessel_table.cursor)


def positions():
    pg_position_table = database.PositionTable(pg_db, schema=pg_schema)
    pg_position_table.select_all()
    sl_position_table = database.PositionTable(sl_db)
    sl_position_table.create()
    sl_position_table.batch_insert(pg_position_table.cursor)


def timeline():
    pg_timeline_table = database.TimelineTable(pg_db, schema=pg_schema)
    pg_timeline_table.select_all()
    sl_timeline_table = database.TimelineTable(sl_db)
    sl_timeline_table.create()
    sl_timeline_table.batch_insert(pg_timeline_table.cursor)


if __name__ == '__main__':
    vessels()
    positions()
    timeline()
