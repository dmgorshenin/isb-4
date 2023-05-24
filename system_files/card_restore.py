import hashlib
import multiprocessing as mp
import logging
import json
from tqdm import tqdm


class RecoverySystem:
    def __init__(self, settings_path: str) -> None:
        self.settings_path = settings_path
        self.hash = ''
        self.bin = ''
        self.last_symbols = ''
        self.settings = {}
        self.load_settings()
    
    def recover_card_number(self, hash: str, last_symbols: str, bin: str, cores: int = mp.cpu_count()) -> str:
        parameters = [(hash, f'{bin}{i}{last_symbols}')
                      for i in range(100000, 1000000)]
        with mp.Pool(processes=cores) as pr:
            results = tqdm(pr.starmap(self.check_hash, parameters))
            for index, result in enumerate(results):
                if result:
                    logging.info(' ')
                    return parameters[index][1]
        return ""

    def check_hash(self, hash: str, card_number: str) -> bool:
        return hashlib.sha1(card_number.encode()).hexdigest() == hash

    def save_text(self, text: str, file_path: str) -> None:
        try:
            with open(file_path, 'w') as file:
                file.write(text)
                logging.info(' ')
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err

    def load_text(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                result = file.read()
                logging.info('')
            return result
        except Exception as err:
            logging.exception(f'Exception: {err}')
            raise err

    def load_settings(self)->None:
        try:
            with open(self.settings_path, 'r') as file:
                self.settings= json.load(file)
                self.hash = self.load_text(self.settings['hash'])
                self.bin = self.load_text(self.settings['bin'])
                self.last_symbols = self.load_text(
                    self.settings['last_symbol'])
                logging.info('')
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err
