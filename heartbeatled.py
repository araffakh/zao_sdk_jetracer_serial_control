#!/usr/bin/python3 -u

# Zao SDK Jetbot
# Pawana LLC.
# Khaldon Araffa
# 2023.07

import time
from threading import Timer, Thread

import RPi.GPIO as GPIO

class HeartbeatLed(Thread):
    def __init__(self,board_type ,gpiopin_rx, gpiopin_tx, waitspan = 0.3, min_flash_span_tx=0.5, min_flash_span_rx=1):
        Thread.__init__(self)
        self.setDaemon(True)

        self.lastupdate_rx = time.time()
        self.lastupdate_tx = time.time()
        self.waitspan = waitspan

        self.board=board_type
        self.gpiopin_rx = gpiopin_rx
        self.gpiopin_tx = gpiopin_tx
        

        self.min_flash_span_tx = min_flash_span_tx
        self.min_flash_span_rx = min_flash_span_rx
        
        if self.board=='raspberry' :
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

        #reset all pins
        for i in range(1,27):
            try:
                GPIO.setup(i, GPIO.OUT)
                GPIO.output(i, GPIO.LOW)                
            except Exception:
                pass
        
        time.sleep(0.2)

        GPIO.setup(self.gpiopin_rx, GPIO.OUT)
        GPIO.setup(self.gpiopin_tx, GPIO.OUT)

    def receivedIndicator(self):
        if self.lastupdate_rx + self.min_flash_span_rx <= time.time():
            self.lastupdate_rx = time.time()
            GPIO.output(self.gpiopin_rx, GPIO.HIGH)

            received_t = Timer(self.waitspan, GPIO.output, args=(self.gpiopin_rx, GPIO.LOW))
            received_t.start()

    def sentIndicator(self, waitspan = 0.1):
        if self.lastupdate_tx + self.min_flash_span_tx <= time.time():
            self.lastupdate_tx = time.time()
            GPIO.output(self.gpiopin_tx, GPIO.HIGH)

            sent_t = Timer(self.waitspan, GPIO.output, args=(self.gpiopin_tx, GPIO.LOW))
            sent_t.start()

    def waitingmodeIndicator(self, waitspan = 0.1):
        self.lastupdate_rx = time.time()
        waiting_t = Timer(waitspan, self.flash(self.gpiopin_rx))
        # waiting_t.start()

    def serverwaitingClientIndicator(self, waitspan=0.1):
        self.lastupdate_tx = time.time()
        waiting_t = Timer(waitspan, self.flash(self.gpiopin_tx))
        # waiting_t.start()

    def flash(self, pin, flashtime = 2, waitspan = 0.1):
        for i in range(flashtime):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(waitspan)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(waitspan)

    def close(self):
        GPIO.output(self.gpiopin_rx, GPIO.LOW)
        GPIO.output(self.gpiopin_tx, GPIO.LOW)
