import sys
import os
import subprocess
import time

skList = ['2', '3', '7', '14', '5', '0', '16', '11', '8', '12', '1', '6']
#dac10List = ['250', '375', '767', '384', '300', '695', '760', '730', '753', '770', '716', '742']
#dac10List = ['465', '700', '850', '855', '630', '580', '830', '850', '840', '860', '830', '855']
dac10List = ['465', '700', '835', '840', '630', '580', '815', '825', '840', '840', '810', '840']

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

for dac10 in range (0,1,1):
	dac8 = 255
		
	while (dac8 >= 255):
		print ('----------------------------')
		print ('DAC8 value  : ' + str(dac8))
		print ('DAC10 value : ' + str(dac10))
		print ('----------------------------')
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

		for Sk in skList :
			arg = ["./ResetSlave", Sk]
			subprocess.call(arg)

		subprocess.call("./Init")
		
		skCounter = 0
		for Sk in skList :
			inputF = open('Core/EASI_Slow_Control.txt', 'r')
			outputF = open('Conf/EASI_Slow_Control_' + Sk + '.txt', 'w')
			s = inputF.readline()
			y = int(Sk)<<10
			w = "{:04x}".format(224 + y)
			outputF.write(w + '\n')
			s = inputF.readline()
			outputF.write(s)
			s = inputF.readline()
			y = int(dac10List[skCounter])<<2
			w = "{:04x}".format(61443 + y)
			outputF.write(w + '\n')
			
			while s:
				s = inputF.readline()
				outputF.write(s)
			inputF.close()
			outputF.close()
			skCounter = skCounter + 1

		input('Press ENTER...')

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

			if (dac8 == 255):
				argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
				subprocess.call(argv)
				argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
				subprocess.call(argv)
				argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
				subprocess.call(argv)
			print('\n')

		print ('\nAquiring Triggers...')
		
		arg = ["./SendFMaster", "MasterCMD/EN_MUX0.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX1.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX2.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX3.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX4.txt"]
		subprocess.call(arg)
		
		arg = ['./ReadMaster_cTrigger', 'MasterCMD/START_TRG_CNT.txt', 'MasterCMD/RD_TRG_CNT.txt']
		subprocess.call(arg)
		
		subprocess.call('./Reset')
		print ('\nAquiring Counts...')
		for Sk in skList :
			argv = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
			subprocess.call(argv)
		time.sleep(11)
		print('\n')
		skCounter = 0
		for Sk in skList :
			argv = ["./SendFSlaves", "Conf/ReadSlave_" + Sk + ".txt"]
			subprocess.call(argv)
			subprocess.call("./ReadMaster_count")
			inp = open('SlaveCounts', 'r')
			outp = open('Counts_GLOBAL', 'a')

			r = inp.readline()
			r = r.replace('\n', '')
			while r :
				w = Sk + '\t' + r + dac10List[skCounter] + '\t' + str(int(time.time())) + '\n'
				outp.write(w)
				r = inp.readline()
			inp.close()
			outp.close()
			argv = ["mv", "SlaveCounts", "/home/muray/TestCounts/SlaveCounts_" + Sk + "_" + str(dac10)]
			subprocess.call(argv)
			print ('END\n')
			skCounter = skCounter + 1

		runCounter = 0
		evts = 10

		while(runCounter<1):
			runCounter = runCounter + 1
			print("Run " + str(runCounter) + " :: Now reading")
			outputF = open('slaveData', 'w')
			outputF.write(str(int(round(time.time()*1000))) + '\n')
			outputF.close()
			#arg = ['./ReadSlave', str(evts) , '2', '3', '7', '14', '5', '0', '16', '11', '8', '12', '1', '6']
			arg = ['./ReadSlave', str(evts) , skList[0], skList[1], skList[2], skList[3], skList[4], skList[5], skList[6], skList[7], skList[8], skList[9], skList[10], skList[11]]
			subprocess.call(arg)
			outputF = open('slaveData', 'a')
			outputF.write(str(int(round(time.time()*1000))))
			outputF.close()
			arg = ['mv', '/home/muBot/slaveData', '/home/muray/CosmicRun/slaveData_evts' + str(evts) + '_run' + str(runCounter)]
			subprocess.call(arg)

		dac8 = dac8 - 64
		if (dac8 == -1):
			dac8 = 0

	print ('\n--- Shutting Down System\n')
	for Sk in skList :
		#argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
		#subprocess.call(argv)
		argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
		subprocess.call(argv)
		argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
		subprocess.call(argv)
