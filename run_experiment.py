import os
from threading import Thread

import gspread

from api import PageSpeedAPI, GTMetrixAPI, IsAlive
from utils import run_probing, SpreadsheetWriter

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

credentials_pool = [
    ('uph02154@eoopy.com', 'd6e3713ad0228616517e366aad4db7e9'),
    ('kojohi3627@bcpfm.com', '6d63a4153e3bc9278fa3d1a94b2c140d'),
    ('fajag83615@bcpfm.com', '076c2642acedf4d5481eb8685ef99ec8')
]

sites = {
    'x-kom': 'https://www.x-kom.pl/g/2-laptopy-i-komputery.html',
    'morele': 'http://www.morele.pl',
}

pagespeed_api = PageSpeedAPI(
    api_key=GOOGLE_API_KEY,
    keys_to_extract=('lighthouseResult', 'audits', 'metrics', 'details', 'items'),
)
gtmetrix_api = GTMetrixAPI(credentials_pool)
is_alive = IsAlive()

gc = gspread.service_account()
spreadsheet = gc.open('Black Friday - SW')
pagespeed_worksheet, gtmetrix_worksheet, is_alive_worksheet = spreadsheet.worksheets()
pagespeed_writer = SpreadsheetWriter(pagespeed_worksheet)
gtmetrix_writer = SpreadsheetWriter(gtmetrix_worksheet)
is_alive_writer = SpreadsheetWriter(is_alive_worksheet)

params = (
    (pagespeed_api, pagespeed_writer, 30),
    (is_alive, is_alive_writer, 10),
    (gtmetrix_api, gtmetrix_writer, 60),
)


for api, writer, sleep_time in params:
    Thread(
        target=lambda: run_probing(api, writer, sites, sleep_in_sec=sleep_time),
        daemon=True,
    ).start()

while True:
    exit = input('Quit?')

    if exit == 'yes':
        break
