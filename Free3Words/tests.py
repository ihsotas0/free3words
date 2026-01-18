'''
Copyright (C) 2023 Free3Words contributors

This file is part of Free3Words.

Free3Words is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Free3Words is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public
License along with Free3Words.  If not, see
<http://www.gnu.org/licenses/>.
'''

'''
Universal testing script.
'''
from Free3Words import Free3Words
import random

tests = [
    (37.456289, -122.345021, 100000),
    (40.712893, -74.006101, 100000),
    (23.543210, 80.234567, 100000),
    (-15.789023, 56.478912, 100000),
    (18.289410, -45.678932, 100000),
    (47.123098, 12.345678, 100000),
    (-3.210120, 44.567898, 100000),
    (29.456783, -32.101201, 100000),
    (14.789012, 78.234563, 100000),
    (-23.456789, 67.890123, 100000),
]

f3w = Free3Words(seed='foo')
CORD = 10 ** 5

print("Standard tests: ")
for test in tests:
    code = f3w.encode(test[0], test[1], test[2])
    decode = f3w.decode(code)
    print(f"({test[0]:11}, {test[1]:11}) -> ({decode[0]:11}, {decode[1]:11}) :: {str(code)}")


print("Random tests: ")
for i in range(500):
    lat = random.randrange(-89_99999, 89_99999) / CORD
    long = random.randrange(1, 179_99999) / CORD
    code = f3w.encode(lat, long)
    decode = f3w.decode(code)
    print(f"({lat:11}, {long:11}) -> ({decode[0]:11}, {decode[1]:11}) :: {str(code)}")

