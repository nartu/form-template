from db import Db
import json
import os
from datetime import datetime
from pprint import pprint

class Migrate(object):
    """Migration of temlates with mongoDB"""

    def __init__(self):
        self.db = Db().get()

    def from_file(self, file='dump_last.json'):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(current_dir, file)
        with open(file,'r') as f:
            dump = json.load(f)
        r = self.db.templates.insert_many(dump)
        return {
            'count_all': self.db.templates.count_documents({}),
            'inserted_ids': r.inserted_ids
        }

    def to_file(self, file=None, dir='dumps', db_table='templates', ids=False):
        # Take data
        if ids:
            db_table_dump = self.db[db_table].find({})
            def id_to_str(d: dict) -> dict:
                d['_id'] = str(d['_id'])
                return d
            db_table_dump = list(map(id_to_str, db_table_dump))
        else:
            db_table_dump = list(self.db[db_table].find({},{ '_id': 0}))
        # return db_table_dump[0:2]

        # Write
        current_dir = os.path.dirname(os.path.realpath(__file__))
        dir = os.path.join(current_dir, dir)
        if not os.path.exists(dir):
            os.mkdir(dir)
        if not file:
            file = f'dump_{datetime.now().strftime("%s")}.json'
        file = os.path.join(dir, file)
        with open(file,'w') as f:
            json.dump(db_table_dump, f, indent=4, ensure_ascii=False)
        return file




######################################################################

def main():
    m = Migrate()
    # print(m.from_file())
    pprint(m.to_file(ids=False))
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)
    # print(os.getcwd())
    # print(os.path.exists('server'))
    # print(f'dump_{datetime.now().strftime("%s")}.json')
    # print(round(datetime.now().timestamp()))


if __name__ == '__main__':
    main()
