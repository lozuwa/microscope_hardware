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
		