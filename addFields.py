from pymarc import MARCReader, Field, MARCWriter
import argparse
from datetime import datetime
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
parser.add_argument('-f2', '--file2')
args = parser.parse_args()
if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.mrc\'): ')
if args.file2:
    filename2 = args.file2
else:
    filename2 = input('Enter filename (including \'.csv\'): ')

df_meta = pd.read_csv(filename2, index_col='bib', dtype='str')
print(df_meta.columns)
print(df_meta.index)

out = open('file.dat', 'wb')

with open(filename, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
        if record:
            bib = record['910']['a']
            bib = int(bib)
            print(bib)
            url = df_meta.at[bib, 'identifier_access']
            ark = df_meta.at[bib, 'identifier_ark']
            ai_id = df_meta.at[bib, 'identifier']
            oclc = df_meta.at[bib, 'OCLC_number']
            if pd.notna(url) and pd.notna(ai_id):
                identifier = '(CaSfIA)'+ai_id
                f_856_sub = ['3', 'Internet Archive', 'u', str(url), 'w', str(identifier)]
                field_856 = Field(tag = '856', indicators = ['4', '1'], subfields = f_856_sub)
                record.add_field(field_856)
            if pd.notna(oclc):
                oclc = str(oclc)
                print(oclc)
                f_035_sub = ['a', oclc]
                field_035 = Field(tag = '035', indicators = [' ', ' '], subfields = f_035_sub)
                record.add_field(field_035)
            if pd.notna(ark):
                ark = str(ark)
                f_024_sub = ['a', ark, '2', 'arkid',]
                field_024 = Field(tag = '024', indicators = ['7', ' '], subfields = f_024_sub)
                record.add_field(field_024)
            print(record.title())
        out.write(record.as_marc())
    out.close()
