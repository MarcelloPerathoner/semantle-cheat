#!/usr/bin/env python3

import argparse

import sqlite3


parser = argparse.ArgumentParser(description='Cheat for https://semantle.novalis.org/')

parser.add_argument('man', metavar='MAN', type=float,
                    help='the similarity for the word: man')
parser.add_argument('red', metavar='RED', type=float,
                    help='the similarity for the word: red')
parser.add_argument('two', metavar='TWO', type=float,
                    help='the similarity for the word: two')

args = parser.parse_args()

con = sqlite3.connect("word2vec.db")
cur = con.cursor()

cur.execute("""
SELECT n1.neighbor FROM nearby as n1, nearby as n2, nearby as n3
WHERE n1.word = 'man' and n1.similarity = ?
  AND n2.word = 'red' and n2.similarity = ?
  AND n3.word = 'two' and n3.similarity = ?
  AND n1.neighbor = n2.neighbor
  AND n1.neighbor = n3.neighbor
""", (args.man, args.red, args.two))

rows = list(cur.fetchall())
print (rows)
