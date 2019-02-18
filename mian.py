import datetime
import re

params = {}
config = {
    'write_logs' : 1,
    'end_day' : 1,
    'start_day' : 1,
    'today_date' : None
}

def read_params():
    params = {}
    print('[INFO] Read params and config')

    file_handler = open('prg.csv', 'r')
    file_write = file_handler.read()
    for i, row in enumerate(file_handler):
        print(str(i))
        row_split = row.rstrip().split(';')
        if i < 11:
            try:
                config[row_split[0]] = row_split[1]
            except:
                pass
        elif i - 10 == config['start_day']:
            params['humidity'] = int(row_split[1])
            params['temp_night'] = int(row_split[2])
            params['temp_day'] = int(row_split[3])
    file_handler.close()

    # Если мы сегодня ещё не записывали данные, то пишем в файл
    print(config['today_date'])
    if datetime.datetime.now().strftime('%Y-%m-%d') != config['today_date']:
        print('[INFO] Write params and config')
        config['today_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        config['start_day'] = str(int(config['start_day']) + 1)
        file_write = re.sub(r'start_day;(.*?);', 'start_day;' + config['start_day'] + ';', file_write)
        file_write = re.sub(r'today_date;(.*?);', 'today_date;' + config['today_date'] + ';', file_write)
        
        with open('prg.csv', 'w') as file_handler:
            file_handler.write(file_write)
            file_handler.close()

    return config, params

# Раз в день обновляемся или при запуске программы
if datetime.datetime.now().strftime('%Y-%m-%d') != config['today_date']:
    config, params = read_params()
    print(config)
    print(params)