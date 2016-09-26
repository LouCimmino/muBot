import sys
import os
import subprocess
import time

skList = ['2', '3', '13', '9', '5', '0', '17', '7', '8', '12', '4', '1']
#dac10List = ['435', '610', '550', '465', '610', '480', '560', '465', '840', '810', '475', '550']
#dac10List = ['552','632','584','601','630','600','567','572','831','823','601','573'] #4th 0100
#dac10List = ['632','694','649','670','700','666','641','641','851','843','671','631'] #3rd 0100
#dac10List = ['488','569','522','529','563','528','500','508','812','805','529','511'] #5th 0100
#dac10List = ['483','572','516','512','566','528','497','503','826','821','525','512'] #4th 0010
#dac10List = ['483','572','516','512','566','528','497','503','795','768','525','512'] #4th 0010 EASI & 4th 0001 Sp0
dac10List = ['494','555','502','524','550','505','527','498','802','768','511','492'] #4th 0010 EASI & 5th 0010 67V Sp0 18C
#dac10List = ['483','572','516','512','566','528','497','503','796','768','525','512'] #4th 0010 EASI & 5th 0010 67V Sp0
#dac10List = ['569','649','601','610','647','611','578','579','846','841','621','588'] #3th 0010
#dac10List = ['409','507','438','429','490','456','414','431','809','800','448','436'] #5th 0010
#dmaskList = [sys.argv[1], sys.argv[2], sys.argv[3]]

