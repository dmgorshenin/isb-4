import hashlib
import multiprocessing as mp
import logging
import json
from tqdm import tqdm


class RecoverySystem():
    def __init__(self, settings_path: str) -> None:
        self.are_settings_loaded = False
        self.settings_path = settings_path
        self.settings = {}
        self.hash = ''
        self.bin = ''
        self.last_symbols = ''

    def recover_card_number(self, hash: str, last_symbols: str, bin: str, cores: int = mp.cpu_count()) -> str:
        parameters = [(hash, f'{bin}{i}{last_symbols}')
                      for i in range(100000, 1000000)]
        with mp.Pool(processes=cores) as pr:
            results = tqdm(pr.starmap(self.check_hash, parameters))
            for index, result in enumerate(results):
                if result:
                    return parameters[index][1]
        return ""

    def check_hash(self, hash: str, card_number: str) -> bool:
        return hashlib.sha1(card_number.encode()).hexdigest() == hash

    def save_card_number(self, text: str) -> None:
        try:
            with open(self.settings['card_number'], 'w') as file:
                file.write(text)
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err

    def load_text(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                result = file.read()
            return result
        except Exception as err:
            logging.exception(f'Exception: {err}')
            raise err

    def load_settings(self):
        try:
            with open(self.settings_path, 'r') as file:
                self.settings = json.load(file)
                self.hash = self.load_text(self.settings['hash'])
                self.bin = self.load_text(self.settings['bin'])
                self.last_symbols = self.load_text(
                    self.settings['last_symbol'])
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err


if __name__ == '__main__':
    a = RecoverySystem('files/settings.json')
    a.load_settings()
    a.save_card_number(a.recover_card_number(a.hash, a.last_symbols, a.bin))
