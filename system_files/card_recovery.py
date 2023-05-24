import hashlib
import multiprocessing as mp
import logging
import json
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt


logger = logging.getLogger()
logger.setLevel('INFO')


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
                    logging.info('Card number found successfully.')
                    return parameters[index][1]
        return ""

    def check_hash(self, hash: str, card_number: str) -> bool:
        return hashlib.sha1(card_number.encode()).hexdigest() == hash

    def save_stat(self, time: float, number_of_processes: int) -> None:
        try:
            with open(self.settings['stats'], "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([number_of_processes, time])
            logging.info('Statistics data saved successfully.')
        except Exception as err:
            logging.exception(f"Error: {err}")
            raise err

    def load_stat(self) -> dict:
        try:
            with open(self.settings['stats'], "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                lines = list(reader)
        except Exception as err:
            logging.exception(f"Error: {err}")
            raise err
        stat = dict()
        for line in lines:
            cores, time = line
            stat[int(cores)] = float(time)
        logging.info('Statistics data uploaded successfully.')
        return stat

    def save_plot_image(self, fig: plt) -> None:
        try:
            fig.savefig(self.settings['plot'])
            logging.info('Image saved successfully.')
        except Exception as err:
            logging.exception(f"Error: {err}")
            raise err

    def save_text(self, text: str, file_path: str) -> None:
        try:
            with open(file_path, 'w') as file:
                file.write(text)
            logging.info('Text saved successfully.')
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err

    def load_text(self, file_path: str) -> str:
        try:
            with open(file_path, 'r') as file:
                result = file.read()
                logging.info('The text has been uploaded successfully.')
            return result
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err

    def load_settings(self) -> None:
        try:
            with open(self.settings_path, 'r') as file:
                self.settings = json.load(file)
                self.hash = self.load_text(self.settings['hash'])
                self.bin = self.load_text(self.settings['bin'])
                self.last_symbols = self.load_text(
                    self.settings['last_symbol'])
            logging.info('Settings have been successfully applied.')
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err
