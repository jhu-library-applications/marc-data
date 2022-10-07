from pymarc import MARCReader
import argparse
from datetime import datetime
import pandas as pd
import re

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()
if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.mrc\'): ')


# Creates k,v pair in dict where key = field_name
# value = values of specific subfield in MARC tag in record.
def subfield_finder(record, field_name, subfields, tags):
    field_list = []
    field = record.get_fields(*tags)
    for my_field in field:
        my_subfield = my_field.get_subfields(*subfields)
        for field in my_subfield:
            field_list.append(field)
    if field_list:
        field_list = sorted(list(set(field_list)))
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
        subfield_finder(record, 'oclc', subfields=['a'], tags=['035'])
        mrc_fields['title'] = record.title()

        # Adds dict created by this MARC record to all_fields list.
        all_fields.append(mrc_fields)
        record_count = record_count + 1
        print(record_count)

oclcPrefixList = ['ocm', 'ocn', 'on', '(OCoLC)', 'OCoLC']

df = pd.DataFrame.from_dict(all_fields)
all_fields2 = []
for count, row in df.iterrows():
    row = row
    bib = row['bib']
    oclcList = row['oclc'].split('|')
    updatedOCLC = []
    for oclc in oclcList:
        oclc_num = re.search(r'(\d+)', oclc)
        oclc_pre = re.search(r'([a-zA-Z]+)', oclc)
        print(oclc)
        print(oclc_pre)
        if oclc_num:
            oclc = oclc_num.group(1)
            if oclc == bib:
                pass
            else:
                if oclc_pre:
                    oclc_pre = oclc_pre.group(1)
                    if oclc_pre in oclcPrefixList:
                        updatedOCLC.append(oclc)
                        print(oclc_pre)
                    else:
                        pass
                else:
                    updatedOCLC.append(oclc)

    row['updatedOCLC'] = list(set(updatedOCLC))
    all_fields2.append(row)
    
df = pd.DataFrame.from_dict(all_fields2)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('barcodes_'+dt+'.csv', header='column_names', index=False)