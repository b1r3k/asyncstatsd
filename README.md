# asyncstatsd

## Installation

    $ pip install asyncstatsd

## Usage

### Pure statsd

```python
from aiostatsd.client import StatsdClient


def foo(statsd):
    statsd.incr('some.counter')
    statsd.timing('some.timer', 320)


async def bar(statsd):
   statsd.incr('some.counter')
   statsd.timing('some.timer', 320)
   with statsd.timer('some.timer'):
       await asyncio.sleep(1)


async def main():
    client = StatsdClient('localhost', 8125)
    await client.connect()
    foo(client)
    await bar(client)
```

### Statsd extended with Datadog tags

```python
from aiostatsd.client import DatadogClient


def foo(statsd):
    statsd.incr('some.counter', tags=['tag1:value1', 'tag2:value2'])
    statsd.timing('some.timer', 320, tags=['tag1:value1', 'tag2:value2'])


async def bar(statsd):
   statsd.incr('some.counter', tags=['tag1:value1', 'tag2:value2'])
   statsd.timing('some.timer', 320, tags=['tag1:value1', 'tag2:value2'])
   with statsd.timer('some.timer', tags=['tag1:value1', 'tag2:value2']):
       await asyncio.sleep(1)


async def main():
    client = DatadogClient('localhost', 8125)
    await client.connect()
    foo(client)
    await bar(client)
```
