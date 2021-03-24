from typing import Tuple
from urllib.parse import urlparse, parse_qs

from app.log.core import logger
from app.rate_parsing.parsers import parse_rate


def conversion(path: str):
	query_components = parse_qs(urlparse(path).query)
	currency = str(query_components['currency'][0])
	if not query_components['amount'][0].isdigit():
		raise ValueError('Amount must be float')
	amount = float(query_components['amount'][0])
	rate = parse_rate(currency)
	conversion_currency, conversion_amount = convert_to_rub(amount, rate)
	return {
		'given_currency': currency, 'given_amount': amount,
		'conversion_currency': conversion_currency, 'conversion_amount': conversion_amount
	}


def convert_to_rub(amount: float, rate: float) -> Tuple[str, float]:
	if amount < 0:
		raise ValueError('Amount below zero')
	conversion_currency = 'RUB'
	conversion_amount = amount*rate
	logger.debug(
		f'{amount = } with {rate = } {conversion_amount = :.2f} in {conversion_currency}',
		extra={'client': ''}
	)
	return conversion_currency, conversion_amount
