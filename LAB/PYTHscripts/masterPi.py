import sys
import os
import subprocess
import time
import serial

skList = ['7', '2', '3', '14', '5', '0', '16', '11', '8', '12', '1', '6']
#skList = ['7']
dac10List = ['400', '400', '677', '384', '400', '695', '760', '730', '753', '770', '716', '742']
#dac10List = ['800']
#skList = ['6']
#dac10List = ['742']

for Sk in skList :
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
	
skCounter = 0

for Sk in skList :
	arg = ["./ResetSlave", Sk]
	subprocess.call(arg)

subprocess.call("./Init")

for dac10 in dac10List:
	inputF = open('EASIprog.c', 'r')
	outputF = open('EASIprog.out', 'w')
	s = inputF.readline()
	while s:
		outputF.write(s)
		#if ('//DAC8' in s):
		#	outputF.write('for (i=0; i<32; i++) error = DACbiasSC_EASI(SC_EASI, i, ' + str(dac8) + ');')
		#	outputF.write('\n')	
		#	s = inputF.readline()
		if ('//DAC10' in s) :
			outputF.write('\tDAC10thrsSC_EASI(SC_EASI,' + str(dac10) +');\n')
			s = inputF.readline()
		s = inputF.readline()
	inputF.close()
	outputF.close()
	arg = ["mv", "EASIprog.out", "EASIprog.c"]
	subprocess.call(arg)
	arg = ["gcc", "-O2", "EASIprog.c", "libreriaSC_EASI.c", "-o", "EASIprog"]
	subprocess.call(arg)
	subprocess.call("./EASIprog")

	inputF = open('Core/EASI_Slow_Control.txt', 'r')
	outputF = open('Conf/EASI_Slow_Control_' + skList[skCounter] + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(224 + y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()
	print(dac10 + '\t' + skList[skCounter] + '\n')
	skCounter = skCounter + 1


for Sk in skList :
	arg = ["./SendFSlaves", "Conf/EASI_Probe_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendFSlaves", "Conf/EASI_Hold_Pot_46ns_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendFSlaves", "Conf/EASI_TimeOut_Pot_300ns_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendFSlaves", "Conf/EASI_Slow_Control_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
	subprocess.call(arg)
	arg = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
	subprocess.call(arg)
	time.sleep(1)
	print('---' + Sk + '\n')

arg = ["./SendFMaster", "MasterCMD/EN_MUX0.txt"]
subprocess.call(arg)
time.sleep(1)
arg = ["./SendFMaster", "MasterCMD/EN_MUX1.txt"]
subprocess.call(arg)
time.sleep(1)
arg = ["./SendFMaster", "MasterCMD/EN_MUX2.txt"]
subprocess.call(arg)
time.sleep(1)
arg = ["./SendFMaster", "MasterCMD/EN_MUX3.txt"]
subprocess.call(arg)
time.sleep(1)
arg = ["./SendFMaster", "MasterCMD/EN_MUX4.txt"]
subprocess.call(arg)

print ("---> System Ready!\n")
count = 0
evts = 100

while(count<1):
	count = count + 1
	print("Run " + str(count) + " :: Now reading")
	outputF = open('slaveDatas1', 'w')
	outputF.write(str(int(round(time.time()*1000))) + '\n')
	outputF.close()
	arg = ['./ReadSlave', str(evts) , '2', '3', '7', '14', '5', '0', '16', '11', '8', '12', '1', '6']
	#arg = ['./ReadSlave', str(evts) , skList[0]]
	subprocess.call(arg)
	outputF = open('slaveDatas1', 'a')
	outputF.write(str(int(round(time.time()*1000))))
	outputF.close()
	arg = ['mv', '/home/muBot/slaveDatas1', '/home/muray/TestRun_New/slaveData_evts' + str(evts) + '_run' + str(count)]
	#arg = ['mv', '/home/muBot/slaveDatas1', '/home/muray/TestRun_New/slaveData_evts' + str(evts) + '_sk' + skList[0]]
	subprocess.call(arg)

print ('\n--- Shutting Down System\n')
for Sk in skList :
	#argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
	#subprocess.call(argv)
	argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
	subprocess.call(argv)
	argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
	subprocess.call(argv)
