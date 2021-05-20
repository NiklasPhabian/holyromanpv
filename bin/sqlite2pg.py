import database

config = holyromanpv.config.get_config('config.ini')
db_path = config ['sqlite']['dbpath']

pg_db = database.PostgresDatabase(config_file='config.ini', config_name='postgres')
sl_db = database.SQLiteDatabase(db_path)
pg_schema = 'public'


def upsert_sce():
    print('Upserting vessels')
    sl_vessels = database.SceTable(sl_db)
    sl_vessels.select_all()
    pg_vessels = database.SceTable(pg_db, schema=pg_schema)
    pg_vessels.drop()
    pg_vessels.create()
    pg_vessels.add_pkey()
    pg_vessels.batch_insert(sl_vessels.cursor)
    pg_vessels.restart_sequence()
    pg_vessels.commit()


def upsert_positions():
    print('Upserting positions')
    sl_positions = database.PositionTable(sl_db)
    sl_positions.select_all()
    pg_positions = database.PositionTable(pg_db, schema=pg_schema)
    pg_positions.drop()
    pg_positions.create()
    pg_positions.add_pkey()
    pg_positions.batch_insert(sl_positions.cursor)
    pg_positions.restart_sequence()
    pg_positions.commit()


def upsert_timeline():
    print('Upserting timeline')
    sl_timeline = database.TimelineTable(sl_db)
    sl_timeline.select_all()
    pg_timeline = database.TimelineTable(pg_db, schema=pg_schema)
    pg_timeline.drop()
    pg_timeline.create()
    pg_timeline.add_pkey()
    pg_timeline.add_mmsi_index()
    pg_timeline.batch_insert(sl_timeline.cursor)
    pg_timeline.restart_sequence()
    pg_timeline.commit()


upsert_sce()
upsert_positions()
upsert_timeline()


