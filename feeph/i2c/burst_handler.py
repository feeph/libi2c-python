#!/usr/bin/env python3
"""
short-lived transmission handler for feeph.i2c

usage:
```
import busio
import feeph.i2c

i2c_bus = busio.I2C(...)

with feeph.i2c.Burst(i2c_bus=i2c_bus, i2c_adr=0x4C) as bh:
    value = bh.read_register(register)
    bh.write_register(register, value + 1)

with feeph.i2c.Burst(i2c_bus=i2c_bus, i2c_adr=0x70) as bh:
    value = bh.get_state()
    bh.set_state(value + 1)
```
"""

import logging
import time

# module busio provides no type hints
import busio  # type: ignore
from feeph.i2c.conversions import convert_bytearry_to_uint, convert_uint_to_bytearry

LH = logging.getLogger("i2c")


class BurstHandle:
    """
    internal abstraction - !! do not instantiate !!

    Please use `feeph.i2c.BurstHandler() instead`.
    """

    def __init__(self, i2c_bus: busio.I2C, i2c_adr: int):
        self._i2c_bus = i2c_bus
        if 0 <= i2c_adr <= 255:
            self._i2c_adr = i2c_adr
        else:
            raise ValueError(f"Provided I²C address {i2c_adr} is out of range! (allowed range: 0 ≤ x ≤ 255)")

    # fundamentally there isn't actually much difference between accesses
    # to a device's register or internal state
    #
    #    read from register        write to register
    # 1. write one byte            write one byte          (device address)
    # 2. write one byte            write one byte          (register address)
    # 2. read one or more bytes    write one or more bytes (register value)
    #
    # step 2. is skipped when accessing the internal state,
    # step 1. and 3. are kept

    def read_register(self, register: int, byte_count: int = 1, max_tries: int = 5) -> int:
        """
        read a single register from I²C device identified by `i2c_adr` and
        return its contents as an integer value
        - may raise a RuntimeError if it was not possible to acquire
            the bus within allowed time
        - may raise a RuntimeError if there were too many errors
        """
        _validate_register_address(register)
        buf_r = bytearray(byte_count)
        buf_r[0] = register
        buf_w = bytearray(byte_count)
        cur_try = 0
        for cur_try in range(1, 1 + max_tries):
            try:
                self._i2c_bus.writeto_then_readfrom(address=self._i2c_adr, buffer_out=buf_r, buffer_in=buf_w)
                return convert_bytearry_to_uint(buf_w)
            # protect against sporadic errors on actual devices
            # (maybe we can do something to prevent these errors?)
            except (OSError, RuntimeError) as e:
                # [Errno 121] Remote I/O error
                LH.warning("[%s] Unable to read register 0x%02X (%i/%i): %s", __name__, register, cur_try, max_tries, e)
                time.sleep(0.001)
        raise RuntimeError(f"Unable to read register 0x{register:02X} after {cur_try} attempts. Giving up.")

    def write_register(self, register: int, value: int, byte_count: int = 1, max_tries: int = 3):
        """
        write a single register to I²C device identified by `i2c_adr`
          - may raise a ValueError if I²C address is out of range
          - may raise a ValueError if the provided value is out of range
          - may raise a RuntimeError if it was not possible to acquire
            the bus within allowed time
          - may raise a RuntimeError if there were too many errors
        """
        _validate_register_address(register)
        ba = convert_uint_to_bytearry(value, byte_count)
        buf = bytearray([register])
        for byte in ba:
            buf.append(byte)
        cur_try = 0
        for cur_try in range(1, 1 + max_tries):
            try:
                self._i2c_bus.writeto(address=self._i2c_adr, buffer=buf)
                return
            # protect against sporadic errors on actual devices
            # (maybe we can do something to prevent these errors?)
            except (OSError, RuntimeError) as e:
                # [Errno 121] Remote I/O error
                LH.warning("[%s] Unable to write register 0x%02X (%i/%i): %s", __name__, register, cur_try, max_tries, e)
                time.sleep(0.1)
        raise RuntimeError(f"Unable to read register 0x{register:02X} after {cur_try} attempts. Giving up.")

    # it is unclear if it's possible to have a multi-byte state registers
    # (a register write looks exactly like a multi-byte state write)

    def get_state(self, byte_count: int = 1, max_tries: int = 5) -> int:
        """
        get current state of I²C device identified by `i2c_adr` and
        return its contents as an integer value
        - may raise a RuntimeError if it was not possible to acquire
            the bus within allowed time
        - may raise a RuntimeError if there were too many errors
        """
        if byte_count > 1:
            LH.warning("Multi byte reads are not implemented yet! Returning a single byte instead.")
            byte_count = 1
        buf = bytearray(byte_count)
        cur_try = 0
        for cur_try in range(1, 1 + max_tries):
            try:
                self._i2c_bus.readfrom_into(address=self._i2c_adr, buffer=buf)
                return buf[0]
            # protect against sporadic errors on actual devices
            # (maybe we can do something to prevent these errors?)
            except (OSError, RuntimeError) as e:
                # [Errno 121] Remote I/O error
                LH.warning("[%s] Unable to read state (%i/%i): %s", __name__, cur_try, max_tries, e)
                time.sleep(0.001)
        raise RuntimeError(f"Unable to read state after {cur_try} attempts. Giving up.")

    def set_state(self, value: int, byte_count: int = 1, max_tries: int = 3):
        """
        set current state of I²C device identified by `i2c_adr`
        - may raise a RuntimeError if it was not possible to acquire
            the bus within allowed time
        - may raise a RuntimeError if there were too many errors
        """
        if byte_count > 1:
            LH.warning("Multi byte writes are not implemented yet! Returning a single byte instead.")
            byte_count = 1
        buf = convert_uint_to_bytearry(value, byte_count)
        cur_try = 0
        for cur_try in range(1, 1 + max_tries):
            try:
                self._i2c_bus.writeto(address=self._i2c_adr, buffer=buf)
                return
            # protect against sporadic errors on actual devices
            # (maybe we can do something to prevent these errors?)
            except (OSError, RuntimeError) as e:
                # [Errno 121] Remote I/O error
                LH.warning("[%s] Unable to write state (%i/%i): %s", __name__, cur_try, max_tries, e)
                time.sleep(0.1)
        raise RuntimeError(f"Unable to write state after {cur_try} attempts. Giving up.")


