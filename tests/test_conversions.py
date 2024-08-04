#!/usr/bin/env python3

import unittest

import feeph.i2c.conversions as sut  # system under test


class TestConvertUnsignedToBytes(unittest.TestCase):

    def test_convert_to_8bit(self):
        # -----------------------------------------------------------------
        computed = sut.convert_uint_to_bytearry(255, 1)
        expected = bytearray([0xFF])
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_convert_to_16bit(self):
        # -----------------------------------------------------------------
        computed = sut.convert_uint_to_bytearry(32767, 2)
        expected = bytearray([0x7F, 0xFF])
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_convert_to_32bit(self):
        # -----------------------------------------------------------------
        computed = sut.convert_uint_to_bytearry(305419896, 4)
        expected = bytearray([0x12, 0x34, 0x56, 0x78])
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_value_too_small(self):
        # provided value is out of range
        self.assertRaises(ValueError, sut.convert_uint_to_bytearry, -1, 2)

    def test_value_too_big(self):
        # provided value is out of range
        self.assertRaises(ValueError, sut.convert_uint_to_bytearry, 65536, 2)


class TestConvertBytesToUnsigned(unittest.TestCase):

    def test_convert_to_uint8(self):
        # -----------------------------------------------------------------
        computed = sut.convert_bytearry_to_uint(bytearray([0xFF]))
        expected = 255
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_convert_to_uint16(self):
        # -----------------------------------------------------------------
        computed = sut.convert_bytearry_to_uint(bytearray([0x7F, 0xFF]))
        expected = 32767
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_convert_to_uint32(self):
        # -----------------------------------------------------------------
        computed = sut.convert_bytearry_to_uint(bytearray([0x12, 0x34, 0x56, 0x78]))
        expected = 305419896
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)
