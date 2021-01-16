import boto3
import datetime
import json
import requests

import private_data

headers = {
    'authority': 'citizen.com',
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://citizen.com/explore',
    'accept-language': 'en-US,en;q=0.9',
}

params = (
    ('lowerLatitude', '40.755214826229405'),
    ('lowerLongitude', '-73.97147728020968'),
    ('upperLatitude', '40.78296257504613'),
    ('upperLongitude', '-73.94611568719881'),
    ('fullResponse', 'true'),
    ('limit', '100'),
)

response = requests.get('https://citizen.com/api/incident/trending', headers=headers, params=params)

citizen_data = response.json()

file_name = 'citizen_' + str(datetime.datetime.now()).replace(' ', 'T') + '.json'


session = boto3.Session(
    aws_access_key_id=private_data.S3_ID,
    aws_secret_access_key=private_data.S3_KEY,
)

s3 = session.resource('s3')

s3object = s3.Object(private_data.S3_BUCKET_NAME, file_name)

s3object.put(
    Body=(bytes(json.dumps(citizen_data).encode('UTF-8')))
)
