import csv

def main():
    '''Creates extended_bigrams.csv and extended_chars.csv to be used to create extended_stats.csv. Reads .txt-files found here: http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/swedish-letter-frequencies/ '''
    create_extended_chars()
    create_extended_bigrams()
    create_extended_stats()

def _read_that_txt_format(name):
    with open(name) as fb:
        _file = csv.reader(fb, delimiter=' ')
        return {row[0].lower(): row[1] for row in _file}

def _add_new_letters_to_old_csv_file(old_file_name, new_data):
    old_file = {}
    n = 1
    with open(old_file_name) as fb:
        _old_file = csv.reader(fb, delimiter=',')
        for row in _old_file:
            old_file[row[0].lower()] = row[1:]
            n = len(row)

    old_keys = old_file.keys()
    added_new_letters = []
    for key, value in new_data.items():
        if key not in old_keys:
            added_new_letters.append( [key] + ['0'] * (n-1))
    return added_new_letters

def _append_row_to_csv_file(old_file_name, padding_data, new_data):
    with open(old_file_name) as fb:
        old_file = list(csv.reader(fb, delimiter=','))
    old_file += padding_data
    new_file = []
    for row in old_file:
        try:
            new_file.append(row + [new_data[row[0]]])
        except KeyError:
            if row[0] == '':
                new_file.append(row + ['vrac_swe'])
            else:
                new_file.append(row + ['0'])
    return new_file

def _write_new_file(file_name, new_data):
    with open(file_name, 'w', newline='') as fb:
        writer = csv.writer(fb,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
        for row in new_data:
            writer.writerow(row)

def create_extended_chars():
    swe_chars = _read_that_txt_format('swedish_monograms.txt')
    padding_data = _add_new_letters_to_old_csv_file('chars.csv', swe_chars)
    new_data = _append_row_to_csv_file('chars.csv', padding_data, swe_chars)
    _write_new_file('extended_chars.csv', new_data)

def create_extended_bigrams():
    swe_bigrams = _read_that_txt_format('swedish_bigrams.txt')
    padding_data = _add_new_letters_to_old_csv_file('bigrams.csv', swe_bigrams)
    new_data = _append_row_to_csv_file('bigrams.csv', padding_data, swe_bigrams)
    _write_new_file('extended_bigrams.csv', new_data)

def create_extended_stats():
    total = 0
    swe_bigrams = {}
    with open('swedish_bigrams.txt') as fb:
        _file = csv.reader(fb, delimiter=' ')
        for row in _file:
            total += int(row[1])
            swe_bigrams[row[0].lower()] = row[1]

    padding_data = _add_new_letters_to_old_csv_file('../layout_evaluation/stats.csv', swe_bigrams)

    new_file = []
    with open('../layout_evaluation/stats.csv') as fb:
        old_file = csv.reader(fb, delimiter=',')
        old_file = list(old_file) + padding_data
        for row in old_file:
            try:
                new_file.append(row + [format( (int(swe_bigrams[row[0]]) / total) , '.6f')])
            except KeyError:
                if row[0] == '':
                    new_file.append(row + ['swe'])
                else:
                    new_file.append(row + ['0'])

    _write_new_file('../layout_evaluation/extended_stats.csv', new_file)

if __name__ == '__main__':
    main()
