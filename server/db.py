from pymongo import MongoClient

class Db:
    """Mongo Db connection"""

    def __init__(self):
        # for local (dubug) use this file
        self.mongo_server = "127.0.0.10:27017"
        # for fastapi, docker ftnet
        # self.mongo_server = "mongodb:27017"
        self.mongo_connect = f'mongodb://root:9999@{self.mongo_server}/?authSource=admin'
        self.db_name = "forms"
        self.db = self.get()

    def get(self, db_name=None):
        client = MongoClient(self.mongo_connect)
        if not db_name:
            db_name = self.db_name
        return client[db_name]

    def status(self):
        serverStatusResult = self.db.command("serverStatus")
        return serverStatusResult

######################################################################

def main():
    db = Db()
    print(db.get("admin"))
    # print(db.status())

if __name__ == '__main__':
    main()
