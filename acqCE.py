import sys
import os
import subprocess
import time

skList = ['2', '3', '13', '9', '5', '0', '17', '7', '8', '12', '4', '1']
dac10List = ['435', '610', '550', '465', '610', '480', '560', '465', '840', '810', '475', '550']

zero = ['8','12']
unoA = ['2','3','0','5']
unoB = ['17','7','4','1','13','9']

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
	s = inputF.readline()
	if (Sk in zero) : y = 6
	if (Sk in unoA) : y = 6
	if (Sk in unoB) : y = 6
	ht = "{:04x}".format(255-y)
	outputF.write(ht + '\n')
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

		subprocess.call('./Init')

		for Sk in skList :
			arg = ["./ResetSlave", Sk]
			subprocess.call(arg)
	
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
		
		inputF = open('Conf/EASI_Slow_Control_12.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[11] = '7bd7\n'
		s[12] = 'fff5\n'
		s[13] = 'fafd\n'
		s[14] = '7fff\n'
		s[15] = 'ffaf\n'
		s[16] = 'ffeb\n'
		s[17] = 'f5fa\n'
		s[18] = 'fd7e\n'
		s[19] = 'bf5f\n'
		s[20] = 'afff\n'
		s[21] = 'ebf5\n'
		s[22] = 'faff\n'
		s[23] = 'febf\n'
		s[24] = '5faf\n'
		s[25] = 'ffeb\n'
		s[26] = 'fffa\n'
		s[27] = 'fd7e\n'
		s[28] = 'bf5f\n'
		s[29] = 'ff00\n'

		outputF = open('Conf/EASI_Slow_Control_12.txt', 'w')
		for line in s:
			outputF.write(line)
		outputF.close()

		inputF = open('Conf/EASI_Slow_Control_13.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[4] = 'fff9\n'
		outputF = open('Conf/EASI_Slow_Control_13.txt', 'w')
		for line in s:
			outputF.write(line)
		outputF.close()

		for Sk in skList :
			subprocess.call('./Init')
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
		
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL0.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL1.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL2.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL3.txt"]
		#subprocess.call(arg)


		subprocess.call('./Reset')

		runCounter = 1
		evts = 10000
		
		while(runCounter<2):
			runCounter = runCounter + 1
			print ('\nAquiring Counts...')
		
			for Sk in skList :
				argv = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
				subprocess.call(argv)
			time.sleep(11)
			for Sk in skList :
				argv = ["./SendFSlaves", "Conf/ReadSlave_" + Sk + ".txt"]
				subprocess.call(argv)
			
				subprocess.call("./ReadMaster_count")
				inp = open('SlaveCounts', 'r')
				outp = open('Counts_LAB', 'a')

				r = inp.readline()
				r = r.replace('\n', '')
				while r :
					w = Sk + '\t' + r + str(dac10) + '\t' + str(int(time.time())) + '\n'
					outp.write(w)
					r = inp.readline()
				inp.close()
				outp.close()
				
				argv = ["mv", "SlaveCounts", "/home/muray/TestCounts/SlaveCounts_" + Sk]
				subprocess.call(argv)
				
		
			argv = ["mv", "Counts_LAB", "/home/muray/CosmicRun/SlavesCount_run" + str(runCounter)]
			subprocess.call(argv)
			print ('I END Count\n\n')
			print("Run " + str(runCounter) + " :: Now reading")
			outputF = open('slaveData', 'w')
			outputF.write(str(int(round(time.time()*1000))) + '\n')
			outputF.close()
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
