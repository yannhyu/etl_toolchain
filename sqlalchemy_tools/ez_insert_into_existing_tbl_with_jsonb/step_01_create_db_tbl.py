import json  
import sqlalchemy
from sqlalchemy import Column, Integer, Text  
from sqlalchemy.dialects.postgresql import JSONB

# db_uri = 'postgresql://u:p@host/database'
db_uri = 'postgresql://postgres:psql@localhost/testdb'
db = sqlalchemy.create_engine(db_uri)  
engine = db.connect()  
meta = sqlalchemy.MetaData(engine) 


sqlalchemy.Table("jsonbtable", meta,  
                Column('id', Integer, primary_key=True),
                Column('name', Text),
                Column('email', Text),
                Column('doc', JSONB))
meta.create_all() 