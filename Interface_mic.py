import serial
import time
s=serial.Serial('/dev/ttyACM0',115200)

def x_f(pasos,dir, time_):
	s.write('x,'+str(pasos)+','+str(dir)+','+str(time_)) # time=250
	time.sleep(0.01)
def x_s(pasos,dir,time_):
	s.write(bytes('x,'+str(pasos)+','+str(dir)+','+str(time_))) # time=500
	time.sleep(0.09)
def x_ss(pasos,dir):
	s.write('x,'+str(pasos)+','+str(dir)+','+str(1000))
	time.sleep(0.01)
def x_sss(pasos,dir):
	s.write('x,'+str(pasos)+','+str(dir)+','+str(2000))
	time.sleep(0.01)
def y_f(pasos,dir):
	s.write('y,'+str(pasos)+','+str(dir)+','+str(250))
	time.sleep(0.01)
def y_s(pasos,dir,time_):
	s.write('y,'+str(pasos)+','+str(dir)+','+str(time_)) # time=500
	time.sleep(0.01)
def y_ss(pasos,dir):
	s.write('y,'+str(pasos)+','+str(dir)+','+str(1000))
	time.sleep(0.01)
def y_sss(pasos,dir):
	s.write('y,'+str(pasos)+','+str(dir)+','+str(2000))
	time.sleep(0.01)
def z_f(pasos,dir):
	s.write('z,'+str(pasos)+','+str(dir)+','+str(250))
	time.sleep(0.01)
def z_s(pasos,dir,time_):
	s.write('z,'+str(pasos)+','+str(dir)+','+str(time_)) #time=500
	time.sleep(0.01)
def z_ss(pasos,dir):
	s.write('z,'+str(pasos)+','+str(dir)+','+str(1000))
	time.sleep(0.01)
def z_sss(pasos,dir):
	s.write('z,'+str(pasos)+','+str(dir)+','+str(2000))
	time.sleep(0.01)
def brigthness(b):
	s.write('l,'+str(0)+','+str(0)+','+str(0)+','+str(b))
	time.sleep(0.01)
