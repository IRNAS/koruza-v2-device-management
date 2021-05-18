# koruza-v2-device-management

## Description
KORUZA v2 Pro Device Management provides a secondary communication channel for two mounted units.

Through this communication channel the following operations are conducted:
* Initial unit configuration
* Data monitoring
* Remote unit management
* Alignment and tracking

Currently three techonologies are in development:
* WiFi - the two units can connect using wireless USB dongles
* Local Network Connection - the two units can connect if they are on the same local network
* Bluetooth - the two units can connect using external Bluetooth dongles

## Config

To enable this channel the units have to be configured in a primary/secondary relation. A `config.json` file is included in the [KORUZA v2 Pro](https://github.com/IRNAS/koruza-v2-pro) repository. Before running the code for the first time move the included `config.json` file into the `config` folder located in the main repository.

The contents of the file are as follows:
```
{
    "device_mgmt": {
        "channel": "wifi",
        "ble": {
            "mode": "primary",
            "addr": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "remote_unit_addr": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        },
        "wifi": {
            "mode": "primary",
            "addr": "xxx.xxx.xxx.xxx",
            "remote_unit_addr": "xxx.xxx.xxx.xxx"
        },
        "local": {
            "mode": "primary",
            "addr": "xxx.xxx.xxx.xxx",
            "remote_unit_addr": "xxx.xxx.xxx.xxx"
        },
        "lora": {
            "mode": "primary",
            "addr": "xxx.xxx.xxx.xxx",
            "remote_unit_addr": "xxx.xxx.xxx.xxx"
        }
    },
    "camera": {
        "width": 720,
        "height": 720
    }
}
```

## License
Firmware and software originating from KORUZA v2 Pro project, including KORUZA v2 Pro Device Management, is licensed under [GNU General Public License v3.0](https://github.com/IRNAS/koruza-v2-device-management/blob/master/LICENSE).

Open-source licensing means the hardware, firmware, software and documentation may be used without paying a royalty, and knowing one will be able to use their version forever. One is also free to make changes, but if one shares these changes, they have to do so under the same conditions they are using themselves. KORUZA, KORUZA v2 Pro and IRNAS are all names and marks of IRNAS LTD. These names and terms may only be used to attribute the appropriate entity as required by the Open Licence referred to above. The names and marks may not be used in any other way, and in particular may not be used to imply endorsement or authorization of any hardware one is designing, making or selling.