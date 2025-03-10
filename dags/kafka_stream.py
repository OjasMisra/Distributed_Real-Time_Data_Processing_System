from datetime import datetime
from ensurepip import bootstrap

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Ojas',
    'start_date' : datetime(2025,3,1,4,45)
}

def get_data():
    import json
    import requests

    res=requests.get("https://randomuser.me/api/").json()
    res = res['results'][0]

    return res

def format_data(res):

    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street'] ['number'])} {location['street'] ['name']}"\
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['postcode'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login'] ['username']
    data['dob'] = res['dob'] ['date']
    data['registered_date'] = res['registered'] ['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():
    import json
    import kafka
    import time

    res = get_data()
    res = format_data(res)
    #print(json.dumps(res,indent=2))

    producer = kafka.KafkaProducer(bootstrap_servers = ['localhost:9092'], max_block_ms=5000)

    producer.send('Users_Created', json.dumps(res).encode('utf-8'))


# with DAG('user_automation',
#          default_args = default_args,
#          schedule_interval='@daily',
#          catchup=False) as dag:
#
#     streaming_task = PythonOperator(
#         task_id='stream_data_from_api',
# #        python_callable=
#     )

stream_data()