#!/usr/bin/env python3
"""
"""

# modules board and busio provide no type hints
import board  # type: ignore
import busio  # type: ignore

from feeph.i2c.interface import I2cBusInterface


class HardwareI2cBus(I2cBusInterface):

    def __init__(self, scl: board.pin = board.SCL, sda: board.pin = board.SDA):
        self.i2c_bus = busio.I2C(scl=scl, sda=sda)

    def writeto(self, address: int, buffer: bytearray, *, start: int = 0, end: int | None = None):
        self.i2c_bus.writeto(address=address, buffer=buffer, start=start, end=end)

    def writeto_then_readfrom(self, address: int, buffer_out: bytearray, buffer_in: bytearray, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        self.i2c_bus.writeto_then_readfrom(address=address, buffer_out=buffer_out, buffer_in=buffer_in, out_start=out_start, out_end=out_end, in_start=in_start, in_end=in_end, stop=stop)


class SimulatedI2cBus(I2cBusInterface):
    """
    simulate an I²C bus

    This simulation is useful to ensure the right values are read and written.
    It is unable to simulate device-specific behavior! (e.g. duplicated registers)
    """

    def __init__(self, state: dict[int, dict[int, int]]):
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

    def writeto(self, address, buffer, *, start=0, end=None):
        i2c_device_address  = address
        i2c_device_register = buffer[0]
        self._state[i2c_device_address][i2c_device_register] = buffer[1]

    def writeto_then_readfrom(self, address: int, buffer_out: bytearray, buffer_in: bytearray, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        i2c_device_address  = address
        i2c_device_register = buffer_out[0]
        buffer_in[0] = self._state[i2c_device_address][i2c_device_register]
