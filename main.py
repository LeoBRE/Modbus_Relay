from libs import modbus_serial_relay
from libs import modbus_eth_relay

DEVICE_ADRESS = 0x01

relay_serial = modbus_serial_relay.modbus_serial_relay(port="/dev/ttyUSB0", baudrate=9600, device_adress=DEVICE_ADRESS)
relay_eth = modbus_eth_relay.modbus_eth_relay('192.168.1.0', 1111)

while True:
    relay_serial.open_single_relay(1)
    relay_serial.close_single_relay(1)
    relay_serial.flip_single_relay(1)
    relay_serial.open_all_relay()
    relay_serial.close_all_relay()
    relay_serial.flip_all_relay()
    print(relay_serial.read_all_relay_states())
    print(relay_serial.read_one_relay_state(1))
    relay_serial.change_device_baudrate(115200)
    relay_serial.change_device_adress(0x02)
    relay_serial.read_device_adress()
    relay_serial.read_device_software_version()

    relay_eth.open_single_relay(1)
    relay_eth.close_single_relay(1)
    relay_eth.flip_single_relay(1)
    relay_eth.open_all_relay()
    relay_eth.close_all_relay()
    relay_eth.flip_all_relay()
    print(relay_eth.read_all_relay_states())
    print(relay_eth.read_one_relay_state(1))
    relay_eth.change_device_baudrate(115200)
    relay_eth.change_device_adress(0x02)
    relay_eth.read_device_adress()
    relay_eth.read_device_software_version()


    
    