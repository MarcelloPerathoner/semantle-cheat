#!/usr/bin/env python3

"""This script initializes the cheat database.

It calculates the similarity of each of three arbitrarily chosen words to all
words in the corpus and stores the values in the database.
"""


import numpy as np
from numpy import dot
from numpy.linalg import norm

from more_itertools import chunked
import sqlite3
import tqdm

def expand_bfloat(vec):
    """
    expand the bfloat16 in the stock database to real float32

    N.B. this hack is faster than using the bfloat16 dtype from tensorflow:

    .. code::

       import tensorflow as tf
       bfloat16 = tf.bfloat16.as_numpy_dtype

       def expand_bfloat(vec):
          return np.frombuffer(vec, dtype=bfloat16)

    """

    buffer = np.zeros(600, dtype=np.int16)
    buffer[1::2] = np.frombuffer(vec, dtype=np.int16)
    return buffer.view(dtype=np.float32)


print ('initializing ...')

con = sqlite3.connect("word2vec.db")
con.execute("PRAGMA journal_mode=WAL")
cur = con.cursor()

cur.execute("DROP TABLE nearby")
cur.execute("CREATE TABLE nearby (word TEXT, neighbor TEXT, similarity FLOAT)")
con.commit()

# get and cache the probe words

cur.execute("SELECT word, vec FROM word2vec WHERE word IN ('man', 'red', 'two')")
probes = []
for row in cur.fetchall():
    vec = expand_bfloat(row[1])
    print (norm(vec))
    probes.append ( (row[0], vec, norm(vec)) )

# calculate the similarity of the probe words vs. all the words

cur.execute("SELECT word, vec FROM word2vec")

print ('calculating similarities ...')

for chunk in chunked(tqdm.tqdm(cur.fetchall()), 16 * 1024):
    values = []
    for row in chunk:
        word = row[0]
        word_vec = expand_bfloat(row[1])
        for probe, probe_vec, probe_norm in probes:
            values.append((probe, word, round (100 * abs(dot(probe_vec, word_vec) / (probe_norm * norm (word_vec))), 2)))

    cur.executemany('INSERT INTO nearby (word, neighbor, similarity) VALUES (?, ?, ?)', values)
    con.commit()

print ('indexing table ...')

cur.execute("CREATE INDEX nearby_words ON nearby (word, similarity)")
con.commit()
