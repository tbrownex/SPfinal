import sqlalchemy

def getPostgresConnection():
    LOCAL_PG_USER  = "tom"
    LOCAL_PG_HOST  = "localhost"
    LOCAL_DB_NAME  = "simplify"
    PASSWORD = 'bronco'
    engine = sqlalchemy.create_engine('postgresql://{username}:{pwd}@{host}/{db}'.format(
          username=LOCAL_PG_USER,
          host=LOCAL_PG_HOST,
          db=LOCAL_DB_NAME,
          pwd=PASSWORD))
    return engine.connect()