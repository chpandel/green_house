#!/usr/bin/env python
# -*- coding: utf-8 -*-

import globs
import datetime

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


def write_config(config):
    print('[INFO] Write config')

    save_config = 'key,data\n'
    for i, item in config.items():
        save_config += i + ',' + item + '\n'

    file_config = open(globs.DIR_CSV_CONFIG, 'w')
    file_config.write(save_config)
    file_config.close()


def read_config(config):
    print('[INFO] Read config')
    for key, data in csv_read(globs.DIR_CSV_CONFIG, ('key', 'data')):
        config[key] = data
    return config


def read_params(config, params):
    print('[INFO] Read params')

    for day, humidity, temp_day, temp_night, whater_time, light_time in csv_read(globs.DIR_CSV_PRG, ('day',
    'humidity', 'temp_day', 'temp_night', 'whater_time', 'light_time')):
        if int(day) == int(config['today_day']):
            params['humidity'] = humidity
            params['temp_day'] = temp_day
            params['temp_night'] = temp_night

            #TODO::Переписать планировщик поливов
            whater_time_array = []
            for item in whater_time.split(';'):
                item = item.split(':')
                whater_time_start = datetime.time(int(item[0]), int(item[1]), int(item[2]))
                whater_time_end = (datetime.datetime.combine(datetime.date(1,1,1),
                    whater_time_start) + datetime.timedelta(seconds=int(config['whater_time']))
                ).time()
                whater_time_array.append([whater_time_start, whater_time_end])
            params['whater_time'] = whater_time_array
            
            #Парсим световое время
            light_time_array = []
            for item in light_time.split(';'):
                item = item.split('/')
                item_0 = item[0].split(':')
                item_1 = item[1].split(':')
                light_time_array.append({
                    'light_time_start' : datetime.time(int(item_0[0]), int(item_0[1]), int(item_0[2])),
                    'light_time_end' : datetime.time(int(item_1[0]), int(item_1[1]), int(item_1[2]))
                })
            params['light_time'] = light_time_array

            break

    return params


def read_sensors():
    print('read_sensors')