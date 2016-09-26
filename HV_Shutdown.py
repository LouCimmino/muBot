import sys
import os
import subprocess
import time

skList = ['2', '3', '13', '9', '5', '0', '17', '7', '8', '12', '4', '1']
#skList = ['2', '3', '13', '14', '5', '0', '16', '11', '8', '12', '4', '6']

print ('\n--- Shutting Down System\n')
for Sk in skList :
	#argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
	#subprocess.call(argv)
	argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
	subprocess.call(argv)
	argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
	subprocess.call(argv)
