import pathlib
import webbrowser
from UniDrive import UniDrive
from exceptions import *


def prepareUnidrive():
    prjdir = pathlib.Path('.').resolve()
    unidrive = UniDrive(prjdir)
    # google
    try:
        auth_url = unidrive.register_store('GoogleDriveStore', 'test-googledrive')
        webbrowser.open_new(auth_url)
        res = input('response url for test-googledrive :')
        if unidrive.activate_store('test-googledrive', res):
            print ('success test-googledrive')
        else:
            print ('fail test-googledrive')
    except Exception:
        print('test-googledrive is already registered')
    # dropbox

    try:
        auth_url = unidrive.register_store('DropboxStore', 'test-dropbox')
        webbrowser.open_new(auth_url)
        res = input('response url for test-dropbox :')
        if unidrive.activate_store('test-dropbox', res):
            print('success test-dropbox')
        else:
            print('fail test-dropbox')
    except Exception:
        print('test-dropbox is already registered')
    return unidrive


def run(unidrive):
    while True:
        cmd = input('>> ')
        cmd = cmd.split()
        args = cmd[1:]
        cmd = cmd[0]
        if cmd == 'q':
            print('quit!')
            break
        if cmd == 'ls':
            if len(args) != 1:
                print('please check arguments. ls [path]')
                continue
            arg = args[0]
            try:
                res = unidrive.get_list(arg)
            except BaseStoreException as e:
                print('error :', e.message)
            else:
                for entry in res:
                    if entry.is_dir:
                        print('[{0}]'.format(entry.name))
                    else:
                        print(entry.name)
                continue

        if cmd == 'up':
            if len(args) != 2:
                print('please check arguments. up [from] [to]')
                continue
            src_path = pathlib.Path(args[0])
            if src_path.is_file() is False:
                print('file does not exists')
                continue
            with open(src_path, 'rb') as src_file:
                src_data = src_file.read()
            dest_path = args[1]
            try:
                unidrive.upload_file(dest_path, src_data)
            except BaseStoreException as e:
                print('error :', e.message)
            else:
                print('Done.')
                continue

        if cmd == 'down':
            if len(args) != 2:
                print('please check arguments. down [from] [to]')
                continue
            src_path = args[0]
            dest_path = pathlib.Path(args[1])
            if dest_path.exists() is True or (dest_path.parent).is_dir() is False:
                print('please check destination path :', dest_path)
                continue
            try:
                tmp_data = unidrive.download_file(src_path)
            except BaseStoreException as e:
                print('error :', e.message)
            else:
                with open(dest_path, 'wb') as outfile:
                    outfile.write(tmp_data)
                print('Done.')
                continue

        if cmd == 'mkdir':
            if len(args) != 2:
                print('please check arguments. mkdir [path] [dir name]')
                continue
            dest_path = args[0]
            dir_name = args[1]
            try:
                unidrive.make_directory(dest_path, dir_name)
            except BaseStoreException as e:
                print('error :', e.message)
            else:
                print('Done.')
                continue

        if cmd == 'rm':
            if len(args) != 1:
                print('please check arguments. rm [path]')
                continue
            dest_path = args[0]
            try:
                unidrive.remove_file(dest_path)
            except BaseStoreException as e:
                print('error :', e.message)
            else:
                print('Done.')
                continue

        print('Command does not exist')

if __name__ == '__main__':
    unidrive = prepareUnidrive()
    run(unidrive)