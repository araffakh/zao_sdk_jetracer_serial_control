#!/usr/bin/python3 -u

# Zao SDK Jetbot
# Pawana LLC.
# Khaldon Araffa
# 2023.07

import os
import time
from threading import Thread
# import qwiic_scmd
from jetracer.nvidia_racecar import NvidiaRacecar
import logging

JOYSTIC_INPUT_MIN = 1
JOYSTIC_INPUT_MAX = 0

DEAD_BAND = 5

LEFT_MOTOR = 0
RIGHT_MOTOR = 1

HANDLE_TRIM = 0.05 #0-1

class MotorController(Thread):
    def __init__(self, maxspeed=255, speedchangetime=1):
        Thread.__init__(self)
        self.setDaemon(True)

        self.current_speed_left = 0
        self.current_speed_right = 0
        self.target_speed_left = 0
        self.target_speed_right = 0
        self.speed_increment_left = 0
        self.speed_increment_right = 0
        self.update_interval = 0.01
        self.maxspeed = maxspeed
        self.speedchangetime = speedchangetime

        # self.motor = qwiic_scmd.QwiicScmd()
        self.motor = NvidiaRacecar()
        self.motor.throttle_gain = 0.5
        self.motor.throttle = 0

        # if self.motor.connected == False:
        #     logging.error("Motor Driver not connected. Check connections.")
        #     os._exit(1)

        # #initialize motor
        # self.motor.begin()
        # time.sleep(.250)
        # self.stop()

        # self.start()

    def setmotor(self, x_axis, y_axis):
        # x = self.maprange(x_axis)
        # y = self.maprange(y_axis)
        self.motor.throttle=x_axis
        self.motor.steering=y_axis

        # self.target_speed_left = max(min((int(self.maxspeed*y * (1-x+HANDLE_TRIM))), self.maxspeed), -self.maxspeed)
        # self.target_speed_right = max(min((int(self.maxspeed*y * (1+x+HANDLE_TRIM))), self.maxspeed), -self.maxspeed)     

        # self.speed_increment_left = (self.target_speed_left - self.current_speed_left) / (self.speedchangetime / self.update_interval)
        # self.speed_increment_right = (self.target_speed_right - self.current_speed_right) / (self.speedchangetime / self.update_interval)

        # logging.debug(f'setspeed {self.target_speed_left} {self.target_speed_right} {self.speed_increment_left} {self.speed_increment_right}')
        logging.debug(f'setspeed {0} {self.motor.throttle} {self.motor.steering} {0}')


    def stop(self):
        logging.debug('stop motor')
        # self.target_speed_left = 0
        # self.target_speed_right = 0
        # self.current_speed_right = 0
        # self.current_speed_left = 0
        # self.motor.set_drive(LEFT_MOTOR, 0, 0)
        # self.motor.set_drive(RIGHT_MOTOR, 0, 0)
        # self.motor.disable()
        self.motor.throttle=0
        self.motor.steering=0


    # def maprange(self, value, from_low=JOYSTIC_INPUT_MIN, from_up=JOYSTIC_INPUT_MAX, to_low=-1, to_up=1):
    #     return  float(to_low + ((value - from_low) * (to_up - to_low) / (from_up - from_low)))       

    # def run(self):
    #     while True:            
    #         if abs(self.target_speed_left - self.current_speed_left) > abs(self.speed_increment_left):
    #             self.current_speed_left += self.speed_increment_left
    #         else:
    #             self.current_speed_left = self.target_speed_left
                
    #         if abs(self.target_speed_right - self.current_speed_right) > abs(self.speed_increment_right):
    #             self.current_speed_right += self.speed_increment_right
    #         else:
    #             self.current_speed_right = self.target_speed_right
            
    #         if DEAD_BAND < abs(self.current_speed_left) or DEAD_BAND < abs(self.current_speed_right):
    #             self.motor.enable()
    #             self.motor.set_drive(LEFT_MOTOR, 0, int(self.current_speed_left))
    #             self.motor.set_drive(RIGHT_MOTOR, 0, int(self.current_speed_right))
    #         else:
    #             self.motor.set_drive(LEFT_MOTOR, 0, 0)
    #             self.motor.set_drive(RIGHT_MOTOR, 0, 0)
                
            # time.sleep(self.update_interval)

                    
