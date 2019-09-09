import requests
import time
from datetime import datetime
import pytz

timezone_utc = pytz.timezone('UTC')
timezone_warszawa = pytz.timezone('Europe/Warsaw')


class ApiWebHmi:
    """ Umozliwia połaczenie sie z urzadzniem webHMI za pomocą jego API """

    def __init__(self, device_adress, api_kay):
        self.device_adress = device_adress
        self.headers = {'X-WH-APIKEY': api_kay,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-WH-CONNS': '',
                        'X-WH-START': '',
                        'X-WH-END': '',
                        'X-WH-REG-IDS': '',
                        'X-WH-SLICES': '',
                        'X-WH-REGS': '',
                        }

        self.api_adress = {'connectionList': {'adress': '/api/connections'},
                           'registerList': {'adress': '/api/registers/'},
                           'trendList': {'adress': '/api/trends/'},
                           'graphList': {'adress': '/api/graphs'},
                           'getCurValue': {'adress': '/api/register-values'},
                           'getLocTime': {'adress': '/api/timeinfo'},
                           'getRegLog': {'adress': '/api/register-log'},
                           'getGraphData': {'adress': '/api/graph-data/'},
                           }

    def doc(self):
        """Drukuje dokumnetacja dla metod"""
        with open('help.txt', 'r') as f:
            data = f.read()
        print(data, '\n')

    def make_api_adress(self, action_name, kwargs):
        '''Robi adres zapytania'''

        if 'ID' in kwargs:  # sprawdznie czy nie trzeba uzyc rozszerzonej wersji api adresu
            ID = kwargs['ID']
        else:
            ID = ''
        api_adress = self.api_adress[action_name]['adress'] + '{}'.format(ID)
        return api_adress

    def make_headers(self, kwargs):
        '''Robi nagłowkek zapytania'''
        headers = self.headers
        # sprawdznie czy nie trzeba nadpisac naglowka
        for k, v in kwargs.items():
            k = k.replace('_', '-')  # zamiana spacji na myślnik
            if k in headers.keys():
                headers[k] = v
        return headers

    def make_req(self, action_name, response=False, **kwargs):
        '''Wykonuje zapytanie (rodzaj zapytania, sczegoly zapytania, argumenty opcionalne)'''
        # ADRESS
        api_adress = self.make_api_adress(action_name, kwargs)
        url = self.device_adress + api_adress
        print('Polaczenie na adres: ', url)
        # HEAD
        head = self.make_headers(kwargs)
        # GET
        try:
            r = requests.get(url, headers=head)
            if response == True or r.status_code != 200:
                self.response_status(action_name, r)
            return r.json()
        except Exception as e:
            print(e)
            exit(1)

    def response_status(self, action, r):
        '''Drukuje status odpowiedzi'''
        # Response, status etc
        print('\n' + 140 * '-' + '\n')
        print('* {0} dla URL: {1}\n  Kodowanie znaków: {2}\n'.format(action, r.url, r.apparent_encoding))
        print('* ODPOWIEDZ SERWERA:\n{0}'.format(r.text))  # TEXT/HTML
        print('* KOD STATUSU I STATUS:\n[{0} --> {1}]\n'.format(r.status_code, r.reason))  # HTTP
        print('* NAGLOWEK ODPOWIEDZI:\n{0}\n'.format(r.headers))
        print('<!---------koniec-----------!>')

    def req_time(self, *args):
        ''' Zwraca unix time do zapytan'''
        dt = datetime(*args)
        dt = dt.astimezone(timezone_utc)
        t = dt.timestamp()
        return str(t - 7200)

    def string_time(self, unix_sec):
        '''Zwraca date w fromacie strina. '''
        format = "%Y-%m-%d %H:%M:%S %Z%z"
        date_time = datetime.fromtimestamp(unix_sec, tz=timezone_warszawa)
        d = date_time.strftime(format)
        return d


if __name__ == "__main__":
    from settings import device_adress, APIKEY

    web = ApiWebHmi(device_adress, APIKEY)

    # con0=web.make_req('connectionList')
    # for i in con0:
    #     print(i)

    # X_WH_CONNS = '10,12,14'
    # con1 = web.make_req('getCurValue', response=False, X_WH_CONNS=X_WH_CONNS)
    # print(con1)

    ID = '1'
    X_WH_START = web.req_time(2019, 9, 2, 9, 0)
    X_WH_END = web.req_time(2019, 9, 2, 10, 0)
    X_WH_SLICES = '5'

    print(X_WH_START, X_WH_END)
    # web.device_adress="83.12.5.6"
    # web.headers['X-WH-APIKEY']='22222233'

    con2 = web.make_req('getGraphData',
                        response=True,
                        ID=ID,
                        X_WH_START=X_WH_START,
                        X_WH_END=X_WH_END,
                        X_WH_SLICES=X_WH_SLICES)
    for n, i in enumerate(con2):
        t = web.string_time(i['x'] / 1000)
        print(n, t, i)
