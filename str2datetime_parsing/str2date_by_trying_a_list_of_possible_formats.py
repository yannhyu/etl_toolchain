from datetime import datetime

def try_parsing_date(text, formats):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found')

possible_formats = ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y')
dobs = ['1966-06-14', '24.07.1957', '01/03/2003']
for dob in dobs:
    dob_date = try_parsing_date(dob, possible_formats)
    print(dob_date)
    print(type(dob_date)) 