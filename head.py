import json, os

cur_path = os.path.dirname(__file__)

filepath = cur_path+'/setup.json'



def json_save(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)


def json_read(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


data = json_read(filepath)

APIKEY = data["properties"]['APIKEY']
# USER = 'admin'
# PASS = 'elam4321'
# device_adress = 'http://80.50.4.62:60043'
device_adress = data["properties"]['device_adress']

headers = {'X-WH-APIKEY': APIKEY,
           'Accept': 'application/json',
           'Content-Type': 'application/json',
           'X-WH-CONNS': '',
           'X-WH-START': '',
           'X-WH-END': '',
           'X-WH-REG-IDS': '',
           'X-WH-SLICES': '',
           'X-WH-REGS': '',

           }

if __name__ == "__main__":
    print(data)
    print(APIKEY)
    print(device_adress)
    print(data['comment'])
