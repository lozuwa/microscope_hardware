import serial
import time
from multiprocessing import Process

s=serial.Serial('/dev/ttyACM0',115200)
c=0

def x_s(pasos,dir,time_):
	s.write(('x,'+str(pasos)+','+str(dir)+','+str(time_)).encode()) # time=500
	time.sleep(0.01)
def y_s(pasos,dir,time_):
	s.write(('y,'+str(pasos)+','+str(dir)+','+str(time_)).encode()) # time=500
	time.sleep(0.01)
def z_s(pasos,dir,time_):
	s.write(('z,'+str(pasos)+','+str(dir)+','+str(time_)).encode()) # time=500
	time.sleep(0.01)
def brigthness(b):
	s.write(('l,'+str(0)+','+str(0)+','+str(0)+','+str(b)).encode())
	time.sleep(0.01)
def auto(time_):
	y_s(2000,1,time_)
	time.sleep(3)
	for i in range(10):
		time.sleep(0.5)
		y_s(2000,0,time_)
		time.sleep(5)
		x_s(30,1,time_)
		time.sleep(0.5)
		y_s(2000,1,time_)
		time.sleep(5)
		x_s(30,1,time_)
def exit():
	s.close()
def proc_H_y():
    while(1):
        s.write(('y,'+str(20)+','+str(0)+','+str(500)).encode())
        time.sleep(0.01)
        #print 'home y'
def proc_H_x():
    while(1):
        s.write(('x,'+str(20)+','+str(1)+','+str(500)).encode())
        time.sleep(0.01)
        #print 'home x'

H_y_ = Process(target=proc_H_y)
H_x_ = Process(target=proc_H_x)

def home():
	global H_y_
	global H_x_
	z_s(5000,0,200)
	time.sleep(3.5)
	H_y_.start()
	print('aqui')
	if (s.readline()[0]==121):
		H_y_.terminate()
	H_y_ = Process(target=proc_H_y)
	time.sleep(0.05)
	H_x_.start()
	if (s.readline()[0]==120):
		time.sleep(0.05)
		H_x_.terminate()
	H_x_ = Process(target=proc_H_x)
	time.sleep(0.5)
	x_s(3000,0,500)
	time.sleep(1.5)
	y_s(1700,1,500)
	time.sleep(4)
	z_s(5000,1,200)
	time.sleep(5)

def cambio():
	global c
	c=c+1
	if c<15:
		y_s(40,1,5000)
	elif c==15:
		x_s(60,1,5000)
	elif c>15 and c<30:
		y_s(40,0,5000)
	elif c==30:
		x_s(60,1,5000)
		c=0
