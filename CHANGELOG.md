# Changelog

## [0.7.4](https://github.com/feeph/libi2c-python/compare/v0.7.3...v0.7.4) (2024-08-13)


### Bug Fixes

* improve code quality and testing procedure ([#57](https://github.com/feeph/libi2c-python/issues/57)) ([eb578e1](https://github.com/feeph/libi2c-python/commit/eb578e1865690a85fc79c5db650773216fb389fd))
* resolve issues identified by pylint ([af706d0](https://github.com/feeph/libi2c-python/commit/af706d0bfc10275c35ab4d6331356f4153749a2a))

## [0.7.3](https://github.com/feeph/libi2c-python/compare/v0.7.2...v0.7.3) (2024-08-11)


### Bug Fixes

* remove warning messages that were used for debugging ([#48](https://github.com/feeph/libi2c-python/issues/48)) ([6327fd9](https://github.com/feeph/libi2c-python/commit/6327fd9a961e9444db628865e18e79082a367540))

## [0.7.2](https://github.com/feeph/libi2c-python/compare/v0.7.1...v0.7.2) (2024-08-11)


### Bug Fixes

* remove warning messages that were used for debugging ([#46](https://github.com/feeph/libi2c-python/issues/46)) ([1f20ded](https://github.com/feeph/libi2c-python/commit/1f20ded75476035b914ae78bf32acf2adcb10d02))

## [0.7.1](https://github.com/feeph/libi2c-python/compare/v0.7.0...v0.7.1) (2024-08-04)


### Bug Fixes

* use correct byte order for multi-byte read/write ([352d5e9](https://github.com/feeph/libi2c-python/commit/352d5e9cf24e646253ebb09db2b4e0e3a4c655a1))
* use correct byte order for multi-byte read/write ([#38](https://github.com/feeph/libi2c-python/issues/38)) ([7ff10f6](https://github.com/feeph/libi2c-python/commit/7ff10f6b42737e656f97e48b2a75be66247aa61d))

## [0.7.0](https://github.com/feeph/libi2c-python/compare/v0.6.0...v0.7.0) (2024-07-29)


### Features

* support multi-byte reads for device registers ([#31](https://github.com/feeph/libi2c-python/issues/31)) ([6bc1ff5](https://github.com/feeph/libi2c-python/commit/6bc1ff55a7661995e386f4bde78ec57dc9ff1552))

## [0.6.0](https://github.com/feeph/libi2c-python/compare/v0.5.0...v0.6.0) (2024-07-23)


### Features

* add configuration for dependabot ([31f07f2](https://github.com/feeph/libi2c-python/commit/31f07f237817fdc11fb5b999edfdfdc5bb8ab14c))
* allow reading and writing of device state ([67a72cf](https://github.com/feeph/libi2c-python/commit/67a72cf2d96687d6fe94eda694bcdddf30d33163))


### Bug Fixes

* delete obsolete code in 'BurstHandler' ([0741bd4](https://github.com/feeph/libi2c-python/commit/0741bd423cd7fe121c5367afcb0375bd4aad4bfc))
* remove obsolete file ([559d320](https://github.com/feeph/libi2c-python/commit/559d3201ef6a8219546d4ffcc0ffffb90d0f81cc))
* update package versions ([5df0bb9](https://github.com/feeph/libi2c-python/commit/5df0bb91e51970433583dae5f20091407275ccba))

## [0.5.0](https://github.com/feeph/libi2c-python/compare/v0.4.1...v0.5.0) (2024-07-20)


### Features

* provide a context manager for read/write operations ([#20](https://github.com/feeph/libi2c-python/issues/20)) ([a728a8b](https://github.com/feeph/libi2c-python/commit/a728a8b55ff67f85c390e238a0cf884c3bfa8ac0))

## [0.4.1](https://github.com/feeph/libi2c-python/compare/v0.4.0...v0.4.1) (2024-07-20)


### Bug Fixes

* fix the retry-on-error logic ([#17](https://github.com/feeph/libi2c-python/issues/17)) ([254f9b3](https://github.com/feeph/libi2c-python/commit/254f9b39bb9d44fb99cea3d6fbebb6b16f4b8266))

## [0.4.0](https://github.com/feeph/libi2c-python/compare/v0.3.2...v0.4.0) (2024-07-20)


### Features

* provide type hints marker ([#14](https://github.com/feeph/libi2c-python/issues/14)) ([91b93bc](https://github.com/feeph/libi2c-python/commit/91b93bcb5bb3cbddcd90d02b10e057d5c73058e2))

## [0.3.2](https://github.com/feeph/libi2c-python/compare/v0.3.1...v0.3.2) (2024-07-15)


### Documentation

* Update design.md ([#12](https://github.com/feeph/libi2c-python/issues/12)) ([f51a191](https://github.com/feeph/libi2c-python/commit/f51a19154346ff742de315bad1b984e70b9f5408))

## [0.3.1](https://github.com/feeph/libi2c-python/compare/v0.3.0...v0.3.1) (2024-07-15)


### Bug Fixes

* update package dependencies ([#10](https://github.com/feeph/libi2c-python/issues/10)) ([688e814](https://github.com/feeph/libi2c-python/commit/688e81421a03503c13852914fd9033f4696bf552))

## [0.3.0](https://github.com/feeph/libi2c-python/compare/v0.2.1...v0.3.0) (2024-07-14)


### Features

* redesign the library and document its philosophy ([67f1671](https://github.com/feeph/libi2c-python/commit/67f1671e57f4ce06c160c39705e63b14dfb3c196))

## [0.2.1](https://github.com/feeph/libi2c-python/compare/v0.2.0...v0.2.1) (2024-07-08)


### Bug Fixes

* update 'feeph/i2c/__init__.py' with correct import ([#4](https://github.com/feeph/libi2c-python/issues/4)) ([e2105f4](https://github.com/feeph/libi2c-python/commit/e2105f45055faecf435c2e3494d74cb9341930bf))

## [0.2.0](https://github.com/feeph/libi2c-python/compare/v0.1.0...v0.2.0) (2024-07-08)


### Features

* provide a simulated I²C bus ([#1](https://github.com/feeph/libi2c-python/issues/1)) ([5c85f6b](https://github.com/feeph/libi2c-python/commit/5c85f6b691384ecc1e9aee7f635a86a2d3a1dbc7))
