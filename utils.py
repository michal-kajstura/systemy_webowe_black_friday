import time
from datetime import datetime


def save(result, worksheet, row, header=False):
    #     max_col = chr(ord('A') + len(result))
    keys = list(result.keys())
    values = list(result.values())
    max_col = 'AM' if len(keys) == 37 else 'X'
    if header:
        worksheet.update(f'A1:{max_col}1', [keys])

    worksheet.update(f'A{row}:{max_col}{row}', [values])


def run(api_and_sheets, sites, sleep_in_sec=120):
    row = 2
    header = True
    while True:
        for name, url in sites.items():
            for api, worksheet in api_and_sheets:
                result = api.query(url)

                if result is None:
                    continue

                now = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                print(f'{now} - {result}')
                result['site'] = name
                result['time'] = now
                save(result, worksheet, row, header)
            row += 1
            header = False

        time.sleep(sleep_in_sec)