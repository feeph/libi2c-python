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

    def readinto(self, buffer, *, start: int = 0, end: int | None = None):
        # provided to ensure we will never call `I2C.readinto()`
        raise RuntimeError("EmulatedI2cBus.readinto() is not implemented")

    def writeto(self, address, buffer, *, start=0, end=None):
        i2c_device_address  = address
        i2c_device_register = buffer[0]
        self._state[i2c_device_address][i2c_device_register] = buffer[1]

    def writeto_then_readfrom(self, address: int, buffer_out: bytearray, buffer_in: bytearray, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        i2c_device_address  = address
        i2c_device_register = buffer_out[0]
        buffer_in[0] = self._state[i2c_device_address][i2c_device_register]