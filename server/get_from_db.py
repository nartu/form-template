from pymongo import MongoClient
from pprint import pprint

class FindTemplate(object):
    """
    Searching a match template in db.
    `input_template` is dict {'field': 'type'}
    It is considered a matched if temlate in db contains all fields and field_types of `input_template`.
    Output is matched templates names in the db.
    """

    def __init__(self, input_template):
        self.input_template = input_template
        # for local use this file
        # self.mongo_server = "127.0.0.10:27017"
        # for fastapi, docker ftnet
        self.mongo_server = "mongodb:27017"
        self.mongo_connect = f'mongodb://root:9999@{self.mongo_server}/?authSource=admin'
        self.db_name = "forms"
        self.db = self.get_db()

    def get_db(self):
        client = MongoClient(self.mongo_connect)
        return client[self.db_name]

    def db_status(self):
        serverStatusResult = self.db.command("serverStatus")
        return serverStatusResult

    def matched_ids(self):
        # Input template must contain 100% of template in db
        # candidate's set
        matches = set()
        for k,v in self.input_template.items():
            filter = {k: v}
            match = self.db.templates.find(
                filter=filter,
                projection={"_id": 1}
            )
            # matches_ar += [set([i.get("_id") for i in match])]
            field_match = {i.get("_id") for i in match}
            matches.update(field_match)
        # print(f'Candidates matches: {list(matches)[1]}')
        # Checked templates list
        valid_templates_ids = []
        for match in matches:
            # print(f'Match: {match}')
            # Temlate's fields
            fields = self.db.templates.find_one(
                filter={"_id": match},
                projection={"_id": 0, "name": 0}
            )

            template_match_valid = True
            # Check every matched template in db
            # All fields with types (values) must be in `self.input_template`
            for field_name, field_value in fields.items():
                if (field_name not in self.input_template or self.input_template.get(field_name)!=field_value):
                    template_match_valid = False
                    # break
            if template_match_valid:
                valid_templates_ids += [match]

        return valid_templates_ids

    def response(self):
        out = {}
        valid_templates_ids = self.matched_ids()
        if len(valid_templates_ids) > 0:
            out["matches"] = True
            out["templates"] = []
            for id in valid_templates_ids:
                match = self.db.templates.find_one(
                    filter={"_id": id},
                    projection={"_id": 1, "name": 1}
                )
                out["templates"] += [match]
        else:
            out["matches"] = False
            out["custom_template"] = self.input_template

        return out

    def response_names(self):
        out = {}
        valid_templates_ids = self.matched_ids()
        if len(valid_templates_ids) > 0:
            out["matches"] = True
            out["templates_names"] = []
            for id in valid_templates_ids:
                match = self.db.templates.find_one(
                    filter={"_id": id},
                    projection={"_id": 0, "name": 1}
                )
                out["templates_names"] += [match.get("name")]
        else:
            out["matches"] = False
            out["custom_template"] = self.input_template

        return out

######################################################################

def main():
    input_template2 = {
        "customer_name": "text",
        "customer_birthday_date": "date",
        'customer_phone': 'phone',
        'customer_email': "email"
    }

    ft = FindTemplate(input_template2)

    # print(ft.matched_ids(), sep="\n")
    # pprint(ft.response())
    # pprint(ft.response_names())
    pprint(ft.db_status())

if __name__ == '__main__':
    main()
