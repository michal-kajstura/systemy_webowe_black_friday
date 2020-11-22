import os
from threading import Thread

import gspread

from api import PageSpeedAPI, GTMetrixAPI, IsAlive
from utils import run_probing, SpreadsheetWriter

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

credentials_pool = [
    ('glgkwzknsyebslemnv@niwghx.online', 'a19b3e94487495f2d5dbfa1624e54012'),
    ('ojcyucqnuemhkstode@tsyefn.com', '1b51a4715cbf07af63a29cc6df959c47'),
    ('mofixap434@1981pc.com', 'f8a4e8055f075bac79e349c715cbdc3d'),
    ('bewag35604@1981pc.com', '55713370c555e27ca212f8dbe24c53bb'),
    ('vabade4166@bcpfm.com', 'b96735edf39e312be4b7f9d5c11da2a3'),
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
    (pagespeed_api, pagespeed_writer, 30),
    (is_alive, is_alive_writer, 10),
    (gtmetrix_api, gtmetrix_writer, 5 * 60),
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
