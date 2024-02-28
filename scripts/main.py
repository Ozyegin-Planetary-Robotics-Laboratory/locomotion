#!/usr/bin/python3
from sensor_msgs.msg import Joy
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from TMotorCANControl.servo_can import TMotorManager_servo_can
from datetime import datetime, timezone, timedelta
import threading
import csv
import rospy
import time


if __name__=="__main__":
  rospy.init_node("ozurover_locomotion", anonymous=True)
  with TMotorManager_servo_can(motor_type="AK70-10", motor_ID=1) as motor1:
    loop = SoftRealtimeLoop(dt=0.0001, report=True, fade=0.0)
    motor1.enter_velocity_control()
    time.sleep(1)
    
    for t in loop:
      motor1.set_velocity(0.1)
      motor1.update()
      if loop.kill_now:
        break