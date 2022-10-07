import json
import csv
import time


def extract_marc_field(tag):
    data_fields = record['record']['datafield']
    tag_data = ''
    for dataField in data_fields:
        if dataField['tag'] == '910':
            bib_number = dataField['subfield']
            if isinstance(bib_number, basestring):
                bib_number = bib_number
            else:
                bib_number = bib_number[0]
    for dataField in data_fields:
        if dataField['tag'] == tag:
            value = dataField['subfield']
            indicator1 = dataField['ind1']
            indicator2 = dataField['ind2']
            if isinstance(value, basestring):
                tag_data = value
            else:
                for subfield in value:
                    tag_data = tag_data + subfield + ' '
            if bib_number in missed_bibs:
                f.writerow([bib_number] + [tag] + [indicator1] + [indicator2] + [tag_data])


def extract_marc_field_starts_with(digit):
    data_fields = record['record']['datafield']
    for dataField in data_fields:
        if dataField['tag'] == '910':
            bib_number = dataField['subfield']
            if isinstance(bib_number, basestring):
                bib_number = bib_number
            else:
                bib_number = bib_number[0]
    for dataField in data_fields:
        tag_data = ''
        if dataField['tag'].startswith(digit):
            tag_number = dataField['tag']
            value = dataField['subfield']
            indicator1 = dataField['ind1']
            indicator2 = dataField['ind2']
            if isinstance(value, basestring):
                tag_data = value
            else:
                for subfield in value:
                    if isinstance(subfield, basestring):
                        tag_data = tag_data + subfield + '--'
            if bib_number in missed_bibs:
                f.writerow([bib_number]+[tag_number]+[indicator1]+[indicator2]+[tag_data])


startTime = time.time()
file = input('Enter file name')

records = json.load(open(file))

f = csv.writer(open('marcFields.csv', 'w'))
f.writerow(['bibnum']+['tag']+['indicator1']+['indicator2']+['value'])

for record in records:
    extract_marc_field_starts_with('1')
    extract_marc_field('245')
    extract_marc_field('520')
    extract_marc_field('540')
    extract_marc_field('544')
    extract_marc_field('545')
    extract_marc_field('561')
    extract_marc_field_starts_with('6')
    extract_marc_field_starts_with('7')

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))