"""
Author: Khalil Nallar
Company: pfm medical
Description: Supporting functions for microscope's movement feature
"""

import serial
import os, sys, time
from multiprocessing import Process

### Serial Port ###
class serialPort:
	def __init__(self, portNumber, baudrate):
		self.portNumber = '/dev/ttyACM' + str(portNumber)
		self.baudrate = int(baudrate)
		self.startPort()

	def startPort(self):
		try:
			self.port = serial.Serial(self.portNumber, self.baudrate)
		except:
			raise Exception('Problem with serial port. Port: {}, baudrate: {}'.format(self.portNumber, self.baudrate))

	def closePort(self):
		try:
			self.port.close()
		except:
			raise Exception('Could not close serial port')

	def set_portNumber(self, portNumber):
		self.portNumber = portNumber

	def get_portNumber(self, portNumber):
		return self.portNumber

	def set_baudrate(self, baudrate):
		self.baudrate = baudrate

	def get_baudrate(self, baudrate):
		return self.baudrate

### Led ###
class Led:
	def __init__(self, state):
		self.state = int(state)

	def set_state(self, state):
		self.state = int(state)

	def get_state(self):
		return self.state

### Individual axis move ###
class axisMovement:
	def __init__(self, port = 0):
		# Other classes inst
		self.serPortClass = serialPort(portNumber = port, baudrate = 115200)
		self.serPort = self.serPortClass.port
		self.led = Led(state = 0)
		# Variables
		self.fieldCounter = 0

	def x(self, steps, dir, time_):
		self.serPort.write(('x,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)

	def xResponse(self, steps, dir, time_):
		self.serPort.write(('x,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)
		self.wait()

	def y(self, steps, dir, time_):
		self.serPort.write(('y,'+str(steps*2)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)

	def yResponse(self, steps, dir, time_):
		self.serPort.write(('y,'+str(steps*2)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)
		self.wait()

	def z(self, steps, dir, time_):
		self.serPort.write(('z,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)

	def zResponse(self, steps, dir, time_):
		#self.serPort.write(('z_r,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		self.serPort.write(('z,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		result, code = self.wait()
		print("Hardware code: {}".format(code))
		return code

	def zUp(self, steps = 250, dir = 1, time_ = 250):
		self.serPort.write(('zUp,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		result, code = self.wait()
		return code

	def moveFieldY(self, dir):
		if dir == 0:
			self.y(10, 0, 5000)
		elif dir == 1:
			self.y(10, 1, 5000)
		else:
			pass

	def moveFieldX(self, dir):
		if dir == 0:
			self.x(10, 0, 5000)
		elif dir == 1:
			self.x(10, 1, 5000)
		else:
			pass

	def homeZ(self):
		self.serPort.write('homeZ'.encode())
		self.wait()

	def homeX(self):
		self.serPort.write('homeX'.encode())
		self.wait()

	def homeY(self):
		self.serPort.write('homeY'.encode())
		self.wait()

	### HOME ###
	def home(self):
		# Reset input buffer
		self.serPort.flushInput()
		# Reset movefield counter
		k = 0
		self.fieldCounter = 0
		# Turn on led
		self.led.set_state(1)
		ledState = self.led.get_state()
		self.writeLed(ledState)
		time.sleep(0.2)
		# Restart the axis
		self.homeZ()
		self.homeX()
		self.homeY()
		# Move axis to intial position
		self.y(1400,1,150)
		time.sleep(2)
		self.x(1300,1,300)
		time.sleep(2)
		self.zResponse(3500,1,300)

	### Support functions ###
	def wait(self, code = "o"):
		counter = 0
		time.sleep(0.01)
		k = self.serPort.read().decode("utf-8")
		while (True):
			counter += 1
			if k == code or k == "u" or counter == 600:
				break
			else:
				k = self.serPort.read().decode("utf-8")
				time.sleep(0.01)
		#print("wait function: ", k)
		return ("done", k)

	def writeLed(self, ledState):
		self.serPort.write(('l,'+str(0)+','+str(0)+','+\
						str(0)+','+str(ledState)).encode())

"""
##################################################################################
        elif msg.topic == AUTOFOCUS_TOPIC:
            print(msg.topic, msg.payload)
            if msg.payload.decode("utf-8") == "start":
                axMov.homeZ()
                time.sleep(0.5)
                autofocusState = True
                countFrames = 0
        ##################################################################################
        elif msg.topic == VARIANCE_TOPIC:
            if autofocusState:
                if hardwareCode != "u":
                    if countFrames < 1:
                        print(msg.payload)
                        saveAutofocusCoef.append((countPositions, float(msg.payload)))
                        countFrames += 1
                    else:
                        hardwareCode = axMov.zResponse(500, 1, 1000)
                        print("Hardware (mqtt) code: {}".format(hardwareCode))
                        countPositions += 1
                        countFrames = 0
                else:
                    autofocusState = False
                    hardwareCode = "o"
                    publishMessage(AUTOFOCUS_TOPIC, "stop")
                    aut = autofocus(saveAutofocusCoef)
                    pos = aut.focus()
                    print(saveAutofocusCoef)
                    print("Need to go back {} positions".format(pos))
                    if pos >= 0:
                        for i in range(pos):
                            print("Going back {}".format(i))
                            hardwareCode = axMov.zResponse(250,0,500)
"""
