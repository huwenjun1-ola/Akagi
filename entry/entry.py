import asyncio
import sys
import signal
import threading

from mitm.client import Client
import os
from .logger import logger
import time
from settings.settings import settings, MITMType
from mitm.jpmaj import start_proxy, stop_proxy, mjai_messages

os.environ["LOGURU_AUTOINIT"] = "False"


class Application:
    def __init__(self):
        pass

    def signal_handler(self, signum, frame):
        """处理信号的回调函数"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        stop_proxy()
        logger.info("Akagi stopped")
        sys.exit(0)

    def run(self):
        # 注册信号处理器
        signal.signal(signal.SIGHUP, self.signal_handler)
        _thread = threading.Thread(
            target=lambda: asyncio.run(start_proxy(settings.mitm.host, settings.mitm.port)))
        _thread.start()
        #  在这里阻塞 - 实现持续运行和信号检测
        while True:
            # 短暂休眠避免CPU占用过高
            time.sleep(10)



def main():
    app = Application()
    app.run()
