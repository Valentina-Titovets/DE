import json
from abc import abstractmethod, ABC


class Saver(ABC):
    @staticmethod
    @abstractmethod
    def save(values_list: list, result_name: str):
        pass


class JsonSaver(Saver):
    @staticmethod
    def save(values_list: list, result_name: str):
        with open('{}.json'.format(result_name), 'w') as write_file:
            json.dump(values_list, write_file, indent=4)