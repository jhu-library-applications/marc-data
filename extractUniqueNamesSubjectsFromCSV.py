import csv

filename = 'marcFields.csv'

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    personalNames = []
    for row in reader:
        if row['tag'] == '100':
            if row['value'] not in personalNames:
                personalNames.append(row['value'])
        if row['tag'] == '600':
            if row['value'] not in personalNames:
                personalNames.append(row['value'])
        if row['tag'] == '700':
            if row['value'] not in personalNames:
                personalNames.append(row['value'])
        personalNames.sort()

f=csv.writer(open('personalNamesUnique.csv', 'w'))
f.writerow(['value'])
for name in personalNames:
    f.writerow([name])

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    corporateNames = []
    for row in reader:
        if row['tag'] == '110':
            if row['value'] not in corporateNames:
                corporateNames.append(row['value'])
        if row['tag'] == '610':
            if row['value'] not in corporateNames:
                corporateNames.append(row['value'])
        if row['tag'] == '710':
            if row['value'] not in corporateNames:
                corporateNames.append(row['value'])
        corporateNames.sort()

f=csv.writer(open('corporateNamesUnique.csv', 'w'))
f.writerow(['value'])
for name in corporateNames:
    f.writerow([name])

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    miscNames = []
    for row in reader:
        if row['tag'].startswith('1') and row['tag'] != '100' and row['tag'] != '110':
            if row['value'] not in miscNames:
                miscNames.append(row['value'])
        if row['tag'].startswith('7') and row['tag'] != '700' and row['tag'] != '710':
            if row['value'] not in miscNames:
                miscNames.append(row['value'])
        miscNames.sort()

f=csv.writer(open('miscNamesUnique.csv', 'w'))
f.writerow(['value'])
for name in miscNames:
    f.writerow([name])

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    subjects = []
    for row in reader:
        if row['tag'].startswith('6') and row['tag'] != '600' and row['tag'] != '610':
            if row['value'] not in subjects:
                subjects.append(row['value'])
        subjects.sort()

f=csv.writer(open('subjectsUnique.csv', 'w'))
f.writerow(['value'])
for name in subjects:
    f.writerow([name])
