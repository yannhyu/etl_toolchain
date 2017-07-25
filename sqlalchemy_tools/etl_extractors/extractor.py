#!/usr/bin/python

import sys
import fileinput
import itertools
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Sequence
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.dialects.postgresql import \
    CHAR, VARCHAR, DATE, TIMESTAMP, INTEGER, BIGINT, NUMERIC

IRREGULARITY_TOLERANCE = 2
# SAMPLE_INPUT_FILE = 'Data/test9_three_bad_row.txt'
SAMPLE_INPUT_FILE = 'Data/test9_one_bad_row.txt'
# SAMPLE_INPUT_FILE = 'Data/test9.txt'

def parse_command_line_args():
    # parse args for our_run_date and cust_id
    if len(sys.argv) != 2:
        sys.stderr.write("Usage : python {} MMDDYY_HHMMSS_cust_id (051317_000001_000015)\n"
            .format(sys.argv[0]))
        raise SystemExit(1)
    mmddyy, hhmmss, raw_cust_id = sys.argv[1].split('_')
    our_run_date = datetime.strptime('{} {}'.format(mmddyy, hhmmss), '%m%d%y %H%M%S')
    param_cust_id = raw_cust_id.lstrip('0')
    return our_run_date, param_cust_id

def generate_headers(table_name):
    ex_table = metadata.tables[table_name]
    return [column.name for column in ex_table.columns]

def generate_data_line(versioned_headers, inputfile):
    unstaged_headers = tuple(generate_headers('test_unstaged_t'))
    # print(unstaged_headers)
    for line in fileinput.input(inputfile):
        # print('{} - {}'.format(fileinput.lineno(), line.strip()))
        items = line.strip().split('|')
        data_line = dict(zip(versioned_headers, items))
        res = {k:data_line[k] for k in unstaged_headers if k in data_line}
        # fill missed attr
        res['dataload'] = line.strip()
        res['id_rec'] = None
        if res.get('hid') is None:
            res['hid'] = 0
        # print('# of items: {} --> # of delimiters: {}\n'.format(len(versioned_headers), line.count('|')))
        if len(versioned_headers) == line.count('|') + 1:
            res['delimiter_flag'] = True
        else:
            res['delimiter_flag'] = False
        yield res

# when count of delimiters and data item count do not match right
# ideally delimiters_count + 1 ought to equal to items_count
def number_of_irregular_rows(data_lines):
    return sum(not dl.get('delimiter_flag') for dl in data_lines)

def cust_id_match(data_lines, expected_cust_id):
    for dl in data_lines:
        if dl['cust_id'] != expected_cust_id:
            return False
        else:
            continue
    return True            

def persist2db(our_run_date, data_rows):
    session = Session(engine)
    TABLE_ID = Sequence('insurance0_acctnum_t_id_acct_seq', start=1000)
    for row_dict in data_rows:
        row_dict['id_rec'] = TABLE_ID.next_value()
        row_dict['our_run_date'] = our_run_date
        session.add(Unstaged(**row_dict))
    session.commit()

if __name__ == '__main__':
    our_run_date, param_cust_id = parse_command_line_args() 
    # print(our_run_date)
    # print(type(our_run_date))
    # print(param_cust_id)

    db_uri = 'postgresql://u:p@host/database'
    engine = create_engine(db_uri)
    metadata = MetaData(engine)
    metadata.reflect(engine,
                     only=[
                         'test_unstaged_t',
                         'read_insurance0_v1_t',
                         'read_insurance0_v2_t',
                    ])
    Base = automap_base(metadata=metadata)
    Base.prepare(engine, reflect=False)
    Unstaged = Base.classes.test_unstaged_t    

    v1_headers = tuple(generate_headers('read_insurance0_v1_t'))
    # print(v4_headers)
    data_lines = generate_data_line(v1_headers, SAMPLE_INPUT_FILE)
    data_lines, data_lines01, data_lines02 = itertools.tee(data_lines, 3)

    # TODO: check param_cust_id with cust_id from input, 
    # if not match, raise ERROR
    if not cust_id_match(data_lines01, param_cust_id):
        raise RuntimeError('Error: cust_id does not match...')

    # check if there are more than we can tolerate
    irregulars_count = number_of_irregular_rows(data_lines)
    if irregulars_count <= IRREGULARITY_TOLERANCE:
        persist2db(our_run_date, data_lines02)
    else:
        raise RuntimeError(
            'Error: too many rows with irregularity: {} found !!'
            .format(irregulars_count))