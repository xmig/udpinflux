# udpinflux


## Asyncio InfluxDB UDP Client

Important:
 - InfluxDB server should be configured for support UDP
   (please UNCOMMENT the corresponded section in 'influxdb.conf' file)
 - The ONLY a predefined database name (default 'udp') can be used for UPD
   (you can configure different ports for different databases)


Protocol description: https://docs.influxdata.com/influxdb/v0.9/write_protocols/write_syntax/

USAGE:
```python
EXAMPLE = {
        "value1": 100,
        "value2": 200,
        "tag0": 'Hello, World!',
        "tag1": '100i',
    }

TAGS = ["tag0", "tag1"]

from udpinflux.influx_UDP_client import InfluxUDPClint

async def store_example(loop):
    async with InfluxUDPClint(loop=loop, port=8089) as client:
        await client.insert('test', EXAMPLE, TAGS)
```
        
