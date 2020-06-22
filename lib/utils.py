from hashlib import md5
from operator import itemgetter

from pandas import DataFrame, concat, read_csv


def load_csv(csv_files):
     delimiter = ';'
     encoding = 'iso-8859-1'

     try:
         df = concat(map(lambda file: read_csv(file, sep=delimiter, encoding=encoding, low_memory=False), csv_files))

     except FileNotFoundError:
         return {}

     return df.to_dict('records')


def dump_csv(data, csv_file):
    DataFrame(data).to_csv(csv_file, index=False)

    return True


def dedupe(duped_data, encoding='utf-8'):
    deduped_data = []
    codes = set()

    for item in duped_data:
        hash_digest = md5(str(item).encode(encoding)).hexdigest()

        if hash_digest not in codes:
            codes.add(hash_digest)
            deduped_data.append(item)

    return deduped_data


def group_data(ungrouped_data):
    grouped_data = {}

    for item in dedupe(ungrouped_data):
        mail_address = item['rechnungaddressemail']

        if mail_address not in grouped_data.keys():
            grouped_data[mail_address] = []

        grouped_data[mail_address].append(item)

    return grouped_data


def sort_data(unsorted_data):
    sorted_data = sorted(unsorted_data, key=itemgetter('Nachname', 'Vorname'))

    return sorted_data
