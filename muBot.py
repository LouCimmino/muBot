import sys
import os
import subprocess

print ('\n\nMuDog (MuBot ver 4.0) - MuRay Experiment')
print ('Copyright 2013(C) 19LC77 (email : luigi.cimmino@na.infn.it)')
print ('__________________________________________________________\n')

subprocess.call('./DTCrcvr')

DTCfile = '/home/DatiTB/DTC/DTC.txt'
inputF = open(DTCfile, 'r')
s = inputF.readline()
s = s.replace('$PEDS\t', '')
peds = s.replace('\n', '')
s = inputF.readline()
s = s.replace('$EVTS\t', '')
evts = s.replace('\n', '')
inputF.close()
try :
	arg = ['python3', 'acqCPE.py', peds, evts]
	subprocess.call(arg)
except :
	arg = ['python3', 'HV_Shutdown.py']
	subprocess.call(arg)
	
