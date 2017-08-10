# Author: Khalil Nallar
# Company: pfm medical
# Description: Supporting functions for microscope movement

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
	def __init__(self):
		# Other classes inst
		self.serPortClass = serialPort(portNumber = 0, baudrate = 115200)
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
		time.sleep(0.01)
		self.wait()

	def moveField(self, dir):
		campos = 40
		if dir == 0:
			self.fieldCounter -= 1
			if self.fieldCounter < campos-1 and self.fieldCounter != -1:
				self.x(40,0,5000)
			elif self.fieldCounter == campos-1:
				self.y(80,1,5000)
			elif self.fieldCounter > campos-1 and self.fieldCounter < (campos*2)-1:
				self.x(40,1,5000)
			elif self.fieldCounter == -1:
				self.y(90,1,5000)
				self.fieldCounter = 0
		elif dir:
			self.fieldCounter += 1
			if self.fieldCounter < campos:
				self.x(40,1,5000)
			elif self.fieldCounter == campos:
				self.y(30,0,4000)
			elif self.fieldCounter > campos and self.fieldCounter < campos*2:
				self.x(40,0,5000)
			elif self.fieldCounter == campos*2:
				self.y(60,0,4000)
				self.fieldCounter = 0

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
		self.y_response(1400,1,150)
		self.x_response(1300,1,300)
		self.z_response(15000,1,300)

		### Support functions ###
	def wait(self):
		counter = 0
		time.sleep(0.01)
		k = self.serPort.read().decode("utf-8")
		#print(k)
		while (k != "o"):
			#print(k)
			counter += 1
			if counter == 600: # 6 seconds timeout
				print("Counter exceeded")
				break
			k = self.serPort.read().decode("utf-8")
			time.sleep(0.01)
		print(k)

	def writeLed(self, ledState):
		self.serPort.write(('l,'+str(0)+','+str(0)+','+str(0)+','+str(ledState)).encode())
