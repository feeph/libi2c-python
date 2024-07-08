#!/usr/bin/env python3
"""
perform I²C bus related tests
"""

import unittest

import feeph.i2c.bus as sut  # sytem under test


class TestSimulatedI2cBus(unittest.TestCase):

    def test_read_singlebyte_register(self):
        registers = {
            0x00: 0x12,
            0x01: 0x23,
        }
        i2c_adr = 0x4C
        i2c_bus = sut.SimulatedI2cBus(state={i2c_adr: registers})
        buf_r = bytearray(1)
        buf_r[0] = 0x00
        # -----------------------------------------------------------------
        buf_w = bytearray(1)
        i2c_bus.writeto_then_readfrom(address=i2c_adr, buffer_out=buf_r, buffer_in=buf_w)
        computed = buf_w[0]
        expected = 0x12
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_write_singlebyte_register(self):
        registers = {
        }
        i2c_adr = 0x4C
        i2c_bus = sut.SimulatedI2cBus(state={i2c_adr: registers})
        # -----------------------------------------------------------------
        buf = bytearray(2)
        buf[0] = 0x00  # address
        buf[1] = 0x12  # value
        i2c_bus.writeto(address=i2c_adr, buffer=buf)
        computed = i2c_bus._state[i2c_adr][0x00]
        expected = 0x12
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)
