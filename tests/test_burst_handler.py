#!/usr/bin/env python3
"""
perform I²C bus related tests
"""

import unittest

import feeph.i2c as sut  # sytem under test


class TestBurstHandler(unittest.TestCase):

    def test_read_device_register(self):
        state = {
            0x4C: {
                0x00: 0x12,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            computed = bh.read_register(0x00)
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
        computed = list()
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            computed.append(bh.read_register(0x01))
            computed.append(bh.read_register(0x10))
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
        computed = list()
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            computed.append(bh.read_register(0x01))
            computed.append(bh.read_register(0x10))
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
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            bh.write_register(register=0x00, value=0x12)
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
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            bh.write_register(register=0x01, value=0x12)
            bh.write_register(register=0x10, value=0x34)
        computed = i2c_bus._state[0x4C]
        expected = {0x01: 0x12, 0x10: 0x34}
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_write_device_registers_congested(self):
        state = {
            0x4C: {
                0x01: 0x00,
                0x10: 0x00,
            },
        }
        # simulating an extremely busy I²C bus
        # (there's a 1 percent chance to successfully lock the bus)
        i2c_bus = sut.EmulatedI2C(state=state, lock_chance=1)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            bh.write_register(register=0x01, value=0x12)
            bh.write_register(register=0x10, value=0x34)
        computed = i2c_bus._state[0x4C]
        expected = {0x01: 0x12, 0x10: 0x34}
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_mixed_access(self):
        state = {
            0x4C: {
                0x00: 0x12,
                0x01: 0x00,
                0x10: 0x00,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            computed_r = bh.read_register(0x00)
            bh.write_register(register=0x01, value=0x34)
            bh.write_register(register=0x10, value=0x56)
        expected_r = 0x12
        computed_w = i2c_bus._state[0x4C]
        expected_w = {0x00: 0x12, 0x01: 0x34, 0x10: 0x56}
        # -----------------------------------------------------------------
        self.assertEqual(computed_r, expected_r)
        self.assertEqual(computed_w, expected_w)

    # ---------------------------------------------------------------------

    def test_get_state(self):
        state = {
            0x70: 0x01,
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
            computed = bh.get_state()
        expected = 0x01
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_set_state(self):
        state = {
            0x70: 0x00,
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
            bh.set_state(value=0x01)
        computed = i2c_bus._state[0x70]
        expected = 0x01
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    # ---------------------------------------------------------------------

    def test_no_timeout(self):
        state = {
            0x4C: {
                0x00: 0x12,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state, lock_chance=1)
        # -----------------------------------------------------------------
        # simulating an extremely busy I²C bus
        # (there's a 1 percent chance to successfully lock the bus)
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C, timeout_ms=None) as bh:
            computed = bh.read_register(0x00)
        expected = 0x12
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)
