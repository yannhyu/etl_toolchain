from collections import namedtuple

master_headers = ('fname', 'lname', 'sex', 'age', 'bday', 'special')

blank_master = (None,) * len(master_headers)

Row = namedtuple('Row', master_headers)

empty = Row(*blank_master)
# print(empty)

headers_v1 = ('lname', 'bday', 'special')
data_v1 = [
        ('Roberts', '2000-03-12', 'opera'),
        ('Ashford', '1995-07-15', 'books'),
        ('Whatitis', '2017-01-03', 'music'),
    ]

headers_v2 = ('fname', 'lname', 'special', 'age')
data_v2 = [
        ('David', 'Roberts', 'ping pong', 36),
        ('Carlo', 'Ashford', 'python', 35),
        ('Howabout', 'Whatitis', 'music', 3),
    ]

for d_v1 in data_v1:
    transformed = empty._replace(**dict(zip(headers_v1, d_v1)))
    print(transformed)

for d_v2 in data_v2:
    transformed = empty._replace(**dict(zip(headers_v2, d_v2)))
    print(transformed)
    print('|'.join((str(x) if x else '' for x in transformed)))
