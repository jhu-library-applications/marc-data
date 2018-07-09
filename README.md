# marc-data
Scripts for manipulating MARC-related data

#### [extractCompleteNamesSubjectsFromCSV](extractCompleteNamesSubjectsFromCSV.py)
Categorizes headings depending on the MARC tags used (e.g. 110,610, 710 as corporate names and 100, 600, 700 as personal names) and produces corresponding CSV files.

#### [extractMarcFields](extractMarcFields.py)
Produces a CSV of selected MARC fields from a JSON file of MARC data produced by [Traject](https://github.com/traject/traject).

#### [extractUniqueNamesSubjectsFromCSV](extractMarcFields.py)
Deduplicates and categorizes headings depending on the MARC tags used (e.g. 110,610, 710 as corporate names and 100, 600, 700 as personal names) and produces corresponding CSV files.
