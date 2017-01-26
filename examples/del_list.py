#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from keys import misp_url, misp_key, misp_verifycert
import argparse


# Usage for pipe masters: ./last.py -l 5h | jq .


def init(url, key):
    return PyMISP(url, key, misp_verifycert, 'json', debug=True)

def delete_event(m, eventid):
    result = m.delete_event(eventid)
    print(result)

def list_delete(filename):
    with open(filename, 'r') as f:
        for l in f:
            delete(l)

def delete(eventid):
    eventid = eventid.strip()
    if len(eventid) == 0 or not eventid.isdigit():
        print('empty line or NaN.')
        return
    eventid = int(eventid)
    print(eventid, 'deleting...')
    r = delete_event(eventid)
    if r.status_code >= 400:
        loc = r.headers['location']
        if loc is not None:
            event_to_update = loc.split('/')[-1]
            print('updating', event_to_update)
            r = update_event(eventid, event_to_update)
            if r.status_code >= 400:
                print(r.status_code, r.headers)
        else:
            print(r.status_code, r.headers)
    print(eventid, 'done.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mass delete events from a MISP instance.')
    parser.add_argument("-e", "--event", help="Event ID to delete.")
    parser.add_argument('-f', '--filename', type=str,
                        help='File containing a list of event id.')

    args = parser.parse_args()

    misp = init(misp_url, misp_key)

    if args.filename is not None:
        list_delete(args.filename)
    else:
        delete_event(misp, args.event)
