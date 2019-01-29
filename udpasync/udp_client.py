from .udp_abstract import UDPAbstract


class UDPClient(UDPAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def connect(self):
        if self._logger:
            self._logger.info("UDP CLIENT Connection '{}' '{}:{}'...".format(self.name, self.host, self.port))
        return await self.loop.create_datagram_endpoint(lambda: self, remote_addr=(self.host, self.port))

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._logger:
            self._logger.info("UDP CLIENT Connection '{}' '{}:{}' CLOSED".format(self.name, self.host, self.port))
        await self.close()
