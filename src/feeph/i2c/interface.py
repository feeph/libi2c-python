#!/usr/bin/env python3
"""
"""

from abc import ABC, abstractmethod


class I2cBusInterface(ABC):
    """
    interface definition for I2cBus

    This abstract base class ensures that I2cBus and SimulatedI2cBus
    share exactly the same interface.
    """

    @abstractmethod
    def writeto(self, address: int, buffer: bytearray, *, start: int = 0, end: int | None = None):
        """
        The method's signature was copied from adafruit's "busio.I2C". Keep exactly as is!
        """
        pass

    @abstractmethod
    def writeto_then_readfrom(self, address: int, buffer_out: bytearray, buffer_in: bytearray, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        """
        The method's signature was copied from adafruit's "busio.I2C". Keep exactly as is!
        """
        pass
