import asyncio
import logging
import numpy as np
from nptyping import NDArray, Shape, UInt8
import serial_asyncio
import dropbot

class DropbotController:
    def __init__(self):
        self.proxy = None
        self.last_state: NDArray[Shape['*, 1'], UInt8] = np.zeros(128, dtype='uint8')
        self.loop = asyncio.get_event_loop()

    async def init_dropbot_proxy(self):
        while self.proxy is None:
            try:
                _, self.proxy = await serial_asyncio.open_serial_connection(url='hwgrep://USB Serial', baudrate=115200)
                break
            except Exception as e:
                logging.error(f"Connection failed: {e}, retrying in 1 second.")
                await asyncio.sleep(1)

    async def poll_voltage(self):
        while True:
            if self.proxy:
                try:
                    voltage = await self.proxy.high_voltage()
                    print(f"Voltage: {voltage} V")
                except Exception as e:
                    logging.error(f"Failed to read voltage: {e}")
            await asyncio.sleep(1)

    def run(self):
        self.loop.run_until_complete(self.init_dropbot_proxy())
        self.loop.create_task(self.poll_voltage())
        self.loop.run_forever()

if __name__ == "__main__":
    controller = DropbotController()
    controller.run()
