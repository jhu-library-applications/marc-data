from pymarc import Record, Field, Leader
import pandas as pd
import ast
import numpy as np

df = pd.read_csv('AFABriefBibs_2022-10-28.csv', encoding='utf8')
df = df.fillna(value=np.nan)


def addfieldfromsheet(field_tag, indicators, subfields):
    record.add_field(
        Field(
            tag=field_tag,
            indicators=indicators,
            subfields=subfields))


my_marc_records = []
for index, row in df.iterrows():
    print(index)
    record = Record(force_utf8=True)
    ind_blanks = [' ', ' ']
    new_leader = Leader(record.leader)
    # Sets Record Status
    new_leader.record_status = 'n'
    # Sets Type
    new_leader.type_of_record = 'g'
    # Sets BLvl
    new_leader.bibliographic_level = 'm'
    # Sets ELvl
    new_leader.encoding_level = '3'
    # Sets Desc
    new_leader.cataloging_form = 'i'
    record.leader = new_leader

    # Add 007 field
    field_007 = 'vruuuuuuu'
    field = Field(tag='007', data=field_007)
    record.add_field(field)

    # Add 008 field
    byte00_05 = '220820'
    byte06 = row['DtSt']
    byte07_10 = str(row['date_1'])
    date_2 = row.get('date_2')
    if pd.notna(date_2):
        byte11_14 = str(date_2)
    else:
        byte11_14 = '    '
    byte15_17 = 'xx '
    run_time = row.get('run_time')
    run_time = str(run_time).zfill(3)
    byte18_20 = run_time
    byte21_27 = '       '
    byte28 = 'u'
    byte29_32 = '    '
    byte33 = 'm'
    byte34 = 'u'
    byte35_37 = row['language']
    byte38 = ' '
    byte39 = 'c'
    field_008 = byte00_05 + byte06 + byte07_10 + byte11_14 + byte15_17 + byte18_20 + byte21_27 + byte28 + byte29_32 + \
                byte33 + byte34 + byte35_37 + byte38 + byte39
    print(len(field_008))
    field = Field(tag='008', data=field_008)
    record.add_field(field)

    # Add local identifiers.
    film_id = row['film_id']
    film_id = str(film_id).zfill(4)
    with_prefix_film_id = 'AFADatabaseID_' + film_id
    fields_099 = ['a', with_prefix_film_id]
    addfieldfromsheet('099', ind_blanks, fields_099)

    # Add 041 field
    field_041 = row.get('lang')
    if pd.notna(field_041):
        field_041 = ast.literal_eval(field_041)
        addfieldfromsheet('041', ['1', ' '], field_041)
    else:
        pass

    # Add translation of title.
    a_242 = row.get('242_a')
    b_242 = row.get('242_b')
    ii_242 = row.get('242_2')
    ii_242 = str(ii_242)
    ind_242 = ['1', ii_242]
    if pd.notna(b_242):
        fields_242 = ['a', a_242 + ': ', 'b', b_242 + ' /']
        addfieldfromsheet('242', ind_242, fields_242)
    elif pd.notna(a_242):
        fields_242 = ['a', a_242 + '/']
        addfieldfromsheet('242', ind_242, fields_242)
    else:
        pass

    # Add title statement.
    a_245 = row.get('245_a')
    b_245 = row.get('245_b')
    n_245 = row.get('245_n')
    if pd.notna(b_245) and pd.notna(n_245):
        fields_245 = ['a', a_245 + '.', 'n', n_245 + ':', 'b', b_245 + ' /']
    elif pd.notna(b_245):
        fields_245 = ['a', a_245 + ' : ', 'b', b_245 + ' /']
    elif pd.notna(n_245):
        fields_245 = ['a', a_245 + '.', 'n', n_245]
    else:
        fields_245 = ['a', a_245 + ' /']
    ii_245 = row['245_2']
    ii_245 = str(ii_245)
    ind_245 = ['0', ii_245]
    addfieldfromsheet('245', ind_245, fields_245)

    # Add varying form of title.
    a_246 = row.get('246_a')
    if pd.notna(a_246):
        addfieldfromsheet('246', ['3', ' '], ['a', a_246])
    else:
        pass

    # Add edition information.
    a_250 = row.get('250_a')
    if pd.notna(a_250):
        addfieldfromsheet('250', ind_blanks, ['a', a_250])
    else:
        pass

    # Add publication information.
    c_264 = row['264_c']
    c_264 = str(c_264)
    ind_264 = [' ', '1']
    fields_264 = ['a', '[Place of publication not identified] :', 'b', '[publisher not identified], ', 'c', c_264]
    addfieldfromsheet('264', ind_264, fields_264)

    # Add extent information.
    a_300 = row['300_a']
    b_300 = row['300_b']
    c_300 = '16 mm'
    fields_300 = ['a', a_300 + ' :', 'b', b_300 + ' ;', 'c', c_300]
    addfieldfromsheet('300', ind_blanks, fields_300)

    # Add content and media type.
    addfieldfromsheet('336', ind_blanks, ['a', 'two-dimensional moving image', 'b', 'tdi', '2', 'rdacontent'])
    addfieldfromsheet('337', ind_blanks, ['a', 'video', 'b', 'v', '2', 'rdamedia'])
    addfieldfromsheet('338', ind_blanks, ['a', 'film reel', 'b', 'mr', '2', 'rdacarrier'])
    # Add 500 note.
    a_500 = row.get('500_a')
    if pd.notna(a_500):
        addfieldfromsheet('500', ind_blanks, ['a', a_500])
    else:
        pass

    # Add gift note.
    addfieldfromsheet('541', ind_blanks, ['3', 'Sheridan Libraries copy : ', 'c',
                                          'Gift of Geoff Alexander, Director, Academic Film Archive of North America;',
                                          'd', 'FY2022.', '5', 'JHE.'])

    # Add source of description note.
    addfieldfromsheet('588', ['0', ' '], ['a',
                                          'Description in record from Academic Film Archive database; '
                                          'physical films were not viewed.'])

    # Add local note about physical condition.
    a_590 = row.get('590_a')
    if pd.notna(a_590):
        addfieldfromsheet('590', ['1', ' '], ['a', a_590])
    else:
        pass

    # Add collection note.
    addfieldfromsheet('710', ['2', ' '], ['a', 'Academic Film Archive of North America Collection.', '5', 'JHE'])
    # Add corporate bodies.
    corporate_bodies = row.get('corporate_bodies')
    if pd.notna(corporate_bodies):
        corporate_bodies = corporate_bodies.split("|")
        for corporate_body in corporate_bodies:
            corporate_body = ast.literal_eval(corporate_body)
            addfieldfromsheet('710', ['2', ' '], corporate_body)
    else:
        pass

    # Add series if available.
    t_760 = row.get('760_t')
    if pd.notna(t_760):
        addfieldfromsheet('760', ['0', '8'], ['i', 'In series:', 't', t_760])
    else:
        pass

    # Add URL if available.
    u_856 = row.get('856_u')
    w_856 = row.get('856_w')
    iii_856 = row.get('856_3')
    iii_856 = str(iii_856)
    if pd.notna(u_856):
        links = u_856.split('|')
        for link in links:
            if pd.notna(w_856):
                addfieldfromsheet('856', ['4', '1'], ['3', iii_856, 'u', link, 'w', w_856])
            else:
                addfieldfromsheet('856', ['4', '1'], ['3', iii_856, 'u', link])
    else:
        pass

    # Add item information
    total_reels = row['reels'].strip()
    if total_reels != "unknown":
        total_reels = int(total_reels)
        for reel_no in range(total_reels):
            reel_no = reel_no + 1
            item_type = 'enonav'  # subfield h
            location = 'elsc'  # subfield c
            collection = 'eofav'  # subfield d
            call_type = 'eformat'  # subfield b
            call_no = 'Video ' + film_id  # subfield a
            copy_statement = 'reel ' + str(reel_no)  # subfield g
            item_status = 't'  # subfield z
            addfieldfromsheet('970', ['1', ' '], ['h', item_type, 'c', location, 'd', collection, 'b', call_type, 'a',
                                                  call_no, 'g', copy_statement, 'z', item_status])

    print(record)
    my_marc_records.append(record)


# Divide list of records into n-sized batches


def divide_chunks(list_to_divide, n):
    # looping till length l
    for i in range(0, len(list_to_divide), n):
        yield list_to_divide[i:i + n]


batches_marc_records = list(divide_chunks(my_marc_records, 1000))
for index, batch in enumerate(batches_marc_records):
    index = index + 1
    index = str(index).zfill(2)
    # Create a new dat file.
    my_new_marc_filename = 'AFABriefBibs_' + index + '.dat'
    with open(my_new_marc_filename, 'wb') as data:
        for my_record in batch:
            data.write(my_record.as_marc())