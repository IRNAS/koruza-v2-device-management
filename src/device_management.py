import logging
import logging.handlers
import socket
import time

import xmlrpc.client

from ...src.constants import DEVICE_MANAGEMENT_PORT, KORUZA_MAIN_PORT
from ...src.config_manager import get_config

socket.setdefaulttimeout(0.5)  # this solves our blocking problem apparently - TODO find a better way
RC_TIMEOUT = 10  # try again every 10 seconds

log = logging.getLogger()

filename = "./koruza_v2/logs/device_management_log.log"
logging.basicConfig(format='%(asctime)s - %(module)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
rotate_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=10485760, backupCount=4)
rotate_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M:%S'))
logging.getLogger().addHandler(rotate_handler)

log = logging.getLogger()
log.info("-------------- NEW RUN with logging enabled --------------")

class DeviceManagement():
    def __init__(self):

        # init local rpc communication
        self.local_koruza_client = xmlrpc.client.ServerProxy(f"http://localhost:{KORUZA_MAIN_PORT}", allow_none=True)

        # init device to device communication
        # read config file
        config = get_config()["device_mgmt"]

        print(f"Read config: {config}")

        #1. select communication channel - either WIFI or BLE
        channel = config["channel"]
        
        #2. get other unit address - has to be configured beforehand in config step - enter manually in config? TODO
        remote_unit_address = config[channel]["remote_unit_addr"]
        
        #3. set mode based on configuration
        self.mode = config[channel]["mode"]

        print(f"Starting in mode {self.mode}")

        if self.mode == "master":
            #4. init remote device_client with selected communication channel
            # WIFI
            if channel == "wifi":
                self.remote_device_client = xmlrpc.client.ServerProxy(f"http://{remote_unit_address}:{DEVICE_MANAGEMENT_PORT}", allow_none=True)
            # BLE TODO
            if channel == "ble":
                pass


        # variable checking for response - stop sending if no response for a few tries
        self.retry_count = 0
        self.timeout_triggered = False
        # keep track of last request, allow retry every 10 seconds for example
        self.time_of_last_request = time.time()
        self.time_of_last_reply = time.time()


    def request_remote(self, command, params):
        """
        Used locally from koruza.py
        Request remote command over one of the available channels

        Only used to pipe command to remote endpoint!
        """
        self.time_of_last_request = time.time()

        if self.time_of_last_request - self.time_of_last_reply > RC_TIMEOUT and not self.timeout_triggered:  # if more than RC_TIMEOUT seconds passed increase retry count
            self.timeout_triggered = True

        if self.timeout_triggered:  
            if int((self.time_of_last_request - self.time_of_last_reply) / RC_TIMEOUT) > self.retry_count:
                self.retry_count += 1
                log.warning("Second unit doesn't seem to be available! Retrying")
                pass

            else:
                return # return

        # if unit is in slave mode don't request any data, handle here or in GUI? TODO
        if self.mode == "slave":
            return

        # if not in slave mode get response from communication channel

        # WIFI/LAN
        # NOTE - this part has to be done async or with a timeout
        print(f"Received remote request command: {command}, params: {params}")
        response = self.remote_device_client.handle_remote_request(command, params)
        self.timeout_triggered = False  # set retry count to 0 if response was received
        self.time_of_last_reply = time.time()
        print(f"Received response from remote: {response}")
        return response

        # BLE TODO

    def handle_remote_request(self, command, params):
        """
        Exposed externally as endpoint for remote calls
        """

        # pipe data to koruza client (main) and respond with response from main
        if command == "get_sfp_diagnostics":
            response = self.local_koruza_client.get_sfp_diagnostics()

        if command == "get_motors_position":
            response = self.local_koruza_client.get_motors_position()

        if command == "move_motors":
            response = self.local_koruza_client.move_motors(*params)  # unpack params

        if command == "move_motors_to":
            response = self.local_koruza_client.move_motors_to(*params)  # unpack params

        if command == "home":
            response = self.local_koruza_client.home()

        if command == "toggle_led":
            response = self.local_koruza_client.toggle_led()

        return response