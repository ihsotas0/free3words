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
from ff3 import FF3Cipher
import pygeohash as Geohash

import hashlib
import random
import math
import string

__gh_b32 = "0123456789bcdefghjkmnpqrstuvwxyz"
__py_b32 = "0123456789ABCDEFGHIJKLMNOPQRSTUV"

class Free3Words:

    GH_B32 = "0123456789bcdefghjkmnpqrstuvwxyz" # Geohash base 32 encoding, not RFC 4648.
    PY_B32 = "0123456789ABCDEFGHIJKLMNOPQRSTUV" # Python base 32 encoding, not RFC 4648.

    def __init__(self, seed='free3words', word_list='en'):
        '''
        Makes a f3w factory.

        Args:
            seed (string): Determines the shuffling of the word list and the encryption of each Geohash, default is "free3words".
            word_list (string): Choose a alternative "word_list", default is "en" (default english word list).

        Returns:
            Free3Words: f3w object to encode/decode many values for the same seed/word_list
        '''

        # Generate word_arr from word_list
        filename = './' + word_list + '.txt'
        self.word_arr = []

        try:
            with open(filename, 'rt', encoding='utf-8') as file:
                self.word_arr = [line.rstrip() for line in file.readlines()]

        except FileNotFoundError:
            print(f"Word list: {filename} does not exist.")

        # Shuffle word_arr to remove alphabetic bias for lists longer then 32768
        random.Random(seed).shuffle(self.word_arr)

        # Initialize cryptography
        sha = hashlib.sha256(seed.encode()).hexdigest().upper()
        self.cipher = FF3Cipher.withCustomAlphabet(sha, sha[0:14], Free3Words.GH_B32)

    def encode(self, lat, long, elevation=None):
        '''
        Encodes coordinates into a f3w code.

        Args:
            lat (float): Latitude.
            long (float): Longitude.

        Returns:
            str: A three word f3w string array.
        '''

        # Coords -> decrypted Geohash
        geohash = Geohash.encode(lat, long, precision=9)

        # Elevations values not in the encodable range will be ignored
        if elevation in range(0,32767):
            geohash += Free3Words._to_b32(elevation)

        # Decrypted Geohash -> encrypted Geohash
        geohash_cipher = self.cipher.encrypt(geohash)

        # encrypted Geohash -> words
        words_b32 = [geohash_cipher[i:i+3] for i in range(0, len(geohash), 3)] # split Geohash into strings of 3 chars each
        words_index = [Free3Words._to_int(s) for s in words_b32] # b32 -> int conversion
        words = [self.word_arr[i] for i in words_index] # get words associated with index

        return words

    def decode(self, words):
        '''
        Decodes a f3w code into coordinates.

        Args:
            words (str): Array of 3 words (f3w code).

        Returns:
            float: Latitude and longitude of the f3w code in tuple.
        '''

        # Words -> encrypted Geohash
        words_index = [self.word_arr.index(s) for s in words]  # get index associated with each word
        words_b32 = [Free3Words._to_b32(i) for i in words_index] # nightmare one-liner left as an exercise for the reader, int -> b32 conversion
        
        # Encrypted Geohash -> decrypted Geohash
        geohash = self.cipher.decrypt(''.join(words_b32)) # join b32 segments into Geohash then decrypt

        # Decrypted Geohash -> coords
        lat, long = Geohash.decode(geohash[0:8])

        if len(geohash) > 9:
            elevation = Free3Words._to_int(geohash[9:11])
        else:
            elevation = None

        return lat, long, elevation

    # int <-> b32 conversions
    def _to_int(s):
        table = str.maketrans(Free3Words.GH_B32, Free3Words.PY_B32)
        return int(s.translate(table), 32)

    def _to_b32(i):
        return ''.join([Free3Words.GH_B32[k] for k in reversed([i // (32**j) % 32 for j in range(int(math.log(i, 32)) + 1)])])