#dac10List = ['576', '634', '590', '627', '635', '599', '608', '569', '851', '820', '600', '567'] #3th 18C
#dac10List = ['493', '550', '500', '546', '543', '510', '530', '497', '827', '796', '513', '490'] #4th 18C
#dac10List = ['409', '481', '423', '449', '464', '432', '458', '407', '800', '768', '430', '423'] #5th 18C
#dac10List = ['339', '414', '353', '377', '390', '365', '385', '344', '779', '737', '359', '356'] #6th 18C
#dac10List = ['265', '344', '273', '297', '310', '285', '315', '274', '759', '709', '279', '286'] #7h 18C

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
		
		inputF = open('Conf/EASI_Slow_Control_12.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		#s[10] = '0340\n'
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

		#inputF = open('Conf/EASI_Slow_Control_8.txt', 'r')
		#s = inputF.readlines()
		#inputF.close()
		#s[10] = '0340\n'
		#outputF = open('Conf/EASI_Slow_Control_8.txt', 'w')
		#for line in s:
		#	outputF.write(line)
		#outputF.close()

		inputF = open('Conf/EASI_Slow_Control_13.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[4] = 'fff9\n'
		outputF = open('Conf/EASI_Slow_Control_13.txt', 'w')
		for line in s:
			outputF.write(line)
		outputF.close()

		#for Sk in dmaskList :
		#	inputF = open('Conf/EASI_Slow_Control_' + Sk + '.txt', 'r')
		#	s = inputF.readlines()
		#	inputF.close()
		#	s[3] = 'ffe3\n'
		#	outputF = open('Conf/EASI_Slow_Control_' + Sk + '.txt', 'w')
		#	for line in s:
		#		outputF.write(line)
		#	outputF.close()

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

			if (dac8 == 255):
				argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
				subprocess.call(argv)
				argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
				subprocess.call(argv)
				argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
				subprocess.call(argv)
			print('\n')
		stepCounter = 1
		
		print ('\nAquiring Triggers (6P)...')
		
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
						
		#for cicla in range(0,25,1):
		arg = ['./ReadMaster_cTrigger', '61', 'MasterCMD/START_TRG_CNT_60.txt', 'MasterCMD/RD_TRG_CNT.txt']
		subprocess.call(arg)

		subprocess.call("./Reset")
		
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL0.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL1.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL2.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL3.txt"]
		#subprocess.call(arg)
		
		#arg = ['./ReadMaster_cTrigger_DLY', '60', 'MasterCMD/START_TRG_CNT_60.txt', 'MasterCMD/RD_TRG_CNT.txt']
		#subprocess.call(arg)
		
		#subprocess.call("./Reset")

		print ('\nAquiring Counts...')
		for Sk in skList :
			argv = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
			subprocess.call(argv)
		time.sleep(12)
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
			argv = ["mv", "SlaveCounts", "/home/muray/EffCounts/SlaveCounts_" + Sk + "_" + str(dac10)]
			subprocess.call(argv)
			print ('END\n')
			skCounter = skCounter + 1

		#while (stepCounter < 7):
		while (stepCounter < 0):
			print ('\nAquiring Triggers (5P)...')
			
			outputF = open('MasterCMD/EN_MUX_EX.txt', 'w')
			if (stepCounter == 1) : outputF.write('0001\nfff0')
			if (stepCounter == 2) : outputF.write('0001\neeee')
			if (stepCounter == 3) : outputF.write('0002\nfff0')
			if (stepCounter == 4) : outputF.write('0002\neeee')
			if (stepCounter == 5) : outputF.write('0003\nfff0')
			if (stepCounter == 6) : outputF.write('0003\neeee')
			outputF.close()
			
			if (not(stepCounter == 1) and not(stepCounter == 2)) :
				arg = ["./SendFMaster", "MasterCMD/EN_MUX0.txt"]
				subprocess.call(arg)
			else :
				arg = ["./SendFMaster", "MasterCMD/EN_MUX_EX.txt"]
				subprocess.call(arg)
				
			if (not(stepCounter == 3) and not(stepCounter == 4)) :
				arg = ["./SendFMaster", "MasterCMD/EN_MUX1.txt"]
				subprocess.call(arg)
			else :
				arg = ["./SendFMaster", "MasterCMD/EN_MUX_EX.txt"]
				subprocess.call(arg)

			if (not(stepCounter == 5) and not(stepCounter == 6)) :
				arg = ["./SendFMaster", "MasterCMD/EN_MUX2.txt"]
				subprocess.call(arg)
			else :
				arg = ["./SendFMaster", "MasterCMD/EN_MUX_EX.txt"]
				subprocess.call(arg)

			arg = ["./SendFMaster", "MasterCMD/EN_MUX3.txt"]
			subprocess.call(arg)
			arg = ["./SendFMaster", "MasterCMD/EN_MUX4.txt"]
			subprocess.call(arg)
		
			#for cicla in range(0,25,1):
			arg = ['./ReadMaster_cTrigger', '300', 'MasterCMD/START_TRG_CNT_300.txt', 'MasterCMD/RD_TRG_CNT.txt']
			subprocess.call(arg)

			subprocess.call("./Reset")
		
			arg = ["./SendFMaster", "MasterCMD/EN_DEL0.txt"]
			subprocess.call(arg)
			arg = ["./SendFMaster", "MasterCMD/EN_DEL1.txt"]
			subprocess.call(arg)
			arg = ["./SendFMaster", "MasterCMD/EN_DEL2.txt"]
			subprocess.call(arg)
			arg = ["./SendFMaster", "MasterCMD/EN_DEL3.txt"]
			subprocess.call(arg)
		
			arg = ['./ReadMaster_cTrigger_DLY', '60', 'MasterCMD/START_TRG_CNT_60.txt', 'MasterCMD/RD_TRG_CNT.txt']
			subprocess.call(arg)
		
			subprocess.call("./Reset")
	
			print ('\nAquiring Counts...')
			for Sk in skList :
				argv = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
				subprocess.call(argv)
			time.sleep(12)
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
				argv = ["mv", "SlaveCounts", "/home/muray/EffCounts/SlaveCounts_" + Sk + "_" + str(dac10)]
				subprocess.call(argv)
				print ('END\n')
				skCounter = skCounter + 1
			stepCounter = stepCounter + 1

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
