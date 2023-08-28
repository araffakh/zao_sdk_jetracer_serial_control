#!/usr/bin/python3 -u

# Zao SDK Jetbot
# Pawana LLC.
# Khaldon Araffa
# 2023.07

import os
import asyncio
import logging
import time
from collections import deque 
from communication import Communication
from motorcontroller import MotorController
from heartbeatled import HeartbeatLed

import subprocess

logging.basicConfig(level=logging.INFO)
    
VERSION = '1.0.0.3'

BASE_BOARD_TYPE= "jetson"
HEARTBEAT_LED_GPIO_PIN_RX = 'DAP4_DIN'  #ハートビート用LED RX
HEARTBEAT_LED_GPIO_PIN_TX = 'SPI2_MOSI'

# serial port
SERIAL_PORT = '/run/zao/ttyZAOV1'
#SERIAL_PORT = '/dev/ttyUSB0'

# serial port baud rate
BAUD = 115200

# frequency of sending data to the robot
FREQUENCY = 100

CONNECTINO_TIMEOUT = 2  #sec

MOTORSPEED_MAX = 1    #0-255
SPEED_CHANGE_TIME = 0.3   #sec

BUTTON_PIN = 17

class ZaoSDKJetbot: 
    def __init__(self):
        self.led = HeartbeatLed(BASE_BOARD_TYPE,HEARTBEAT_LED_GPIO_PIN_RX, HEARTBEAT_LED_GPIO_PIN_TX)
        self.motor_controller = MotorController(MOTORSPEED_MAX, SPEED_CHANGE_TIME)        
        self.com = Communication(SERIAL_PORT, BAUD, FREQUENCY)
        
        self.prev_hertbeat_sent_time = time.time()
        self.prev_hertbeat_received_time = time.time()                  

    def move(self, cmd):
        logging.debug(f'move {cmd}')
        try:
            throttle, stealing = cmd.split(',')
            logging.debug(f'move : {throttle} {stealing}')
            self.motor_controller.setmotor(float(throttle), float(stealing))
        except:
            pass

    async def start(self, loop):
        logging.info(f"Zao SDK Jetbot started. {VERSION}")

        self.com.start()

        while True:
            #send heart beat
            if time.time() - self.prev_hertbeat_sent_time >= 1.0:
                self.com.add_write_data('h\n') #add hert beat
                self.led.sentIndicator()
                self.prev_hertbeat_sent_time = time.time()

            #offline check
            if CONNECTINO_TIMEOUT < time.time() - self.prev_hertbeat_received_time:
                logging.info('heart beat timeout')
                self.motor_controller.stop()
                time.sleep(0.1)
            
            #received data
            if self.com.received_data:
                cmd = self.com.received_data.popleft()
                logging.debug(cmd)
                if cmd =='h':
                    self.led.receivedIndicator()
                    self.prev_hertbeat_received_time = time.time()
                    logging.debug('hertbeat received')
                elif ',' in cmd:
                    self.move(cmd)
                
            #button        
            # if GPIO.input(BUTTON_PIN):
            #     logging.info('button pressed')
            #     self.stop()
            #     # subprocess.run(('/sbin/shutdown', 'now'))
            #     break

            time.sleep(1/FREQUENCY)


if __name__ == '__main__':
    zaosdkbot = ZaoSDKJetbot()

    loop = asyncio.new_event_loop()  
    loop.run_until_complete(zaosdkbot.start(loop))
