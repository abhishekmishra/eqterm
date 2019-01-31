import os, os.path

hd = os.path.expanduser('~')
eqterm_dir = os.path.join(hd, '.eqterm')
eqterm_data_dir = os.path.join(eqterm_dir, 'data')
os.makedirs(eqterm_data_dir, exist_ok=True)

def data_file_exists(fname):
    return os.path.exists(data_file_path(fname))

def data_file_path(fname):
    return os.path.join(eqterm_data_dir, fname)