from mlxlibrary import get_lname

people_names = [
    ('John Smith', 'Smith'),
    ('John Maxwell Smith', 'Smith'),
    # ('John Smith Jr', 'Smith Jr'),
    ('John van Damme', 'van Damme'),
    # ('John Smith, IV', 'Smith, IV'),
    ('John Mark Del La Hoya', 'Del La Hoya')
]

print('name --> we got <-- supposed to get')
for name, target in people_names:
    print('{} --> {} <-- {}'.format(name, get_lname(name), target))
    assert get_lname(name) == target
