#!/usr/bin/env python3
"""
"""

import time

# module busio provides no type hints
import busio  # type: ignore


def try_lock_with_timeout(i2c_bus: busio.I2C, timeout_ms: int, sleep_time_ms: int = 1):
    """
    Try to acquire a lock for exclusive access on the I²C bus.

    Raises a RuntimeError if it wasn't possible to acquire the lock within
    the given timeout.
    """
    if not isinstance(timeout_ms, int) or timeout_ms < 0:
        raise ValueError("Timeout must be a positive integer.")
    # 0.001         = 1 millisecond
    # 0.000_001     = 1 microsecond
    # 0.000_000_001 = 1 nanosecond
    timeout_ns = timeout_ms * 1000 * 1000
    sleep_time = float(sleep_time_ms) / 1000
    deadline = time.monotonic_ns() + timeout_ns
    while not i2c_bus.try_lock():
        if time.monotonic_ns() <= deadline:
            # I²C bus was busy, wait and retry
            time.sleep(sleep_time)  # sleep for 1 milliseconds
        else:
            # unable to acquire the I²C bus
            raise RuntimeError("timed out while waiting on I²C bus to become available")
