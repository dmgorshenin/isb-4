import logging
import json
import csv
import matplotlib.pyplot as plt


logger = logging.getLogger()
logger.setLevel('INFO')


class FilesSystem:
    def __init__(self, settings_path: str) -> None:
        """Initializes class settings.

        Args:
            settings_path (str): path to the json file
        """
        self.settings_path = settings_path
        self.settings = {}
        self.load_settings()

    def save_stat(self, time: float, number_of_processes: int) -> None:
        """Saves statistics

        Args:
            time (float): execution time
            number_of_processes (int): number of processes
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
        """
        try:
            fig.savefig(self.settings['plot'])
            logging.info('Image saved successfully.')
        except Exception as err:
            logging.exception(f"Error: {err}")
            raise err

    def load_text(self, file_path: str) -> str:
        """Loads the text

        Args:
            file_path (str): File path

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
