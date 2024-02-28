#!/usr/bin/python3
from sensor_msgs.msg import Joy
#from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from TMotorCANControl.servo_can import TMotorManager_servo_can
#from datetime import datetime, timezone, timedelta
import threading
#import csv
import rospy
#import requests
import time

start_time = time.time()

class MotorController:
  def __init__(self):
    time.sleep(2.0)
    rospy.init_node("ozurover_motor_interface", anonymous=True)
    self.subscriber = rospy.Subscriber("/joy", Joy, self.joy_callback)
    
  def getTime():
    return time.time() - start_time

  def writeMotorStates(self):
    motor_data = [self.getTime(),
                  motor1.get_motor_velocity_radians_per_second(),
                  motor1.get_current_qaxis_amps(),
                  motor2.get_motor_velocity_radians_per_second(),
                  motor2.get_current_qaxis_amps(),
                  motor3.get_motor_velocity_radians_per_second(),
                  motor3.get_current_qaxis_amps(),
                  motor4.get_motor_velocity_radians_per_second(),
                  motor4.get_current_qaxis_amps()]
    writer.writerow(motor_data)
  
  def joy_callback(self, joystick_data):
    print(joystick_data.axes[1], joystick_data.axes[4])
    l_joy_val, r_joy_val = float(joystick_data.axes[1]), float(joystick_data.axes[4])
    angular_vel_range, joy_range = 13.6, 2.0
    speed_coefficient = 0.5 #Coefficient to tame the speed output. 
    motor1.velocity = (-r_joy_val * angular_vel_range/joy_range) * speed_coefficient
    motor2.velocity = (l_joy_val * angular_vel_range/joy_range) * speed_coefficient
    motor3.velocity = (-r_joy_val * angular_vel_range/joy_range) * speed_coefficient
    motor4.velocity = (l_joy_val * angular_vel_range/joy_range) * speed_coefficient
  

if __name__ == '__main__':
    with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=1) as motor1:
        with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=2) as motor2:
            with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=3) as motor3:
                with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=4) as motor4:
                    def joy_callback(joystick_data):
                        print(joystick_data.axes[1], joystick_data.axes[4])
                        l_joy_val, r_joy_val = float(joystick_data.axes[1]), float(joystick_data.axes[4])
                        angular_vel_range, joy_range = 13.6, 2.0
                        speed_coefficient = 0.5 #Coefficient to tame the speed output. 
                        motor1.velocity = (-r_joy_val * angular_vel_range/joy_range) * speed_coefficient
                        motor2.velocity = (l_joy_val * angular_vel_range/joy_range) * speed_coefficient
                        motor3.velocity = (-r_joy_val * angular_vel_range/joy_range) * speed_coefficient
                        motor4.velocity = (l_joy_val * angular_vel_range/joy_range) * speed_coefficient
                    #with open('data.csv', 'w', newline='') as data_f:
                      #headers = ['time', 'motor1_v', 'motor1_c', 'motor2_v', 'motor2_c', 'motor3_v', 'motor3_c', 'motor4_v', 'motor4_c']
                      #writer = csv.writer(data_f)
                      #writer.writerow(headers)
                      
                    motor1.enter_velocity_control()
                    motor2.enter_velocity_control()
                    motor3.enter_velocity_control()
                    motor4.enter_velocity_control()
                    
                    time.sleep(2.0)
                    def motorGoBr():
                      while True:
                        motor1.velocity = 0.0
                        motor2.velocity = 0.0
                        motor3.velocity = 1.0
                        motor4.velocity = 1.0
                        time.sleep(0.1)
                        
                    threading.Thread(target=motorGoBr).start()
                    
                    while a is not 'q':
                        a = input("Enter 'q' to quit: ")
                    
                    motor1.velocity = 0.0
                    motor2.velocity = 0.0
                    motor3.velocity = 0.0
                    motor4.velocity = 0.0
                    
                    #motor_interface = MotorController()
                    #rospy.init_node("ozurover_motor_interface", anonymous=True)
                    #subscriber = rospy.Subscriber("/joy", Joy, joy_callback)
                    #rospy.spin()
                      #data_f.close()