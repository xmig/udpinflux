"""
Asyncio InfluxDB UDP Client

Important:
 - InfluxDB server should be configured for support UDP
   (please UNCOMMENT the corresponded section in 'influxdb.conf' file)
 - The ONLY a predefined database name (default 'udp') can be used for UPD
   (you can configure different ports for different databases)


Protocol description: https://docs.influxdata.com/influxdb/v0.9/write_protocols/write_syntax/

USAGE:

EXAMPLE = {
        "value1": 100,
        "value2": 100,
        "tag0": 'Hello, World!',
        "tag1": '100i',
    }

TAGS = ["tag0", "tag1"]


async def store_example(loop):
    async with InfluxUDPClint(loop=loop, port=8089) as client:
        await client.insert('test', EXAMPLE, TAGS)

"""

import asyncio
from udpasync.udp_client import UDPClient


class InfluxUDPClint:
    def __init__(self,
                 host: str = '0.0.0.0',
                 port: int = 8089,
                 **kwargs):

        self._transport = None
        self._sender = None

        self.host = host
        self.port = port

        self.loop = kwargs.pop('loop', None) or asyncio.new_event_loop()
        self.client = UDPClient(host=self.host, port=port, loop=self.loop, **kwargs)

    async def __aenter__(self):
        self._transport, self._sender = await self.client.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
        self._transport = self._sender = None

    @staticmethod
    def pack_message(measurement, data, tags=None, timestamp=None, skip_escaping=False):
        """ Escaping / wrapping keys & values according to influx syntax  """
        tags = {x for x in tags} if tags else {}

        def check_any_in(value, keys):
            for i in range(0, len(value)-1):
                if value[i] not in keys:
                    return False
            return True

        def probe_as_integer(value):
            """ check if integer - something likes '100i' """
            return value[-1] == 'i' \
                and check_any_in(value, {'0','1','2','3','4','5','6','7','8','9'})

        def pack_value(value):
            if isinstance(value, str):
                if not probe_as_integer(value):
                    value = escape(value, {'"'})
                    value = '"' + value + '"'
            return value

        def pack_key_value(value):
            if isinstance(value, str):
                if not probe_as_integer(value):
                    value = escape(value, {',', ' ', '='})
            return value

        def escape(value, mask):
            if skip_escaping:
                return value

            parts = []
            for i in range(0, len(value)):
                c = value[i]
                if c in mask:
                    parts.append('\\')
                parts.append(c)
            return "".join(parts)

        def pack_key(key):
            return escape(key, {',', ' ', '='})

        def pack_measurement(measurement):
            return escape(measurement, {',', ' '})

        tags_part = []
        value_part = []

        for name in sorted(data.keys()):
            value = data[name]
            if name in tags:
                tags_part.append("{}={}".format(pack_key(name), pack_key_value(value)))
            else:
                value_part.append("{}={}".format(pack_key(name), pack_value(value)))

        mess = pack_measurement(measurement)

        if len(tags_part) > 0:
            mess += ","
            mess += ",".join(tags_part)

        if len(value_part) > 0:
            mess += ' '
            mess += ",".join(value_part)

        if timestamp:
            mess += ' '
            mess += str(timestamp)

        return mess

    async def insert(self, measurement, data, keys=None, timestamp=None, skip_escaping=False):
        self._sender.sendto(self.pack_message(measurement, data, keys, timestamp, skip_escaping=skip_escaping))
