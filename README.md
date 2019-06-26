# Qwiic_Proximity_Py
<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>
</p>

Python module to interface with the [Qwiic Proximity board](https://www.sparkfun.com/products/15177).

![SparkFun Proximity Breakout](https://cdn.sparkfun.com//assets/parts/1/3/5/9/2/15177-SparkFun_Proximity_Sensor_Breakout_-_20cm__VCNL4040__Qwiic_-01.jpg)

This package is a port of the [SparkFun VCNL4040 Proximity Sensor Arduino Library](https://github.com/sparkfun/SparkFun_VCNL4040_Arduino_Library)

## Dependencies 
This driver package depends on the qwii I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

### PyPi Installation
On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```
  sudo pip install sparkfun_qwiic_proximity
```
For the current user:

```
  pip install sparkfun_qwiic_proximity
```

### Local Installation

To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```
  $ python setup.py install
```

To build a package for use with pip:
```
  $ python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```
  cd dist
  pip install sparkfun_qwiic_proximity-<version>.tar.gz
```

## Example Use
See the examples directory for more detailed use examples.

```python
import qwiic_proximity
import time
import sys

def runExample():

	print("\nSparkFun Proximity Sensor VCN4040 Example 1\n")
	oProx = qwiic_proximity.QwiicProximity()

	if oProx.isConnected() == False:
		print("The Qwiic Proximity device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	oProx.begin()

	while True:
		proxValue = oProx.getProximity()
		print("Proximity Value: %d" % proxValue)
		time.sleep(.4)
    
runExample()

```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
