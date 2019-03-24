import unittest
from tmp1075 import Tmp1075

class FakeI2C:
    ''' Replace the 'real' I2C with a mock object.

    Note: Only necessary because MicroPython doesn't yet have a mock library...
    '''

    def __init__(self):
        self.register_values = {}
    
    def register(self, reg, values):
        self.register_values[reg] = (values).to_bytes(2, 'big')

    def readfrom_mem(self, addr, register, bytes_to_read):
        if register not in self.register_values:
            raise ValueError('Register not known')  # fixme: Which register
        if len(self.register_values[register]) != bytes_to_read:
            raise ValueError('Unexpected length')  # fixme: Improve error report
        return self.register_values[register]

class TestTemperatureConversions(unittest.TestCase):
    ''' To run at the REPL:

        import unittest
        unittest.main('test_tmp1075')
    '''

    def testDatasheetPositiveNumbers(self):

        # Should be able to use a TestSuite

        fake = FakeI2C()
        with self.assertRaises(ValueError):
            # Should fail if DIE ID is not 0x7500
            tmp1075 = Tmp1075(fake)
        fake.register_values[Tmp1075.REG_DIEID] = bytes([0x75, 0x00])
        tmp1075 = Tmp1075(fake)

        #fake.register(Tmp1075.REG_DIEID, 0x0000)
        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x00, 0x00])
        self.assertAlmostEqual(tmp1075.get_temperature(), 0)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x00, 0x10])
        self.assertAlmostEqual(tmp1075.get_temperature(), 0.0625)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x00, 0x40])
        self.assertAlmostEqual(tmp1075.get_temperature(), 0.25)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x19, 0x00])
        self.assertAlmostEqual(tmp1075.get_temperature(), 25)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x32, 0x00])
        self.assertAlmostEqual(tmp1075.get_temperature(), 50)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x4B, 0x00])
        self.assertAlmostEqual(tmp1075.get_temperature(), 75)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x50, 0x00])
        self.assertAlmostEqual(tmp1075.get_temperature(), 80)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x64, 0x00])
        self.assertAlmostEqual(tmp1075.get_temperature(), 100)

        fake.register_values[Tmp1075.REG_TEMP] = bytes([0x7F, 0xF0])
        self.assertAlmostEqual(tmp1075.get_temperature(), 127.9375)

        
if __name__ == '__main__':
    unittest.main()
