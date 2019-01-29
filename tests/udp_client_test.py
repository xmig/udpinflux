import asyncio
from udpinflux.influx_UDP_client import InfluxUDPClint
from udpasync.utils.trivial_logger import PrintLogger

EXAMPLE = {
        "value1": 200,
        "value2": 200,
        "tag0": 'Just hello',
        "tag1": 'sys=tem',
    }

TAGS = ["tag0", "tag1"]


async def test(loop):
    async with InfluxUDPClint(loop=loop, port=8089, logger=PrintLogger()) as client:
        await client.insert('test', EXAMPLE, TAGS)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
