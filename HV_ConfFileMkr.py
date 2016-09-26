import sys
import os
import subprocess
import time

skList = ['2', '3', '13', '9', '5', '0', '17', '7', '8', '12', '4', '1']

for Sk in skList :
	inputF = open('Core/EASI_SwHV_ON.txt', 'r')
	outputF = open('Conf_HV/EASI_SwHV_ON_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(768 + y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/EASI_HV-OUT_ShutDown.txt', 'r')
	outputF = open('Conf_HV/EASI_HV-OUT_ShutDown_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(672+y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/EASI_SwHV_OFF.txt', 'r')
	outputF = open('Conf_HV/EASI_SwHV_OFF_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(800+y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()
