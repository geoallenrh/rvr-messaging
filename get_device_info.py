import os
import sys
import time
import json
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import SpheroRvrTargets
from sphero_sdk import RvrStreamingServices

config = configparser.ConfigParser()
config.read('config.ini')
hostname = config['DEFAULT']['KAFKA_BRIDGE_HOSTNAME']

rvr = SpheroRvrObserver()

data = {}
data['records'] = []

sensor_data = {}

sensor_data['value'] = {}


  
def get_sku_handler(sku):
    print('Device SKU: ', sku)

def get_mac_address_handler(mac):
    print('MAC: ', mac)
    global sensor_data
    sensor_data['key'] = mac['macAddress']
    
def battery_percentage_handler(battery_percentage):
    print('Battery percentage: ', battery_percentage)
    global sensor_data
    sensor_data['value']['battery'] = battery_percentage['percentage']

def accelerometer_handler(accelerometer_data):
    print('Accelerometer data response: ', accelerometer_data)
    global sensor_data
    sensor_data['value']['accelerometer'] = accelerometer_data['Accelerometer']

    global data
    data['records'].append(sensor_data) 
    ## probably want to batch up multiple records
    post_to_kafka(data)
    
    
def post_to_kafka(records):
    print('Python Object: ' ,records)
    json_data = json.dumps(records)
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
    
 
def initSensorData():
    """ Obtain Device Info.
    """
    try:
        
        # Give RVR time to wake up
        time.sleep(2)

        rvr.get_mac_address(handler=get_mac_address_handler)

        time.sleep(1)

        rvr.get_battery_percentage(handler=battery_percentage_handler)

        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')
        rvr.close()

    finally:
        print('\nDo some cleanup.')
        

def getSensorStream():
    """ This program demonstrates how to enable a single sensor to stream.
    """

    try:
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.accelerometer,
            handler=accelerometer_handler
        )

        rvr.sensor_control.start(interval=2000)

        while True:
            # Delay to allow RVR to stream sensor data
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')
        rvr.close()

    finally:
        print('\nDo some cleanup.')
        


def main():
    """ Obtain Sensor Data.
    """

    try:
        rvr.wake()
        initSensorData()
        getSensorStream()
        

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
