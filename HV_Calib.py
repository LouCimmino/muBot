import sys
import os
import subprocess
import time

#skList = ['5', '11', '16', '12', '8', '6', '1', '3', '2', '14', '7']
#skList = ['9', '13', '17', '4']
skList = ['13']

for Sk in skList :
	inputF = open('Core/EASI_Slow_Control.txt', 'r')
	outputF = open('Conf/EASI_Slow_Control_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(224 + y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/EASI_Probe.txt', 'r')
	outputF = open('Conf/EASI_Probe_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(256+y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/EASI_HV-OUT_bas.txt', 'r')
	outputF = open('Conf_HV/EASI_HV-OUT_Vop_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(672+y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

subprocess.call("./Reset")

for Sk in skList :
	arg = ["./ResetSlave", Sk]
	subprocess.call(arg)

subprocess.call("./Init")
for Sk in skList :
	time.sleep(1)
	arg = ["./SendFSlaves", "Conf/EASI_Probe_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendFSlaves", "Conf/EASI_Slow_Control_" + Sk + ".txt"]
	subprocess.call(arg)
	print('\n')

print ("---> System Ready!\n")

for Sk in skList :
	argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
	subprocess.call(argv)
	argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
	subprocess.call(argv)
	argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vop_" + Sk + ".txt"]
	subprocess.call(argv)
	input()
	for i in range(0, 41, 5):
		inputF = open('Core/EASI_HV-OUT_bas.txt', 'r')
		outputF = open('Conf_HV/EASI_HV-OUT_Vop_' + Sk + '.txt', 'w')
		s = inputF.readline()
		y = int(Sk)<<10
		w = "{:04x}".format(672+y)
		outputF.write(w + '\n')
		s = inputF.readline()
		w = "{:04x}".format(35+i)
		print(w)
		outputF.write(w + '\n')
		inputF.close()
		outputF.close()
		argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_Vop_" + Sk + ".txt"]
		subprocess.call(argv)
		input()
	argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vop_" + Sk + ".txt"]
	subprocess.call(argv)
	argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
	subprocess.call(argv)
	argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
	subprocess.call(argv)
