import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from app.log.core import logger

URL = 'https://plus.yandex.ru/invest/catalog/currency/'


def parse_rate(currency: str) -> float:
	try:
		current_rate_response = urlopen(f'{URL}{currency.lower()}/').read().decode('UTF-8')
	except HTTPError:
		raise ValueError('Unknown currency')
	regex = re.compile(r'"askPrice":(\d+\.\d+),')
	groups = regex.search(current_rate_response)
	if groups is None:
		raise URLError('Price not found')
	logger.debug(
		f'Requested {currency.upper()} rate: {groups.group(1)}',
		extra={'client': ''}
	)
	return float(groups.group(1))
