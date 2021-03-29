from micropython import const
from adafruit_bus_device.spi_device import SPIDevice
import time

# _________________________________________________________________
# |                         Address Bits                          |
# |---------------------------------------------------------------|
# |  ~R/W |   A06 |   A05 |   A04 |   A03 |   A02 |   A01 |   A00 |
# |---------------------------------------------------------------|
# |                           Data Bits                           |
# |---------------------------------------------------------------|
# |   D07 |   D06 |   D05 |   D04 |   D03 |   D02 |   D01 |   D00 |
# -----------------------------------------------------------------

_DS3234_READ_MASK = const(0x7F)
_DS3234_WRITE_MASK = const(0x80)
_DS3234_12HOUR = const(0x40)

_DS3234_SECONDS = const(0x00)  # BCD
_DS3234_MINUTES = const(0x01)  # BCD
_DS3234_HOUR = const(0x02)  # BCD

_DS3234_DAY = const(0x03)
_DS3234_DATE = const(0x04)  # BCD
_DS3234_MONTH = const(0x05)  # BCD
_DS3234_YEAR = const(0x06)  # BCD

_DS3234_ALARM1_SECONDS = const(0x07)  # BCD
_DS3234_ALARM1_MINUTE = const(0x08)  # BCD
_DS3234_ALARM1_HOUR = const(0x09)  # BCD
_DS3234_ALARM1_DAY = const(0x0A)  # BCD

_DS3234_ALARM2_MINUTE = const(0x0B)  # BCD
_DS3234_ALARM2_HOUR = const(0x0C)  # BCD
_DS3234_ALARM2_DAY = const(0x0D)  # BCD

_DS3234_CONTROL_REG = const(0x0E)
_DS3234_STATUS_REG = const(0x0F)

_DS3234_XTAL_OFFSET = const(0x10)

_DS3234_TEMP_MSB = const(0x11)
_DS3234_TEMP_LSB = const(0x12)

_DS3234_DIS_TEMP_CONV = const(0x13)

_DS3234_SRAM_ADDR = const(0x18)
_DS3234_SRAM_DATA = const(0x19)

_DS3234_MAX_SCLK = const(4000000)


def _bcd2bin(value):
    """Convert binary coded decimal to Binary

    :param value: the BCD value to convert to binary (required, no default)
    """
    return value - 6 * (value >> 4)


def _bin2bcd(value):
    """Convert a binary value to binary coded decimal.

    :param value: the binary value to convert to BCD. (required, no default)
    """
    return value + 6 * (value // 10)


class DS3234:
    time_buf = bytearray(8)

    def __init__(self, spi, cs):
        self.spi_device = SPIDevice(spi, cs, baudrate=_DS3234_MAX_SCLK, polarity=0, phase=1)

    @property
    def datetime(self):
        self.time_buf[0] = _DS3234_SECONDS & _DS3234_READ_MASK
        with self.spi_device as spi:
            spi.write_readinto(self.time_buf, self.time_buf)
        return time.struct_time(
            (
                _bcd2bin(self.time_buf[7]) + 2000,
                _bcd2bin(self.time_buf[6]),
                _bcd2bin(self.time_buf[5]),
                _bcd2bin(self.time_buf[3]),
                _bcd2bin(self.time_buf[2]),
                _bcd2bin(self.time_buf[1]),
                (self.time_buf[4] & 0x07),
                -1,
                -1,
            )
        )

    @datetime.setter
    def datetime(self, time):
        self.time_buf[0] = _DS3234_SECONDS | _DS3234_WRITE_MASK
        self.time_buf[1] = _bin2bcd(time[5]) & 0x7F
        self.time_buf[2] = _bin2bcd(time[4])
        self.time_buf[3] = _bin2bcd(time[3])
        self.time_buf[4] = (time[6] & 0x07)
        self.time_buf[5] = _bin2bcd(time[2])
        self.time_buf[6] = _bin2bcd(time[1])
        self.time_buf[7] = _bin2bcd(time[0] - 2000)
        with self.spi_device as spi:
            spi.write(self.time_buf)

