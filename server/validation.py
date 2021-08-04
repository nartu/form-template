import re

def field_pattern(string: int) -> str:
    result = "text"
    re_patterns = {
        # DD.MM.YYYY или YYYY-MM-DD
        'date': [
            r"(?P<day>[0-2]\d|[0-3][0-1])\.(?P<month>[0]\d|[1][0-2])\.(?P<year>[0-2]\d{3})",
            r"(?P<year>[0-2]\d{3})-(?P<month>[0]\d|[1][0-2])-(?P<day>[0-2]\d|[0-3][0-1])"
        ],
        # +7 xxx xxx xx xx
        'phone': [r"[\+\s]7(?:\s\d{3}){2}(?:\s\d{2}){2}"],
        # a.b.user@post.com.ru
        'email': [r"(?:\w[\._-])*\w+@\w+(?:\.\w+)+"]
    }
    for name, patterns in re_patterns.items():
        for pattern in patterns:
            is_it = re.search(pattern, string)
            if is_it:
                result = name
    return result

def fields_patterns(fields_and_data: dict) -> dict:
    fields_and_type = {}
    for k,v in fields_and_data.items():
        fields_and_type.update({k: field_pattern(v)})
    return fields_and_type

def main():
    # print(field_pattern("+7 903 777 77 77"))
    fields_and_data = {
        "name": "A. A. Ivanov",
        "phone": " 7 903 777 77 77",
        "email": "a.a.ivanov@gmail.com.ru",
        'date1': '10.06.2014',
        'date2': '2021-12-01',
        "message": "Всем привет!"
    }

    print(fields_patterns(fields_and_data))

    # p = re.compile(r'\d+')
    #
    # s = "Over \u0e55\u0e57 57 flavours"
    # print(s)
    # m = p.search(s)
    # print(repr(m.group()))


    # print(field_pattern("ivanov@gmail.com.ru"))


if __name__ == '__main__':
    main()
