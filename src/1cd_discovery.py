#coding: utf-8
import os, re, json, sys
import configparser
from pyzabbix import ZabbixMetric, ZabbixSender
if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(sys.executable)
elif __file__:
    current_path = os.path.dirname(__file__)

disks = re.findall(r"[A-Z]+:.*$", os.popen("mountvol /").read(), re.MULTILINE)
extf = set(('$RECYCLE.BIN', 'System Volume Information'))
config = configparser.ConfigParser()
config.read(os.path.join(current_path, '1cd_config.cfg'))
data = []

for disk in disks:
    try:
        for root, dirs, files in os.walk(disk):
            dirs[:] = [d for d in dirs if d not in extf]
            for file in files:
                if file.endswith(".1CD") \
                        and file != 'cache.1CD' \
                        and '$Recycle.Bin' not in root \
                        and not file.endswith('v8tmp.1CD'):  # 1Cv8tmp.1CD]
                    # print(os.path.join(root, file))
                    db_path = os.path.join(root, file).replace('\\', '//')
                    data.append({'{#DBNAME}': os.path.basename(root).replace(' ', '-'),
                                 '{#DBPATH}': db_path})
    except Exception as e:
        print(e)



# Send to zbx (trapper discovery)
if len(sys.argv) > 1 and sys.argv[1] == 'trap':
    try:
        metrics = []
        zdata = json.dumps({"data": data}, ensure_ascii=False)
        hostname = config['GENERAL']['hostname']
        zkey = config['GENERAL']['zbx_key']
        zserver = (config['GENERAL']['zbx_server'])
        print('Адрес Zabbix: {0}'.format(zserver))
        print('Отправка на hostname {0} в key {1}'.format(hostname, zkey))
        m = ZabbixMetric(hostname, zkey, zdata)
        metrics.append(m)
        zbx = ZabbixSender(zserver)
        zbx.send(metrics)
        print('Sended to zbx: {0}'.format(zdata))
    except Exception as e:
        print('Ошибка при отправке данных')
        print(e)
else:
    # print to output (userparameter discovery)
    outtext = (json.dumps({"data": data}, ensure_ascii=False)).encode('utf8')
    sys.stdout.buffer.write(outtext)

