# Calculates how many voters moved from each old district to each new district
# as a result of Canada's 2015 federal redistricting. This affects Ontario
# because most of Ontario's electoral districts are based on the federal ones.

import csv
import sys

def die(message):
    print message
    sys.exit()

# The keys are tuples: (new_district_id, old_district_id)
# The values are the number of people transferred.
transfers = {}

# District names, keyed by district ID.
new_names = {}
old_names = {}

with open('TRANSPOSITION_338FED.csv', 'rb') as input_file:
    # Skip the first few lines of the file, to get to the data part.
    for i in range(4):
        next(input_file)
    reader = csv.DictReader(input_file)
    for row in reader:
        new_id = row['2013 FED Number']
        new_name = row['2013 FED Name']
        old_id = row['2003 FED Number from which the 2013 FED Number ' +
                     'is constituted']
        old_name = row['2003 FED from which the 2013 FED Name is constituted']
        pop_moved = row['Population transferred to 2013 FED']
        province = row['Province and territory numeric code']
        # Ontario only.
        if province != '35':
            continue
        if (new_id, old_id) in transfers:
            # Sanity check to make sure the data is self-consistent.
            if transfers[(new_id, old_id)] != pop_moved:
                die('Conflicting information found.')
        transfers[(new_id, old_id)] = pop_moved
        new_names[new_id] = new_name
        old_names[old_id] = old_name
with open('ontario-federal-transposition.csv', 'wb') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['New District ID', 'New District Name', 'Old District ID',
                     'Old District Name', 'Population Transferred'])
    for new_id, old_id in sorted(transfers.keys()):
        writer.writerow([new_id, new_names[new_id],
                         old_id, old_names[old_id],
                         transfers[(new_id, old_id)]])
