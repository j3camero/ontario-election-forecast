import csv
import os
import shutil
import string

homepage_template = """
<html>
<head>
  <title>No Doug Ford</title>
  <meta name="description" content="Strategic voting guide for the 2018 Ontario provincial election. Anyone but Ford!" />
  <!-- <meta name=viewport content="width=device-width, initial-scale=1"> -->
  <link rel="stylesheet" type="text/css" href="style.css">
  <link rel="shortcut icon" type="image/x-icon" href="mapleleaf.ico">
</head>
<body>
{analytics}
<div class="provincetitle">Ontario Election 2018</div>
<p>If the election were held today, these are the projected seat counts
  based on the latest polls.</p>
{projected_barchart}
<p>Some moar text to replace.</p>
{hypothetical_barchart}
<p>Register to vote and such.</p>
<div class="footnote">Projections updated {update_date}</div>
<div class="provincetitle">Strategic Vote Lookup for All 124 Ontario Ridings
</div>
{ridings}
<p>
  More information about
  <a href="https://en.wikipedia.org/wiki/Tactical_voting">
  strategic voting</a>.
</p>
<p>
  All projections and strategic voting recommendations displayed on this page
  are calculated by an impartial algorithm.
  <a href="https://github.com/j3camero/ontario-election-forecast">
  The code is on GitHub</a>. The model forecasts the popular vote in all 124
  Ontario ridings using the 2014 election results, by-elections since 2014,
  and the latest polling data.
</p>
<p>
  Election forecasting is not an exact science. Many of the projections
  listed on this page will be wrong. The data is provided
  under the philosophy that an educated guess is better than no
  information at all.
</p>
<p>Register to vote aight?</p>
<div class="footnote">Projections updated {update_date}</div>
</body>
</html>
"""

# Clear the contents of the build directory, if any.
if os.path.exists('build'):
    shutil.rmtree('build')
os.mkdir('build')

# First pass through the riding forecasts to calculate seat totals.
projected_seats = {}
hypothetical_seats = {}
with open('riding-forecast.csv', 'rb') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        leader = row['Leader']
        hyp = row['Hypothetical']
        projected_seats[leader] = projected_seats.get(leader, 0) + 1
        hypothetical_seats[hyp] = hypothetical_seats.get(hyp, 0) + 1

with open('build/index.html', 'w') as homepage:
    html = homepage_template.format(
        analytics='',
        hypothetical_barchart='<p>What could be</p>',
        projected_barchart='<p>Projections</p>',
        ridings='<p>Riding data goes here.</p>',
        update_date='April 22, 2018')
    homepage.write(html)
