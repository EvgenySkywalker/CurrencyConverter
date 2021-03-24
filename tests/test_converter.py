import pytest
from mock import patch

from app.converting.converter import conversion


@pytest.mark.parametrize(
	('currency', 'amount', 'expected'), [
		('EUR', 0, 0.00),
		('USD', 1, 1.00),
	]
)
@patch('app.converting.converter.parse_rate')
def test_conversion(parse_rate, currency, amount, expected):
	parse_rate.return_value = 1
	path = f'/?currency={currency}&amount={str(amount)}'
	result = conversion(path)
	assert float(result['conversion_amount']) == expected


@pytest.mark.parametrize(
	('currency', 'amount', 'expected'), [
		('blf', 'str', ValueError),
	]
)
def test_conversion_exception(currency, amount, expected):
	path = f'/?currency={currency}&amount={str(amount)}'
	with pytest.raises(expected):
		conversion(path)
