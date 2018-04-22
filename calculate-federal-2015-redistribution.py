# Calculates how many voters moved from each old district to each new district
# as a result of Canada's 2015 federal redistricting. This affects Ontario
# because most of Ontario's electoral districts are based on the federal ones.

import csv
import sys

transfers = set()

def handle_row(row, writer):
    new_id = row['2013 FED Number']
    new_name = row['2013 FED Name']
    old_id = row['2003 FED Number from which the 2013 FED Number ' +
                 'is constituted']
    old_name = row['2003 FED from which the 2013 FED Name is constituted']
    pop_moved = row['Population transferred to 2013 FED']
    new_total_pop = row['2013 FED - Population']
    province = row['Province and territory numeric code']
    # Ontario only.
    if province != '35':
        return
    if pop_moved in [0, '0', '']:
        return
    if (new_id, old_id) in transfers:
        return
    transfers.add((new_id, old_id))
    writer.writerow([new_id, new_name, new_total_pop,
                     old_id, old_name, pop_moved])

with open('TRANSPOSITION_338FED.csv', 'rb') as input_file:
    with open('ontario-federal-transposition.csv', 'wb') as output_file:
        # Skip the first few lines of the file, to get to the data part.
        for i in range(4):
            next(input_file)
        reader = csv.DictReader(input_file)
        writer = csv.writer(output_file)
        writer.writerow(
            ['New District ID', 'New District Name', 'New Total Population',
             'Old District ID', 'Old District Name', 'Population Transferred'])
        for row in reader:
            handle_row(row, writer)
