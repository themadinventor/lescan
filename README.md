lescan
======

[![Build Status](https://travis-ci.com/themadinventor/lescan.svg?branch=master)](https://travis-ci.com/themadinventor/lescan)

`lescan` is a minimalistic LE scanning utility based on the excellent [gatt-python](https://github.com/getsenic/gatt-python) library.

`gatt-python` (and thus `lescan`) currently only supports Linux and BlueZ.


Installing
----------

Install the latest distribution from [Pypi](https://pypi.org/project/lescan/):
```
pip3 install --user lescan
sudo apt-get install python3-dbus
```

The `python3-dbus` package is needed by `python-gatt`. Please refer to the `python-gatt` documentation for details.

Usage
-----

Simply run `lescan` in your shell. `lescan` will pretty-print all received BLE advertisements.

License
-------
`lescan` is released under the MIT license.