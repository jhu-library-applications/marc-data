from pymarc import MARCReader
import csv
import argparse
import re
import os
from datetime import datetime
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()
if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.mrc\'): ')


fileDir = os.path.dirname(__file__)

datetypes_dict = {}
marc_lang = {}
cat_dict = {}


def create_dict(csvname, column1, column2, dictname):
    with open(csvname) as codes:
        codes = csv.DictReader(codes)
        for row in codes:
            code = row[column1]
            name = row[column2]
            dictname[code] = name


#  Import type codes used in 006.
create_dict(os.path.join(fileDir, 'dictionaries/marc_datetypes.csv'), 'Type',
            'Name', datetypes_dict)
# Import language codes used in language.
create_dict(os.path.join(fileDir, 'dictionaries/marc_lang.csv'), 'Code', 'Name',
            marc_lang)
# Import category codes used in 007.
create_dict(os.path.join(fileDir, 'dictionaries/marc_007categoryMaterial.csv'),
            'Code', 'Name', cat_dict)


#  Creates k,v pair in dict where key = field_name,
#  value = values of MARC tags in record.
def field_finder(field_name, tags):
    field_list = []
    field = record.get_fields(*tags)
    for my_field in field:
        my_field = my_field.format_field()
        field_list.append(my_field)
    if field_list:
        field_list = '|'.join(str(e) for e in field_list)
        mrc_fields[field_name] = field_list
    else:
        mrc_fields[field_name] = ''


# Creates k,v pair in dict where key = field_name, value = values of
# specific subfield in MARC tag in record.
def subfield_finder(field_name, subfields, tags):
    field_list = []
    field = record.get_fields(*tags)
    for my_field in field:
        my_subfield = my_field.get_subfields(*subfields)
        for field in my_subfield:
            if field not in field_list:
                field_list.append(field)
    if field_list:
        field_list = '|'.join(str(e) for e in field_list)
        mrc_fields[field_name] = field_list
    else:
        mrc_fields[field_name] = ''


# Converts code from MARC record into name from imported dictionaries.
def convert_to_name(keyname, dictname):
    v = mrc_fields.get(keyname)
    if '|' in v:
        v = v.split('|')
        for count, item in enumerate(v):
            for key, value in dictname.items():
                if item == key:
                    v[count] = value
        mrc_fields[keyname] = '|'.join(v)
    else:
        for key, value in dictname.items():
            if v == key:
                mrc_fields[keyname] = value


all_fields = []
record_count = 0
with open(filename, 'rb') as fh:
    marc_recs = MARCReader(fh, to_unicode=True)
    for record in marc_recs:
        mrc_fields = {}
        leader = record.leader
        #  Finds fields/subfield values in record.
        field_finder('category', tags=['007'])
        field_finder('008', tags=['008'])
        subfield_finder('bib', subfields=['a'], tags=['910'])
        subfield_finder('oclc', subfields=['a'], tags=['035'])
        subfield_finder('links', subfields=['u'], tags=['856'])
        mrc_fields['title'] = record.title()
        subfield_finder('alt_title', subfields=['a', 'b'], tags=['246'])
        subfield_finder('statresp', subfields=['c'], tags=['245'])
        field_finder('desc500', tags=['500'])
        subfield_finder('language', subfields=['a', 'b', 'c', 'd', 'f'], tags=['041'])
        subfield_finder('temporal', subfields=['x', 'y'], tags=['034'])
        subfield_finder('barcode', subfields=['a', 'i'], tags=['991'])
        subfield_finder('iso_subject', subfields=['a'], tags=['690'])
        subfield_finder('geonames', subfields=['a'], tags=['691'])
        subfield_finder('genre', subfields=['a'], tags=['655'])
        field_finder('people', tags=['700', '100'])
        field_finder('corporate', tags=['110', '710'])
        subfield_finder('link', subfields=['u'], tags=['856'])
        catValue = mrc_fields.get('category')
        if catValue:
            mrc_fields['category'] = catValue[0]
        convert_to_name('category', cat_dict)
        convert_to_name('language', marc_lang)

        # Edit & convert values in dictionary.
        for k, v in mrc_fields.items():
            # Find DtSt and Dates from field 008.
            if k == '008':
                if v:
                    datetype = v[6]
                    date1 = v[7:11].strip()
                    date2 = v[11:15].strip()
                    lang = v[35:38]
                else:
                    datetype = ''
                    date1 = ''
                    date2 = ''
                    lang = ''
            # Finds only oclc number, deleting prefixes.
            elif k == 'oclc' and v != '':
                oclc_list = []
                v = v.split('|')
                for item in v:
                    item = str(item)
                    oclc_num = re.search(r'(\d+)', item)
                    if oclc_num:
                        oclc_num = oclc_num.group(1)
                        if oclc_num not in oclc_list:
                            if oclc_num != mrc_fields['bib'][0]:
                                oclc_list.append(oclc_num)
                v = '|'.join(str(e) for e in oclc_list)
                mrc_fields[k] = v

        del mrc_fields['008']
        mrc_fields['datetype'] = datetype
        convert_to_name('datetype', datetypes_dict)
        mrc_fields['date1'] = date1
        mrc_fields['date2'] = date2
        mrc_fields['lang'] = lang
        convert_to_name('lang', marc_lang)
        if mrc_fields.get('language') == '':
            mrc_fields['language'] = mrc_fields.get('lang')
        else:
            pass
        del mrc_fields['lang']

        # Adds dict created by this MARC record to all_fields list.
        all_fields.append(mrc_fields)
        record_count = record_count + 1
        print(record_count)

df = pd.DataFrame.from_dict(all_fields)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('marcRecords_'+dt+'.csv', index=False)