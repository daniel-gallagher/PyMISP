#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from keys import misp_url, misp_key, misp_verifycert
import argparse


# Usage for pipe masters: ./last.py -l 5h | jq .


def init(url, key):
    return PyMISP(url, key, misp_verifycert, 'json', debug=True)

def del_event(m, eventid):
    result = m.delete_event(eventid)
    print(result)

misp = init(misp_url, misp_key)

def list_delete(filename):
    with open(filename, 'r') as f:
        for l in f:
            del_event(misp, l)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mass delete events from a MISP instance.')
    parser.add_argument('-f', '--filename', type=str,
                        help='File containing an event id list.')

    args = parser.parse_args()

    if args.filename is not None:
        list_delete(args.filename)
    else:
        exit(0)
