import csv, os

import pandas as pd

def displayHeader(dic):
    print('\nHeader')
    for k, v in dic.items():
        print(k, ':', v)
    print('\n')


def displayList(list):
    print('\nLista')
    for i in list:
        print(i)
    print('\n')


def makeRegIDs(ids):
    regs = ''
    for i in ids:
        regs = regs + i + ','
    regs = regs[:-1]
    return regs


def csv_writer(file_path, df):
    # key_set = set()
    dict_list = list()


    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

    print("Zapis do: ", file_path)
    try:
        df.to_csv(file_path)
    except Exception as e:
        print('Nie mozna zapisac pliku csv', e)


