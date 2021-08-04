from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://root:9999@127.0.0.10:27017/?authSource=admin')
filter={}

db = client.forms

filter={
    'customer_name': 'text'
}

result = db.templates.find(
  filter=filter
)

# for n in result:
#     print(n.get("name"))
#
# print(result)

input_template = {
    "customer_name": "text",
    "customer_birthday_date": "date",
    'customer_phone': 'phone',
    'customer_email': "email"
}

input_template3 = {
    "customer_name": "text",
    "customer_birthday_date": "text",
}

# Searching matches in the db
# matches_ar = []
matches = set()
for k,v in input_template.items():
    filter = {k: v}
    match = db.templates.find(
        filter=filter,
        projection={"_id": 1}
    )
    # matches_ar += [set([i.get("_id") for i in match])]
    field_match = {i.get("_id") for i in match}
    matches.update(field_match)

# pprint("*********")
# pprint(matches)

valid_templates_ids = []
for match in matches:
    # Temlate's fields
    fields = db.templates.find_one(
        filter={"_id": match},
        projection={"_id": 0, "name": 0}
    )
    template_match_valid = True
    # Input template must contain 100% of template in db
    for field_name, field_value in fields.items():
        if (field_name not in input_template or input_template.get(field_name)!=field_value):
            template_match_valid = False
            break
    if template_match_valid:
        valid_templates_ids += [match]

print(f'Valid: {valid_templates_ids}')


# Answer
json_out = {}
if len(valid_templates_ids)>0:
    json_out["matches"] = True
    json_out["templates"] = []
    for id in valid_templates_ids:
        match = db.templates.find_one(
            filter={"_id": id},
            projection={"_id": 1, "name": 1}
        )
        json_out["templates"] += [match]
        print(match.get("name"))
else:
    json_out["matches"] = False
    json_out["custom_template"] = input_template

pprint(json_out)
