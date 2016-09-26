import sys
import os
import subprocess
import time

#skList = ['2', '3', '7', '14', '5', '0', '16', '11', '8', '12', '1', '6']
#dac10List = ['465', '700', '835', '840', '630', '580', '835', '825', '860', '860', '810', '840']
#dac10List = ['380', '525', '800', '801', '467', '475', '797', '788', '777', '800', '771', '799']

skList = ['7']
dac10List = ['850']

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
		
		
		inputF = open('Conf/EASI_Slow_Control_7.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[4] = 'fff9\n'
		outputF = open('Conf/EASI_Slow_Control_7.txt', 'w')
		for line in s:
			outputF.write(line)
		outputF.close()

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

			#if (dac8 == 255):
			#	argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
			#	subprocess.call(argv)
			#	argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
			#	subprocess.call(argv)
			#	argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
			#	subprocess.call(argv)
			print('\n')
		subprocess.call("./Reset")
		time.sleep(1)
		stepCounter = 1
		
		arg = ['./SendFMaster', 'MasterCMD/RUN.txt']
		subprocess.call(arg)
		
		

		#while (stepCounter < 11):
		#	print ('\nAquiring Triggers (6P)...')
		#
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
		input("PRESS ENTER...")
		#	
		#	arg = ['./ReadMaster_cTrigger', 'MasterCMD/START_TRG_CNT.txt', 'MasterCMD/RD_TRG_CNT.txt']
		#	subprocess.call(arg)
		#	
		#	print ('\nAquiring Counts...')
		#	for Sk in skList :
		#		argv = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
		#		subprocess.call(argv)
		#	time.sleep(11)
		#	print('\n')
		#	skCounter = 0
		#	for Sk in skList :
		#		argv = ["./SendFSlaves", "Conf/ReadSlave_" + Sk + ".txt"]
		#		subprocess.call(argv)
		#		subprocess.call("./ReadMaster_count")
		#		inp = open('SlaveCounts', 'r')
		#		outp = open('Counts_GLOBAL', 'a')

		#		r = inp.readline()
		#		r = r.replace('\n', '')
		#		while r :
		#			w = Sk + '\t' + r + dac10List[skCounter] + '\t' + str(int(time.time())) + '\n'
		#			outp.write(w)
		#			r = inp.readline()
		#		inp.close()
		#		outp.close()
		#		argv = ["mv", "SlaveCounts", "/home/muray/TestCounts/SlaveCounts_" + Sk + "_" + str(dac10)]
		#		subprocess.call(argv)
		#		print ('END\n')
		#		skCounter = skCounter + 1

			#print ('\nAquiring Triggers (5P)...')
			
			#outputF = open('MasterCMD/EN_MUX_EX.txt', 'w')
			#if (stepCounter == 1) : outputF.write('0001\nfff0')
			#if (stepCounter == 2) : outputF.write('0001\neeee')
			#if (stepCounter == 3) : outputF.write('0002\nfff0')
			#if (stepCounter == 4) : outputF.write('0002\neeee')
			#if (stepCounter == 5) : outputF.write('0003\nfff0')
			#if (stepCounter == 6) : outputF.write('0003\neeee')
			#outputF.close()
			
			#if (not(stepCounter == 1) and not(stepCounter == 2)) :
			#	arg = ["./SendFMaster", "MasterCMD/EN_MUX0.txt"]
			#	subprocess.call(arg)
			#if (not(stepCounter == 3) and not(stepCounter == 4)) :
			#	arg = ["./SendFMaster", "MasterCMD/EN_MUX1.txt"]
			#	subprocess.call(arg)
			#if (not(stepCounter == 5) and not(stepCounter == 6)) :
			#	arg = ["./SendFMaster", "MasterCMD/EN_MUX2.txt"]
			#	subprocess.call(arg)
			#arg = ["./SendFMaster", "MasterCMD/EN_MUX3.txt"]
			#subprocess.call(arg)
			#arg = ["./SendFMaster", "MasterCMD/EN_MUX_EX.txt"]
			#subprocess.call(arg)
			#arg = ["./SendFMaster", "MasterCMD/EN_MUX4.txt"]
			#subprocess.call(arg)
		
			#arg = ['./ReadMaster_cTrigger', 'MasterCMD/START_TRG_CNT.txt', 'MasterCMD/RD_TRG_CNT.txt']
			#subprocess.call(arg)
		
			#print ('\nAquiring Counts...')
			#for Sk in skList :
			#	argv = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
			#	subprocess.call(argv)
			#time.sleep(12)
			#print('\n')
			#skCounter = 0
			#for Sk in skList :
			#	argv = ["./SendFSlaves", "Conf/ReadSlave_" + Sk + ".txt"]
			#	subprocess.call(argv)
			#	subprocess.call("./ReadMaster_count")
			#	inp = open('SlaveCounts', 'r')
			#	outp = open('Counts_GLOBAL', 'a')

			#	r = inp.readline()
			#	r = r.replace('\n', '')
			#	while r :
			#		w = Sk + '\t' + r + dac10List[skCounter] + '\t' + str(int(time.time())) + '\n'
			#		outp.write(w)
			#		r = inp.readline()
			#	inp.close()
			#	outp.close()
			#	argv = ["mv", "SlaveCounts", "/home/muray/TestCounts/SlaveCounts_" + Sk + "_" + str(dac10)]
			#	subprocess.call(argv)
			#	print ('END\n')
			#	skCounter = skCounter + 1
			#stepCounter = stepCounter + 1

		arg = ['./SendFMaster', 'MasterCMD/DIAG.txt']
		subprocess.call(arg)

		dac8 = dac8 - 64
		if (dac8 == -1):
			dac8 = 0

	print ('\n--- Shutting Down System\n')
	#for Sk in skList :
		#argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
		#subprocess.call(argv)
		#argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
		#subprocess.call(argv)
		#argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
		#subprocess.call(argv)
