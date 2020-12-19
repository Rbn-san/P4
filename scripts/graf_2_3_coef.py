#! /usr/bin/python3 -u

import matplotlib.pyplot as plt
import numpy as np

lp = np.loadtxt('coef/lp_2_3.txt')
lpcc = np.loadtxt('coef/lpcc_2_3.txt')
mfcc = np.loadtxt('coef/mfcc_2_3.txt')

plt.figure()

plt.subplot(311)
plt.plot(lp[:,0], lp[:,1],'r,')
plt.title('LP')

plt.subplot(312)
plt.plot(lpcc[:,0], lpcc[:,1],'r,')
plt.title('LPCC')

plt.subplot(313)
plt.plot(mfcc[:,0], mfcc[:,1],'r,')
plt.title('MFCC')

plt.show()