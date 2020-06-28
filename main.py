#!/usr/bin/python3
# ~*~ coding=utf-8 ~*~

import os
import sys
import glob
import argparse

import pendulum

from lib.utils import load_csv, dump_csv, group_data, sort_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script generates mailmerge-ready customer lists for KNV\'s pcbis.de')
    parser.add_argument(
        '-d', '--date',
        default=pendulum.today().subtract(years=2).to_datetime_string()[:10],
        help='Cutoff date as ISO date format, eg \'YYYY-MM-DD\'. Default: today two years ago',
    )
    parser.add_argument(
        '-f', '--file',
        default='customers.csv',
        help='Output CSV filename, eg \'mailing-list.csv\'. Default: customers.csv',
    )
    args = parser.parse_args()

    # Base variables
    src = 'src'
    dist = 'dist'

    csv_files = glob.glob(os.path.join(src, 'Orders_*.csv'))
    raw = load_csv(csv_files)

    with open('blocklist.txt', 'r') as file:
        blocklist = file.read().splitlines()

    data  = []

    for mail_address, csv_data in group_data(raw).items():
        if mail_address in blocklist:
            continue

        item = max(csv_data, key=lambda x:x['timeplaced'])

        try:
            date_iso = item['timeplaced'][:10]
        except TypeError:
            # Well, it happens ..
            continue

        # Throw out everything before cutoff date
        if date_iso < args.date:
            continue

        # Prepare dictionary
        node = {}

        node['Anrede'] = item['rechnungaddresstitle']
        node['Vorname'] = item['rechnungaddressfirstname']
        node['Nachname'] = item['rechnungaddresslastname']
        node['E-Mail'] = item['rechnungaddressemail']
        node['Letzte Bestelltung'] = date_iso

        data.append(node)

    # Create path if it doesn't exist
    if not os.path.exists(dist):
        os.mkdir(dist)

    # Write to CSV file
    dump_csv(sort_data(data), os.path.join(dist, args.file))
