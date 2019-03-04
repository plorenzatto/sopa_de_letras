import string
import numpy as np
import json

FILD_X = 15
FILD_Y = 15


fild = np.zeros([FILD_Y,FILD_X], dtype='str')


def insert_vertical(fild, word='codin',backwards=False):
    if(backwards):
        word = word[::-1]
    flag = False
    count = 0
    while(flag == False):
        count+=1
        #generate random x,y
        pos = (np.random.randint(FILD_Y),np.random.randint(FILD_X-len(word)))
        #get that space and check if there is no letter there
        fild_row = fild[pos[0]]
        space = fild_row[pos[1]:pos[1]+len(word)]
        space = ''.join(space)
        if(len(space) == 0):
            for i in range(len(word)):
                fild_row[i+pos[1]] = word[i]
            flag = True
        assert count < 10, "something went terrible wrong!"


def insert_horizontal(fild, word,backwards=False):
    if(backwards):
        word = word[::-1]
    flag = False
    count = 0
    while(flag == False):
        count+=1
        #generate random x,y
        pos = (np.random.randint(FILD_Y-len(word)),np.random.randint(FILD_X))
        #get that space and check if there is no letter there
        space = fild[pos[0]:pos[0]+len(word),pos[1]]
        space = ''.join(space)
        if(len(space) == 0):
            for i in range(len(word)):
                fild[pos[0]+i,pos[1]] = word[i]
            flag = True
        assert count < 10, "something went terrible wrong!"


def fill_with_random(fild):
    for x in range(FILD_X):
        for y in range(FILD_Y):
            if(fild[x,y] == ''):
                fild[x,y] = np.random.choice(list(string.ascii_lowercase))

insert_horizontal(fild, 'Codin',True)
insert_vertical(fild, 'Eric')
fill_with_random(fild)
print(fild)

