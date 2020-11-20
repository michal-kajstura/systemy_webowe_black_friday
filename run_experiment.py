import os

import gspread

from api import PageSpeedAPI, GTMetrixAPI
from utils import run

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

credentials_pool = [
    ('uph02154@eoopy.com', 'd6e3713ad0228616517e366aad4db7e9'),
    ('kojohi3627@bcpfm.com', '6d63a4153e3bc9278fa3d1a94b2c140d'),
    ('fajag83615@bcpfm.com', '076c2642acedf4d5481eb8685ef99ec8')
]

sites = {
    'xkom': 'http://xkom.pl',
    'morele': 'http://morele.pl',
}


pagespeed_api = PageSpeedAPI(
    api_key=GOOGLE_API_KEY,
    keys_to_extract=('lighthouseResult', 'audits', 'metrics', 'details', 'items'),
)
gtmetrix_api = GTMetrixAPI(credentials_pool)

gc = gspread.service_account()
spreadsheet = gc.open('Black Friday - SW')
# pagespeed_worksheet = spreadsheet.add_worksheet(title="Pagespeed", rows="1000", cols="50")
# gtmetrics_worksheet = spreadsheet.add_worksheet(title="GTMetrix", rows="1000", cols="50")
pagespeed_worksheet, gtmetrix_worksheet = spreadsheet.worksheets()
run(
    api_and_sheets=[(pagespeed_api, pagespeed_worksheet), (gtmetrix_api, gtmetrix_worksheet)],
    sites=sites
)
