import csv

filename = 'marcFields.csv'

f=csv.writer(open('personalNamesComplete.csv', 'wb'))
f.writerow(['bibnum']+['value'])
f2=csv.writer(open('corporateNamesComplete.csv', 'wb'))
f2.writerow(['bibnum']+['value'])
f3=csv.writer(open('miscNamesComplete.csv', 'wb'))
f3.writerow(['bibnum']+['value'])
f4=csv.writer(open('subjectsComplete.csv', 'wb'))
f4.writerow(['bibnum']+['value'])

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        bibnum = row['bibnum']
        #personal
        if row['tag'] == '100':
            f.writerow([bibnum]+[row['tag']]+[row['value']])
        if row['tag'] == '600':
            f.writerow([bibnum]+[row['tag']]+[row['value']])
        if row['tag'] == '700':
            f.writerow([bibnum]+[row['tag']]+[row['value']])
        #corporate
        if row['tag'] == '110':
            f2.writerow([bibnum]+[row['tag']]+[row['value']])
        if row['tag'] == '610':
            f2.writerow([bibnum]+[row['tag']]+[row['value']])
        if row['tag'] == '710':
            f2.writerow([bibnum]+[row['tag']]+[row['value']])
        #miscNames
        if row['tag'].startswith('1') and row['tag'] != '100' and row['tag'] != '110':
            f3.writerow([bibnum]+[row['tag']]+[row['value']])
        if row['tag'].startswith('7') and row['tag'] != '700' and row['tag'] != '710':
            f3.writerow([bibnum]+[row['tag']]+[row['value']])
        #subjects
        if row['tag'].startswith('6') and row['tag'] != '600' and row['tag'] != '610':
            f4.writerow([bibnum]+[row['tag']]+[row['value']])
