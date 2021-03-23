import json
from http.server import HTTPServer
from urllib.request import urlopen

import pytest

from main import HandleRequests

HOST = '127.0.0.1'
PORT = 9000


@pytest.fixture(scope='module')
def server():
	with HTTPServer((HOST, PORT), HandleRequests) as server:
		yield server


def test_get(server, mocker):
	mocker.patch('main.parse_rate', return_value=0)
	response = json.loads(urlopen(f'http://{HOST}:{PORT}/?currency=USD&amount=32').read())
	print(response)
	assert response['conversion_amount'] == 0





