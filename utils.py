import time
from datetime import datetime


def run_probing(api, writer, sites, sleep_in_sec=120):
    while True:
        for name, url in sites.items():
            try:
                result = api.query(url)

                if result is None:
                    continue

                now = datetime.now().strftime('%H:%M:%S, %d/%m/%Y')
                print(f'{now} - {result}')
                result['site'] = name
                result['time'] = now

                writer.write(result)

            except Exception as e:
                print(e)

        time.sleep(sleep_in_sec)


class SpreadsheetWriter:
    def __init__(self, worksheet, start_from_row=1):
        self._worksheet = worksheet
        self._row = start_from_row
        self._write_header = self._row == 1
        self._first = True
        self._keys = None

    def write(self, result):
        self._keys = self._keys or list(result.keys())
        values = [result[k] for k in self._keys]
        max_col = self._column_num_to_string(len(values))
        if self._write_header:
            self._worksheet.update(f'A1:{max_col}1', [self._keys])
            self._write_header = False
            self._row += 1
        elif self._first:
            self._keys = self._worksheet.row_values(1)
            self._first = False

        self._worksheet.update(f'A{self._row}:{max_col}{self._row}', [values])
        self._row += 1

    def _column_num_to_string(self, n):
        n, rem = divmod(n - 1, 26)
        char = chr(65 + rem)
        if n:
            return self._column_num_to_string(n) + char
        else:
            return char
