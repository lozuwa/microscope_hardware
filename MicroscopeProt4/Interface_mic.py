import serial
import time
s=serial.Serial('/dev/ttyACM0',115200)

def x_s(pasos,dir,time_):
	s.write('x,'+str(pasos)+','+str(dir)+','+str(time_)) # time=500
	time.sleep(0.01)
def y_s(pasos,dir,time_):
	s.write('y,'+str(pasos)+','+str(dir)+','+str(time_)) # time=500
	time.sleep(0.01)
def z_s(pasos,dir,time_):
	s.write('z,'+str(pasos)+','+str(dir)+','+str(time_)) # time=500
	time.sleep(0.01)
def brigthness(b):
	s.write('l,'+str(0)+','+str(0)+','+str(0)+','+str(b))
	time.sleep(0.01)
def auto(time_):
	y_s(1000,1,time_)
	for i in range(10):
		time.sleep(1)
		y_s(2000,0,time_)
		time.sleep(1.5)
		x_s(30,1,time_)
		time.sleep(0.5)
		y_s(2000,1,time_)
		time.sleep(1.5)
		x_s(30,1,time_)
def proc_H_x():
    while(1):
        s.write('x,'+str(20)+','+str(1)+','+str(500))
		time.sleep(0.01)
def proc_H_y():
    while(1):
        s.write('y,'+str(20)+','+str(1)+','+str(500))
		time.sleep(0.01)

H_x_ = Process(target=proc_H_x)
H_y_ = Process(target=proc_H_y)

def home():
	H_x_.start()
	while 1:
		if (s.readline()[0]=='x'):
			break
	H_x_.terminate()
	H_y_.start()
	while 1:
		if (s.readline()[0]=='y'):
			break
	H_y_.terminate()