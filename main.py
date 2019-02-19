#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import globs
import common


params = {}
config = {}
next_update = None

def main_prg():
    # Тут мы поливалькаем...
    for item in params['whater_time']:
        now = datetime.datetime.now().time()
        if item[0] <= now and now <= item[1]:
            # Включим полив
            print('[INFO] Whater ON !!!')
        else:
            # Рубим полив
            pass

    # Тут мы освещаем
    for item in params['light_time']:
        now = datetime.datetime.now().time()
        if item['light_time_start'] <= now and now <= item['light_time_end']:
            # Включим свет
            pass
        else:
            # Рубим свет
            pass

    # Тут мы контролируем температуру


# Обновление параметров и конфигов при первом пуске
config = common.read_config(config)
params = common.read_params(config, params)

while config['end_program'] == '0':
    # Текущая дата и время
    now = datetime.datetime.now()
    if not next_update or next_update <= now:
        # Обновляем дату следующей проверки
        next_update = now
        next_update = next_update + datetime.timedelta(seconds=globs.TIMER)

        # Если новый день, то обновляем конфиги и прочую чушь
        if now.strftime('%Y-%m-%d') != config['today_date']:
            config['today_date'] = now.strftime('%Y-%m-%d')

            # Если программа окончена, то..
            if config['today_day'] == config['end_day']:
                print('[INFO] End program')
                config['end_program'] = '1'
                common.write_config(config)
                break

            config['today_day'] = str(int(config['today_day']) + 1)
            params = common.read_params(config, params)
            common.write_config(config)

        # Считываем показания с сенсоров
        common.read_sensors()

        # Запускаем основную программу регулирования
        main_prg()