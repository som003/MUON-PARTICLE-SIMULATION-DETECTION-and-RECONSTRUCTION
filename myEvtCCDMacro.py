
import os
import numpy as np
import math
from ccdEvent import *
import matplotlib.pyplot as plt

'''
fileName1 = "pixelInfo_mu_1GeV_5621.dat"

evt1 = ccdEvent(fileName1)
'''


'''
import os
dirName = b"C:\Users\Om Shah\Desktop\python\VLNT\mu_100GeV"
for f in dirName:
    filename = os.listdir(dirName)
    evt1 = ccdEvent(filename,)

dirName1= b"C:\Users\Om Shah\Desktop\python\VLNT\mu_1TeV"
for fi in dirName:
    filename = os.listdir(dirName1)
    evt2 = ccdEvent(filename)
'''


import glob
path = b"C:\Users\Om Shah\Desktop\python\VLNT\mu_100GeV"

files = glob.glob(os.path.join(path, "*.txt"))

for f in files:
    filename = os.listdir(f)
    evt1 = ccdEvent(filename)