"""
Author: Rodrigo Loza
Company: pfm 
Description: Main program for microscope's hardware
"""
# General purpose
import os
import time
import datetime
# Tensor manipulation
import numpy as np
# Thread
from multiprocessing import Process
from multiprocessing import Pool
# Support classes 
from interface import *

def moveFieldZUp(message):
    global procZUp
    if int(message) == 1:
        procZUp.start()
    elif int(message) == 2:
        try:
            procZUp.terminate()
            procZUp = Process(target = zUp)
        except:
            print("There was a problem with zu process")
    else:
        pass

def moveFieldZDown(message):
    global procZDown
    if int(message) == 1:
        procZDown.start()
    elif int(message) == 2:
        try:
            procZDown.terminate()
            procZDown = Process(target = zDown)
        except:
            print("There was a problem with zd process")
    else:
        pass

def zUp():
    """
    """
    while(1):
        #print("zup ", os.getpid())
        axMov.zResponse(STEPSZ, 1, TIME)
        time.sleep(0.01)

def zDown():
    """
    """
    while(1):
        #print("zdown ", os.getpid())
        axMov.zResponse(STEPSZ, 0, TIME)
        time.sleep(0.01)

def moveZUp():
    """
    Moves the z motor up a single quantity of steps
    """
    code = axMov.zResponse(STEPSZ, 1, TIME)
    time.sleep(0.01)
    return code

def moveZDown():
    """
    Moves the z motor down a single quantity of steps
    """
    code = axMov.zResponse(STEPSZ, 0, TIME)
    time.sleep(0.01)
    return code

def moveFieldX(message):
    """
    Function to move the motors in the x axis
    :param message: input string that contains a condition
    """
    if int(message) == 1:
        axMov.moveFieldX(1)
    elif int(message) == 0:
        axMov.moveFieldX(0)
    else:
        pass

def moveFieldY(message):
    """
    Function to move the motors in the y axis
    :param message: input string that contains a condition
    """
    if int(message) == 1:
        axMov.moveFieldY(1)
    elif int(message) == 0:
        axMov.moveFieldY(0)
    else:
        pass

def home():
    """
    Function to restart all the motors
    """
    axMov.home()

def homeZTop():
    """
    Function to restart the Z motor
    """
    axMov.homeZTop()
    
def homeZBottom():
    """
    Function to restart the Z motor
    """
    axMov.homeZBottom()

def homeX():
    """
    Function to restart the X motor
    """
    axMov.homeX()
    
def homeY():
    """
    Function to restart the Y motor
    """
    axMov.homeY()

def led(message):
    """
    Function to control the led
    :param message: input string that contains a condition 
    """
    if int(message) == 0:
        axMov.led.setState(0)
        ledState = axMov.led.getState()
        axMov.writeLed(ledState)
    elif int(message) == 1:
        axMov.led.setState(1)
        ledState = axMov.led.getState()
        axMov.writeLed(ledState)
    else:
        pass

# Instantiate movement class
axMov = axisMovement(port = int(1))

# Init processes
global procZUp
global procZDown
procZUp = Process(target = zUp)
procZDown = Process(target = zDown)
