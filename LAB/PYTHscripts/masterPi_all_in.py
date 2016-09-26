import sys
import os
import subprocess
import time
import serial

#skList = ['5', '0', '16', '11', '14', '7', '1', '6', '2', '3', '18', '12']
skList = ['2', '3', '7', '14', '5', '0', '16', '4', '8', '12', '1', '6']

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

	inputF = open('Core/EASI_Hold_Pot_46ns.txt', 'r')
	outputF = open('Conf/EASI_Hold_Pot_46ns_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(736+y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/EASI_TimeOut_Pot_300ns.txt', 'r')
	outputF = open('Conf/EASI_TimeOut_Pot_300ns_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(704+y)
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
	arg = ["./SendFSlaves", "Conf/EASI_Hold_Pot_46ns_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendFSlaves", "Conf/EASI_TimeOut_Pot_300ns_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendFSlaves", "Conf/EASI_Slow_Control_" + Sk + ".txt"]
	subprocess.call(arg)
	print('\n')

arg = ["./SendFMaster", "MasterCMD/MUX_TEST_TRIG.txt"]
subprocess.call(arg)

print ("---> System Ready!\n")
count = 0
evts = 10000

while(count<11):
	count = count + 1
	print("Run " + str(count) + " :: Now reading")
	#arg = ["python3", "masterPi.py", Sk]
	#subprocess.call(arg)
	#subprocess.call("./Reset")
	arg = ['./ReadSlave', str(evts) , '2', '3', '7', '14', '5', '0', '16', '4', '8', '12', '1', '6']
	subprocess.call(arg)
	arg = ['mv', '/home/muBot/slaveDatas1', '/home/muray/TestRun_New/slaveData_evts'+str(evts)+'_run'+str(count)]
	subprocess.call(arg)

arg = ['./ReadSlave', '10' , '2', '3', '7', '14', '5', '0', '16', '4', '8', '12', '1', '6']
subprocess.call(arg)
arg = ['rm', '/home/muBot/slaveDatas1']
subprocess.call(arg)
