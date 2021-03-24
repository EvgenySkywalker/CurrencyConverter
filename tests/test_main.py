import json

import pytest
from mock import patch

from app.main import conversion


@pytest.mark.parametrize(
	('currency', 'amount', 'expected'), [
		('EUR', 0, 0),
		('USD', 1, 1),
	]
)
@patch('main.parse_rate')
def test_conversion(parse_rate, currency, amount, expected):
	parse_rate.return_value = 1
	path = f'/?currency={currency}&amount={str(amount)}'
	result = json.loads(conversion(path))
	assert result['conversion_amount'] == expected