class BurstHandler:
    """
    a short-lived I/O operation on the I²C bus

    Technically speaking this I/O operation could span multiple devices
    but we're making an design choice and assume a single device is being
    used. This simplifies the user interface.
    """

    def __init__(self, i2c_bus: busio.I2C, i2c_adr: int, timeout_ms: int | None = 500):
        self._i2c_bus = i2c_bus
        self._i2c_adr = i2c_adr
        if timeout_ms is None:
            self._timeout_ms = None
        elif isinstance(timeout_ms, int) and timeout_ms > 0:
            self._timeout_ms = timeout_ms
        else:
            raise ValueError("Provided timeout is not a positive integer or 'None'!")
        # register '_timestart_ns' - we will populate it later on
        self._timestart_ns = 0

    def __enter__(self) -> BurstHandle:
        """
        Try to acquire a lock for exclusive access on the I²C bus.

        Raises a RuntimeError if it wasn't possible to acquire the lock
        within the given timeout.
        """
        LH.debug("[%d] Initializing an I²C I/O burst.", id(self))
        # 0.001         = 1 millisecond
        # 0.000_001     = 1 microsecond
        # 0.000_000_001 = 1 nanosecond
        self._timestart_ns = time.perf_counter_ns()
        sleep_time = 0.001  # 1 millisecond
        if self._timeout_ms is not None:
            timeout_ns = self._timeout_ms * 1000 * 1000
            deadline = time.monotonic_ns() + timeout_ns
            while not self._i2c_bus.try_lock():
                if time.monotonic_ns() <= deadline:
                    # I²C bus was busy, wait and retry
                    time.sleep(sleep_time)  # time is given in seconds
                else:
                    # unable to acquire the lock
                    raise RuntimeError("timed out before the I²C bus became available")
        else:
            while not self._i2c_bus.try_lock():
                # I²C bus was busy, wait and retry
                time.sleep(sleep_time)  # time is given in seconds
        # successfully acquired a lock
        elapsed_ns = time.perf_counter_ns() - self._timestart_ns
        LH.debug("[%d] Acquired a lock on the I²C bus after %d ms.", id(self), elapsed_ns / (1000 * 1000))
        return BurstHandle(i2c_bus=self._i2c_bus, i2c_adr=self._i2c_adr)

    def __exit__(self, exc_type, exc_value, exc_tb):
        elapsed_ns = time.perf_counter_ns() - self._timestart_ns
        LH.debug("[%d] I²C I/O burst completed after %d ms.", id(self), elapsed_ns / (1000 * 1000))
        LH.debug("[%d] Releasing the lock on the I²C bus.", id(self))
        self._i2c_bus.unlock()


def _validate_register_address(register: int):
    """
    verify that the register address is within the allowed range
    """
    if register < 0 or register > 255:
        raise ValueError(f"Provided I²C device register {register} is out of range! (allowed range: 0 ≤ x ≤ 255)")
