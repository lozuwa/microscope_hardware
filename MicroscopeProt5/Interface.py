# Author: Khalil Nallar
# Company: pfm medical
# Description: Supporting functions for microscope movement

# Hardware interface
import serial
# General purpose
import os
import sys
import time
# Threads 
from multiprocessing import Process

### Global variables ###
s = serial.Serial("COM4", 115200)#'/dev/ttyACM0',115200)
c = 0

### Move ###
def x(pasos,dir,time_):
	s.write(('x,'+str(pasos)+','+str(dir)+','+str(time_)).encode())
	time.sleep(0.01)

def y(pasos,dir,time_):
	s.write(('y,'+str(pasos*2)+','+str(dir)+','+str(time_)).encode())
	time.sleep(0.01)

def z(pasos,dir,time_):
	s.write(('z,'+str(pasos)+','+str(dir)+','+str(time_)).encode())
	time.sleep(0.01)

def brigthness(b):
	s.write(('l,'+str(0)+','+str(0)+','+str(0)+','+str(b)).encode())
	time.sleep(0.01)

def exit():
	s.close()

def homeZ():
	s.write('homeZ'.encode())

def homeX():
	s.write('homeX'.encode())

def homeY():
	s.write('homeY'.encode())

def home():
	s.flushInput()
	global c
	k=0
	brigthness(255)
	time.sleep(0.2)

	homeZ()
	wait('z')

	homeX()
	wait('x')

	homeY()
	wait('y')

	y(1400,1,150)
	time.sleep(2)
	print ('1')
	x(1300,1,300)
	time.sleep(1)
	print ('2')
	z(15000,1,300)
	print ('ok')
	c=0

def change(dir):
        global c
        campos = 40
        if dir == 0:
            c -= 1
            if c < campos-1 and c!=-1:
                x(40,0,5000)
            elif c == campos-1:
                y(80,1,5000)
            elif c > campos-1 and c < (campos*2)-1:
                x(40,1,5000)
            elif c == -1:
                y(90,1,5000)
                c = 0
        elif dir:
            c += 1
            if c < campos:
                x(40,1,5000)
            elif c == campos:
                y(30,0,4000)
            elif c > campos and c < campos*2:
                x(40,0,5000)
            elif c == campos*2:
                y(60,0,4000)
                c = 0

def wait(axis):
	while(chr(s.read()[0])!=axis):
		continue
	time.sleep(0.1)
