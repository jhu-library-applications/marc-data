import json
import csv
import time

def extractMarcField (tag):
    dataFields = record['record']['datafield']
    tagData = ''
    for dataField in dataFields:
        if dataField['tag'] == '910':
            bibnum = dataField['subfield']
            if isinstance(bibnum, basestring):
                bibnum = bibnum
            else:
                bibnum = bibnum[0]
    for dataField in dataFields:
        if dataField['tag'] == tag:
            value = dataField['subfield']
            indicator1 = dataField['ind1']
            indicator2 = dataField['ind2']
            if isinstance(value, basestring):
                tagData = value
            else:
                for subfield in value:
                    tagData = tagData + subfield + ' '
            if bibnum in missedBibs:
                f.writerow([bibnum]+[tag]+[indicator1]+[indicator2]+[tagData])

def extractMarcFieldStartsWith (digit):
    dataFields = record['record']['datafield']
    for dataField in dataFields:
        if dataField['tag'] == '910':
            bibnum = dataField['subfield']
            if isinstance(bibnum, basestring):
                bibnum = bibnum
            else:
                bibnum = bibnum[0]

    for dataField in dataFields:
        tagData = ''
        if dataField['tag'].startswith(digit):
            tagNumber = dataField['tag']
            value = dataField['subfield']
            indicator1 = dataField['ind1']
            indicator2 = dataField['ind2']
            if isinstance(value, basestring):
                tagData = value
            else:
                for subfield in value:
                    if isinstance(subfield, basestring):
                        tagData = tagData + subfield + '--'
            if bibnum in missedBibs:
                f.writerow([bibnum]+[tagNumber]+[indicator1]+[indicator2]+[tagData])

startTime = time.time()
file = input('Enter file name')

records = json.load(open(file))

f=csv.writer(open('marcFields.csv', 'wb'))
f.writerow(['bibnum']+['tag']+['indicator1']+['indicator2']+['value'])

for record in records:
    extractMarcFieldStartsWith('1')
    extractMarcField('245')
    extractMarcField('520')
    extractMarcField('540')
    extractMarcField('544')
    extractMarcField('545')
    extractMarcField('561')
    extractMarcFieldStartsWith('6')
    extractMarcFieldStartsWith('7')

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
