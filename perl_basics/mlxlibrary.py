#!/usr/bin/env python
from nameparser import HumanName

def get_fname(somename):
	# name = HumanName("Dr. Juan Q. Xavier de la Vega III (Doc Vega)")
    name = HumanName(somename)
    # print(name)
    # print('{} {} {}'.format(name.first, name.middle, name.last))
    # print(name.first)
    # print(name.middle)
    # print(name.last)

    return name.first

def get_mname(somename):
    # name = HumanName("Dr. Juan Q. Xavier de la Vega III (Doc Vega)")
    name = HumanName(somename)
    # print(name)
    # print('{} {} {}'.format(name.first, name.middle, name.last))
    # print(name.first)
    # print(name.middle)
    # print(name.last)

    return name.middle    