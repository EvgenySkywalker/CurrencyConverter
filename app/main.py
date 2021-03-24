from http.server import HTTPServer

from app.log.core import logger
from handlers import HandleRequests

HOST = '127.0.0.1'
PORT = 9000
logger.info(
	f'Http Server Serving at {HOST}:{PORT}',
	extra={'client': ''}
)
HTTPServer((HOST, PORT), HandleRequests).serve_forever()
