#!/usr/bin/env python3
"""
"""

import random

# module busio provide no type hints
import busio  # type: ignore
from feeph.i2c.conversions import convert_bytearry_to_uint, convert_uint_to_bytearry


class EmulatedI2C(busio.I2C):
    """
    emulate an I²C bus (drop-in replacement for busio.I2C)

    This emulation is useful to ensure the right values are read and
    written and test scenarios where it's hard or even impossible to
    acquire a lock on the I²C bus.

    This code is unable to simulate device-specific behavior!
    (e.g. duplicated registers with multiple addresses)
    """

    def __init__(self, state: dict[int, dict[int, int]], lock_chance: int = 100):
        """
        initialize a simulated I2C bus

        ```
        state = {
            <device>: {
                <register>: <value>,
            }
        }
        ```
        """
        self._state = state.copy()
        self._lock_chance = lock_chance
        random.seed()

    def try_lock(self) -> bool:
        # may randomly fail to acquire a lock
        return (random.randint(0, 100) < self._lock_chance)

    def unlock(self):
        pass

    # We're going to use '-1' as a magic marker that the device state is
    # being read/written since the register address must be positive in the
    # range 0 ≤ x ≤ 255.

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """
        read device state

        (buffer is used as an output parameter)
        """
        i2c_device_address  = address
        i2c_device_register = -1
        value = self._state[i2c_device_address][i2c_device_register]
        ba = convert_uint_to_bytearry(value, len(buffer))
        # copy computed result to output parameter
        for i in range(len(buffer)):
            buffer[i] = ba[i]

    def writeto(self, address: int, buffer: bytearray, *, start=0, end=None):
        """
        write device state or register
        """
        if len(buffer) == 1:
            # device status
            i2c_device_address  = address
            i2c_device_register = -1
            value = buffer[0]
        else:
            # device register
            i2c_device_address  = address
            i2c_device_register = buffer[0]
            if i2c_device_register < 0:
                raise ValueError("device register can't be negative")
            value = convert_bytearry_to_uint(buffer[1:])
        self._state[i2c_device_address][i2c_device_register] = value

    def writeto_then_readfrom(self, address: int, buffer_out: bytearray, buffer_in: bytearray, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        """
        read device register

        (buffer_in is used as an output parameter)
        """
        i2c_device_address  = address
        i2c_device_register = buffer_out[0]
        if i2c_device_register < 0:
            raise ValueError("device register can't be negative")
        value = self._state[i2c_device_address][i2c_device_register]
        ba = convert_uint_to_bytearry(value, len(buffer_in))
        # copy computed result to output parameter
        for i in range(len(buffer_in)):
            buffer_in[i] = ba[i]
