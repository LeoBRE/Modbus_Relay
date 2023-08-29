
import serial
from libs import pycrc

NB_RELAY_PER_CARD = 8
BROADCAST_ADRESS = 0x00

READ_STATES_OF_RELAY = 0x01
READ_ADRESS_VERSION = 0x03
CONTROLLING_RELAY = 0x05
SET_BAUDRATE_ADRESS = 0x06
WRITE_RELAY_STATES = 0x0F

OPEN_RELAY = 0xFF
CLOSE_RELAY = 0x00
FLIP_RELAY = 0x55

class Modbus_serial_relay:
    def __init__(self, port:str, baudrate:int=9600, device_adress:int=0x01, timeout:int=1) -> None:
        assert isinstance(port, str)
        assert isinstance(baudrate, int)
        assert isinstance(device_adress, int)

        self.serial_device = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.device_adress = device_adress

    def open_single_relay(self, relay_number:int) -> None:
        """Open a single relay.
        If the relay is cabled as NO, this function close the relay.

        Args:
            relay_number (int): relay number (first one is 0)
        """
        assert isinstance(relay_number, int)
        assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = CONTROLLING_RELAY
        cmd[2] = 0
        cmd[3] = relay_number
        cmd[4] = OPEN_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def close_single_relay(self, relay_number:int) -> None:
        """Close a single relay.
        If the relay is cabled as NO, this function open the relay.

        Args:
            relay_number (int): relay number (first one is 0)
        """
        assert isinstance(relay_number, int)
        assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = CONTROLLING_RELAY
        cmd[2] = 0
        cmd[3] = relay_number
        cmd[4] = CLOSE_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def flip_single_relay(self, relay_number:int) -> None:
        """Change state of a single relay.

        Args:
            relay_number (int): relay number (first one is 0)
        """
        assert isinstance(relay_number, int)
        assert (relay_number >= 0 and relay_number <= (NB_RELAY_PER_CARD - 1))
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = CONTROLLING_RELAY
        cmd[2] = 0
        cmd[3] = relay_number
        cmd[4] = FLIP_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def open_all_relay(self) -> None:
        """Open all relay.
        If relays are cabled as NO, this function open relays.
        """
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = CONTROLLING_RELAY
        cmd[2] = 0x00
        cmd[3] = 0xFF
        cmd[4] = OPEN_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def close_all_relay(self) -> None:
        """Close all relay.
        If relays are cabled as NO, this function close relays.
        """
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = CONTROLLING_RELAY
        cmd[2] = 0x00
        cmd[3] = 0xFF
        cmd[4] = CLOSE_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def flip_all_relay(self) -> None:
        """Change state of all relays.
        """
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = CONTROLLING_RELAY
        cmd[2] = 0x00
        cmd[3] = 0xFF
        cmd[4] = FLIP_RELAY
        cmd[5] = 0
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def read_all_relay_states(self) -> dict:
        """Read all relays state

        Returns:
            dict: State of all relays (0: close, 1: open)
        """
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = READ_STATES_OF_RELAY
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
            assert False, "Timeout"
        assert answer!=b'', "No data received"
        #Store result in a dict
        d = dict()
        for i in range(8):
            if (answer[3] & 1<<i) != 0:
                d['Relay ' + str(i)] = 'Open'
            if (answer[3] & 1<<i) == 0:
                d['Relay ' + str(i)] = 'Close'
        return d
    
    def read_one_relay_state(self, relay_number:int)->dict:
        """Read one relay state

        Args:
            relay_number (int): number of the relay state needed

        Returns:
            dict: State of the relay number
        """
        assert isinstance(relay_number, int)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = READ_STATES_OF_RELAY
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
            print("answer = ", answer)
        except serial.SerialTimeoutException:
            assert False, "Timeout"
        assert answer!=b'', "No data received"
        #Store result in a dict
        d =dict()
        print("answer decalee = ", (answer[3] & 1<< relay_number) )
        if (answer[3] & 1<< relay_number) != 0:
            d['Relay ' + str(relay_number)] = 'Open'
        if (answer[3] & 1<< relay_number) == 0:
            d['Relay ' + str(relay_number)] = 'Close'
        return d

    def __baudrate_calculation(self, baudrate:int)->int:
        """Convert explicit baudrate to device understandable number

        Args:
            baudrate (int): baudrate to convert

        Returns:
            int: converted baudrate
        """
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

    def change_device_baudrate(self, new_baudrate:int=9600, new_parity:int=0) ->None:
        """Change the device baudrate and parity
        User as to be carefull using this function as the communication no longer establish after this function is executed.

        Args:
            new_baudrate (int, optional): New baudrate to set. Defaults to 9600.
            new_parity (int, optional): New parity to set. Defaults to 0.
        """
        assert isinstance(new_baudrate, int)
        assert isinstance(new_parity, int)
        assert (new_parity>=0x00 and new_parity<= 0x02)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = self.device_adress
        cmd[1] = SET_BAUDRATE_ADRESS
        cmd[2] = 0x20
        cmd[3] = 0x00
        cmd[4] = new_parity # 0x00: no parity check, 0x01: even parity check, 0x02: odd parity check 
        cmd[5] = self.__baudrate_calculation(new_baudrate) # 0x00 : 4800, 0x01 : 9600, 0x02 : 19200, 0x03 : 38400, 0x04 : 57600, 0x05 : 115200, 0x06 : 128000, 0x07 : 256000
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def change_device_adress(self, new_adress:int) ->None:
        """Change device adress.
        User as to be carefull using this function as the communication no longer establish after this function is executed.

        Args:
            new_adress (int, optional): New device adress to set. Defaults to 0x01.
        """
        assert isinstance(new_adress, int)
        assert (new_adress>=0x01 and new_adress<= 0xFF)
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = BROADCAST_ADRESS
        cmd[1] = SET_BAUDRATE_ADRESS
        cmd[2] = 0x40
        cmd[3] = 0x00
        cmd[4] = 0x00
        cmd[5] = new_adress # Need to be in 0x0X format
        crc = pycrc.ModbusCRC(cmd[0:6])
        cmd[6] = crc & 0xFF
        cmd[7] = crc >> 8
        self.serial_device.write(cmd)

    def read_device_adress(self)->int:
        """Read device adress

        Returns:
            int: Device adress
        """
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = BROADCAST_ADRESS
        cmd[1] = READ_ADRESS_VERSION
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
            assert False, "Timeout"
        assert answer!=b'', "No data received"
        return answer[4]

    def read_device_software_version(self)->float:
        """Read device software version

        Returns:
            int: software version
        """
        cmd = [0,0,0,0,0,0,0,0]
        cmd[0] = BROADCAST_ADRESS
        cmd[1] = READ_ADRESS_VERSION
        cmd[2] = 0x80
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
            assert False, "Timeout"
        assert answer!=b'', "No data received"
        return float(answer[4]/100)
