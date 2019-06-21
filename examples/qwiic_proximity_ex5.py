#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_proximity_ex5.py
#
# Simple Example for the Qwiic Proximity Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
# Example 5 - Advanced Settings
#

from __future__ import print_function
import qwiic_proximity
import time
import sys

def runExample():

	print("\nSparkFun Proximity Sensor VCN4040 Example 5\n")
	oProx = qwiic_proximity.QwiicProximity()

	if oProx.isConnected() == False:
		print("The Qwiic Proximity device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# begin Setup
	oProx.begin()

	oProx.powerOnAmbient()  	# Power Up the ambient sensor

	# Set the integration time for the proximity sensor
	# 1 to 8 is valid
	oProx.setProxIntegrationTime(8) 

	# Set the integration time for the ambient light sensor in milliseconds
	# 80 to 640ms is valid
	oProx.setAmbientIntegrationTime(80)

	# If sensor sees more than this, interrupt pin will go low
	oProx.setProxHighThreshold(2000)

	# The int pin will stay low until the value goes below the low threshold value
	oProx.setProxLowThreshold(150)

	# Enable both 'away' and 'close' interrupts
	oProx.setProxInterruptType(oProx.VCNL4040_PS_INT_BOTH)

	# This causes the int pin to go low every time a reading is outside the thresholds
	# Get a multimeter and probe the INT pin to see this feature in action
	oProx.enableProxLogicMode()

	while True:

		proxValue = oProx.getProximity()
		print("Proximity Value: \t[%5d]" % proxValue)
		
		ambientValue = oProx.getAmbient()
		print("Ambient Value: \t\t[%5d]\n" % ambientValue)


		time.sleep(1)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 5")
		sys.exit(0)


