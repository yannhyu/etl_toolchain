from random import randint
import fileinput
from functools import partial
from decimal import Decimal
from datetime import datetime
from collections import namedtuple
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.dialects.postgresql import \
    CHAR, VARCHAR, DATE, TIMESTAMP, INTEGER, BIGINT, NUMERIC

db_uri = "postgresql://u:p@host/database"
engine = create_engine(db_uri)

# Create MetaData instance
metadata = MetaData(engine, reflect=True)
# print(metadata.tables)

metadata.reflect(engine, only=['temp_batch_insurance0_unstaged_t',])
# reflect the tables
Base = automap_base(metadata=metadata)
Base.prepare(engine, reflect=True)
TempBatchIns0Unstaged = Base.classes.temp_batch_insurance0_unstaged_t

our_run_date = datetime.now()

# convenient methods
def fixed_size_str(somestring, maxlength):
    return str(somestring)[:maxlength]

def pydate(datestr, dateformat):
    if datestr:
        res = datetime.strptime(datestr[:19], dateformat).date()
    else:
        res = None
    return res 

def generate_headers(table_name):
    ex_table = metadata.tables[table_name]
    return [column.name for column in ex_table.columns]

def generate_data_line(versioned_headers, inputfile):
    for line in fileinput.input(inputfile):
        # print('{} - {}'.format(fileinput.lineno(), line.strip()))
        line = line.strip().split('|')
        data_line = dict(zip(versioned_headers, line))
        data_line['seqnum'] = fileinput.lineno()
        data_line['acctnum_seq'] = randint(0, 99)
        data_line['client_npi1'] = 'supplied'
        data_line['emdeon_billing_id'] = 'ebi'
        yield data_line

def generate_data_type_map():
    fld_type_map = dict()
    ex_table = metadata.tables['temp_batch_insurance0_unstaged_t']
    for column in ex_table.columns:
        if isinstance(column.type, VARCHAR):
            fld_type_map[column.name] = partial(fixed_size_str, maxlength=column.type.length)
        elif isinstance(column.type, (INTEGER, BIGINT)):
            fld_type_map[column.name] = int
        elif isinstance(column.type, NUMERIC):
            fld_type_map[column.name] = Decimal
        elif isinstance(column.type, DATE):
            fld_type_map[column.name] = partial(pydate, dateformat='%Y-%m-%d %H:%M:%S')
        elif isinstance(column.type, TIMESTAMP):
            fld_type_map[column.name] = str 
        else:
            fld_type_map[column.name] = str

    return fld_type_map

# handle data type conversion in each data_line
def convert_data_type(data_line):
    fld_type_map = generate_data_type_map()
    yield {k:fld_type_map[k](v) for k, v in data_line.iteritems()}

def post_type_conversion_add(data_line):
    data_line = next(data_line)
    data_line['our_run_date'] = our_run_date
    return data_line    

v4_headers = tuple(generate_headers('read_insurance0_v4_t'))
# print(v4_headers)
data_lines = generate_data_line(v4_headers, 'Data/reader310.output')

data_lines_typed = [convert_data_type(dl) for dl in data_lines]
data_rows = [post_type_conversion_add(dl) for dl in data_lines_typed]

# TBI0U_HEADERS = generate_headers('temp_batch_insurance0_unstaged_t')
# init_dict = dict.fromkeys(TBI0U_HEADERS)
# EmptyStart = TempBatchIns0Unstaged(**init_dict)

# Persist
session = Session(engine)
for row_dict in data_rows:
    # print(row_dict)
    session.add(TempBatchIns0Unstaged(**row_dict))
session.commit()