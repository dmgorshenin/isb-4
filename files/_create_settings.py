import json

SETTINGS = {
    'bin': 'files/bin.txt',
    'hash': 'files/hash.txt',
    'last_symbol': 'files/last_symbol.txt',
    'card_number': 'files/card_number.txt',
    'result':'files/results/result.txt'
}

if __name__ == '__main__':
    with open('files/settings.json', 'w') as fp:
        json.dump(SETTINGS, fp)
