import json
import logging


from typing import Any
from utilities import JSONDictionary, PossibleKeys, PathLikeString


class DataManager:
	def __init__(self, data_file: PathLikeString = '../assets/data.json'):
		self.__data_file = data_file

	# Data File
	@property
	def data_file(self) -> PathLikeString:
		return str(self.__data_file)

	@data_file.setter
	def data_file(self, value: Any) -> None:
		self.__data_file = str(value)

	@data_file.deleter
	def data_file(self) -> None:
		del self.__data_file

	def __load(self) -> JSONDictionary:
		try:
			with open(self.data_file, 'r', encoding='utf-8') as file:
				return json.load(file)
		except FileNotFoundError:
			logging.critical(f'{self.data_file} doesn\'t exist!')
			return {}
		except IsADirectoryError:
			logging.critical(f'{self.data_file} is a directory!')
			return {}
		except PermissionError:
			logging.critical(f'Cannot access {self.data_file}!')
			return {}
		except json.JSONDecodeError:
			logging.error(f'Cannot decode from {self.data_file}!')
			return {}

	def get_key(self, key: str) -> str:
		return self.__load().get(key)

	def set_key(self, key: PossibleKeys, value: str) -> None:
		data = self.__load()

		data[key] = value

		with open(self.data_file, 'w', encoding='utf-8') as file:
			json.dump(data, file, indent='\t')
