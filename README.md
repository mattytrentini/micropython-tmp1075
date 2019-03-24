# micropython-tmp1075
A MicroPython driver for the [TI TMP1075 temperature sensor](http://www.ti.com/product/TMP1075)

Currently only supports querying of the temperature. 

## Usage

```python
    i2c = I2C(sda=Pin(33), scl=Pin(32), freq=133000)
    tmp1075 = Tmp1075(i2c)
    tmp1075.get_temperature()
```

## Unit tests

Expects the MicroPython [unittest](https://github.com/micropython/micropython-lib/tree/master/unittest) module to be installed.

```python
    import unittest
    unittest.main('test_tmp1075')
```