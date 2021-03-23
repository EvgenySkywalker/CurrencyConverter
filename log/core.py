import logging
import sys

CLR = '\033[1;34m\033[7m'
RESET = '\033[0m'
FORMAT = (
	f'{CLR}%(levelname)-5s{RESET} '
	'%(pathname)s:%(lineno)d '
	'%(asctime)s '
	'%(client)s '
	'%(message)s'
)
logging.basicConfig(
	format=FORMAT,
	datefmt='%H:%M:%S',
	stream=sys.stdout,
	level=logging.DEBUG
)
logger = logging.getLogger('currency_converter')
