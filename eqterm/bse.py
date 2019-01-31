import requests
import click


@click.group()
def bse():
    pass


@bse.command()
@click.option('--scrip', default='index', help='stock/bond/index')
@click.argument('name', default='SENSEX')
def quote(scrip, name):
    if scrip == 'index' and name == 'SENSEX':
        url = 'https://api.bseindia.com/bseindia/api/Sensex/getSensexData?json={"fields": "1,2,3,4,5,6,7"}'
        res = requests.get(url).json()
        out = {
            'market': 'BSE India',
            'name': res[0]['indxnm'],
            'price': res[0]['ltp'],
            'change': res[0]['chg'],
            'change_pct': res[0]['perchg']
        }
        return {'obj': 'quote', 'value': out}
