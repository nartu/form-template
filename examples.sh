#! /usr/bin/env bash
host='127.0.1.20'
port=8000

curl -XPOST -G -v "http://$host:$port/get_form?customer_name=Jul&customer_email=myemai@bk.ru"
echo -e '\n'
echo -e '========================================================================================='
echo -e '\n'

curl -XPOST -G -v "http://$host:$port/get_form?customer_name=Jul&customer_email=myemai@bk.ru" --data-urlencode "customer_phone=+7 999 888 77 66"
echo -e '\n'
echo -e '========================================================================================='
echo -e '\n'

curl -XPOST -G -v "http://$host:$port/get_form?customer_name=Jul&customer_email=myemai@bk.ru" --data-urlencode "customer_phone=+7 999 888 77 66&message=Привет всем"
echo -e '\n'
echo -e '========================================================================================='
echo -e '\n'

curl -XPOST -v "http://$host:$port/get_form" --data-urlencode "test=nothing to find"
echo -e '\n'
echo -e '========================================================================================='
echo -e '\n'

curl -XPOST -v "http://$host:$port/get_form?customer_name=Alex&customer_birthday_date=06.06.2006"
echo -e '\n'
echo -e '========================================================================================='
echo -e '\n'

curl -XPOST -v "http://$host:$port/get_form?participant_name=Jul&date_of_request=$(date +"%Y-%m-%d")"
echo -e '\n'
echo -e '========================================================================================='
echo -e '\n'
