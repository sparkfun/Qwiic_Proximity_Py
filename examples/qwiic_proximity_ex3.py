#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_proximity_ex3.py
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
# Example 3 - Ambient Light
#

from __future__ import print_function
import qwiic_proximity
import time
import sys

def runExample():

	print("\nSparkFun Proximity Sensor VCN4040 Example 3\n")
	oProx = qwiic_proximity.QwiicProximity()

	if oProx.isConnected() == False:
		print("The Qwiic Proximity device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# begin Setup
	oProx.begin()

	oProx.powerOffProximity()  	# Power down the proximity portion of the sensor
	oProx.powerOnAmbient()  	# Power Up the ambient sensor


	while True:
		ambientValue = oProx.getAmbient()
		print("Ambient Value: %d" % ambientValue)

		time.sleep(.4)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)


