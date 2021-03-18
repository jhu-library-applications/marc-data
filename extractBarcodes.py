from pymarc import MARCReader
import argparse
from datetime import datetime
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()
if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.mrc\'): ')


#  Creates k,v pair in dict where key = field_name, value = values of MARC tags in record.
def field_finder(record, field_name, tags):
    field_list = []
    field = record.get_fields(*tags)
    for my_field in field:
        my_field = my_field.format_field()
        field_list.append(my_field)
    if field_list:
        field_list = sorted(field_list)
        field_list = '|'.join(str(e) for e in field_list)
        mrc_fields[field_name] = field_list
    else:
        mrc_fields[field_name] = ''


# Creates k,v pair in dict where key = field_name, value = values of specific subfield in MARC tag in record.
def subfield_finder(record, field_name, subfields, tags):
    field_list = []
    field = record.get_fields(*tags)
    for my_field in field:
        my_subfield = my_field.get_subfields(*subfields)
        for field in my_subfield:
            field_list.append(field)
    if field_list:
        field_list = sorted(field_list)
        field_list = '|'.join(str(e) for e in field_list)
        mrc_fields[field_name] = field_list
    else:
        mrc_fields[field_name] = ''


all_fields = []
record_count = 0
with open(filename, 'rb') as fh:
    marc_recs = MARCReader(fh, to_unicode=True)
    for record in marc_recs:
        mrc_fields = {}
        leader = record.leader
        #  Finds fields/subfield values in record.
        subfield_finder(record, 'bib', subfields=['a'], tags=['910'])
        field_finder(record, 'barcode', tags=['991'])
        subfield_finder(record, 'oclc', subfields=['a'], tags=['035'])
        mrc_fields['title'] = record.title()

        # Adds dict created by this MARC record to all_fields list.
        all_fields.append(mrc_fields)
        record_count = record_count + 1
        print(record_count)

df = pd.DataFrame.from_dict(all_fields)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('barcodes_'+dt+'.csv', header='column_names', index=False)
