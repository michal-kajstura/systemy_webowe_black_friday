import os
from threading import Thread

import gspread

from api import PageSpeedAPI, GTMetrixAPI, IsAlive
from utils import run_probing, SpreadsheetWriter

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

credentials_pool = [
    ('mjxplttymwzqrqarsm@upived.com', '286b0fd5e5941076685b317bd836be8d'),
    ('hakot84492@questza.com', '8536ddb5c83a7ed54ae70a1e3ce90049'),
    ('ronoc49785@tdcryo.com', 'cc42db19efb79747f3f7301777377098'),
    ('labamer331@questza.com', 'cfffee8155519f941ba15ad873534827'),
    ('famipek180@dkt1.com', 'e05160bce1540ecd701278abf74f03df'),
    ('jxnma6ndg1ne@10minut.xyz', '21fc0abdffe157ad76b5256c91e71632'),
    ('abb20858@eoopy.com', '1f2c7c8e3e2f81d3680c5798bef7d6fd'),
    ('peram71797@dkt1.com', 'b6b38d1af2f48841607ade2cd430db20'),
    ('dft50783@cuoly.com', '88baeddd58f4a0a75da4c5837ca5916f'),
    ('podege3372@xhypm.com', 'ade194f4a9dee48d9537b9ed473b27aa'),
    ('ljr62605@eoopy.com', 'a7db053b9337e21147bc3906929cd5f7'),
    ('xofopa9778@questza.com', 'd485a3d2de77597546b1eee17e079527'),
]

sites = {
    'allegro': 'https://www.allegro.pl',
    'morele': 'http://www.morele.pl',
    'x-kom': 'https://www.x-kom.pl',
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
pagespeed_writer = SpreadsheetWriter(pagespeed_worksheet, start_from_row=3830)
gtmetrix_writer = SpreadsheetWriter(gtmetrix_worksheet, start_from_row=504)
is_alive_writer = SpreadsheetWriter(is_alive_worksheet, start_from_row=11750)

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
