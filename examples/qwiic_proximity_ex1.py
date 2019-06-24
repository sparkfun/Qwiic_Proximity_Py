#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_proximity_ex1.py
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
# Example 1
#
# - Setup the device
# - Output the proximity value

from __future__ import print_function
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


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


