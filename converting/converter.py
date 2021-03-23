from typing import Tuple

from log.core import logger


def convert_to_rub(amount: float, rate: float) -> Tuple[str, float]:
	if amount < 0:
		raise ValueError('Amount below zero')
	res_currency = 'RUB'
	result = amount*rate
	logger.debug(
		f'{amount = } with {rate = } {result = :.2f} in {res_currency}',
		extra={'client': ''}
	)
	return res_currency, result
