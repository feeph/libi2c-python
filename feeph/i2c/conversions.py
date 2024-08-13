#!/usr/bin/env python3
"""
short-lived transmission handler for feeph.i2c

usage:
```
import busio
import feeph.i2c

i2c_bus = busio.I2C(...)

with feeph.i2c.Burst(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
    value = bh.read_register(register)
    bh.write_register(register, value + 1)

with feeph.i2c.Burst(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
    value = bh.get_state()
    bh.set_state(value + 1)
```
"""


def convert_uint_to_bytearry(value: int, byte_count: int) -> bytearray:
    """
    convert unsigned integer to byte array

    ```
      255 -> [0xFF]
    32767 -> [0x7F, 0xFF]
    32768 -> [0x80, 0x00]
    65535 -> [0xFF, 0xFF]
    ```
    """
    min_value = 0
    max_value = pow(256, byte_count) - 1
    if min_value <= value <= max_value:
        buf = bytearray(byte_count)
        for idx in range(byte_count):
            pos = byte_count - 1 - idx
            buf[pos] = (value >> idx * 8) & 0xFF
        return buf
    else:
        raise ValueError("provided value is out of range")


def convert_bytearry_to_uint(ba: bytearray) -> int:
    """
    convert byte array to unsigned integer

    ```
      0xFF ->   255
    0x7FFF -> 32767
    0x8000 -> 32768
    0xFFFF -> 65535
    ```
    """
    byte_count = len(ba)
    value = 0
    for idx in range(byte_count):
        pos = byte_count - 1 - idx
        value += ba[pos] << idx * 8
    return value
