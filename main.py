from libs import modbus_serial_relay
from libs import modbus_eth_relay
import time

DEVICE_ADRESS = 0x01

serie = 0
if serie:
    relay_serial = modbus_serial_relay.Modbus_serial_relay(port='COM23', baudrate=9600, device_adress=DEVICE_ADRESS)
    ##### TEST SERIAL #######
    for i in range (8):
        relay_serial.open_single_relay(i)
        time.sleep(1)
        relay_serial.close_single_relay(i)
        time.sleep(1)
        relay_serial.flip_single_relay(i)
        time.sleep(1)
        
    relay_serial.close_all_relay()
    time.sleep(1)
    relay_serial.open_all_relay()
    time.sleep(1)
    relay_serial.flip_all_relay() 
    time.sleep(1)
else:
    relay_eth = modbus_eth_relay.Modbus_eth_relay(IP_adress='192.168.1.200', port_number=4196, device_adress=DEVICE_ADRESS)
    ##### TEST ETHERNET #######
    for i in range (8):
        relay_eth.open_single_relay(i)
        time.sleep(1)
        relay_eth.close_single_relay(i)
        time.sleep(1)
        relay_eth.flip_single_relay(i)
        time.sleep(1)
        
    relay_eth.close_all_relay()
    time.sleep(1)
    relay_eth.open_all_relay()
    time.sleep(1)
    relay_eth.flip_all_relay() 
    time.sleep(1)