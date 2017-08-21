# Author: Rodrigo Loza
# Description: This script contains functions that interact with the microscope's hardware
# and the focus coefficients received from the sensor

from interface import *

class autofocus:
    def __init__(self, list = [(None, None)]):
        self.positions = [each[0] for each in list]
        self.coefficients = [each[1] for each in list]

    def focus(self):
        # Calculate the maximum value
        max_ = max(self.coefficients)
        pos = self.coefficients.index(max_)
        # Calculate position 
        return len(self.positions)-pos
