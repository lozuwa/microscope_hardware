import xy_positioner as xy 
import z_positioner as zz

def up(x):
 [xy.y_forward() for i in range(int(x))]

def down(x):
 [xy.y_down() for i in range(int(x))]

def right(x):
 [xy.x_right() for i in range(int(x))]

def left(x):
 [xy.x_left() for i in range(int(x))]

def seq(x):
 for i in range(int(x)):
  up()
  left()
  down()
  right()

