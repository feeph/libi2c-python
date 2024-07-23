#!/usr/bin/env python3
"""
"""

import random

# module busio provide no type hints
import busio  # type: ignore


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
        """
        i2c_device_address  = address
        i2c_device_register = -1
        buffer[0] = self._state[i2c_device_address][i2c_device_register]

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
            value = buffer[1]
        self._state[i2c_device_address][i2c_device_register] = value

    def writeto_then_readfrom(self, address: int, buffer_out: bytearray, buffer_in: bytearray, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        """
        read device register
        """
        i2c_device_address  = address
        i2c_device_register = buffer_out[0]
        if i2c_device_register < 0:
            raise ValueError("device register can't be negative")
        buffer_in[0] = self._state[i2c_device_address][i2c_device_register]
