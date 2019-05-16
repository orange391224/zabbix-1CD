#coding: utf-8
import onec_dtools #pip install onec_dtools
import sys
import json
import os
if type(sys.argv[1]) == type('str'):
    db_path = sys.argv[1]
else:
    db_path = sys.argv[1].decode(sys.getfilesystemencoding())
try:
    with open(db_path, 'rb') as f:
        db = onec_dtools.DatabaseReader(f)
        version = db.version
        tables_q = len(db.tables)
        data = []
        db_size = os.path.getsize(db_path)
        data.append({'{version}': version,
                     '{tables_q}': tables_q,
                     '{db_size}': db_size,
                     })
    outtext = (json.dumps(data, ensure_ascii=False)).encode('utf8')
    sys.stdout.buffer.write(outtext)
except Exception as e:
    print('Error')
    print(str(type(db_path)))
    print(e)
