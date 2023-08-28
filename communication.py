#!/usr/bin/python3 -u

# Zao SDK Jetbot
# Pawana LLC.
# Khaldon Araffa
# 2023.07

import asyncio
import serial_asyncio
from threading import Thread
from collections import deque 
import logging

class Communication(Thread):
    def __init__(self, port, baud, freq):
        Thread.__init__(self)
        self.setDaemon(True)

        self.port = port
        self.baud = baud
        self.freq = freq

        self.commands = deque()
        self._received_data = deque()

    @property
    def received_data(self):
        return self._received_data
    
    @received_data.setter
    def received_data(self, value):
        self._received_data = value
    
    def run(self):
        logging.debug('com init')
        loop = asyncio.new_event_loop()  
        loop.run_until_complete(self.process_serial())

    def add_write_data(self, data):
        self.commands.append(data)

    async def process_serial(self):
        while True:
            reader, writer = await self.connect_serial(self.port, self.baud)
            sent = self.write_data(writer)
            received = self.read_data(reader)
            await asyncio.wait([sent, received])

            while not self.write.transport.is_closing():
                await asyncio.sleep(0.5)

    async def read_data(self, reader):
        while True:
            data = await reader.readline()
            if data:
                self._received_data.append(data.strip().decode('utf-8'))
#                logging.debug(f"Received: {data} {data.strip().decode('utf-8')}")
            await asyncio.sleep(1/self.freq)

    async def write_data(self, writer):
        while True:
            while self.commands:
                data = f'{self.commands.popleft()}\n'
                
                writer.write(data.encode('utf-8'))
#                logging.debug(f'write data: {data}')
            
            await writer.drain()

            await asyncio.sleep(1/self.freq)

    async def connect_serial(self, port, baudrate):
        while True:
            try:
                reader, writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baudrate)
                logging.info(f'serial connected: {port} {baudrate}')
                return reader, writer
            except Exception as e:
                logging.debug(f'Error connecting to {port}: {e}')
                await asyncio.sleep(1)