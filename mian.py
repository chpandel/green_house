#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

# Интервал таймера в секундах
timer = 1

params = {}
config = {}
next_update = None

def csv_read(filepath, keys):
    """
    Читалка CSV итерабельная с выбором ключей
    """

    with open(filepath, 'rt') as csv_file:
        for i, line in enumerate(csv_file):
            if not i:
                headers = {key.strip():i for i, key in enumerate(line.split(','))}
                keys = keys or headers.keys()
                pointers = [headers[key] for key in keys]
                continue
            data = line.split(',')
            yield [data[i].strip() for i in pointers]

def write_config():
    print('[INFO] Write config')

    save_config = 'key,data\n'
    for i, item in config.items():
        save_config += i + ',' + item + '\n'

    file_config = open('config.csv', 'w')
    file_config.write(save_config)
    file_config.close()

def read_config():
    print('[INFO] Read config')

    for key, data in csv_read('config.csv', ('key', 'data')):
        config[key] = data
    return config

def read_params():
    print('[INFO] Read params')

    for day, humidity, temp_day, temp_night in csv_read('prg.csv', ('day', 'humidity', 'temp_day', 'temp_night')):
        if int(day) == int(config['today_day']):
            params['humidity'] = humidity
            params['temp_day'] = temp_day
            params['temp_night'] = temp_night
            break

    return params

def read_sensors():
    print('read_sensors')
    pass

def main_prg():
    read_sensors()
    pass

config = read_config()

while config['end_program'] == '0':
    # Текущая дата и время
    now = datetime.datetime.now()
    if not next_update or next_update <= now:
        # Обновляем дату следующей проверки
        next_update = now
        next_update = next_update + datetime.timedelta(seconds=timer)

        # Если новый день, то обновляем конфиги и прочую чушь
        if now.strftime('%Y-%m-%d') != config['today_date']:
            config['today_date'] = now.strftime('%Y-%m-%d')

            # Если программа окончена, то..
            if config['today_day'] == config['end_day']:
                print('[INFO] End program')
                config['end_program'] = '1'
                write_config()
                break

            config['today_day'] = str(int(config['today_day']) + 1)
            params = read_params()
            write_config()

        # Запускаем основную программу регулирования
        main_prg()