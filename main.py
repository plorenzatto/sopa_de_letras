import string
import numpy as np
import json

fild = np.random.choice(list(string.ascii_lowercase),  size=(15, 15))


with open('palabras.json', 'r') as f:
    words = json.load(f)


fild = np.random.choice(list(string.ascii_lowercase),  size=(15, 15))

# insert word in fild:
# generate random pos to insert
# check that the word is not going out of bound