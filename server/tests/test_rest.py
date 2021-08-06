import pytest
import os, sys
import requests
import json

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

# params
# local
# server = 'http://127.0.1.20:8000'
# docker
server = 'http://0.0.0.0:80'

def test_app_health():
    r = requests.get(server+'/')
    assert 'message' in r.json()

def test_db_rest():
    r = requests.get(server+'/db_status')
    assert r.json()['process'] == 'mongod'

def test_not_match_custom_template():
    url = server+'/get_form?name=Lil&message=Здравуйте товарищи!&phone=+7 903 777 77 77&email= a.a.ivanov@gmail.com.ru'
    r = requests.post(url)
    j = r.json()
    assert not j['matches']
    assert r.json()['custom_template']['phone'] == 'phone'
    assert j['custom_template']['email'] == 'email'

def test_validation_phone_and_email():
    url = server+'/get_form?phone=  +7 903 777 77 77&email1=a.a.ivanov@gmail.com.ru&email2=user@example.com'
    r = requests.post(url)
    j = r.json()
    assert not j['matches']
    assert j['custom_template']['phone'] == 'phone'
    assert j['custom_template']['email1'] == 'email'
    assert j['custom_template']['email2'] == 'email'

def test_validation_date():
    url = server+'/get_form?date1=23.12.1999&date2=2000-03-31'
    r = requests.post(url)
    j = r.json()
    assert not j['matches']
    assert j['custom_template']['date1'] == 'date'
    assert j['custom_template']['date2'] == 'date'

def test_exact_match():
    file = os.path.join(parent_dir, 'dump_last.json')
    with open(file,'r') as f:
        exm = json.load(f)[0]
        exm.update({'customer_name': 'Jul', 'customer_email': 'myemail@bk.ru', 'customer_phone': '+7 999 112 12 12'})
        template_name = exm.pop('name', None)
    r = requests.post(server+'/get_form', params=exm)
    j = r.json()
    assert j['matches']
    assert [True for t in j['templates'] if t.get('name')==template_name]

# THe template must be matched
def test_match_extra_fields():
    file = os.path.join(parent_dir, 'dump_last.json')
    with open(file,'r') as f:
        exm = json.load(f)[0]
        exm.update({'customer_name': 'Jul', 'customer_email': 'myemail@bk.ru', 'customer_phone': '+7 999 112 12 12'})
        template_name = exm.pop('name', None)
        exm['customer_additiona_phone'] = '+7 666 666 00 00'
    r = requests.post(server+'/get_form', params=exm)
    j = r.json()
    assert j['matches']
    assert [True for t in j['templates'] if t.get('name')==template_name]

# The template must not be matched
def test_not_match_less_fields():
    file = os.path.join(parent_dir, 'dump_last.json')
    with open(file,'r') as f:
        exm = json.load(f)[0]
    exm.update({'customer_name': 'Jul', 'customer_email': 'myemail@bk.ru', 'customer_phone': '+7 999 112 12 12'})
    template_name = exm.pop('name', None)
    for_del = list(exm.keys())[0]
    del exm[for_del]
    r = requests.post(server+'/get_form', params=exm)
    j = r.json()
    assert not j['matches']

# The template must not be matched
def test_not_match_less_fields_and_extra_other():
    file = os.path.join(parent_dir, 'dump_last.json')
    with open(file,'r') as f:
        exm = json.load(f)[0]
    exm.update({'customer_name': 'Jul', 'customer_email': 'myemail@bk.ru', 'customer_phone': '+7 999 112 12 12'})
    exm['customer_additiona_phone'] = '+7 666 666 00 00'
    exm.update({'customer_name2': 'Mi'})
    template_name = exm.pop('name', None)
    for_del = list(exm.keys())[0]
    del exm[for_del]
    r = requests.post(server+'/get_form', params=exm)
    j = r.json()
    assert not j['matches']
