import asyncio
from .udp_abstract import UDPAbstract


class UDPServer(UDPAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def connect(self):
        if self._logger:
            self._logger.info("UDP SERVER Connection '{}:{}'...".format(self.host, self.port))
        return await self.loop.create_datagram_endpoint(lambda: self, local_addr=(self.host, self.port))

    def pack(self, data):
        return data.encode()

    def datagram_received(self, data, addr):
        if self._logger:
            self._logger.debug("UDP Data received by '{}' from '{}:{}'; Message: {}".format(self.name, self.host, self.port, data))
        data = self.unpack(data)
        if self.processor:
            asyncio.ensure_future(self.processor(data, addr, self), loop=self.loop)