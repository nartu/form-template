from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
from random import randint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://root:9999@127.0.0.10:27017/?authSource=admin')
filter={}
db=client.admin
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)
pprint(type(serverStatusResult))

db=client.forms

def first():
    templates = []
    templates += [{
        "name": "Customer contact",
        "customer_name": "text",
        "customer_email": "email",
        "customer_phone": "phone"
    }]
    templates += [{
        "name": "Whatsapp contact",
        "contact_name": "text",
        "whatsapp_id": "phone"
    }]
    templates += [{
        "name": "Customer birthday",
        "customer_name": "text",
        "customer_birthday_date": "date",
    }]
    # pprint(templates)
    db.templates.insert_many(templates)
    # delete = db.temlates.delete_one(templates[2])
    # print(delete.raw_result)

def main():
    # first()
    pass


if __name__ == '__main__':
    main()
