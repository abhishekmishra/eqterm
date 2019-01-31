import io
import requests
import click
from zipfile import ZipFile
import csv
import pandas as pd
from pandas.tseries.offsets import BDay
from eqterm import data_utils


def get_eq_list(dt):
    pass


def _load_bse_provider():
    # https://stackoverflow.com/questions/10908877/extracting-a-zipfile-to-memory
    def extract_zip(input_zip):
        input_zip = ZipFile(input_zip)
        return {name: input_zip.read(name) for name in input_zip.namelist()}

    for i in range(5):
        try:
            dt = pd.datetime.now()
            if i > 0:
                dt = dt - BDay(i)
            print('Downloading BSE securities for date {}'.format(dt))
            eq_file_name = 'EQ_ISINCODE_{}'.format(dt.strftime('%d%m%y'))
            eq_csv_file = eq_file_name + '.CSV'
            if data_utils.data_file_exists(eq_csv_file):
                print('Loading from file as it is already downloaded {}'.format(data_utils.data_file_path(eq_csv_file)))
                with open(data_utils.data_file_path(eq_csv_file)) as fp:
                    eq_list = [row for row in csv.DictReader(fp)]
                    return eq_list
            else:
                eq_request = requests.get(
                    'https://www.bseindia.com/download/BhavCopy/Equity/{}.zip'.format(eq_file_name),
                    stream=True)
                eq_file = extract_zip(io.BytesIO(eq_request.content))[eq_csv_file].decode("utf-8")
                eq_list = [row for row in csv.DictReader(io.StringIO(eq_file))]
                with open(data_utils.data_file_path(eq_csv_file), 'w') as fp:
                    fp.write(eq_file)
                return eq_list
        except ValueError as ve:
            return None
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            continue
    return None


_BSE_EQUITIES = pd.DataFrame.from_dict(_load_bse_provider())


def eq_for_name(name):
    return _BSE_EQUITIES[_BSE_EQUITIES['SC_NAME'].str.contains(name.upper())]


@click.group()
def bse():
    pass


@bse.command()
@click.option('--scrip', default='stock', help='stock/bond/index')
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
        return {'obj': 'quote', 'value': [out]}
    if scrip == 'stock':
        values = []
        eqs = eq_for_name(name)
        for index, eq in eqs.iterrows():
            sc_code = eq['SC_CODE'].strip()
            url = 'https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?Debtflag=&scripcode={}&seriesid=' \
                .format(sc_code)
            res = requests.get(url).json()
            status = res['CurrRate']
            out = {
                'market': 'BSE India',
                'prev': eq.to_dict(),
                'name': res['Cmpname']['FullN'],
                'price': status['LTP'],
                'change': status['Chg'],
                'change_pct': float(status['PcChg'])
            }
            values.append(out)
        return {'obj': 'quote', 'value': values}

if __name__ == "__main__":
    res = quote(['--scrip', 'stock', 'abb'], standalone_mode=False)
    print(res)
