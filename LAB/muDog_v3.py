import sys
import os
import subprocess
import time
import serial

#inputF = open('EASIb_form.c', 'r')
#outputF = open('a.out', 'w')
#s = inputF.readline()
#while s:
#	outputF.write(s)
#	if ('//DAC8' in s):
#		outputF.write('for (i=0; i<32; i++) error = DACbiasSC_EASI(SC_EASI, i, ' + str(dac8) + ');')
#		outputF.write('\n')	
#		s = inputF.readline()
#	if ('//CHNL' in s):
#		outputF.write('DISCRmaskSC_EASI(SC_EASI, ' + str(kk) + ', 1);')
#		outputF.write('\n')
#		s = inputF.readline()
#	s = inputF.readline()
#inputF.close()
#outputF.close()
#arg = ["mv", "a.out", "EASIb_form.c"]
#subprocess.call(arg)
arg = ["gcc", "-O2", "EASIb_form.c", "EASIb_const.c"]
subprocess.call(arg)
subprocess.call("./a.out")
arg = ["rm", "a.out"]
subprocess.call(arg)

subprocess.call("./EASIsub/Init")
subprocess.call("./EASIsub/ResetSlaves")
arg = ["./EASIsub/SendFSlaves", "EASIconf/EASI_Probe.txt"]
subprocess.call(arg)
arg = ["./EASIsub/SendFSlaves", "/home/muray/MUBOT/TestConf/EASI_Hold_Pot_46ns.txt"]
subprocess.call(arg)
arg = ["./EASIsub/SendFSlaves", "/home/muray/MUBOT/TestConf/EASI_TimeOut_Pot_300ns.txt"]
subprocess.call(arg)
arg = ["./EASIsub/SendFMaster", "/home/muray/MUBOT/MasterCMD/MUX_TEST_TRIG.txt"]
subprocess.call(arg)
arg = ["./EASIsub/SendFSlaves", "EASIconf/EASI_Slow_Control.txt"]
subprocess.call(arg)
argv = ["./EASIsub/SendHV_NORUMP", "/home/muray/MUBOT/TestConf/EASI_HV-OUT_ShutDown.txt"]
subprocess.call(argv)
argv = ["./EASIsub/SendFSlaves", "/home/muray/MUBOT/TestConf/EASI_SwHV_ON.txt"]
subprocess.call(argv)
			
print ("---> System Ready!\n")

input('\n*** PRESS ENTER TO SHUTDOWN\n')

print ('\n--- Shutting Down System\n')
	
argv = ["./EASIsub/SendHV_NORUMP", "/home/muray/MUBOT/TestConf/EASI_HV-OUT_ShutDown.txt"]
subprocess.call(argv)
argv = ["./EASIsub/SendFSlaves", "/home/muray/MUBOT/TestConf/EASI_SwHV_OFF.txt"]
subprocess.call(argv)
