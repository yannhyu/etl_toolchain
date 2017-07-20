import fileinput
from functools import partial
from decimal import Decimal
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import \
    CHAR, VARCHAR, DATE, TIMESTAMP, INTEGER, BIGINT, NUMERIC

# db_uri = "postgresql://u:p@host/database"
db_uri = 'postgresql://dev_payorintel_u:u782nmt5@devmaindb/dev_ml_db'
engine = create_engine(db_uri)

# Create MetaData instance
metadata = MetaData(engine, reflect=True)
# print(metadata.tables)

# convenient methods
def fixed_size_str(somestring, maxlength):
    return str(somestring)[:maxlength]

def pydate(datestr, dateformat):
    res = datestr
    if datestr:
        res = datetime.strptime(datestr[:19], dateformat).date()
    return res 

def generate_headers(version_tbl_name):
    ex_table = metadata.tables[version_tbl_name]
    return [column.name for column in ex_table.columns]

def generate_data_line(versioned_headers, inputfile):
    for line in fileinput.input(inputfile):
        # print('{} - {}'.format(fileinput.lineno(), line.strip()))
        line = line.strip().split('|')
        data_line = dict(zip(versioned_headers, line))
        data_line['seqnum'] = fileinput.lineno()
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
    data_line['our_run_date'] = datetime.now()
    yield data_line    

v4_headers = tuple(generate_headers('read_insurance0_v4_t'))
# print(v4_headers)
data_lines = generate_data_line(v4_headers, 'Data/reader310.output')

# for data_line in data_lines:
#     print(data_line)
#     print(convert_data_type(data_line))

data_lines_typed = [convert_data_type(data_line) for data_line in data_lines]
data_rows = [post_type_conversion_add(data_line) for data_line in data_lines_typed]

for row in data_rows:
    print(next(row))