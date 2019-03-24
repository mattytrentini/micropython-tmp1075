from machine import I2C
from micropython import const

class Tmp1075:

    '''
    MicroPython Driver for the TI TMP1075 temperature sensor.

    Example:

        i2c = I2C(sda=Pin(33), scl=Pin(32), freq=133000)
        tmp1075 = Tmp1075(i2c)
        tmp1075.get_temperature()

    See datasheet: http://www.ti.com/lit/ds/symlink/tmp1075.pdf
    
    '''
    REG_TEMP = const(0x00)
    REG_CFGR = const(0x01)
    REG_LLIM = const(0x02)
    REG_HLIM = const(0x03)
    REG_DIEID = const(0x0F)
        
    def __init__(self, i2c=None, addr=0x48):
        # Could check that addr is one of the valid values...
        if not i2c:
            raise ValueError('I2C object needed')
        self._i2c = i2c
        self._addr = addr			  
        self._check_device()

    def _check_device(self):
        ''' Check basic comms; DIE ID should always be 0x7500 '''
        id = self._i2c.readfrom_mem(self._addr, Tmp1075.REG_DIEID, 2)
        if (id[0] << 8 + id[1]) != 0x7500:
            raise ValueError('Incorrect DIE ID (expect 0x7500) or bad I2C comms')
        # Throw exception if DIE ID isn't 0x7500
        # Could also check to ensure self._addr is a valid address.

    def get_temperature(self):
        # return temperature in degrees Celcius
        # Retrieve temp on demand? Check how long since the last read?
        # Make it a property?
        # Read from I2C only if it hasn't been read for some time?
        # Allow a conversion function?
        # Works for negative numbers?
        t = self._i2c.readfrom_mem(self._addr, Tmp1075.REG_TEMP, 2)
        return ((t[0] << 4) + (t[1] >> 4)) * 0.0625
        