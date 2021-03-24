import json
from http import HTTPStatus
from urllib.error import URLError
from http.server import BaseHTTPRequestHandler

from app.log.core import logger
from app.converting.converter import conversion


class HandleRequests(BaseHTTPRequestHandler):
	def _set_headers(self, code):
		self.send_response(code)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		try:
			try:
				result = conversion(self.path)
				self._set_headers(HTTPStatus.OK)
				self.wfile.write(
					json.dumps(result).encode('UTF-8')
				)
				logger.info(
					f"GET RESPONSE {result['conversion_currency'] = }, {result['conversion_amount'] = :.2f}",
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
