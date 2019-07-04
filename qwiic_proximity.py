#-----------------------------------------------------------------------------
# SparkFun qwiic proximity sensor
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
#
# More information on qwiic is at https:www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
"""
qwiic_proximity
================

Python module for the [SparkFun Qwiic Proximity Sensor Breakout](https://www.sparkfun.com/products/15177)

This python package is a port of the existing [SparkFun VCNL4040 Proximity Sensor Arduino Library](https://github.com/sparkfun/SparkFun_VCNL4040_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
# load the i2c bus driver package
import qwiic_i2c

#
# The name of this device 
_DEFAULT_NAME = "Qwiic Proximity Sensor"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_AVAILABLE_I2C_ADDRESS = [0x60]


# Used to select between upper and lower byte of command register
LOWER = True
UPPER = False

# VCNL4040 Command Codes
VCNL4040_ALS_CONF = 0x00
VCNL4040_ALS_THDH = 0x01
VCNL4040_ALS_THDL = 0x02
VCNL4040_PS_CONF1 = 0x03 #Lower
VCNL4040_PS_CONF2 = 0x03 #Upper
VCNL4040_PS_CONF3 = 0x04 #Lower
VCNL4040_PS_MS = 0x04  #Upper
VCNL4040_PS_CANC = 0x05
VCNL4040_PS_THDL = 0x06
VCNL4040_PS_THDH = 0x07
VCNL4040_PS_DATA = 0x08
VCNL4040_ALS_DATA = 0x09
VCNL4040_WHITE_DATA = 0x0A
VCNL4040_INT_FLAG = 0x0B #Upper
VCNL4040_ID = 0x0C


class QwiicProximity(object):
	"""
	QwiicProximity

		:param address: The I2C address to use for the device. 
						If not provided, the default address is used.
		:param i2c_driver: An existing i2c driver object. If not provided 
						a driver object is created. 
		:return: The Proximity device object.
		:rtype: Object
	"""

	# Constructor
	device_name = _DEFAULT_NAME
	available_addresses = _AVAILABLE_I2C_ADDRESS

	# Flags exposed in userspace - make these class vars
	VCNL4040_PS_INT_MASK = (~((1 << 1) | (1 << 0))) & 0xff
	VCNL4040_PS_INT_DISABLE = 0
	VCNL4040_PS_INT_CLOSE = (1 << 0)
	VCNL4040_PS_INT_AWAY = (1 << 1)
	VCNL4040_PS_INT_BOTH = (1 << 1) | (1 << 0)

	# Define commands/commandwords for the sensor
	VCNL4040_ALS_IT_MASK =  (~((1 << 7) | (1 << 6)) ) & 0xff #uint8
	VCNL4040_ALS_IT_80MS = 0
	VCNL4040_ALS_IT_160MS = (1 << 7)
	VCNL4040_ALS_IT_320MS = (1 << 6)
	VCNL4040_ALS_IT_640MS = (1 << 7) | (1 << 6)
	
	VCNL4040_ALS_PERS_MASK = (~((1 << 3) | (1 << 2))) & 0xff
	VCNL4040_ALS_PERS_1 = 0
	VCNL4040_ALS_PERS_2 = (1 << 2)
	VCNL4040_ALS_PERS_4 = (1 << 3)
	VCNL4040_ALS_PERS_8 = (1 << 3) | (1 << 2)
	
	VCNL4040_ALS_INT_EN_MASK = (~(1 << 1)) & 0xff
	VCNL4040_ALS_INT_DISABLE = 0
	VCNL4040_ALS_INT_ENABLE = (1 << 1)
	
	VCNL4040_ALS_SD_MASK = (~(1 << 0)) & 0xff
	VCNL4040_ALS_SD_POWER_ON = 0
	VCNL4040_ALS_SD_POWER_OFF = (1 << 0)
	
	VCNL4040_PS_DUTY_MASK = (~((1 << 7) | (1 << 6))) & 0xff
	VCNL4040_PS_DUTY_40 = 0
	VCNL4040_PS_DUTY_80 = (1 << 6)
	VCNL4040_PS_DUTY_160 = (1 << 7)
	VCNL4040_PS_DUTY_320 = (1 << 7) | (1 << 6)
	
	VCNL4040_PS_PERS_MASK = (~((1 << 5) | (1 << 4))) & 0xff
	VCNL4040_PS_PERS_1 = 0
	VCNL4040_PS_PERS_2 = (1 << 4)
	VCNL4040_PS_PERS_3 = (1 << 5)
	VCNL4040_PS_PERS_4 = (1 << 5) | (1 << 4)
	
	VCNL4040_PS_IT_MASK = (~((1 << 3) | (1 << 2) | (1 << 1))) & 0xff
	VCNL4040_PS_IT_1T = 0
	VCNL4040_PS_IT_15T = (1 << 1)
	VCNL4040_PS_IT_2T = (1 << 2)
	VCNL4040_PS_IT_25T = (1 << 2) | (1 << 1)
	VCNL4040_PS_IT_3T = (1 << 3)
	VCNL4040_PS_IT_35T = (1 << 3) | (1 << 1)
	VCNL4040_PS_IT_4T = (1 << 3) | (1 << 2)
	VCNL4040_PS_IT_8T = (1 << 3) | (1 << 2) | (1 << 1)
	
	VCNL4040_PS_SD_MASK = (~(1 << 0)) & 0xff
	VCNL4040_PS_SD_POWER_ON = 0
	VCNL4040_PS_SD_POWER_OFF = (1 << 0)
	
	VCNL4040_PS_HD_MASK = (~(1 << 3)) & 0xff
	VCNL4040_PS_HD_12_BIT = 0
	VCNL4040_PS_HD_16_BIT = (1 << 3)

	VCNL4040_PS_SMART_PERS_MASK = (~(1 << 4)) & 0xff
	VCNL4040_PS_SMART_PERS_DISABLE = 0
	VCNL4040_PS_SMART_PERS_ENABLE = (1 << 1)
	
	VCNL4040_PS_AF_MASK = (~(1 << 3)) & 0xff
	VCNL4040_PS_AF_DISABLE = 0
	VCNL4040_PS_AF_ENABLE = (1 << 3)
	
	VCNL4040_PS_TRIG_MASK = (~(1 << 3)) & 0xff
	VCNL4040_PS_TRIG_TRIGGER = (1 << 2)
	
	VCNL4040_WHITE_EN_MASK = (~(1 << 7)) & 0xff
	VCNL4040_WHITE_ENABLE = 0
	VCNL4040_WHITE_DISABLE = (1 << 7)
	
	VCNL4040_PS_MS_MASK = (~(1 << 6)) & 0xff
	VCNL4040_PS_MS_DISABLE = 0
	VCNL4040_PS_MS_ENABLE = (1 << 6)
	
	VCNL4040_LED_I_MASK = (~((1 << 2) | (1 << 1) | (1 << 0))) & 0xff
	VCNL4040_LED_50MA = 0
	VCNL4040_LED_75MA = (1 << 0)
	VCNL4040_LED_100MA = (1 << 1)
	VCNL4040_LED_120MA = (1 << 1) | (1 << 0)
	VCNL4040_LED_140MA = (1 << 2)
	VCNL4040_LED_160MA = (1 << 2) | (1 << 0)
	VCNL4040_LED_180MA = (1 << 2) | (1 << 1)
	VCNL4040_LED_200MA = (1 << 2) | (1 << 1) | (1 << 0)
	
	VCNL4040_INT_FLAG_ALS_LOW = (1 << 5)
	VCNL4040_INT_FLAG_ALS_HIGH = (1 << 4)
	VCNL4040_INT_FLAG_CLOSE = (1 << 1)
	VCNL4040_INT_FLAG_AWAY = (1 << 0)

	def __init__(self, address=None, i2c_driver=None):


		# Did the user specify an I2C address?
		self.address = address if address != None else self.available_addresses[0]

		# load the I2C driver if one isn't provided

		if i2c_driver == None:
			self._i2c = qwiic_i2c.getI2CDriver()
			if self._i2c == None:
				print("Unable to load I2C driver for this platform.")
				return
		else:
			self._i2c = i2c_driver

	#----------------------------------------------
	def isConnected(self):
		""" 
			Determine if a Proximity device is conntected to the system..

			:return: True if the device is connected, otherwise False.
			:rtype: bool

		"""
		return qwiic_i2c.isDeviceConnected(self.address)

	#----------------------------------------------
	# //Check comm with sensor and set it to default init settings
	def begin(self):
		""" 
			Initialize the operation of the Proximity module

			:return: Returns true of the initializtion was successful, otherwise False.
			:rtype: bool

		"""
  		# //Check connection
		if self.isConnected() == False: 
  			return False  # I2C comm failure

		if self.getID() != 0x0186:
			return False  # Check default ID value

		# //Configure the various parts of the sensor
		self.setLEDCurrent(200) # Max IR LED current

		self.setIRDutyCycle(40) # Set to highest duty cycle

		self.setProxIntegrationTime(8) # Set to max integration

		self.setProxResolution(16) # Set to 16-bit output
  
		self.enableSmartPersistance() #Turn on smart presistance

		self.powerOnProximity() #Turn on prox sensing

		self.setAmbientIntegrationTime(self.VCNL4040_ALS_IT_80MS) #Keep it short
		self.powerOnAmbient() #Turn on ambient sensing

		return True

	#----------------------------------------------
	# //Set the duty cycle of the IR LED. The higher the duty
	# //ratio, the faster the response time achieved with higher power
	# //consumption. For example, PS_Duty = 1/320, peak IRED current = 100 mA,
	# //averaged current consumption is 100 mA/320 = 0.3125 mA.
	def setIRDutyCycle(self, dutyValue):
		""" 
			Set the duty cycle of the IR LED. The higher the duty
			ratio, the faster the response time achieved with higher power
			consumption. For example, PS_Duty = 1/320, peak IRED current = 100 mA,
			averaged current consumption is 100 mA/320 = 0.3125 mA.

			:param dutyValue: The duty cycle value for the IR LED on the sensor
			:return: No return value

		"""
		if dutyValue > 320 - 1 :
			dutyValue = self.VCNL4040_PS_DUTY_320
		elif dutyValue > 160 - 1 :
			dutyValue = self.VCNL4040_PS_DUTY_160
		elif dutyValue > 80 - 1 :
			dutyValue = self.VCNL4040_PS_DUTY_80
		else:
			dutyValue = self.VCNL4040_PS_DUTY_40
  
		self._bitMask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_DUTY_MASK, dutyValue)

	duty_cycle = property()
	duty_cycle = duty_cycle.setter(setIRDutyCycle)

	#----------------------------------------------	
	# //Set the Prox interrupt persistance value
	# //The PS persistence function (PS_PERS, 1, 2, 3, 4) helps to avoid
	# //false trigger of the PS INT. It defines the amount of
	# //consecutive hits needed in order for a PS interrupt event to be triggered.
	def setProxInterruptPersistance(self, persValue):
		""" 
			Set the Prox interrupt persistance value
			The PS persistence function (PS_PERS, 1, 2, 3, 4) helps to avoid
			false trigger of the PS INT. It defines the amount of
			consecutive hits needed in order for a PS interrupt event to be triggered.

			:param persValue: The persistance value 
			:return: No return value

		"""
		self._bitMask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_PERS_MASK, persValue)


	#----------------------------------------------	
	# //Set the Ambient interrupt persistance value
	# //The ALS persistence function (ALS_PERS, 1, 2, 4, 8) helps to avoid
	# //false trigger of the ALS INT. It defines the amount of
	# //consecutive hits needed in order for a ALS interrupt event to be triggered.
	def setAmbientInterruptPersistance(self, persValue):
		""" 
			Set the Ambient interrupt persistance value
			The ALS persistence function (ALS_PERS, 1, 2, 4, 8) helps to avoid
			false trigger of the ALS INT. It defines the amount of
			consecutive hits needed in order for a ALS interrupt event to be triggered.

			:param persValue: The ambiant interrupt persistance value 
			:return: No return value

		"""
		self._bitMask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_PERS_MASK, persValue)

	def enableAmbientInterrupts(self):
		""" 
			Enable Ambient Interrupts

			:return: No return value
		"""
		self._bitMask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_INT_EN_MASK, self.VCNL4040_ALS_INT_ENABLE)

	def disableAmbientInterrupts(self):
		""" 
			Disable Ambient Interrupts

			:return: No return value
		"""
		self._bitMask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_INT_EN_MASK, self.VCNL4040_ALS_INT_DISABLE)

	# Power on or off the ambient light sensing portion of the sensor
	def powerOnAmbient(self):
		""" 
			Power on the ambient light sensing portion of the sensor

			:return: No return value
		"""
		self._bitMask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_SD_MASK, self.VCNL4040_ALS_SD_POWER_ON)

	def powerOffAmbient(self):
		""" 
			Power off the ambient light sensing portion of the sensor

			:return: No return value
		"""
		self._bitMask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_SD_MASK, self.VCNL4040_ALS_SD_POWER_OFF)

	# Sets the integration time for the ambient light sensor
	def setAmbientIntegrationTime(self, timeValue):
		""" 
			Sets the integration time for the ambient light sensor
			
			:param timeValue: The integration time 
			:return: No return value
		"""

		if timeValue > 640 - 1 :
			timeValue = self.VCNL4040_ALS_IT_640MS
		elif timeValue > 320 - 1:
			timeValue = self.VCNL4040_ALS_IT_320MS
		elif timeValue > 160 - 1:
			timeValue = self.VCNL4040_ALS_IT_160MS
		else:
			timeValue = self.VCNL4040_ALS_IT_80MS

		self._bitMask(VCNL4040_ALS_CONF, LOWER, self.VCNL4040_ALS_IT_MASK, timeValue)

	# Sets the integration time for the proximity sensor
	def setProxIntegrationTime(self, timeValue):
		""" 
			Sets the integration time for the proximity sensor
			
			:param timeValue: The integration time 
			:return: No return value
		"""
		if timeValue > 8 - 1 :
			timeValue = self.VCNL4040_PS_IT_8T
		elif timeValue > 4 - 1 :
			timeValue = self.VCNL4040_PS_IT_4T
		elif timeValue > 3 - 1 :
			timeValue = self.VCNL4040_PS_IT_3T
		elif timeValue > 2 - 1 :
			timeValue = self.VCNL4040_PS_IT_2T
		else:
			timeValue = self.VCNL4040_PS_IT_1T

		self._bitMask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_IT_MASK, timeValue)

	# Power on the prox sensing portion of the device
	def powerOnProximity(self):
		""" 
			Power on the prox sensing portion of the device

			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_SD_MASK, self.VCNL4040_PS_SD_POWER_ON)

	# Power off the prox sensing portion of the device
	def powerOffProximity(self):
		""" 
			Power off the prox sensing portion of the device

			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF1, LOWER, self.VCNL4040_PS_SD_MASK, self.VCNL4040_PS_SD_POWER_OFF)

	# Sets the proximity resolution
	def setProxResolution(self, resolutionValue):
		""" 
			Sets the proximity resolution
			
			:param resolutionValue: The resolution time 
			:return: No return value
		"""
		if(resolutionValue > 16 - 1):
			resolutionValue = self.VCNL4040_PS_HD_16_BIT
		else:
			resolutionValue = self.VCNL4040_PS_HD_12_BIT
	
		self._bitMask(VCNL4040_PS_CONF2, UPPER, self.VCNL4040_PS_HD_MASK, resolutionValue)

	# Sets the proximity interrupt type
	def setProxInterruptType(self, interruptValue):
		""" 
			Sets the proximity interrupt type
			
			:param interruptValue: The interupt type
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF2, UPPER, self.VCNL4040_PS_INT_MASK, interruptValue);

	# Enable smart persistance
	# To accelerate the PS response time, smart
	# persistence prevents the misjudgment of proximity sensing
	# but also keeps a fast response time.
	def enableSmartPersistance(self):
		""" 
			Enable smart persistance
			To accelerate the PS response time, smart
			persistence prevents the misjudgment of proximity sensing
			but also keeps a fast response time.
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF3, LOWER,self.VCNL4040_PS_SMART_PERS_MASK, self.VCNL4040_PS_SMART_PERS_ENABLE)

	def disableSmartPersistance(self):
		""" 
			Disable smart persistance
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_SMART_PERS_MASK, self.VCNL4040_PS_SMART_PERS_DISABLE)

	# Enable active force mode
	# An extreme power saving way to use PS is to apply PS active force mode.
	# Anytime host would like to request one proximity measurement,
	# enable the active force mode. This
	# triggers a single PS measurement, which can be read from the PS result registers.
	# VCNL4040 stays in standby mode constantly.
	def enableActiveForceMode(self):
		""" 
			Enable active force mode
			An extreme power saving way to use PS is to apply PS active force mode.
			Anytime host would like to request one proximity measurement,
			enable the active force mode. This
			triggers a single PS measurement, which can be read from the PS result registers.
			VCNL4040 stays in standby mode constantly.
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_AF_MASK, self.VCNL4040_PS_AF_ENABLE)

	def disableActiveForceMode(self):
		""" 
			Disable active force mode
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_AF_MASK, self.VCNL4040_PS_AF_DISABLE)

	# Set trigger bit so sensor takes a force mode measurement and returns to standby
	def takeSingleProxMeasurement(self):
		""" 
			Set trigger bit so sensor takes a force mode measurement and returns to standby
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_CONF3, LOWER, self.VCNL4040_PS_TRIG_MASK, self.VCNL4040_PS_TRIG_TRIGGER)

	# Enable the white measurement channel
	def enableWhiteChannel(self):
		""" 
			Enable the white measurement channel
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_MS, UPPER, self.VCNL4040_WHITE_EN_MASK, self.VCNL4040_WHITE_ENABLE)

	def disableWhiteChannel(self):
		""" 
			Disable the white measurement channel
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_MS, UPPER, self.VCNL4040_WHITE_EN_MASK, self.VCNL4040_WHITE_ENABLE)

	# Enable the proximity detection logic output mode
	# When this mode is selected, the INT pin is pulled low when an object is
	# close to the sensor (value is above high
	# threshold) and is reset to high when the object moves away (value is
	# below low threshold). Register: PS_THDH / PS_THDL
	# define where these threshold levels are set.
	def enableProxLogicMode(self):
		""" 
			Enable the proximity detection logic output mode
			When this mode is selected, the INT pin is pulled low when an object is
			close to the sensor (value is above high
			threshold) and is reset to high when the object moves away (value is
			below low threshold). Register: PS_THDH / PS_THDL
			define where these threshold levels are set.
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_MS, UPPER, self.VCNL4040_PS_MS_MASK, self.VCNL4040_PS_MS_ENABLE)

	def disableProxLogicMode(self):
		""" 
			Disable the proximity detection logic output mode
			
			:return: No return value
		"""
		self._bitMask(VCNL4040_PS_MS, UPPER, self.VCNL4040_PS_MS_MASK, self.VCNL4040_PS_MS_DISABLE)


	# Set the IR LED sink current to one of 8 settings
	def setLEDCurrent(self, currentValue):
		""" 
			Set the IR LED sink current to one of 8 settings
			
			:param currentValue: The new current value. Valid values are VCNL4040_LED_50MA thru VCNL4040_LED_200MA at 25MA increments
			:return: No return value
		"""

		if currentValue > 200 - 1 :
			currentValue = self.VCNL4040_LED_200MA
		elif currentValue > 180 - 1 :
			currentValue = self.VCNL4040_LED_180MA
		elif currentValue > 160 - 1 :
			currentValue = self.VCNL4040_LED_160MA
		elif currentValue > 140 - 1 :
			currentValue = self.VCNL4040_LED_140MA
		elif currentValue > 120 - 1 :
			currentValue = self.VCNL4040_LED_120MA
		elif currentValue > 100 - 1 :
			currentValue = self.VCNL4040_LED_100MA
		elif currentValue > 75 - 1 :
			currentValue = self.VCNL4040_LED_75MA
		else:
			currentValue = self.VCNL4040_LED_50MA

		self._bitMask(VCNL4040_PS_MS, UPPER, self.VCNL4040_LED_I_MASK, currentValue)


	# Set the proximity sensing cancelation value - helps reduce cross talk
	# with ambient light
	def setProxCancellation(self, cancelValue):
		""" 
			Set the proximity sensing cancelation value - helps reduce cross talk with ambient light
			
			:param cancelValue: the new cancelation value
			:return: No return value
		"""
		self._i2c.writeWord(self.address, VCNL4040_PS_CANC, cancelValue)

	# Value that ALS must go above to trigger an interrupt
	def setALSHighThreshold(self, threshold):
		""" 
			Value that ALS must go above to trigger an interrupt
			
			:param threshold: the new trigger threshold value for ALS
			:return: No return value
		"""
		self._i2c.writeWord(self.address, VCNL4040_ALS_THDH, threshold)

	# Value that ALS must go below to trigger an interrupt
	def setALSLowThreshold(self, threshold):
		""" 
			Value that ALS must go below to trigger an interrupt
			
			:param threshold: the new trigger threshold value for ALS
			:return: No return value
		"""
		self._i2c.writeWord(self.address, VCNL4040_ALS_THDL, threshold)

	# Value that Proximity Sensing must go above to trigger an interrupt
	def setProxHighThreshold(self, threshold):
		""" 
			Value that Proximity Sensing must go above to trigger an interrupt
			
			:param threshold: The new Proximity High Value 
			:return: No return value
		"""
		self._i2c.writeWord(self.address, VCNL4040_PS_THDH, threshold)

	# Value that Proximity Sensing must go below to trigger an interrupt
	def setProxLowThreshold(self, threshold):
		""" 
			Value that Proximity Sensing must go below to trigger an interrupt
			
			:param threshold: The new Proximity Low Value 
			:return: No return value
		"""
		self._i2c.writeWord(self.address, VCNL4040_PS_THDL, threshold);


	#--------------------------------------------------------------------------
	# Read Value methods
	#--------------------------------------------------------------------------
	# getProximity()
	#
	# Read the Proximity value
	def getProximity(self):
		""" 
			Get the current proximity value
			
			:return: The current proximity value
			:rtype: integer
		"""
		return self._i2c.readWord(self.address, VCNL4040_PS_DATA)


	# prox as a readonly prop
	proximity  = property(getProximity)

	# Read the Ambient light value
	def getAmbient(self):
		""" 
			Read the Ambient light value
			
			:return: The current ambient value value
			:rtype: integer
		"""
		return self._i2c.readWord(self.address, VCNL4040_ALS_DATA)

	# Ambient as a readonly prop
	ambient  = property(getAmbient)


	# Read the Whilte light value
	def getWhite(self):
		""" 
			Read the White light value
			
			:return: The current white value value
			:rtype: integer
		"""
		return self._i2c.readWord(self.address, VCNL4040_WHITE_DATA)

	# White light as a readonly prop
	white_light  = property(getWhite)


	# Read the sensors ID
	def getID(self):
		""" 
			Read the sensor ID
			
			:return: The sensor ID
			:rtype: integer
		"""
		return self._i2c.readWord(self.address, VCNL4040_ID)

	# Sensor ID as a readonly prop
	sensor_id  = property(getID)


	# Returns true if the prox value rises above the upper threshold
	def isClose(self):
		""" 
			Returns true if the prox value rises above the upper threshold
			
			:return: True if close
			:rtype: boolean
		"""
		interruptFlags = self._readCommandUpper(VCNL4040_INT_FLAG)
		return (interruptFlags & self.VCNL4040_INT_FLAG_CLOSE) != 0

	# is_close as a readonly prop
	is_close  = property(isClose)


	# Returns true if the prox value drops below the lower threshold
	def isAway(self):
		""" 
			Returns true if the prox value drops below the lower threshold
			
			:return: True if away
			:rtype: boolean
		"""
		interruptFlags = self._readCommandUpper(VCNL4040_INT_FLAG)
		return (interruptFlags & self.VCNL4040_INT_FLAG_AWAY) != 0

	# is_away as a readonly prop
	is_away  = property(isAway)

	# Returns true if the prox value rises above the upper threshold
	def isLight(self):
		""" 
			Returns true if the prox value rises above the upper threshold
			
			:return: True if value light
			:rtype: boolean
		"""
		interruptFlags = self._readCommandUpper(VCNL4040_INT_FLAG)
		return (interruptFlags & self.VCNL4040_INT_FLAG_ALS_HIGH) != 0

	# is_light as a readonly prop
	is_light  = property(isLight)

	#Returns true if the ALS value drops below the lower threshold
	def isDark(self):
		""" 
			Returns true if the prox value drops below the lower threshold
			
			:return: True if dark
			:rtype: boolean
		"""
		interruptFlags = self._readCommandUpper(VCNL4040_INT_FLAG)
		return (interruptFlags & self.VCNL4040_INT_FLAG_ALS_LOW) != 0

	# is_dark as a readonly prop
	is_dark  = property(isDark)

	#--------------------------------------------------------------------------
	# internal I2C Utility Routines 
	#--------------------------------------------------------------------------	

	#--------------------------------------------------------------------------		
	# _writeCommandLower()
	#
	# Given a command code (address) write to the upper byte without affecting the upper byte
	def _writeCommandLower(self, commandCode, newValue):

		commandValue = self._i2c.readWord(self.address, commandCode)
		commandValue &= 0xFF00    #Remove lower 8 bits
		commandValue |= newValue    #Mask in

		return self._i2c.writeWord(self.address, commandCode, commandValue)
	#--------------------------------------------------------------------------	
	# _writeCommandUpper()
	#
	# Given a command code (address) write to the upper byte without affecting the lower byte
	def _writeCommandUpper(self, commandCode, newValue):

		commandValue = self._i2c.readWord(self.address, commandCode)
		commandValue &= 0x00FF    #Remove upper 8 bits
		commandValue |= newValue << 8   #Mask in

		return self._i2c.writeWord(self.address, commandCode, commandValue)
	#--------------------------------------------------------------------------		
	# _readCommandLower()
	#	
	# Given a command code (address) read the lower byte
	def _readCommandLower(self, commandCode):

		commandValue = self._i2c.readWord(self.address, commandCode)

		return commandValue & 0xFF

	#--------------------------------------------------------------------------		
	# _readCommandUpper()
	#	
	# Given a command code (address) read the upper byte
	def _readCommandUpper(self, commandCode):

		commandValue = self._i2c.readWord(self.address, commandCode)

		return commandValue >> 8 

	#--------------------------------------------------------------------------	
	# _bitMask()
	#
	# Given a register, read it, mask it, and then set the thing
	# commandHeight is used to select between the upper or lower byte of command register
	# Example:
	# Write dutyValue into PS_CONF1, lower byte, using the Duty_Mask
	# _bitMask(VCNL4040_PS_CONF1, LOWER, VCNL4040_PS_DUTY_MASK, dutyValue);
	def _bitMask(self, commandAddress, commandHeight, mask, thing):

		# Grab current register context
		if commandHeight == LOWER:
			registerContents = self._readCommandLower(commandAddress)
		else:
			registerContents = self._readCommandUpper(commandAddress)			

		# Zero-out the portions of the register we're interested in
		registerContents &= mask

		# Mask in new thing
		registerContents |= thing

		# Change contents
		if commandHeight == LOWER:
			self._writeCommandLower(commandAddress, registerContents)
		else:
			self._writeCommandUpper(commandAddress, registerContents)  			
