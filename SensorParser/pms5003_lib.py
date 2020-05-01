import struct
import serial
import time

MODE_PASSIVE = [0x42, 0x4D, 0xE1, 0x00, 0x00, 0x01, 0x70]
MODE_ACTIVE = [0x42, 0x4D, 0xE1, 0x00, 0x01, 0x01, 0x71]
READ_PASSIVE = [0x42, 0x4D, 0xE2, 0x00, 0x00, 0x01, 0x71]
SLEEP = [0x42, 0x4D, 0xE4, 0x00, 0x00, 0x01, 0x73]
WAKEUP = [0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74]

_PMS5003_COMMANDS = (
    MODE_PASSIVE,
    MODE_ACTIVE,
    READ_PASSIVE,
    SLEEP,
    WAKEUP
)

_PMS5003_MODES = (
    MODE_PASSIVE,
    MODE_ACTIVE,
)

_PMS5003_STATES = (
    SLEEP,
    WAKEUP
)


# https://learn.adafruit.com/pm25-air-quality-sensor/python-and-circuitpython

class PMS5003(object):
    def __init__(self, port="/dev/serial0"):
        self.uart = serial.Serial(port, baudrate=9600, timeout=0.25)

        self._mode = MODE_ACTIVE
        self._send_command(self._mode)

        self._state = WAKEUP
        self._send_command(self._state)

        self._PM10 = None
        self._PM25 = None
        self._PM100 = None

        self._PM10_ENV = None
        self._PM25_ENV = None
        self._PM100_ENV = None

        self._PART_03 = None
        self._PART_05 = None
        self._PART_10 = None
        self._PART_25 = None
        self._PART_50 = None
        self._PART_100 = None

    def _send_command(self, cmd):
        if cmd not in _PMS5003_COMMANDS:
            raise ValueError("Unknown command: {}".format(cmd))

        self.uart.write(cmd)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode not in _PMS5003_MODES:
            raise ValueError("Unknown mode: {}".format(mode))

        self._mode = mode
        self._send_command(self._mode)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state not in _PMS5003_STATES:
            raise ValueError("Unknown state: {}".format(state))

        self._state = state
        self._send_command(self._state)

        if self._state is WAKEUP:
            time.sleep(32)

    def read(self):
        sleep_back = False

        if self._state == SLEEP:
            self._state = WAKEUP
            self._send_command(self._state)
            sleep_back = True

        if self._mode == MODE_PASSIVE:
            self._send_command(READ_PASSIVE)

        data = self.uart.read(32)
        # data = bytes.fromhex("424D001C003E00540060002A003E0050222309A4014A0028000600056700042C")

        data = list(data)

        if len(data) == 0:
            raise RuntimeError("Data read error: {}".format("empty buffer"))

        if len(data) > 32:
            raise RuntimeError("Data read error: {}".format("oversized buffer"))

        if data[0] != 0x42 or data[1] != 0x4D:
            raise RuntimeError("Data read error: {}".format("inital data error"))

        frame_len = struct.unpack(">H", bytes(data[2:4]))[0]

        if frame_len != 28:
            raise RuntimeError("Data read error: {}".format("size field error"))

        frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(data[4:]))

        self._PM10, self._PM25, self._PM100, self._PM10_ENV, self._PM25_ENV, self._PM100_ENV, \
            self._PART_03, self._PART_05, self._PART_10, self._PART_25, self._PART_50, \
            self._PART_100, reserved, crc = frame

        crc1 = sum(data[0:30])

        if crc != crc1:
            raise RuntimeError("Data read error: {}".format("checksum error"))

        if sleep_back:
            self._state = SLEEP
            self._send_command(self._state)

    @property
    def pm10(self):
        return self._PM10

    @property
    def pm25(self):
        return self._PM25

    @property
    def pm100(self):
        return self._PM100

    @property
    def pm10_env(self):
        return self._PM10_ENV

    @property
    def pm25_env(self):
        return self._PM25_ENV

    @property
    def pm100_env(self):
        return self._PM100_ENV

    @property
    def part_03(self):
        return self._PART_03

    @property
    def part_05(self):
        return self._PART_05

    @property
    def part_10(self):
        return self._PART_10

    @property
    def part_25(self):
        return self._PART_25

    @property
    def part_50(self):
        return self._PART_50

    @property
    def part_100(self):
        return self._PART_100
