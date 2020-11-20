import abc
import time
from itertools import cycle

import requests


class API(abc.ABC):
    @abc.abstractmethod
    def query(self, api_url, **params):
        pass


class PageSpeedAPI(API):
    _api_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

    def __init__(self, api_key, keys_to_extract):
        self._api_key = api_key
        self._keys_to_extract = keys_to_extract

    def query(self, url, **params):
        result = requests.get(
            self._api_url,
            params={
                'key': self._api_key,
                'url': url,
                'category': 'performance',
                **params,
            }
        )
        result_json = result.json()
        res = result_json
        for key in self._keys_to_extract:
            res = res[key]
        return res[0]


class NoCreditsLeft(Exception):
    pass


class GTMetrixAPI(API):
    _api_url = 'https://gtmetrix.com/api/0.1'

    def __init__(self, credentials_pool, retries=30):
        self._credentials = cycle(credentials_pool)
        self._retries = retries

    def query(self, url, **params):
        username, api_key = next(self._credentials)
        test_request = requests.post(
            f'{self._api_url}/test',
            data={'url': url, 'location': '3'},
            auth=(username, api_key),
        )
        test_request_json = test_request.json()
        credits_left = test_request_json['credits_left']
        test_id = test_request_json['test_id']
        poll_url = test_request_json['poll_state_url']

        print(f'{username} credits left: {credits_left}')
        if credits_left == 0:
            raise NoCreditsLeft()

        result = None
        for _ in range(self._retries):
            time.sleep(2)

            test_json = requests.get(
                poll_url,
                auth=(username, api_key)
            ).json()

            status = test_json['state']
            if status in {'queued', 'started'}:
                continue
            elif status == 'error':
                break
            else:
                return test_json['results']
