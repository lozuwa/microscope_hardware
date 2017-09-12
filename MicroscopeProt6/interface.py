# Author: Khalil Nallar
# Company: pfm medical
# Description: Supporting functions for microscope's movement feature

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
		self.serPort.write(('z_r,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		result, code = self.wait()
		#print("Hardware code: {}".format(code))
		return code

	def zUp(self, steps = 250, dir = 1, time_ = 250):
		self.serPort.write(('zUp,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		result, code = self.wait()
		return code

	def moveField(self, dir):
		campos = 80
		print(self.fieldCounter)
		if dir == 0:
			self.fieldCounter += 1
			self.x(40,0,5000)
			if self.fieldCounter == campos:
				self.y(60,0,4000)
				self.fieldCounter = 0
		elif dir == 1:
			self.fieldCounter -= 1
			self.x(40,1,5000)

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
		self.serPort.write(('l,'+str(0)+','+str(0)+','+str(0)+','+str(ledState)).encode())
