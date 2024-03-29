import logging
from typing import Dict

logging_format: str = '%(levelname)s - %(message)s'
logging_colors: Dict[int, str] = {
	logging.DEBUG: '\033[37m',  # White
	logging.INFO: '\033[34m',  # Blue
	logging.WARNING: '\033[33m',  # Yellow
	logging.ERROR: '\033[31m',  # Red
	logging.CRITICAL: '\033[1;31m'  # Bold Red
}


class ColoredFormatter(logging.Formatter):
	def format(self, record: logging.LogRecord) -> str:
		record.log_color = logging_colors.get(record.levelno, '\033[0m')

		return super().format(record)


def setup_logging(level: int) -> None:
	# Setup StreamHandler
	handler = logging.StreamHandler()
	handler.setFormatter(ColoredFormatter('%(log_color)s' + logging_format + '\033[0m'))

	# Basic configuration of logging, setting the level and handler
	logging.basicConfig(level=level, handlers=[handler])
