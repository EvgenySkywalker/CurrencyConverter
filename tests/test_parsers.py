import pytest

from mock import patch

from app.rate_parsing.parsers import parse_rate


@pytest.mark.parametrize(
	('currency', 'expected'), [
		(None, AttributeError),
		('-1', ValueError),
	]
)
def test_parse_rate_exception(currency, expected):
	with pytest.raises(expected):
		parse_rate(currency)


@pytest.mark.parametrize(
	('currency', 'expected'), [
		('USD', float),
	]
)
def test_parse_rate_type(currency, expected):
	assert type(parse_rate(currency)) is expected
