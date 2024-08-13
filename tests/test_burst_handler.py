#!/usr/bin/env python3
"""
perform I²C bus related tests
"""

import unittest

import feeph.i2c as sut  # sytem under test


# pylint: disable=protected-access,too-many-public-methods
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

    def test_read_device_register_multibyte(self):
        state = {
            0x4C: {
                0x00: 0x1234,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            computed = bh.read_register(0x00, byte_count=2)
        expected = 0x1234
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_read_device_register_insufficient_tries(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            # under realistic circumstances the max_tries would be a positive
            # value but we're intentionally setting it to 0 to force an error
            self.assertRaises(RuntimeError, bh.read_register, 0x00, max_tries=0)

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

    def test_write_device_register_multibyte(self):
        state = {
            0x4C: {
                0x00: 0x0000,
            },
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            bh.write_register(register=0x00, value=0x1234, byte_count=2)
        computed = i2c_bus._state[0x4C]
        expected = {0x00: 0x1234}
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_write_device_register_insufficient_tries(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            # under realistic circumstances the max_tries would be a positive
            # value but we're intentionally setting it to 0 to force an error
            self.assertRaises(RuntimeError, bh.write_register, 0x00, value=0x12, max_tries=0)

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
            0x70: {-1: 0x01},
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
            computed = bh.get_state()
        expected = 0x01
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_get_state_multibyte(self):
        state = {
            0x70: {-1: 0x01},
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
            computed = bh.get_state(byte_count=2)
        expected = 0x01  # byte count was ignored
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_get_state_insufficient_tries(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            # under realistic circumstances the max_tries would be a positive
            # value but we're intentionally setting it to 0 to force an error
            self.assertRaises(RuntimeError, bh.get_state, max_tries=0)

    def test_set_state(self):
        state = {
            0x70: {-1: 0x00},
        }
        i2c_bus = sut.EmulatedI2C(state=state)
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
            bh.set_state(value=0x01)
        computed = i2c_bus._state[0x70]
        expected = {-1: 0x01}
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_set_state_multibyte(self):
        i2c_bus = sut.EmulatedI2C(state={0x70: {-1: 0x00}})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
            self.assertRaises(ValueError, bh.set_state, value=0x0102, byte_count=2)

    def test_set_state_insufficient_tries(self):
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
            # under realistic circumstances the max_tries would be a positive
            # value but we're intentionally setting it to 0 to force an error
            self.assertRaises(RuntimeError, bh.set_state, value=0x12, max_tries=0)

    # ---------------------------------------------------------------------

    def test_invalid_device_address(self):
        # this code tests the equivalent of:
        # with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0xFFFF) as bh:
        #     ...
        i2c_bus = sut.EmulatedI2C(state={})
        bh = sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0xFFFF)
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(ValueError, bh.__enter__)

    def test_invalid_device_register(self):
        # this code tests the equivalent of:
        # with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0xFFFF) as bh:
        #     ...
        i2c_bus = sut.EmulatedI2C(state={})
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
            self.assertRaises(ValueError, bh.read_register, register=0xFFFF)

    def test_invalid_timeout(self):
        # this code tests the equivalent of:
        # with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C, timeout_ms=0) as bh:
        #     ...
        i2c_bus = sut.EmulatedI2C(state={}, lock_chance=1)
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(ValueError, sut.BurstHandler, i2c_bus=i2c_bus, i2c_adr=0x4C, timeout_ms=0)

    def test_hard_to_lock(self):
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

    def test_unable_to_lock(self):
        # this code tests the equivalent of:
        # with sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
        #     ...
        i2c_bus = sut.EmulatedI2C(state={}, lock_chance=0)  # impossible to acquire a lock
        bh = sut.BurstHandler(i2c_bus=i2c_bus, i2c_adr=0x4C)
        # -----------------------------------------------------------------
        # -----------------------------------------------------------------
        self.assertRaises(RuntimeError, bh.__enter__)
