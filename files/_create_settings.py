import json


SETTINGS = {
    'bin': 220220,
    'hash': 'bf67709b1216cb66038f3ae5ad2b4c066be03cbb',
    'last_symbol': 5688,
    'card_number': 0,
    'result': '',
    'stats': 'files/stats.csv',
    'plot': 'files/plot.jpg'
}

if __name__ == '__main__':
    with open('files/settings.json', 'w') as fp:
        json.dump(SETTINGS, fp)
