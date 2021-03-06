# SigNetSim.py -- Python program that wraps the SigNetSim framework.
#
#    This file is part of the featsel program
#    Copyright (C) 2017  Marcelo S. Reis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys

X = str (sys.argv[0])

sys.stdout = open('output/SigNetSim.tmp', 'w')

print ("The value received by the Python script is: " + X)

#
# End of program.
