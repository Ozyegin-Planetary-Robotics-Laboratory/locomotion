#!/usr/bin/python3
from sensor_msgs.msg import Joy
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from TMotorCANControl.servo_can import TMotorManager_servo_can
from datetime import datetime, timezone, timedelta
import threading
import csv
import rospy
import time

wheel_speeds = [.0, .0, .0, .0]

def joy_callback(data):
  global wheel_speeds
  wheel_speeds[0] = -data.axes[4]
  wheel_speeds[1] = data.axes[1] # apparently broke lol
  wheel_speeds[2] = data.axes[1]
  wheel_speeds[3] = -data.axes[4]

if __name__=="__main__":
  rospy.init_node("ozurover_locomotion", anonymous=True)
  with TMotorManager_servo_can(motor_type="AK70-10", motor_ID=1) as motor1:
    with TMotorManager_servo_can(motor_type="AK70-10", motor_ID=2) as motor2:
      with TMotorManager_servo_can(motor_type="AK70-10", motor_ID=3) as motor3:
        with TMotorManager_servo_can(motor_type="AK70-10", motor_ID=4) as motor4:
          
          def update_loop():
            global wheel_speeds
            speed_coeff = 10.0
            while not rospy.is_shutdown():
              motor1.velocity = wheel_speeds[0]*speed_coeff
              motor2.velocity = wheel_speeds[1]*speed_coeff
              motor3.velocity = wheel_speeds[2]*speed_coeff
              motor4.velocity = wheel_speeds[3]*speed_coeff
              motor1.update()
              motor2.update()
              motor3.update()
              motor4.update()
              time.sleep(0.05)
          
          motor1.enter_velocity_control()
          motor2.enter_velocity_control()
          motor3.enter_velocity_control()
          motor4.enter_velocity_control()
          time.sleep(1)
          
          update_thread = threading.Thread(target=update_loop)
          update_thread.start()
          
          rospy.Subscriber("/joy", Joy, joy_callback)
          rospy.spin()
