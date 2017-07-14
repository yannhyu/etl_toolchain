#!/usr/bin/env python
from nameparser import HumanName

def get_lname(somename):
    name = HumanName(somename)
    return name.last 

people_names = [
    ('John Smith', 'Smith'),
    ('John Maxwell Smith', 'Smith'),
    # ('John Smith Jr', 'Smith Jr'),
    ('John van Damme', 'van Damme'),
    # ('John Smith, IV', 'Smith, IV'),
    ('John Mark Del La Hoya', 'Del La Hoya')
]

for name, target in people_names:
    print('{} --> {} <-- {}'.format(name, get_lname(name), target))
    assert get_lname(name) == target  