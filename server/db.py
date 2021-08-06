from pymongo import MongoClient

class Db:
    """Mongo Db connection"""

    def __init__(self, mongo_server=None):
        # for local (dubug) use this file
        # self.mongo_server = "127.0.0.10:27017"
        # for fastapi, docker ftnet
        self.mongo_server = self._mongo_server(mongo_server)
        self.mongo_connect = f'mongodb://root:9999@{self.mongo_server}/?authSource=admin'
        self.db_name = "forms"
        self.db = self.get()

    def _mongo_server(self, mongo_server):
        if mongo_server:
            return mongo_server
        else:
            return "mongodb:27017"

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
    db = Db("127.0.0.10:27017")
    print(db.mongo_server)
    print(db.get("admin"))
    print(db.status())

if __name__ == '__main__':
    main()
