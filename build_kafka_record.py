import json
import requests

mac = {'macAddress': 'f05eccbc9b2c'}
battery = {'percentage': 26}
accelerometer = {'Accelerometer': {'Y': -0.09791087733998616, 'Z': 0.9689884225300034, 'X': -0.030332561589389684, 'is_valid': True}}

data = {}
data['records'] = []

sensor_data = {}

sensor_data['key'] = mac['macAddress']
sensor_data['value'] = {}
sensor_data['value']['battery'] = battery['percentage']
sensor_data['value']['accelerometer'] = accelerometer['Accelerometer']
  
data['records'].append(sensor_data) 

print('Python Object: ' ,data)
json_data = json.dumps(data)
print('JSON Dump: ',json_data)

hostname ='http://rvr-route-rvr.apps.cluster-ses-77e1.ses-77e1.example.opentlc.com/'
url = hostname + '/topics/rvr-telemetry'
headers = {'content-type': 'application/vnd.kafka.json.v2+json'}
    # post messages through Kafka Bridge
    
resp = requests.post(url,headers=headers,data=json_data)
print(resp.status_code)
print(resp)
if (resp.status_code == 200 ):
    # This means we should have some data, if we don't will wait and try again.
    print(resp.json())
    
else:
    print(resp.status_code)

