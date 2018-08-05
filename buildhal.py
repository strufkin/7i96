import os
from datetime import datetime

def buildhal(parent):
	configPath = os.path.join(parent.configsDir, parent.configName.text())
	halFilePath = os.path.join(configPath, parent.configName.text() + '.hal')
	halContents = []
	halContents = ['# This file was created with the 7i96 Wizard on ']
	halContents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	halContents.append('# If you make changes to this file your screwed\n\n')
	# build the standard header
	halContents.append('# kinematics\n')
	halContents.append('loadrt [KINS]KINEMATICS\n\n')
	halContents.append('# motion controller\n')
	halContents.append('loadrt [EMCMOT]EMCMOT ')
	halContents.append('servo_period_nsec=[EMCMOT]SERVO_PERIOD ')
	halContents.append('num_joints=[KINS]JOINTS\n\n')
	halContents.append('# standard components\n')
	halContents.append('loadrt pid num_chan={} \n\n'.format(len(parent.coordinatesL.text())))
	halContents.append('# hostmot2 driver\n')
	halContents.append('loadrt hostmot2\n\n')
	halContents.append('loadrt [HOSTMOT2](DRIVER) ')
	halContents.append('board_ip=[HOSTMOT2](IPADDRESS) ')
	halContents.append('config="num_encoders=[HOSTMOT2](ENCODERS)')
	halContents.append('num_stepgens=[HOSTMOT2](STEPGENS)"')
	halContents.append('sserial_port_0=[HOSTMOT2](SSERIAL_PORT)\n')
	halContents.append('setp hm2_[HOSTMOT2](BOARD).0.watchdog.timeout_ns 25000000\n')
	halContents.append('# THREADS\n')
	halContents.append('addf hm2_[HOSTMOT2](BOARD).0.read servo-thread\n')
	halContents.append('addf motion-command-handler servo-thread\n')
	halContents.append('addf motion-controller servo-thread\n')
	halContents.append('addf pid.0.do-pid-calcs servo-thread\n')
	halContents.append('addf hm2_[HOSTMOT2](BOARD).0.write servo-thread\n')
	for index in range(len(parent.coordinatesL.text())):
		halContents.append('# Joint {0}\n\n'.format(str(index)))
		halContents.append('# axis enable chain\n')
		halContents.append('newsig emcmot.{0}.enable bit\n'.format(str(index)))
		halContents.append('sets emcmot.{0}.enable FALSE\n\n'.format(str(index)))
		halContents.append('net emcmot.{0}.enable <= joint.{0}.amp-enable-out\n'.format(str(index)))
		halContents.append('net emcmot.{0}.enable => hm2_[HOSTMOT2](BOARD).{0}.stepgen.{0}.enable pid.{0}.enable\n\n'.format(str(index)))
		halContents.append('# position command and feedback\n')
		halContents.append('net emcmot.{0}.pos-cmd joint.{0}.motor-pos-cmd => pid.{0}.command\n'.format(str(index)))
		halContents.append('net emcmot.{0}.vel-cmd joint.{0}.vel-cmd => pid.{0}.command-deriv\n'.format(str(index)))
		halContents.append('net motor.{0}.pos-fb <= hm2_[HOSTMOT2](BOARD).{0}.stepgen.{0}.position-fb joint.{0}.motor-pos-fb pid.{0}.feedback\n'.format(str(index)))
		halContents.append('net motor.{0}.command pid.{0}.output hm2_[HOSTMOT2](BOARD).{0}.stepgen.{0}.velocity-cmd\n'.format(str(index)))
		halContents.append('setp pid.{0}.error-previous-target true\n'.format(str(index)))

		halContents.append('\n')

	"""
		halContents.append('\n')
		halContents.append('\n'.format(str(index)))
	"""

	halContents.append('# Standard I/O Block - EStop, Etc\n\n')
	halContents.append('# create a signal for the estop loopback\n')
	halContents.append('net estop-loop iocontrol.0.user-enable-out => iocontrol.0.emc-enable-in\n\n')
	halContents.append('# create signals for tool loading loopback\n')
	halContents.append('net tool-prep-loop iocontrol.0.tool-prepare => iocontrol.0.tool-prepared\n')
	halContents.append('net tool-change-loop iocontrol.0.tool-change => iocontrol.0.tool-changed\n')

	with open(halFilePath, 'w') as halFile:
		halFile.writelines(halContents)
	return True

def buildtool(parent):
	configPath = os.path.join(parent.configsDir, parent.configName.text())
	toolFilePath = os.path.join(configPath, parent.configName.text() + '.tbl')
	toolContents = []
	toolContents = [';\n']
	toolContents.append('T1 P1\n')
	try:
		with open(toolFilePath, 'x') as toolFile:
			toolFile.writelines(toolContents)
	except FileExistsError:
		pass

	return True

def buildvar(parent): #just create an empty file if it does not exist
	configPath = os.path.join(parent.configsDir, parent.configName.text())
	varFilePath = os.path.join(configPath, parent.configName.text() + '.var')
	try:
		open(varFilePath, 'x')
	except FileExistsError:
		pass

	return True
