import logging
import logging.handlers

import xmlrpc.client

from ...src.constants import DEVICE_MANAGEMENT_PORT, KORUZA_MAIN_PORT, REMOTE_UNIT_IP
from ...src.config_manager import get_config

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
        self.local_koruza_client = xmlrpc.client.ServerProxy(f"http://localhost:{DEVICE_MANAGEMENT_PORT}", allow_none=True)

        # init device to device communication
        # read config file
        config = get_config()["device_mgmt"]

        print(f"Read config: {config}")

        #1. select communication channel - either WIFI or BLE
        channel = config["channel"]
        
        #2. get other unit address - has to be configured beforehand in config step - enter manually in config? TODO
        remote_unit_address = config[channel]["remote_unit_addr"]
        
        #3. init remote device_client with selected communication channel
        # WIFI
        if channel == "wifi":
            self.remote_device_client = xmlrpc.client.ServerProxy(f"http://{REMOTE_UNIT_IP}:{DEVICE_MANAGEMENT_PORT}", allow_none=True)
        # BLE TODO
        if channel == "ble":
            pass
        
        #4. set mode based on configuration
        self.mode = config[channel]["mode"]

    def request_remote(self, command, params):
        """
        Used locally from koruza.py
        Request remote command over one of the available channels
        TODO: enable multiple channels in config, only local network is supported for now

        Only used to pipe command to remote endpoint!
        """

        # if unit is in slave mode don't request any data, handle here or in GUI? TODO
        if self.mode == "slave":
            return

        # if not in slave mode get response from communication channel

        # WIFI 
        print(f"Received remote request command: {command}, params: {params}")
        response = self.remote_device_client.handle_remote_request(command, params)
        print(f"Received response from remote: {response}")
        return response

        # BLE TODO

    def handle_remote_request(self, command, params):
        """
        Exposed externally as endpoint for remote calls
        """

        print(f"Handling remote request: {command} with params {params}")

        # pipe data to koruza client (main) and respond with response from main
        if command == "get_sfp_data":
            response = self.local_koruza_client.get_sfp_data()

        if command == "get_motors_position":
            response = self.local_koruza_client.get_motors_position()

        if command == "move_motors":
            response = self.local_koruza_client.move_motors(*params)  # unpack params

        if command == "home":
            response = self.local_koruza_client.home()

        if command == "disable_led":
            response = self.local_koruza_client.disable_led()

        print(f"Response from slave unit: {response}")
        return response