# Author: Khalil Nallar
# Company: pfm medical
# Description: Supporting functions for microscope movement

import serial
import os, sys, time
from multiprocessing import Process

# Global variables
s = serial.Serial('/dev/ttyACM0',115200)
c = 0
TIME_HOME = 200

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
	global c
	brigthness(255)
	time.sleep(0.2)
	homeZ()
	time.sleep(6)
	print ('z')
	homeX()
	time.sleep(2)
	print ('x')
	homeY()
	time.sleep(2)
	print ('y')
	y(3000,1,150)
	time.sleep(2)
	print ('2')
	x(1300,1,300)
	time.sleep(1)
	print ('2')
	z(20000,1,300)
	print ('ok')
	c=0
def change(dir):
        global c
        campos = 30
        if dir == 0:
            c -= 1
            if c < campos:
                x(40,0,5000)
            elif c == campos:
                y(80,1,5000)
            elif c > campos and c < campos*2:
                x(40,1,5000)
            elif c == campos*2:
                y(120,1,5000)
                c = 0
        elif dir:
            c += 1
            if c < campos:
                x(40,1,5000)
            elif c == campos:
                y(80,0,5000)
            elif c > campos and c < campos*2:
                x(40,0,5000)
            elif c == campos*2:
                y(120,0,5000)
                c = 0
