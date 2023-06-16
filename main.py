import lib

DEVICE_ADRESS = 0x01

relay_controller = lib.modbus_serial_relay(port="/dev/ttyUSB0", baudrate=9600, device_adress=DEVICE_ADRESS)

while True:
    relay_controller.open_single_relay(1)
    relay_controller.close_single_relay(1)
    relay_controller.flip_single_relay(1)
    relay_controller.open_all_relay()
    relay_controller.close_all_relay()
    relay_controller.flip_all_relay()
    print(relay_controller.read_all_relay_states())
    print(relay_controller.read_one_relay_state(1))
    relay_controller.change_device_baudrate(115200)
    relay_controller.change_device_adress(0x02)
    relay_controller.read_device_adress()
    relay_controller.read_device_software_version()
    
    