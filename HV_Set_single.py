import sys
import os
import subprocess
import time

skList = ['2', '3', '7', '14', '5', '0', '16', '11', '8', '12', '1', '6']
Sk = sys.argv[1]
Volt = sys.argv[2]
Temp = sys.argv[3]

inputF = open('Core/EASI_HV-OUT_bas.txt', 'r')
outputF = open('Conf_HV/EASI_HV-OUT_Vbias_' + Sk + '.txt', 'w')
s = inputF.readline()
y = int(Sk)<<10
w = "{:04x}".format(672+y)
outputF.write(w + '\n')
s = inputF.readline()
if (Sk == '0') :
	m = 0.1942
	q = 77.492
	DVop = 0
if (Sk == '5') :
	m = 0.1943
	q = 77.429
	DVop = 0.20
if (Sk == '11') :
	m = 0.1941
	q = 77.519
	DVop = 0.20
if (Sk == '16') :
	m = 0.1931
	q = 77.224
	DVop = 0.20
if (Sk == '17') :
	m = 0.1903
	q = 77.157
	DVop = 0.20
if (Sk == '14') :
	m = 0.1940
	q = 77.423
	DVop = 0.20
if (Sk == '7') :
	m = 0.1933
	q = 77.227
	DVop = 0.20
if (Sk == '3') :
	m = 0.1932
	q = 77.423
	DVop = 0
if (Sk == '2') :
	m = 0.1929
	q = 77.516
	DVop = 0.20
if (Sk == '1') :
	m = 0.1935
	q = 77.229
	DVop = 0
if (Sk == '6') :
	m = 0.1915
	q = 77.660
	DVop = 0
#if (Sk == '8') :
#	m = 0.1930
#	q = 77.308
#	DVop = 0
if (Sk == '8') :
	m = 0.1958
	q = 77.228
	DVop = 0
if (Sk == '12') :
	m = 0.1915
	q = 77.173
	DVop = 0

digiVolt = int(((q - (float(Volt) + DVop +(float(Temp)-25)*0.05))//m))	
w = "{:04x}".format(digiVolt)
outputF.write(w + '\n')
while s:
	s = inputF.readline()
	outputF.write(s)
inputF.close()
outputF.close()
