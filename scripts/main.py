#!/usr/bin/python3
from sensor_msgs.msg import Joy
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from TMotorCANControl.servo_can import TMotorManager_servo_can
from datetime import datetime, timezone, timedelta
import threading
import csv
import rospy
import time

start_time = time.time()

class MotorController:
    def __init__(self):
        time.sleep(2.0)
        rospy.init_node("ozurover_motor_interface", anonymous=True)
        self.subscriber = rospy.Subscriber("/joy", Joy, self.joy_callback)

    def getTime(self):
        current_time = time.time() - start_time
        return current_time
    
    def joy_callback(self, joystick_data):
        l_joy_val, r_joy_val = float(joystick_data.axes[1]), float(joystick_data.axes[4])
        angular_vel_range, joy_range = 13.6, 2.0
        speed_coefficient = 0.5 #Coefficient to tame the speed output.
        motor1.set_motor_velocity_radians_per_second((-r_joy_val * angular_vel_range/joy_range) * speed_coefficient)
        motor2.set_motor_velocity_radians_per_second((l_joy_val * angular_vel_range/joy_range) * speed_coefficient)
        motor3.set_motor_velocity_radians_per_second((-r_joy_val * angular_vel_range/joy_range) * speed_coefficient)
        motor4.set_motor_velocity_radians_per_second((l_joy_val * angular_vel_range/joy_range) * speed_coefficient) 
        #motor1.velocity = (-r_joy_val * angular_vel_range/joy_range) * speed_coefficient
        #motor2.velocity = (l_joy_val * angular_vel_range/joy_range) * speed_coefficient
        #motor3.velocity = (-r_joy_val * angular_vel_range/joy_range) * speed_coefficient
        #motor4.velocity = (l_joy_val * angular_vel_range/joy_range) * speed_coefficient

if __name__ == '__main__':
    with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=1) as motor1:
        with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=2) as motor2:
            with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=3) as motor3:
                with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=4) as motor4:
                      motor1.enter_velocity_control()
                      motor2.enter_velocity_control()
                      motor3.enter_velocity_control()
                      motor4.enter_velocity_control()
                      motor_interface = MotorController()
                      rospy.spin()