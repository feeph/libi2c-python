# design

## desired features

- provide user friendly names that relate to actual usage scenarios
- read or write multiple registers in a single transaction
- automatically retry in case of typical errors
- configurable timeout if I²C bus lock can't be acquired

## why not 'busio.I2C()' or 'i2c_device.I2CDevice()'?

The primary reasons for providing this alternative implementation are:

__busio.I2C()__

can be used directly but exposes implementation details

- `I2C.readfrom_into()`, `I2C.writeto()`, `I2C.writeto_then_readfrom()` are
  named weirdly and have confusing signatures.
   - It is unclear what purpose the method `I2C.readfrom_into()` has.
   - It is unclear whether 'in_buffer' and 'out_buffer' relate to
     direction "device-to-caller" or "caller-to-device" without looking
     at the implementation.
- You must remember to acquire a lock before and unlock the bus. Failing to
  lock/unlock the I²C bus is likely to lead to errors and/or deadlocks.

__i2c_device.I2CDevice()__

automates the locking but shares similar usability issues:

- uses equally weird (but different) method names
- uses C-inspired output parameters for readinto() and write_then_readinto().
  It is unclear why these methods can't optimize for convenience and use a
  conventional getter instead. (Smells like a literal translation of an
  Arduino-based implementation.)
- is unable to guarantee temporal consistency when reading from
  multiple registers
- will wait forever if something else blocks the I²C bus

__method names and purpose__

| purpose                  | I2C                       | I2CDevice                                                           |
|--------------------------|---------------------------|---------------------------------------------------------------------|
|                          | `readfrom_into()`         | `readinto(buffer, start, end)`                                      |
| write value to register  | `writeto()`               | `write(buffer, start, end)`                                         |
| read value from register | `writeto_then_readfrom()` | `write_then_readinto(buffer1, buffer2, start1, end1, start2, end2)` |

- Technically speaking the method names are correct. Unfortunately they
  describe a technical implementation detail (what's happening on the bus)
  instead of a usage scenario (reading/writing a value).
- The methods `I2C.writeto()` and `I2CDevice.write()` don't seem to be
  particularly useful. It is unclear what their intended purpose is.

__Conclusion__

The interface of `busio.I2C()` is a typical low-level implementation.
There's nothing fundamentally wrong with that, but we can add a layer
and make it more convenient to use and harder to accidentally mis-use.

The interface of `i2c_device.I2CDevice()` is a bit too convoluted for what
it's doing. It's a nice touch to see support for reading multi-byte values
but it's not able to read non-consecutive locations and that diminishes the
worth of this functionality. To improve user convenience it would be much more
useful to hide the buffer handling logic and provide a conventional
getter/setter style interface instead of C-Style output parameters.

- The primary benefit of using I2CDevice boils down to implicit acquiring
  and releasing the lock on the I²C bus for single reads.
- It is apparent some considerations are made to conserve memory. But since
  I2CDevice doesn't offer any substantial improvements to I2C it's probably
  a better choice to ignore I2CDevice in memory-restricted environments and
  perform the locking manually.
