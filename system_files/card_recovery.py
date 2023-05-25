import hashlib
import multiprocessing as mp
import logging
import json
import csv
import matplotlib.pyplot as plt
from typing import Callable


logger = logging.getLogger()
logger.setLevel('INFO')


class RecoverySystem:
    def __init__(self, settings_path: str) -> None:
        """Initializes class settings.

        Args:
            settings_path (str): path to the json file
        """
        self.settings_path = settings_path
        self.settings = {}
        self.load_settings()

    def recover_card_number(self, hash: str, last_symbols: str, bin: str, progress_callback: Callable[[int], None] = None, cores: int = mp.cpu_count()) -> int:
        """Iterates through the BIN values for the card number

        Args:
            hash (str): Hash cards
            last_symbols (str): the last 4 digits of the card
            bin (str): BIN's card
            progress_callback (Callable[[int], None], optional): Defaults to None.
            cores (int, optional): Number of cores used for multiprocessing. Defaults to mp.cpu_count().

        Returns:
            int: Card number
        """
        parameters = [(hash, f'{bin}{str(i).zfill(6)}{last_symbols}')
                      for i in range(0, 1000000)]
        with mp.Pool(processes=cores) as pr:
            results = pr.starmap(self.check_hash, parameters)
            for index, result in enumerate(results):
                if progress_callback:
                    progress_callback(index)
                if result:
                    logging.info('Card number found successfully.')
                    return int(parameters[index][1])
        return 0

    def check_hash(self, hash: str, card_number: str) -> bool:
        """Compares this hash of the card with the selected number

        Args:
            hash (str): Hash card
            card_number (str): The interrupted number

        Returns:
            bool: Does the hash match
        """
        return hashlib.sha1(card_number.encode()).hexdigest() == hash

    def save_stat(self, time: float, number_of_processes: int) -> None:
        """Saves statistics

        Args:
            time (float): execution time
            number_of_processes (int): number of processes

        Raises:
            err:
        """
        try:
            with open(self.settings['stats'], "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([number_of_processes, time])
            logging.info('Statistics data saved successfully.')
        except Exception as err:
            logging.exception(f"Error: {err}")
            raise err

    def load_stat(self) -> dict:
        """Loads statistics

        Raises:
            err:

        Returns:
            dict: List key: number of cores and value: processing time
        """
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
        """Saves an image from matplotlib

        Args:
            fig (plt): plot from matplotlib

        Raises:
            err:
        """
        try:
            fig.savefig(self.settings['plot'])
            logging.info('Image saved successfully.')
        except Exception as err:
            logging.exception(f"Error: {err}")
            raise err

    def luhn_algorithm(self, card_number: str) -> bool:
        """Checks by the Luhn algorithm whether the card is valid

        Args:
            card_number (str): Number of card

        Raises:
            err:

        Returns:
            bool: confirmation or refutation
        """
        try:
            if not card_number.isdigit():
                return False
            total_sum = 0
            is_second_digit = False
            for digit in card_number:
                current_digit = int(digit)
                if is_second_digit:
                    current_digit *= 2
                    if current_digit > 9:
                        current_digit -= 9
                total_sum += current_digit
                is_second_digit = not is_second_digit
            logging.info('The Luhn algorithm has worked successfully.')
            return total_sum % 10 == 0
        except Exception as err:
            logging.exception(f"Error: {err}")
            raise err

    def load_text(self, file_path: str) -> str:
        """Loads the text

        Args:
            file_path (str): File path

        Raises:
            err: 

        Returns:
            str: Text
        """
        try:
            with open(file_path, 'r') as file:
                result = file.read()
                logging.info('The text has been uploaded successfully.')
            return result
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err

    def save_settings(self) -> None:
        """Saves settings

        Raises:
            err:
        """
        try:
            with open(self.settings_path, 'w', newline='') as file:
                json.dump(self.settings, file)
            logging.info('Settings saved successfully.')
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err

    def load_settings(self) -> None:
        """Load settings

        Raises:
            err: 
        """
        try:
            with open(self.settings_path, 'r') as file:
                self.settings = json.load(file)
                self.hash = self.settings['hash']
                self.bin = self.settings['bin']
                self.last_symbols = self.settings['last_symbol']
            logging.info('Settings have been successfully applied.')
        except Exception as err:
            logging.exception(f'Error: {err}')
            raise err
