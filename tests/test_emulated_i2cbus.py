#!/usr/bin/env python3
"""
perform I²C bus related tests
"""

import unittest

import feeph.i2c as sut  # sytem under test


class TestEmulatedI2C(unittest.TestCase):

    def test_read_device_register(self):
        state = {
            0x4C: {
                0x00: 0x12,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        computed = sut.read_device_register(i2c_bus, 0x4C, 0x00)
        expected = 0x12
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_read_device_registers(self):
        state = {
            0x4C: {
                0x01: 0x12,
                0x10: 0x23,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        computed = sut.read_device_registers(i2c_bus, [(0x4C, 0x01, 1), (0x4C, 0x10, 1)])
        expected = [0x12, 0x23]
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_read_device_registers_congested(self):
        state = {
            0x4C: {
                0x01: 0x12,
                0x10: 0x23,
            },
        }
        # simulating an extremely busy I²C bus
        # (there's a 1 percent chance to successfully lock the bus)
        i2c_bus = sut.EmulatedI2C(state=state, lock_chance=1)
        # -----------------------------------------------------------------
        computed = sut.read_device_registers(i2c_bus, [(0x4C, 0x01, 1), (0x4C, 0x10, 1)])
        expected = [0x12, 0x23]
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_write_device_register(self):
        state = {
            0x4C: {
                0x00: 0x00,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        sut.write_device_register(i2c_bus, 0x4C, 0x00, 0x12)
        computed = i2c_bus._state[0x4C]
        expected = {0x00: 0x12}
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_write_device_registers(self):
        state = {
            0x4C: {
                0x01: 0x00,
                0x10: 0x00,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        sut.write_device_registers(i2c_bus, [(0x4C, 0x01, 1, 0x12), (0x4C, 0x10, 1, 0x34)])
        computed = i2c_bus._state[0x4C]
        expected = {0x01: 0x12, 0x10: 0x34}
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_write_device_registers_congested(self):
        # simulating an extremely busy I²C bus
        # (there's a 1 percent chance to successfully lock the bus)
        state = {
            0x4C: {
                0x01: 0x00,
                0x10: 0x00,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state, lock_chance=1)
        # -----------------------------------------------------------------
        sut.write_device_registers(i2c_bus, [(0x4C, 0x01, 1, 0x12), (0x4C, 0x10, 1, 0x34)])
        computed = i2c_bus._state[0x4C]
        expected = {0x01: 0x12, 0x10: 0x34}
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)
