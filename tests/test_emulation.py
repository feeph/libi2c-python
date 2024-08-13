#!/usr/bin/env python3
"""
perform I²C bus related tests
"""

import unittest

import feeph.i2c as sut  # sytem under test


# pylint: disable=protected-access
class TestEmulatedI2C(unittest.TestCase):

    def test_input_validation1(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(ValueError, i2c_bus.readfrom_into, 0x12, [-1, 0x00])

    def test_input_validation2(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(ValueError, i2c_bus.writeto, 0x12, [-1, 0x00])

    def test_input_validation3(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(ValueError, i2c_bus.writeto_then_readfrom, 0x12, bytearray(0), [-1, 0x00])

    def test_input_validation4(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(ValueError, i2c_bus.writeto_then_readfrom, 0x12, [-1, 0x00], bytearray(0))
