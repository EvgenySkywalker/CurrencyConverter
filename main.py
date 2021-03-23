import json
from time import sleep
from http import HTTPStatus
from urllib.error import URLError
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

from log.core import logger
from rate_parsing.parsers import parse_rate
from converting.converter import convert_to_rub

HOST = '127.0.0.1'
PORT = 9000


class HandleRequests(BaseHTTPRequestHandler):
	def _set_headers(self, code):
		self.send_response(code)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		try:
			try:
				query_components = parse_qs(urlparse(self.path).query)
				currency = str(query_components['currency'][0])
				if not query_components['amount'][0].isdigit():
					raise ValueError('Amount must be float')
				amount = float(query_components['amount'][0])
				rate = parse_rate(currency)
				conversion_currency, conversion_amount = convert_to_rub(amount, rate)
				self._set_headers(HTTPStatus.OK)
				self.wfile.write(
					json.dumps({
						'given_currency': currency, 'given_amount': amount,
						'conversion_currency': conversion_currency, 'conversion_amount': f'{conversion_amount:.2f}'
					}).encode('UTF-8')
				)
				logger.info(
					f'GET RESPONSE {conversion_currency = }, {conversion_amount = :.2f}',
					extra={'client': self.client_address[0]}
				)
			except URLError as e:
				self.send_error(HTTPStatus.SERVICE_UNAVAILABLE, str(e))
			except ValueError as e:
				logger.error(e, extra={'client': self.client_address[0]})
				self.send_error(HTTPStatus.BAD_REQUEST, str(e))
			except KeyError as e:
				logger.error(f'Missing required argument: {e}', extra={'client': self.client_address[0]})
				self.send_error(HTTPStatus.BAD_REQUEST, f'Missing required argument: {e}')
		except (ConnectionAbortedError, ConnectionResetError) as e:
			logger.error(
				f'Connection error: {e}',
				extra={'client': self.client_address[0]}
			)

	def log_message(self, _, *args):
		pass


logger.info(
	f'Http Server Serving at {HOST}:{PORT}',
	extra={'client': ''}
)
