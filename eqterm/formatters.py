def color_change(value):
    if float(value) >= 0:
        return '<ansigreen>{}</ansigreen>'.format(value)
    else:
        return '<ansired>{}</ansired>'.format(value)


def quote_formatter(value):
    return '<b>{index}</b>: {quote} [{chg}/{pct_chg}%]'.format(
        index=value['name'],
        quote=value['price'],
        chg=color_change(value['change']),
        pct_chg=color_change(value['change_pct']))


def format_output(obj, value):
    if obj == 'quote':
        return quote_formatter(value)
    return value
