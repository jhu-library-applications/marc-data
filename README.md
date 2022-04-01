# marc-data
Scripts for manipulating MARC-related data.



## Libraries and tools

- [pymarc](https://pymarc.readthedocs.io/en/latest/)
- [pandas](https://pandas.pydata.org/)
- [MarcEdit](https://marcedit.reeset.net/)

## Script descriptions

### Extract
#### [extractCompleteNamesSubjectsFromCSV](extractCompleteNamesSubjectsFromCSV.py)
Categorizes headings depending on the MARC tags used (e.g. 110, 610, 710 as corporate names and 100, 600, 700 as personal names) and produces corresponding CSV files.

#### [extractMarcFields](extractMarcFields.py)
Produces a CSV of selected MARC fields from a JSON file of MARC data produced by [Traject](https://github.com/traject/traject).

#### [extractUniqueNamesSubjectsFromCSV](extractUniqueNamesSubjectsFromCSV.py)
Deduplicates and categorizes headings depending on the MARC tags used (e.g. 110, 610, 710 as corporate names and 100, 600, 700 as personal names) and produces corresponding CSV files.

### Edit
#### [addFields.py](addFields.py)
Adds fields based on spreadsheet with column 'bib', which is made into the DataFrame index. Uses `at[]` to grab the correct value for that bib.

*Note on encoding/diacritics:*
- To get this to work in our LMS (Horizon), I used MarcEdit to convert the .mrc export file from Horizon to UTF-8 in MarcEdit using *Tools→Character Conversion→CharacterSet Conversions* with "Original Encoding" set to MARC8 and "Final Encoding" to UTF-8.
- Then I ran the new converted .mrc file against addFields.py to get the output file called file.dat.
- The output file, file.dat, when opened in MarcEdit should show all of the diacritics without any encoding errors. However, the diacritics were still an issue in Horizon (the character disappeared and left a missing letter) so then I converted the output file from this script (file.dat) from UTF-8 to MARC-8 in MarcEdit using *Tools→Character Conversions→CharacterSet Conversion* with "Original Encoding" set to UTF-8 and "Final Encoding" to MARC8.
