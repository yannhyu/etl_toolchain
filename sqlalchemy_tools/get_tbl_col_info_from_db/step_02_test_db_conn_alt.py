# start with an engine
from sqlalchemy import create_engine
from sqlalchemy import MetaData

engine = create_engine("postgresql://u:p@host/database")


m = MetaData()
m.reflect(engine)
for table in m.tables.values():
    print('*** {} ***'.format(table.name))
    for column in table.c:
        print(column.name)