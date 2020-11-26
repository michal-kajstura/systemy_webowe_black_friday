import os
from threading import Thread

import gspread

from api import PageSpeedAPI, GTMetrixAPI, IsAlive
from utils import run_probing, SpreadsheetWriter

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

credentials_pool = [
    ('xzolltgvggpenhjotb@niwghx.online', '60e84f310e6667fa5d7c6a30f9b3dcff'),
    ('tsuwofydhgrboggtui@kiabws.online', '535c0eab867adaa6e0c4cd4eada62a3c'),
    ('ofe78683@bcaoo.com', '061a25a58fde27f7bd6ca27210c650e1'),
    ('hakedi4977@tdcryo.com', '3cb141e5c02e20c8cc77fc66fd2577df'),
    ('betokob432@tdcryo.com', '96765f08639a5ca03210645d0455023b'),
    ('locavog447@tdcryo.com', '9f32620da2ef3a1524f23351a020006e'),
    ('dakov44406@tdcryo.com', '7d65608cbd9295d550fc27f7a468ee4d'),
]

sites = {
    'x-kom': 'https://www.x-kom.pl',
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
    (pagespeed_api, pagespeed_writer, 60),
    (is_alive, is_alive_writer, 30),
    (gtmetrix_api, gtmetrix_writer, 10 * 60),
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
