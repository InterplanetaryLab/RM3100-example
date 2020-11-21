import logging
from spi_dev import Spi_Dev

log = logging.getLogger(__name__)

def twos_comp(val, bits):
    if (val & (1 << (bits-1))) != 0:
        val = val - (1 <<bits)
    return val
class QRM3100(object):

    QRM3100_CMM = 0x01
    QRM3100_CCXMSB = 0x04
    QRM3100_CCXLSB = 0x05
    QRM3100_CCYMSB = 0x06
    QRM3100_CCYLSB = 0x07
    QRM3100_CCZMSB = 0x08
    QRM3100_CCZLSB = 0x09
    QRM3100_NOS_REG = 0x0A
    QRM3100_TMRC = 0x0B
    QRM3100_MX2 = 0xA4
    QRM3100_MX1 = 0xA5
    QRM3100_MX0 = 0xA6
    QRM3100_MY2 = 0xA7
    QRM3100_MY1 = 0xA8
    QRM3100_MY0 = 0xA9
    QRM3100_MZ2 = 0xAA
    QRM3100_MZ1 = 0xAB
    QRM3100_MZ0 = 0xAC
    QRM3100_STATUS_REG = 0xB4
    QRM3100_I2C_ADDRESS = 0x20
    QRM3100_POLL = 0x00
    QRM3100_STATUS = 0x34

    CALIBRATION_TIMEOUT = 5000
    DEG_PER_RAD = 180.0/3.14159265358979

    def __init__(self, spi=None):
        self.spi = spi

    def measure(self, address):
        res = self.spi.readRegister(address)
        return res
    def initcmm(self):
        self.spi.writeRegister(self.QRM3100_CMM, (0x70|0x08|0x01))
    def read_x(self):
        lower = self.measure(self.QRM3100_MX0)
        mid = self.measure(self.QRM3100_MX1)
        upper = self.measure(self.QRM3100_MX2)
        return twos_comp((lower + (mid <<8) + (upper<<16)),24)
    def read_y(self):
        lower = self.measure(self.QRM3100_MY0)
        mid = self.measure(self.QRM3100_MY1)
        upper = self.measure(self.QRM3100_MY2)
        return twos_comp((lower + (mid <<8) + (upper<<16)),24)
    def read_z(self):
        lower = self.measure(self.QRM3100_MZ0)
        mid = self.measure(self.QRM3100_MZ1)
        upper = self.measure(self.QRM3100_MZ2)
        return twos_comp((lower + (mid <<8) + (upper<<16)),24)

if __name__ == "__main__":
    port = 0
    device = 1
    spi = Spi_Dev(port, device)
    rm3100 = QRM3100(spi)
    rm3100.initcmm()
    try:
        while True:
            print("status: ")
            print(rm3100.measure(rm3100.QRM3100_STATUS))
            print("\n")
            print("x measurement: ")
            print(rm3100.read_x())
            print("\n")
            print("y measurement: ")
            print(rm3100.read_y())
            print("\n")
            print("z measurement: ")
            print(rm3100.read_z())
            print("\n")
    except KeyboardInterrupt:
        print("Press CTRL-C to terminate")
        pass

