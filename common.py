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

    def convert_time(time):
        time = time.split(':')
        return datetime.time(int(time[0]), int(time[1]), int(time[2]))

    for day, humidity, temp_day, temp_night, whater_time, light_time, light_day in csv_read(globs.DIR_CSV_PRG, ('day',
    'humidity', 'temp_day', 'temp_night', 'whater_time', 'light_time', 'light_day')):
        if int(day) == int(config['today_day']):
            params['humidity'] = humidity
            params['temp_day'] = temp_day
            params['temp_night'] = temp_night

            # Планировщик поливов
            whater_time_array = []
            for item in whater_time.split(';'):
                whater_time_start = convert_time(item)
                whater_time_end = (datetime.datetime.combine(datetime.date(1,1,1),
                    whater_time_start) + datetime.timedelta(seconds=int(config['whater_time']))
                ).time()
                whater_time_array.append([whater_time_start, whater_time_end])
            params['whater_time'] = whater_time_array

            # Парсим световое время
            light_time_array = []
            for item in light_time.split(';'):
                item = item.split('/')
                light_time_array.append({
                    'light_time_start' : convert_time(item[0]),
                    'light_time_end' : convert_time(item[1])
                })
            params['light_time'] = light_time_array

            # Парсим световой день
            light_day_array = light_day.split('/')
            params['light_day'] = {
                'light_day_start' : convert_time(light_day_array[0]),
                'light_day_end' : convert_time(light_day_array[1])
            }
            break

    return params

def read_sensors():
    print('read_sensors')