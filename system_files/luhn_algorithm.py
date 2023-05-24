import logging


logger = logging.getLogger()
logger.setLevel('INFO')


def luhn_algorithm(card_number: str) -> bool:
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
