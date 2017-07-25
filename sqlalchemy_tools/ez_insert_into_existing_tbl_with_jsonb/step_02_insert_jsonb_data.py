#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Sequence
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

def generate_headers(metadata, table_name):
    ex_table = metadata.tables[table_name]
    return [column.name for column in ex_table.columns]

def generate_sample_data_lines():
    lines = [
        (None, 'Arletty', 'Arletty@paradis.com', {'color': 'noir', 'year': 1945}),
        (None, 'Marcel Carné', 'mc@paradis.com', {'role': 'director', 'film': 'Les Enfants du Paradis'}),
        (None, 'Jean-Louis Barrault', 'jlb@paradis.com', {'type': 'mime artist', 'jouer': 'Baptiste Debureau'}),
    ]
    for line in lines:
        yield line

def make_data_rows(fields):    
    for data in generate_sample_data_lines():
        res = dict(zip(fields, data))
        yield res

def persist2db(fields, engine):
    session = Session(engine)
    for row_dict in make_data_rows(fields):
        session.add(Jsonbtable(**row_dict))
    session.commit()

# db_uri = 'postgresql://u:p@host/database'
db_uri = 'postgresql://postgres:psql@localhost/testdb'
db = create_engine(db_uri)  
engine = db.connect()  
metadata = MetaData(engine) 

metadata.reflect(engine,
                 only=[
                     'jsonbtable',
                ])
Base = automap_base(metadata=metadata)
Base.prepare(engine, reflect=False)
Jsonbtable = Base.classes.jsonbtable

fields = tuple(generate_headers(metadata, 'jsonbtable'))
print(fields)

persist2db(fields, engine)