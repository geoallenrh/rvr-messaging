import requests
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
host = config['DEFAULT']['KAFKA_BRIDGE_HOSTNAME']
consumer_group = config['DEFAULT']['CONSUMER_GROUP']
consumer_name = config['DEFAULT']['CONSUMER_NAME']
url = host + '/consumers/rvr-group'

#Create Consumer
response = requests.post(url ,
data={
'name': 'rvr-consumer',
"format": "json",
"enable.auto.commit": "false"
},
headers = {'accept': 'application/vnd.kafka.json.v2+json'},
)
print(response.status_code)


#Subscribe to Topic


#Get Subscriptions (determine if we need to recreate consumer)   