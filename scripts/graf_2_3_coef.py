import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
plt.style.use('ggplot')

lp = np.loadtxt('python/lp_2_3.txt')
lpcc = np.loadtxt('python/lpcc_2_3.txt')
mfcc = np.loadtxt('python/mfcc_2_3.txt')

plt.figure()

plt.subplot(311)
plt.plot(lp_2_3[:,0], lp_2_3[:,1],'r,')
plt.title('LP')

plt.subplot(312)
plt.plot(lpcc_2_3[:,0], lpcc_2_3[:,1],'r,')
plt.title('LPCC')

plt.subplot(313)
plt.plot(mfcc_2_3[:,0], mfcc_2_3[:,1],'r,')
plt.title('MFCC')

plt.show()