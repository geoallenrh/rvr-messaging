import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import SpheroRvrTargets
from sphero_sdk import RvrStreamingServices
from sphero_sdk import DriveFlagsBitmask


rvr = SpheroRvrObserver()


def accelerometer_handler(accelerometer_data):
    print('Accelerometer data response: ', accelerometer_data)

def main():
    """ This program has initializes the RVR and messaging components.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()

        rvr.reset_locator_x_and_y()

    

        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.accelerometer,
            handler=accelerometer_handler
        )

        rvr.sensor_control.start(interval=1000)
        #rvr.sensor_control.stop()


        # Delay to allow RVR to send data?
        time.sleep(3)

        rvr.drive_with_heading(
            speed=64,  # Valid speed values are 0-255
            heading=0,  # Valid heading values are 0-359
            flags=DriveFlagsBitmask.none.value
        )


        # Delay to allow RVR to drive
        time.sleep(1)

        rvr.drive_with_heading(
            speed=64,  # Valid speed values are 0-255
            heading=90,  # Valid heading values are 0-359
            flags=DriveFlagsBitmask.none.value
        )

        # Delay to allow RVR to drive
        time.sleep(3)

        #rvr.sensor_control.start(interval=1000)
        

        # Delay to allow RVR to drive

        while True:
            # Delay to allow RVR to stream sensor data
            time.sleep(3)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
