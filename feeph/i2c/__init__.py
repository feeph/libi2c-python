#!/usr/bin/env python3
"""
provide a user-friendly interface for the I2C bus
"""


import logging
import time

# module busio provides no type hints
import busio  # type: ignore

import feeph.i2c.utility

# the following imports are provided for user convenience
# flake8: noqa: F401
from feeph.i2c.burst_handler import BurstHandler, BurstHandle
from feeph.i2c.emulation import EmulatedI2C

LH = logging.getLogger("i2c")


def read_device_register(i2c_bus: busio.I2C, i2c_adr: int, register: int, byte_count: int = 1, max_tries: int = 3, timeout_ms: int = 500) -> int:
    """
    read a single register from I²C device identified by `i2c_adr` and
    return its contents as an integer value
      - may raise a RuntimeError if it was not possible to acquire
        the bus within allowed time
      - may raise a RuntimeError if there were too many errors

    If you need to read multiple registers in a single transaction please
    use `feeph.i2c.Burst()` instead. This will ensure all values are
    read while holding the same lock and prevent outside interference.

    typical usage:
    ```
    value1 = read_device_register(i2c_bus, 0x4C, 0x00)
    ```
    """
    with BurstHandler(i2c_bus=i2c_bus, i2c_adr=i2c_adr, timeout_ms=timeout_ms) as bh:
        return bh.read_register(register=register, byte_count=byte_count, max_tries=max_tries)


def read_device_registers(i2c_bus: busio.I2C, reads: list[tuple[int, int, int]], max_tries: int = 3, timeout_ms: int = 500) -> list[int]:
    """
    read from multiple registers on one or more I²C devices in a single
    transaction and return their contents as a list of integer values
      - may raise a RuntimeError if it was not possible to acquire
        the bus within allowed time
      - may raise a RuntimeError if there were too many errors

    If you need to read a single register please use the function
    `read_device_register()` instead. It uses exactly the same
    implementation but makes it more convenient to use.

    typical usage:
    ```
    reads = [
        (0x4C, 0x01, 1)
        (0x4C, 0x10, 1)
    ]
    values = read_device_registers(i2c_bus, reads)
    ```
    """
    for i2c_adr, _, _ in reads:
        if i2c_adr < 0 or i2c_adr > 255:
            raise ValueError(f"Provided I²C address {i2c_adr} is out of range! (allowed range: 0 <= x <= 255)")
    for cur_try in range(1, 1 + max_tries):
        is_success = False
        # make sure we have exclusive access to the I²C bus
        feeph.i2c.utility.try_lock_with_timeout(i2c_bus=i2c_bus, timeout_ms=timeout_ms)
        # read from the registers and unlock the bus again
        values = list()
        try:
            buf_r = bytearray(1)
            for i2c_adr, register, byte_count in reads:
                if byte_count < 1:
                    raise ValueError("byte count must be at least 1 (value: {byte_count})")
                elif byte_count > 1:
                    LH.warning("Multi byte reads are not implemented yet! Returning a single byte instead.")
                buf_r[0] = register
                buf_w = bytearray(byte_count)
                i2c_bus.writeto_then_readfrom(address=i2c_adr, buffer_out=buf_r, buffer_in=buf_w)
                # TODO properly handle multi byte reads
                values.append(buf_w[0])
            is_success = True
        except OSError as e:
            # [Errno 121] Remote I/O error
            LH.warning("[%s] Failed to read register 0x%02X (%i/%i): %s",  __name__, register, cur_try, max_tries, e)
            time.sleep(0.1)
        except RuntimeError as e:
            LH.warning("[%s] Unable to read register 0x%02X (%i/%i): %s", __name__, register, cur_try, max_tries, e)
            time.sleep(0.1)
        finally:
            i2c_bus.unlock()
        # are we done yet?
        if is_success:
            return values
        else:
            LH.debug("Failed to process all reads. Retrying.")
    else:
        raise RuntimeError(f"Unable to read register 0x{register:02X} after {cur_try} attempts. Giving up.")


def write_device_register(i2c_bus: busio.I2C, i2c_adr: int, register: int, value: int, byte_count: int = 1, max_tries: int = 3, timeout_ms: int = 500):
    """
    write a single register to I²C device identified by `i2c_adr`
      - may raise a RuntimeError if it was not possible to acquire
        the bus within allowed time
      - may raise a RuntimeError if there were too many errors

    If you need to write multiple registers in a single transaction please
    use `feeph.i2c.Burst()` instead. This will ensure all values are
    written while holding the same lock and prevent outside interference.

    typical usage:
    ```
    write_device_register(i2c_bus, 0x4C, 0x00, value)
    ```
    """
    with BurstHandler(i2c_bus=i2c_bus, i2c_adr=i2c_adr, timeout_ms=timeout_ms) as bh:
        bh.write_register(register=register, value=value, byte_count=byte_count, max_tries=max_tries)


def write_device_registers(i2c_bus: busio.I2C, writes: list[tuple[int, int, int, int]], max_tries: int = 3, timeout_ms: int = 500):
    """
    write to multiple registers on one or more I²C devices in a single
    transaction
      - may raise a RuntimeError if it was not possible to acquire
        the bus within allowed time
      - may raise a RuntimeError if there were too many errors

    If you need to read a single register please use the function
    `read_device_register()` instead. It uses exactly the same
    implementation but makes it more convenient to use.

    typical usage:
    ```
    writes = [
        (0x4C, 0x01, 12, 1)
        (0x4C, 0x10, 34, 1)
    ]
    values = write_device_registers(i2c_bus, writes)
    ```
    """
    for i2c_adr, _, _, _ in writes:
        if i2c_adr < 0 or i2c_adr > 255:
            raise ValueError(f"Provided I²C address {i2c_adr} is out of range! (allowed range: 0 <= x <= 255)")
    for cur_try in range(1, 1 + max_tries):
        is_success = False
        # make sure we have exclusive access to the I²C bus
        feeph.i2c.utility.try_lock_with_timeout(i2c_bus=i2c_bus, timeout_ms=timeout_ms)
        # write to the registers and unlock the bus again
        try:
            for i2c_adr, register, byte_count, value in writes:
                if byte_count < 1:
                    raise ValueError("byte count must be at least 1 (value: {byte_count})")
                elif byte_count > 1:
                    LH.warning("Multi byte reads are not implemented yet! Returning a single byte instead.")
                buf = bytearray(1 + byte_count)
                buf[0] = register
                buf[1] = value & 0xFF
                # TODO properly handle multi byte reads
                i2c_bus.writeto(address=i2c_adr, buffer=buf)
            is_success = True
        except OSError as e:
            # [Errno 121] Remote I/O error
            LH.warning("[%s] Failed to read register 0x%02X (%i/%i): %s",  __name__, register, cur_try, max_tries, e)
            time.sleep(0.1)
        except RuntimeError as e:
            LH.warning("[%s] Unable to read register 0x%02X (%i/%i): %s", __name__, register, cur_try, max_tries, e)
            time.sleep(0.1)
        finally:
            i2c_bus.unlock()
        # are we done yet?
        if is_success:
            return
        else:
            LH.debug("Failed to process all writes. Retrying.")
    else:
        raise RuntimeError(f"Unable to read register 0x{register:02X} after {cur_try} attempts. Giving up.")
