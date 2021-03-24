from io import BytesIO as IO

import pytest

from app.handlers import HandleRequests


@pytest.mark.parametrize(
	('my_request', 'expected'), [
		(b'/', "HTTP/1.0 400 Missing required argument: 'currency'"),
		(b'/?currency=USD', "HTTP/1.0 400 Missing required argument: 'amount'"),
		(b'/?currency=smth&amount=0', 'HTTP/1.0 400 Unknown currency'),
		(b'/?currency=USD&amount=str', 'HTTP/1.0 400 Amount must be float'),
	]
)
def test_do_get_exception(my_request, expected):
	class TestableHandler(HandleRequests):
		wbufsize = 1

		def finish(self):
			self.wfile.flush()
			self.rfile.close()

		def date_time_string(self, timestamp=None):
			""" Mocked date time string """
			return 'DATETIME'

		def version_string(self):
			""" mock the server id """
			return 'BaseHTTP/x.x Python/x.x.x'

	class MockSocket(object):
		def getsockname(self):
			return 'sockname',

	class MockRequest(object):
		_sock = MockSocket()

		def __init__(self, path):
			self._path = path

		def makefile(self, *args, **kwargs):
			if args[0] == 'rb':
				return IO(b"GET %s HTTP/1.0" % self._path)
			elif args[0] == 'wb':
				return IO(b'')
			else:
				raise ValueError("Unknown file type to make", args, kwargs)

	handler = TestableHandler(MockRequest(my_request), (0, 0), None)
	assert handler.wfile.getvalue().decode('UTF-8').split('\r\n')[0] == expected
