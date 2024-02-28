#!/usr/bin/python3
from sensor_msgs.msg import Joy
from TMotorCANControl.servo_can import TMotorManager_servo_can
import threading
import rospy
import time

motors = []
speed = 0.0
alive = True

if __name__ == '__main__':
    with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=1) as motor1:
        with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=2) as motor2:
            with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=3) as motor3:
                with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=4) as motor4:

                    motors.append(motor1)
                    motors.append(motor2)
                    motors.append(motor3)
                    motors.append(motor4)
                    
                    motor1.enter_velocity_control()
                    motor2.enter_velocity_control()
                    motor3.enter_velocity_control()
                    motor4.enter_velocity_control()
                    
                    def motorGoBr():
                      global motors, speed, alive
                      while alive:
                        motors[1].velocity = speed
                        motors[2].velocity = speed
                        motors[3].velocity = speed
                        motors[4].velocity = speed
                        time.sleep(0.1)    
                    thread = threading.Thread(target=motorGoBr).start()
                    
                    # Input loop
                    # q: quit
                    # w: forward
                    # s: backward
                    # a: abort
                    c_in = 'b'
                    while c_in != 'q':
                        c_in = input("Enter command: ")
                        if c_in == 'w':
                          speed += 0.1
                        elif c_in == 's':
                          speed += -0.1
                        elif c_in == 'a':
                          speed = 0.0
                        elif c_in == 'q':
                          speed = 0.0
                          break
                        else:
                          print("Invalid command")
                          
                    
                    print("Exiting...")
                    motor1.velocity = 0.0
                    motor2.velocity = 0.0
                    motor3.velocity = 0.0
                    motor4.velocity = 0.0
                    
                    alive = False
                    thread.join()