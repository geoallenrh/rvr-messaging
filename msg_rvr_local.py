import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import Colors

import requests
import polling

rvr = SpheroRvrObserver()


url = 'http://rvr-kafka-bridge-route-rvr.apps.cluster-sgf-633d.sgf-633d.example.opentlc.com/consumers/rvr-group/instances/rvr-consumer/records'
headers = {'accept': 'application/vnd.kafka.json.v2+json'}


def get_command(resp):
    print(resp.status_code)

    if (resp.status_code == 200 and resp.text != "[]"):
        # This means we should have some data.
        records = resp.json()
        command = records[0]['value']['Body'].lower().strip()
        print("Command: " + command)
        
        #rvr.led_control.set_all_leds_color(color=Colors.blue)

        rvr.wake()
        
        if (command == "drive"):
            time.sleep(2)

            rvr.drive_control.reset_heading()

            rvr.drive_control.roll_start(
                speed=25,
                heading=90
            )

            # Delay to allow RVR to drive
            time.sleep(1)

            rvr.drive_control.roll_stop(heading=270)

            # Delay to allow RVR to drive
            time.sleep(1)

        # Give RVR time to wake up
        #time.sleep(2)

        #rvr.led_control.turn_leds_off()

        # Delay to show LEDs change
        #time.sleep(1)
        else:
            colorValue = (Colors[command])
            print(colorValue)

            #rvr.led_control.set_all_leds_color(color=Colors.blue)
            rvr.led_control.set_all_leds_color(Colors[command])

            # Delay to show LEDs change
            #time.sleep(1)

            #rvr.led_control.turn_leds_off()

            # Delay to show LEDs change
            #await asyncio.sleep(1)

            #await rvr.led_control.set_all_leds_rgb(red=255, green=144, blue=0)

            # Delay to show LEDs change
        
            #rvr.close()
    

def main():
    """ This program demonstrates how to set the all the LEDs of RVR using the LED control helper.
    """
    try:
        polling.poll(
        lambda: requests.get(url,headers=headers),
        check_success=get_command,
        step=10,
        poll_forever=True
        )
    
    except KeyboardInterrupt:
        print('\nProgram termintated with keyboard interrupt.')
    
    finally:
        rvr.close()
        

if __name__ == '__main__':
    main()