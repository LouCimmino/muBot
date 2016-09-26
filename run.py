#!/usr/bin/env bash

import sys
import os
import subprocess

#arg = ['python3', 'detEfficiency_sCounts_cycle.py', '2', '1', '5']
#subprocess.call(arg)

#arg = ['python3', 'detEfficiency_sCounts_cycle.py', '8', '16', '7']
#subprocess.call(arg)

for i in range(0,50,4):
#for j in range(0,1):
	inputF = open('Core/EASI_Hold_Pot_46ns.txt', 'r')
	s = inputF.readlines()
	inputF.close()

	#i = 32
	outputF = open('Core/EASI_Hold_Pot_46ns.txt', 'w')
	ht = "{:04x}".format(255-i)
	s[1] = ht + '\n'
	 
	outputF.write(s[0] + s[1])
	outputF.close()
	
	arg = ['python3', 'acq4Hold.py', '2', ht]
	subprocess.call(arg)
