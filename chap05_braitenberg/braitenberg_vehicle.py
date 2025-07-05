import sys, os
import time
sys.path.append(os.pardir)
import numpy as np
from alifebook_lib.simulators import VehicleSimulator

# initialize simulator
simulator = VehicleSimulator(obstacle_num=5)

while simulator:
  # get sensor data
  sensor_data = simulator.get_sensor_data()
  # inside braitenberg vehicle
  left_wheel_speed = 20 + 20 * sensor_data["left_distance"]
  right_wheel_speed = 20 + 20 * sensor_data["right_distance"]
  # update with creating action
  action = [left_wheel_speed, right_wheel_speed]
  simulator.update(action)


