import sys, os
import time
sys.path.append(os.pardir)
import numpy as np
from abc import abstractmethod
from alifebook_lib.simulators import VehicleSimulator


OBSTACLE_NUM = 5
FEED_NUM = 20

class SubsumptionModule(object):

  def __init__(self):
    super(SubsumptionModule, self).__init__();
    self.__inputs = {}
    self.__outputs = {}
    self.child_modules = {}
    self.set_active_module_name("")
    self.on_init()

  def add_child_module(self, name, module):
    self.child_modules[name] = module

  def set_inputs(self, inputs):
    self.__inputs = inputs
    for m in self.child_modules.values():
      m.set_inputs(inputs)

  def get_input(self, name):
    return self.__inputs.get(name, None)

  def set_output(self, name, val):
    self.__outputs[name] = val

  def get_output(self, name):
    return self.__outputs.get(name, None)

  def update(self):
    for m in self.child_modules.values():
      m.update()
    self.on_update()

  def set_active_module_name(self, name):
    self.__active_module_name = name

  def get_active_module_name(self):
    return self.__active_module_name

  @abstractmethod
  def on_init(self):
    pass

  @abstractmethod
  def on_update(self):
    pass



class AvoidModule(SubsumptionModule):
  def on_init(self):
    pass

  def on_update(self):
    self.set_output("left_wheel_speed", 10 + 30 * self.get_input("left_distance"))
    self.set_output("right_wheel_speed", 10 + 30 * self.get_input("right_distance"))
    self.set_active_module_name(self.__class__.__name__)


class BackModule(SubsumptionModule):
  TURN_START_STEP = 500 # this means that if the time which both sensors detect obstacles is continuing, it is justified to need to back
  TURN_END_STEP = 700
  def on_init(self):
    self.back_counter = 0
    self.add_child_module('avoid', AvoidModule())
    # init: 0, left: 1, right: -1
    self.direction = 0

  def on_update(self):
    if self.get_active_module_name() == self.child_modules['avoid'].get_active_module_name() and self.get_input("right_distance") >= 0.001 and self.get_input("left_distance") >= 0.001:
      # count up while avoid module is continuing and both sensors detect obstacles
      self.back_counter = self.back_counter + 1
      # decide back direction
      if self.direction == 0:
        if np.random.rand() < 0.5:
          self.direction = 1 # left
        else:
          self.direction = -1 # right

    elif self.TURN_START_STEP <= self.back_counter and self.back_counter <= self.TURN_END_STEP:
      # continue to count up between TURN_START_STEP and TURN_END_STEP
      self.back_counter = self.back_counter + 1
    else:
      self.back_counter = 0
      self.direction = 0

    if self.back_counter < self.TURN_START_STEP:
      # before TURN_START_STEP, do not inhibit under layer module
      self.set_output("left_wheel_speed", self.child_modules['avoid'].get_output("left_wheel_speed"))
      self.set_output("right_wheel_speed", self.child_modules['avoid'].get_output("right_wheel_speed"))
      self.set_active_module_name(self.child_modules['avoid'].get_active_module_name())
    else:
      # back
      if self.direction > 0:
        self.set_output("left_wheel_speed", -20)
        self.set_output("right_wheel_speed", -10)
        self.set_active_module_name(self.__class__.__name__)
      else:
        self.set_output("left_wheel_speed", -10)
        self.set_output("right_wheel_speed", -20)
        self.set_active_module_name(self.__class__.__name__)




class WanderModule(SubsumptionModule):
  #TURN_START_STEP = 100
  #TURN_END_STEP = 180
  TURN_START_STEP = 10
  TURN_END_STEP = 180
  def on_init(self):
    self.counter = 0
    self.add_child_module('back', BackModule())

  def on_update(self):
    if self.get_input("right_distance") < 0.001 and self.get_input("left_distance") < 0.001:
      self.counter = (self.counter + 1) % self.TURN_END_STEP
    else:
      self.counter = 0

    if self.counter < self.TURN_START_STEP:
      # do not inherit under layer module until counter reach TURN_START_STEP
      self.set_output("left_wheel_speed", self.child_modules['back'].get_output("left_wheel_speed"))
      self.set_output("right_wheel_speed", self.child_modules['back'].get_output("right_wheel_speed"))
      self.set_active_module_name(self.child_modules['back'].get_active_module_name())
    elif self.counter == self.TURN_START_STEP:
      # random walk
      if np.random.rand() < 0.5:
        self.set_output("left_wheel_speed", 15)
        self.set_output("right_wheel_speed", 10)
      else:
        self.set_output("left_wheel_speed", 10)
        self.set_output("right_wheel_speed", 15)

      self.set_active_module_name(self.__class__.__name__)
    else:
      # wheel is kept until counter reset
      pass



