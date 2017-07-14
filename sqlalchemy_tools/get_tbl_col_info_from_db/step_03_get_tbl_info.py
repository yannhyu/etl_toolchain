from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

db_uri = "postgresql://u:p@host/database"
engine = create_engine(db_uri)

# Create MetaData instance
metadata = MetaData(engine, reflect=True)
# print(metadata.tables)

# Get Table
ex_table = metadata.tables['temp_batch_insurance0_t']
print(ex_table)

# User.name.property.columns[0].type.length
# print user.columns.name.type.length

len_entity_name1 = ex_table.columns.entity_name1.type.length
print('length of entity_name1: {}'.format(len_entity_name1))

len_entity_pay_to_street1 = ex_table.columns.entity_pay_to_street1.type.length
print('length of entity_pay_to_street1: {}'.format(len_entity_pay_to_street1))

len_entity_pay_to_city1 = ex_table.columns.entity_pay_to_city1.type.length
print('length of entity_pay_to_city1: {}'.format(len_entity_pay_to_city1))