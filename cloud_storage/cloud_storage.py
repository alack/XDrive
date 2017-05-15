from __future__ import print_function
import sys
sys.path.insert()
import box_cloud_storage
import json


STORAGE_CONFIG_FILE = './data/idpw.json'


def main():
    storage_names = ['BOX', 'GOOGLE', 'DROPBOX']
    f = open(STORAGE_CONFIG_FILE, 'r')
    json_data = json.loads(f.read())
    f.close()
    storage = [[]]
    for storage_name in storage_names:
        for i in range(0, json_data[storage_name]['CNT']):
            if storage_name == 'BOX':
                storage[storage_name][i] = box_storage_controller(json_data[storage_name]['LIST'][i])
            elif storage_name == 'GOOGLE':
                storage[storage_name][i] = google_storage_controller(json_data[storage_name]['LIST'][i])
            elif storage_name == 'DROPBOX':
                storage[storage_name][i] = dbx_storage_controller(json_data[storage_name]['LIST'][i])
            storage[storage_name][i].authenticate()
            storage[storage_name][i].test_run()
    os._exit(0)


if __name__ == '__main__':
    main()