from t3 import T3

class ChaosWanderModule(SubsumptionModule):
  def on_init(self):
    self.add_child_module('back', BackModule())
    self.t3 = T3(omega0 = 0.9, omega1 = 0.3, epsilon = 0.1)
    #self.t3.set_parameters(omega0 = np.random.rand())
    #self.t3.set_parameters(omega1 = np.random.rand())
    self.t3.set_parameters(omega0 = np.random.rand(), omega1 = np.random.rand())

  def on_update(self):
    x,y = self.t3.next() # update chaos dynamics
    if self.get_input("right_distance") < 0.001 and self.get_input("left_distance") < 0.001:
      # wander with chaos value
      left_wheel_speed = x * 50
      right_wheel_speed = y * 50
      self.set_output("left_wheel_speed", left_wheel_speed)
      self.set_output("right_wheel_speed", right_wheel_speed)
      self.set_active_module_name(self.__class__.__name__)
    else:
      # activate under layer module if sensor detects an obstacle, and change chaos parameter
      self.set_output("left_wheel_speed", self.child_modules['back'].get_output("left_wheel_speed"))
      self.set_output("right_wheel_speed", self.child_modules['back'].get_output("right_wheel_speed"))
      #self.t3.set_parameters(omega0 = np.random.rand())
      #self.t3.set_parameters(omega1 = np.random.rand())
      self.t3.set_parameters(omega0 = np.random.rand(), omega1 = np.random.rand())
      self.set_active_module_name(self.child_modules['back'].get_active_module_name())





class ExploreModule(SubsumptionModule):
  def on_init(self):
    #self.add_child_module('wander', WanderModule())
    self.add_child_module('wander', ChaosWanderModule())

  def on_update(self):
    if self.get_input('feed_touching'):
      # inhibit under layer modules and speed down due to realising the feed
      self.set_output("left_wheel_speed", 0)
      self.set_output("right_wheel_speed", 0)
      self.set_active_module_name(self.__class__.__name__)
    else:
      # do not inhibit under layer modules when feeds are nothing
      self.set_output("left_wheel_speed", self.child_modules['wander'].get_output("left_wheel_speed"))
      self.set_output("right_wheel_speed", self.child_modules['wander'].get_output("right_wheel_speed"))
      self.set_active_module_name(self.child_modules['wander'].get_active_module_name())




# change architecture
#controller = AvoidModule()
#controller = BackModule()
#controller = WanderModule()
#controller = ChaosWanderModule() # chaos including in wander module
controller = ExploreModule()

# initialize simulator
simulator = VehicleSimulator(obstacle_num=OBSTACLE_NUM, feed_num=FEED_NUM)
is_end = False

while simulator:

  # get sensor data
  sensor_data = simulator.get_sensor_data()
  # update controller of subsumption
  controller.set_inputs(sensor_data)
  controller.update()

  # create action and update
  left_wheel_speed = controller.get_output("left_wheel_speed")
  right_wheel_speed = controller.get_output("right_wheel_speed")
  action = [left_wheel_speed, right_wheel_speed]
  active_module = controller.get_active_module_name()

  #print(active_module)
  #print(active_module, left_wheel_speed, right_wheel_speed, sep=" : ")

  if active_module == "AvoidModule":
    simulator.set_bodycolor((255, 0, 0, 255))
  elif active_module == "BackModule":
    simulator.set_bodycolor((255, 255, 0, 255))
  elif active_module in ("WanderModule", "ChaosWanderModule"):
    simulator.set_bodycolor((0, 255, 0, 255))
  elif active_module == "ExploreModule":
    simulator.set_bodycolor((0, 0, 255, 255))

  simulator.update(action)

  is_end = simulator.did_eat_all_feed()
  if is_end:
    simulator.update([0,0])
    time.sleep(10)
    break







