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
device_adress = data["properties"]['device_adress']

if __name__ == "__main__":
    print(data)
    print(APIKEY)
    print(device_adress)
    print(data['comment'])
