import abc
from abc import abstractmethod
import asyncio
import traceback


class UDPAbstract(asyncio.DatagramProtocol, metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        self.loop = kwargs.get("loop")
        self.host = kwargs.get("host") or "0.0.0.0"
        self.port = kwargs.get("port") or 9999
        self.processor = kwargs.get("processor")
        self.name = kwargs.get("name") or self.__class__.__name__
        self.transport = None

        self._logger = kwargs.get("logger")

    @abstractmethod
    async def connect(self):
        raise NotImplemented()

    def is_connected(self):
        return self.transport is not None and not self.transport.is_closing()

    async def close(self):
        self.transport.close()
        self.transport = None

    def connection_made(self, transport):
        if self._logger:
            self._logger.info("UDP Connection '{}' '{}:{}' OK".format(self.name, self.host, self.port))
        self.transport = transport

    def connection_lost(self, exc):
        if self._logger:
            self._logger.info("UDP Connection '{}' '{}:{}' LOST".format(self.name, self.host, self.port))

    def unpack(self, data):
        return data

    def pack(self, data):
        return data

    def sendto(self, data, raise_if_exception=False):
        try:
            data = self.pack(data)
            data = data if isinstance(data, bytes) else data.encode()
            self.transport.sendto(data)
            if self._logger:
                self._logger.debug("UDP message SENT by '{}' to '{}:{}'; SENT: {}".format(self.name, self.host, self.port, data))
        except Exception as ex:
            if self._logger:
                self._logger.warning("Exception: {}; {}".format(ex, traceback.format_exc()))
            if raise_if_exception:
                raise

    def error_received(self, exc):
        if self._logger:
            self._logger.info("UDP Connection '{}' '{}:{}' ERROR RECEIVED: {}".format(self.name, self.host, self.port, exc))
