# Author: Khalil Nallar
# Company: pfm medical
# Description: Supporting functions for microscope movement

import serial
import os, sys, time
from multiprocessing import Process

### Global variables ###
#s = serial.Serial('/dev/ttyACM0',115200)
#c = 0

class serialPort:
	def __init__(self, portNumber = 0, baudrate = 115200):
		self.portNumber = '/dev/ttyACM' + str(portNumber)
		self.baudrate = int(baudrate)
		startPort()

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

### Individual axis move ###
class axisMovement:
	def __init__(self):
		self.s = serialPort(portNumber = 0, baudrate = 115200)
		self.c = 0
		
	def x(self, steps, dir, time_):
		self.s.write(('x,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)

	def x_response(self, steps, dir, time_):
		self.s.write(('x,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)
		wait()

	def y(self, steps, dir, time_):
		self.s.write(('y,'+str(steps*2)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)

	def y_response(self, steps, dir, time_):
		self.s.write(('y,'+str(steps*2)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)
		wait()

	def z(self, steps, dir, time_):
		self.s.write(('z,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)

	def z_response(self, steps, dir, time_):
		self.s.write(('z,'+str(steps)+','+str(dir)+','+str(time_)).encode())
		time.sleep(0.01)
		self.wait()

	def change(self, dir):
		campos = 40
		if dir == 0:
			self.c -= 1
			if self.c < campos-1 and self.c != -1:
				self.x(40,0,5000)
			elif self.c == campos-1:
				self.y(80,1,5000)
			elif self.c > campos-1 and self.c < (campos*2)-1:
				self.x(40,1,5000)
			elif self.c == -1:
				self.y(90,1,5000)
				self.c = 0
			elif dir:
				self.c += 1
				if self.c < campos:
					self.x(40,1,5000)
				elif self.c == campos:
					self.y(30,0,4000)
				elif self.c > campos and self.c < campos*2:
					self.x(40,0,5000)
				elif self.c == campos*2:
					self.y(60,0,4000)
					self.c = 0

	def homeZ(self):
		s.write('homeZ'.encode())

	def homeX(self):
		s.write('homeX'.encode())

	def homeY(self):
		s.write('homeY'.encode())

	### Support functions ###
	def wait(self):
		counter = 0
		time.sleep(0.01)
		k = self.s.read().decode("utf-8")
		#print(k)
		while (k != "o"):
			#print(k)
			counter += 1
			if counter == 600: # 6 seconds timeout
				print("Counter exceeded")
				break
			k = self.s.read().decode("utf-8")
			time.sleep(0.01)
		print(k)

### HOME ###
def home():
	global c

	# Reset input buffer
	s.flushInput()
	# Reset movefield counter
	k = 0
	c = 0
	# Turn on led
	brigthness(1)
	time.sleep(0.2)

	# Restart the axis
	homeZ()
	wait()

	homeX()
	wait()

	homeY()
	wait()

	y(1400,1,150)
	time.sleep(2)
	print ('y ok')
	x(1300,1,300)
	time.sleep(1)
	print ('x ok')
	z(15000,1,300)
	print ('z ok')

### Led ###
def brigthness(b):
	s.write(('l,'+str(0)+','+str(0)+','+str(0)+','+str(b)).encode())
	time.sleep(0.01)
