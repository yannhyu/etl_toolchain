from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

db_uri = "postgresql://u:p@host/database"
engine = create_engine(db_uri)

# Create MetaData instance
metadata = MetaData(engine, reflect=True)
# print(metadata.tables)

# Get Table
ex_table = metadata.tables['temp_batch_t']
print(ex_table)

# User.name.property.columns[0].type.length
# print user.columns.name.type.length

for column in ex_table.columns:
    try:
        print('{}: {}'.format(column.name, column.type.length))
    except AttributeError as ae:
        # print("{} - 'NUMERIC' object has no attribute 'length'".format(column.name))
        print('{}: NUMERIC'.format(column.name))