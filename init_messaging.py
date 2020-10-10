import requests
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
host = config['DEFAULT']['KAFKA_BRIDGE_HOSTNAME']


## is Kafka Cluster Health
response = requests.get(
    url = host + '/healthy',
    headers = {'accept': 'application/vnd.kafka.json.v2+json'},
)

# View the new `text-matches` array which provides information
# about your search term within the results
print(response.status_code)
if (response.status_code == 200):
    print("Kafka Cluster Healthly")

    #Create Consumer
    response = requests.post(
    url = host + '/consumers/rvr-group',
    data={
    'name': 'rvr-consumer',
    "format": "json",
    "enable.auto.commit": false
    },
    headers = {'accept': 'application/vnd.kafka.json.v2+json'},
    )
    print(response.status_code)

 #Subscribe to Topic


#Get Subscriptions (determine if we need to recreate consumer)   