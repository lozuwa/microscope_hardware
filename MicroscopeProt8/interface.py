"""
Author: Khalil Nallar
Company: pfm medical
Description: Supporting functions for microscope"s movement feature
"""
# General purpose
import os
import sys
import time
# Serial port
import serial
import serial.tools.list_ports
# Regular expressions
import re
# Threads
from multiprocessing import Process
# Support libraries
from utils import *

class serialPort:
	"""
	Creates an instance of a serial port
	"""
	def __init__(self,
				portNumber = 0,
				baudrate = 115200):
		"""
		Constructor
		:param portNumber: input int that defines the number of the port 
							to connect to. 
		:param baudrate: input int that defines the baudrate
		"""
		# Assert variables
		assert type(portNumber) == int, VARIABLE_IS_NOT_INT
		assert type(baudrate) == int, VARIABLE_IS_NOT_INT
		# Instantiate variables
		self.portNumber = "".join(["/dev/ttyACM", str(portNumber)])
		self.baudrate = int(baudrate)
		self.startPort()

	def startPort(self):
		"""
		Creates a binding with the physical serial port
		"""
		try:
			self.port = serial.Serial(self.portNumber, self.baudrate)
		except:
			raise Exception("Problem with serial port. Port: {}, baudrate: {}".format(self.portNumber, self.baudrate))

	def closePort(self):
		"""
		Closes connection to serial port
		"""
		try:
			self.port.close()
		except:
			raise Exception("Could not close serial port")

	def getAvailablePorts(self,\
							filter):
		"""
		Prints all the available ports
		:param filter: input int that filters a keyword
		"""
		# Get all the available ports
		ports = list(serial.tools.list_ports.comports())
		# Find the relevant port
		for port in ports:
			port = str(port)
			print(port)

	def setPortNumber(self,\
						portNumber):
		"""
		Setter port number
		"""
		self.portNumber = portNumber

	def getPortNumber(self,\
						portNumber):
		"""
		Getter portnumber
		"""
		return self.portNumber

	def setBaudrate(self,\
					baudrate):
		"""
		Setter portnumber
		"""
		self.baudrate = baudrate

	def getBaudrate(self,\
					baudrate):
		"""
		Getter baudrate
		"""
		return self.baudrate

"""
Led class
"""
class Led:
	def __init__(self,\
					state):
		"""
		Defines the state of the led
		"""
		self.state = int(state)

	def setState(self,\
					state):
		self.state = int(state)

	def getState(self):
		return self.state

"""
Interface to xy movement
"""
class axisMovement:
	def __init__(self,\
				port = 0):
		"""
		Constructor
		:param port: input int that defines the serial port
		"""
		# Other classes inst
		self.serPortClass = serialPort(portNumber = port,\
										baudrate = 115200)
		self.serPort = self.serPortClass.port
		self.led = Led(state = 0)
		# Variables
		self.fieldCounter = 0

	def x(self,\
			steps,\
			dir,\
			time_):
		self.serPort.write(("x,"+str(steps)+","+str(dir)+","+str(time_)).encode())
		time.sleep(0.01)

	def xResponse(self,\
					steps,\
					dir,\
					time_):
		self.serPort.write(("x,"+str(steps)+","+str(dir)+","+str(time_)).encode())
		time.sleep(0.01)
		result, code = self.wait()
		print("Hardware code: {}".format(code))

	def y(self,\
			steps,\
			dir,\
			time_):
		self.serPort.write(("y,"+str(steps*2)+","+str(dir)+","+str(time_)).encode())
		time.sleep(0.01)

	def yResponse(self,\
					steps,\
					dir,\
					time_):
		self.serPort.write(("y,"+str(steps*2)+","+str(dir)+","+str(time_)).encode())
		time.sleep(0.01)
		result, code = self.wait()
		print("Hardware code: {}".format(code))

	def z(self,\
			steps,\
			dir,\
			time_):
		self.serPort.write(("z,"+str(steps)+","+str(dir)+","+str(time_)).encode())
		time.sleep(0.01)

	def zResponse(self,\
					steps,\
					dir,\
					time_,\
					hardwareCode = "o"):
		#self.serPort.write(("z_r,"+str(steps)+","+str(dir)+","+str(time_)).encode())
		self.serPort.write(("z,"+str(steps)+","+str(dir)+","+str(time_)).encode())
		result, code = self.wait(code = hardwareCode)
		print("Hardware code: {}".format(code))
		return code

	def moveFieldY(self,\
					dir):
		if dir == 0:
			self.yResponse(10, 0, 5000)
		elif dir == 1:
			self.yResponse(10, 1, 5000)
		else:
			pass

	def moveFieldX(self,\
					dir):
		if dir == 0:
			self.xResponse(10, 0, 5000)
		elif dir == 1:
			self.xResponse(10, 1, 5000)
		else:
			pass

	def homeZTop(self):
		self.serPort.write("homeZTop".encode())
		self.wait()

	def homeZBottom(self):
		self.serPort.write("homeZBottom".encode())
		self.wait()

	def homeX(self):
		self.serPort.write("homeX".encode())
		self.wait()

	def homeY(self):
		self.serPort.write("homeY".encode())
		self.wait()

	def wait(self,\
			code = "o"):
		"""
		Support function that creates a response interface with 
		the serial port
		:param code: input string that defines the break condition
		"""
		counter = 0
		time.sleep(0.01)
		k = self.serPort.read().decode("utf-8")
		while (True):
			print("here")
			counter += 1
			if k == code or k == "t" or k == "d" or counter == 600:
				break
			else:
				k = self.serPort.read().decode("utf-8")
				time.sleep(0.01)
		print("wait function: ", k)
		return ("done", k)

	def writeLed(self,\
				ledState):
		self.serPort.write(("l,"+str(0)+","+str(0)+","+\
						str(0)+","+str(ledState)).encode())
