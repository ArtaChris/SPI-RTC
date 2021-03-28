from micropython import const
from adafruit_bus_device.spi_device import SPIDevice

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
_DS3234_WRITE_MASK = const(0xFF)
_DS3234_12HOUR = const(0x40)

_DS3234_SECONDS = const(0x00) # BCD
_DS3234_MINUTES = const(0x01) # BCD
_DS3234_HOUR = const(0x02) # BCD

_DS3234_DAY = const(0x03)
_DS3234_DATE = const(0x04) # BCD
_DS3234_MONTH = const(0x05) # BCD
_DS3234_YEAR = const(0x06) # BCD

_DS3234_ALARM1_SECONDS = const(0x07) # BCD
_DS3234_ALARM1_MINUTE = const(0x08) # BCD
_DS3234_ALARM2_HOUR = const(0x09) # BCD
_DS3234_ALARM1_DAY = const(0x0A) # BCD

_DS3234_ALARM2_MINUTE = const(0x0B)
_DS3234_ALARM2_HOUR = const(0x0C)
_DS3234_ALARM2_DAY = const(0x0D)

_DS3234_CONTROL_REG = const(0x0E)
_DS3234_STATUS_REG = const(0x0F)

_DS3234_XTAL_OFFSET = const(0x10)

_DS3234_TEMP_MSB = const(0x11)
_DS3234_TEMP_LSB = const(0x12)

_DS3234_DIS_TEMP_CONV = const(0x13)

_DS3234_SRAM_ADDR = const(0x18)
_DS3234_SRAM_DATA = const(0x19)

_DS3234_MAX_SCLK = const(4000000)

class DS3234:
    def __init__(self, spi, cs)
        self.spi_device = SPIDevice(spi, cs, baudrate=_DS3234_MAX_SCLK, polarity=0, phase=1)
