
import serial
import time
from libs import pycrc
from enum import Enum

NB_RELAY_PER_CARD = 8
BROADCAST_ADRESS = 0x00

class function_code(Enum):
    READ_STATES_OF_RELAY = 0x01
    READ_ADRESS_VERSION = 0x03
    CONTROLLING_RELAY = 0x05
    SET_BAUDRATE_ADRESS = 0x06
    WRITE_RELAY_STATES = 0x0F

class write_relay_state(Enum):
    OPEN_RELAY = 0xFF
    CLOSE_RELAY = 0x00
    FLIP_RELAY = 0x55

class modbus_serial_relay:
    def __init__(self, port:str, baudrate:int=115200, device_adress:int=0x01, timeout:int=1) -> None:
        assert isinstance(port, str)
        assert isinstance(baudrate, int)
        assert isinstance(device_adress, int)

        self.serial_device = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.device_adress = device_adress

    def open_single_relay(self, relay_number:int) -> None:
        assert isinstance(relay_number, int)
        assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
        # self.activate_single_relay(relay_number=relay_number)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.CONTROLLING_RELAY
        cmd[2] = 0
        cmd[3] = relay_number
        cmd[4] = write_relay_state.OPEN_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def close_single_relay(self, relay_number:int) -> None:
        assert isinstance(relay_number, int)
        assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
        # self.activate_single_relay(relay_number=relay_number)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.CONTROLLING_RELAY
        cmd[2] = 0
        cmd[3] = relay_number
        cmd[4] = write_relay_state.CLOSE_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def flip_single_relay(self, relay_number:int) -> None:
        assert isinstance(relay_number, int)
        assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
        # self.activate_single_relay(relay_number=relay_number)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.CONTROLLING_RELAY
        cmd[2] = 0
        cmd[3] = relay_number
        cmd[4] = write_relay_state.FLIP_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def open_all_relay(self) -> None:
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.CONTROLLING_RELAY
        cmd[2] = 0x00
        cmd[3] = 0xFF
        cmd[4] = write_relay_state.OPEN_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def close_all_relay(self) -> None:
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.CONTROLLING_RELAY
        cmd[2] = 0x00
        cmd[3] = 0xFF
        cmd[4] = write_relay_state.CLOSE_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def flip_all_relay(self) -> None:
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.CONTROLLING_RELAY
        cmd[2] = 0x00
        cmd[3] = 0xFF
        cmd[4] = write_relay_state.CLOSE_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def read_all_relay_states(self) -> dict:
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.READ_STATES_OF_RELAY
        cmd[2] = 0
        cmd[3] = 0
        cmd[4] = 0
        cmd[5] = 0x08
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)
        try:
            answer = self.serial_device.read(6)
        except serial.SerialTimeoutException:
            assert False, "No data received"
        #Store result in a dict
        d = dict()
        for i in range [0:8]:
            if (answer[3] & 1<<i) == 1:
                d['Relay ' + str(i)] = 'Open'
            if (answer[3] & 1<<i) == 0:
                d['Relay ' + str(i) +': '] = 'Close'
        return d
    
    def read_one_relay_state(self, relay_number:int)->dict:
        assert isinstance(relay_number, int)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.READ_STATES_OF_RELAY
        cmd[2] = 0
        cmd[3] = 0
        cmd[4] = 0
        cmd[5] = 0x08
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)
        try:
            answer = self.serial_device.read(6)
        except serial.SerialTimeoutException:
            assert False, "No data received"
        d =dict()
        if (answer[3] & 1<< relay_number) == 1:
            d['Relay ' + str(relay_number)] = 'Open'
        if (answer[3] & 1<< relay_number) == 0:
            d['Relay ' + str(relay_number)] = 'Close'

    def __baudrate_calculation(self, baudrate:int)->int:
        assert isinstance(baudrate, int)
        if baudrate == 4800:
            return 0x00
        if baudrate == 9600:
            return 0x01
        if baudrate == 19200:
            return 0x02
        if baudrate == 38400:
            return 0x03
        if baudrate == 57600:
            return 0x04
        if baudrate == 115200:
            return 0x05
        if baudrate == 128000:
            return 0x06
        if baudrate == 256000:
            return 0x07
        else:
            assert False, "Non standard baudrate"

    def change_device_baudrate(self, new_baudrate:int, new_parity:int) ->None:
        assert isinstance(new_baudrate, int)
        assert isinstance(new_parity, int)
        assert (new_parity>=0x00 and new_parity<= 0x02)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.SET_BAUDRATE_ADRESS
        cmd[2] = 0x20
        cmd[3] = 0x00
        cmd[4] = new_parity # 0x00: no parity check, 0x01: even parity check, 0x02: odd parity check 
        cmd[5] = self.__baudrate_calculation(new_baudrate) # 0x00 : 4800, 0x01 : 9600, 0x02 : 19200, 0x03 : 38400, 0x04 : 57600, 0x05 : 115200, 0x06 : 128000, 0x07 : 256000
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def change_device_adress(self, new_adress:int) ->None:
        assert isinstance(new_adress, int)
        assert (new_adress>=0x01 and new_adress<= 0xFF)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = function_code.SET_BAUDRATE_ADRESS
        cmd[2] = 0x40
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = new_adress
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def read_device_adress(self)->int:
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = BROADCAST_ADRESS
        cmd[1] = function_code.READ_ADRESS_VERSION
        cmd[2] = 0x40
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = 0x01
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)
        try:
            answer = self.serial_device.read(7)
        except serial.SerialTimeoutException:
            assert False, "No data received"
        return answer[4]

    def read_device_software_version(self)->int:
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = BROADCAST_ADRESS
        cmd[1] = function_code.READ_ADRESS_VERSION
        cmd[2] = 0x20
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = 0x01
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)
        try:
            answer = self.serial_device.read(7)
        except serial.SerialTimeoutException:
            assert False, "No data received"
        return answer[4]/100


    # LACK OF COMPREHENSION on this part

    # def activate_single_relay(self, relay_number:int) -> None:
    #     assert isinstance(relay_number, int)
    #     assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
    #     relay_states = self.read_all_relay_states()
    #     cmd = [0,0,0,0,0,0,0,0,0,0]
    #     cmd[0] = self.device_adress
    #     cmd[1] = function_code.WRITE_RELAY_STATES
    #     cmd[2] = 0
    #     cmd[3] = 0
    #     cmd[4] = 0
    #     cmd[5] = 0x08
    #     cmd[6] = 0x01
    #     cmd[7] = 
    #     crc = pycrc.ModbusCRC(cmd[0:8])
    #     cmd[8] = crc & 0xFF
    #     cmd[9] = crc >> 8
    #     self.serial_device.write(cmd)

    # def deactivate_single_relay(self, relay_number:int) -> None:
    #     assert isinstance(relay_number, int)
    #     assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
    #     cmd = [0,0,0,0,0,0,0,0,0,0]
    #     cmd[0] = self.device_adress
    #     cmd[1] = function_code.WRITE_RELAY_STATES
    #     cmd[2] = 0
    #     cmd[3] = 0
    #     cmd[4] = 0
    #     cmd[5] = 0x08
    #     cmd[6] = # NEED TO CHECK STATUS
    #     crc = pycrc.ModbusCRC(cmd[0:8])
    #     cmd[8] = crc & 0xFF
    #     cmd[9] = crc >> 8
    #     self.serial_device.write(cmd)
