import hashlib
from typing import Callable
import multiprocessing as mp
import logging


logger = logging.getLogger()
logger.setLevel('INFO')


def recover_card_number(hash: str, last_symbols: str, bin: str, progress_callback: Callable[[int], None] = None, cores: int = mp.cpu_count()) -> int:
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
        results = pr.starmap(check_hash, parameters)
        for index, result in enumerate(results):
            if progress_callback:
                progress_callback(index)
            if result:
                logging.info('Card number found successfully.')
                return int(parameters[index][1])
    return 0


def check_hash(hash: str, card_number: str) -> bool:
    """Compares this hash of the card with the selected number

    Args:
        hash (str): Hash card
        card_number (str): The interrupted number

    Returns:
        bool: Does the hash match
    """
    return hashlib.sha1(card_number.encode()).hexdigest() == hash
