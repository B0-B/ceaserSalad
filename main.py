#!/usr/bin/env python3
#
# Main Code For ceaserSalad
#
class engine:
    soup = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~0123456789 \n\t'''
    def __init__(self):
        self.map = {}
        for char in self.soup:
            self.map[char] = self.soup.index(char)
    def encrypt(self, plainText, secret):
        ind, cypher, l, s = 0, str(), len(secret), len(self.soup)
        for char in plainText:
            cypher += self.shift(char, secret, ind, l, s)
            ind += 1
        return cypher
    def decrypt(self, cipher, secret):
        ind, plain, l, s = 0, str(), len(secret), len(self.soup)
        for letter in cipher:
            plain += self.shift(letter, secret, ind, l, s, -1)
            ind += 1
        return plain
    def shift(self, letter, secret, ind, l, s, sign=1):
        try:
            return self.soup[(self.map[letter] + sign * self.map[secret[ind % l]]) % s]
        except:
            raise ValueError(f'String includes invalid characters, allowed are \n{self.soup}')
