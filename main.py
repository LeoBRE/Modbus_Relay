from libs import modbus_serial_relay
from libs import modbus_eth_relay
import time

DEVICE_ADRESS = 0x01

relay_serial = modbus_serial_relay.Modbus_serial_relay(port="/dev/ttyUSB0", baudrate=9600, device_adress=DEVICE_ADRESS)
# relay_eth = modbus_eth_relay.Modbus_eth_relay(IP_adress='192.168.1.0', port_number=1111)

for i in range (0,10):
    relay_serial.open_single_relay(6)
    time.sleep(0.2)
    relay_serial.close_single_relay(6)
    time.sleep(0.2)
    # relay_serial.flip_single_relay(1)
    # relay_serial.open_all_relay()
    # relay_serial.close_all_relay()
    # relay_serial.flip_all_relay()
    # print(relay_serial.read_all_relay_states())
    # print(relay_serial.read_one_relay_state(1))
    # relay_serial.change_device_baudrate(115200, new_parity=0)
    # relay_serial.change_device_adress(0x01)
    # relay_serial.read_device_adress()
    # relay_serial.read_device_software_version()

    # relay_eth.open_single_relay(1)
    # relay_eth.close_single_relay(1)
    # relay_eth.flip_single_relay(1)
    # relay_eth.open_all_relay()
    # relay_eth.close_all_relay()
    # relay_eth.flip_all_relay()
    # print(relay_eth.read_all_relay_states())
    # print(relay_eth.read_one_relay_state(1))
    # relay_eth.change_device_baudrate(115200, new_parity=0)
    # relay_eth.change_device_adress(0x02)
    # relay_eth.read_device_adress()
    # relay_eth.read_device_software_version()


    
    