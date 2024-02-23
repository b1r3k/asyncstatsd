# asyncstatsd

## Installation

    $ pip install asyncstatsd

## Usage

### Pure statsd

```python
import asyncio
from asyncstatsd.client import StatsdClient


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
import asyncio
from asyncstatsd.client import DatadogClient


def foo(statsd):
    statsd.incr('some.counter', tags=dict(tag1='value1', tag2='value2'))
    statsd.timing('some.timer', 320, tags=dict(tag1='value1', tag2='value2'))


async def bar(statsd):
   statsd.incr('some.counter', tags=dict(tag1='value1', tag2='value2'))
   statsd.timing('some.timer', 320, tags=dict(tag1='value1', tag2='value2')
   with statsd.timer('some.timer', tags=dict(tag1='value1', tag2='value2'):
       await asyncio.sleep(1)


async def main():
    client = DatadogClient('localhost', 8125)
    await client.connect()
    foo(client)
    await bar(client)
```

## Statsd null client

```python
import asyncio
import os
from asyncstatsd.client import DatadogClient, NullStatsdClient


def get_statsd_client():
    if os.environ.get('STATSD_ENABLED', 'false').lower() == 'true':
        return DatadogClient('localhost', 8125)
    else:
        return NullStatsdClient()


def foo():
    statsd = get_statsd_client()
    statsd.incr('some.counter', tags=dict(tag1='value1', tag2='value2'))
    statsd.timing('some.timer', 320, tags=dict(tag1='value1', tag2='value2'))


async def bar(statsd):
    statsd = get_statsd_client()
    statsd.incr('some.counter', tags=dict(tag1='value1', tag2='value2'))
    statsd.timing('some.timer', 320, tags=dict(tag1='value1', tag2='value2')
    with statsd.timer('some.timer', tags=dict(tag1='value1', tag2='value2'):
        await asyncio.sleep(1)


async def main():
    client = DatadogClient('localhost', 8125)
    await client.connect()
    foo()
    await bar()
```
