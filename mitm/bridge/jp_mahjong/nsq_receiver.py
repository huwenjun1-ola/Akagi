"""NSQ接收器，用于接收Go服务发送的MJAI格式数据"""

import asyncio
import json
import nsq
from ..logger import logger



class JpMahjongNsqReceiver:
    MahjongTopic = "game.jpmahjong.robot.msg"

    def __init__(self):
        self.connected = False
        self.address = ""
        self.reader: nsq.Reader = None
        self.writer: nsq.Writer = None


    async def check_writer(self):
         # 注意：Writer 初始化时不会立即报错，只有在交互时才会发现连接问题
        writer = nsq.Writer(nsqd_tcp_addresses=[self.address])
        self.writer=writer
        try:
            await asyncio.sleep(1)
            # 尝试发送一个测试心跳消息
            self.writer.pub('health_check', b'ping')
            return True
        except Exception as e:
            logger.warning(f"Writer 健康检查失败: {str(e)}")
            return False

    async def connect(self, address="localhost:4150"):
        """连接到NSQ服务器"""
        try:
            # 解析地址
            self.address = address
            await self.check_writer()
            self.connected = True
            logger.info(f"Connected to NSQ server: {address}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to NSQ: {e}")
            return False
    
    async def subscribe_to_akagi_events(self, topic, channel, handler):
        """订阅来自Go服务的MJAI事件"""
        if not self.connected:
            logger.error("Not connected to NSQ")
            return
        
        try:
            # Reader 创建后会自动启动，无需调用 run() 方法
            logger.info(f"Creating NSQ Reader  {self.address} for topic={topic}, channel={channel}")
            reader = nsq.Reader(
                topic=topic,
                channel=channel,
                nsqd_tcp_addresses=[self.address],
                max_in_flight=10,
                message_handler=handler,
            )
            self.reader=reader
            logger.info(f"Subscribed to {topic} on NSQ, waiting for messages...")
        except Exception as e:
            logger.error(f"Failed to subscribe to events: {e}", exc_info=True)
            raise e
    



    def close(self):
        """优雅地关闭连接"""
        logger.info("正在关闭NSQ接收器...")
        self.connected = False
        self.reader.close()



    def publish_akagi_events(self, topic, param):
        """
        发布 NSQ 消息，自动处理重连
        确保参数是 bytes 类型
        """
        # 检查Writer连接
        if self.writer is None:
            logger.error("Writer未初始化，无法发送消息")
            return False
        
        # 处理不同类型的输入参数
        if isinstance(param, str):
            # 字符串转为 bytes
            param_bytes = param.encode('utf-8')
        elif isinstance(param, bytes):
            # 已经是 bytes 类型
            param_bytes = param
        elif isinstance(param, (int, float, bool)):
            # 数值类型转为字符串再转为 bytes
            param_bytes = str(param).encode('utf-8')
        elif isinstance(param, (dict, list)):
            # JSON 数据序列化为字符串再转为 bytes
            param_bytes = json.dumps(param, ensure_ascii=False).encode('utf-8')
        else:
            # 其他类型都转为字符串再转为 bytes
            param_bytes = str(param).encode('utf-8')
        self.writer.pub(topic, param_bytes)