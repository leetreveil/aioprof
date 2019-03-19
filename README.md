# aioprof

Ever tried to debug code that blocks the event loop? If you've tried you've probably came across warning messages from `asyncio` that look like this:

```
Executing <Task finished coro=<Application._handle() done,
defined at /usr/local/lib/python3.7/site-packages/aiohttp/web_app.py:428> result=<Response OK not prepared>
created at /usr/local/lib/python3.7/site-packages/aiohttp/web_protocol.py:417> took 1.011 seconds
```

Understanding exactly what blocked the event loop is almost impossible from just looking at the log message alone.

`aioprof` builds on top of the excellent call stack profiler [pyinstrument](https://github.com/joerick/pyinstrument) to turn log messages like the above into something much more useful:

```shell
Executing <Task finished coro=<Application._handle() done,
defined at /usr/local/lib/python3.7/site-packages/aiohttp/web_app.py:428> result=<Response OK not prepared>
created at /usr/local/lib/python3.7/site-packages/aiohttp/web_protocol.py:417> took 1.011 seconds

  _     ._   __/__   _ _  _  _ _/_   Recorded: 14:51:29  Samples:  4
 /_//_/// /_\ / //_// / //_'/ //     Duration: 6.310     CPU time: 0.020
/   _/                      v3.0.1

Program: maiohttp.py

1.011 <module>  maiohttp.py:1
└─ 1.011 run_app  aiohttp/web.py:375
   └─ 1.011 run_until_complete  asyncio/base_events.py:549
      └─ 1.011 run_forever  asyncio/base_events.py:522
         └─ 1.011 _run_once  asyncio/base_events.py:1679
            └─ 1.011 _run  asyncio/events.py:86
               └─ 1.011 _handle  aiohttp/web_app.py:428
                  └─ 1.011 simple  maiohttp.py:44
                     └─ 1.011 blocking_method  maiohttp.py:40
```

From the call stack above we can see that the `blocking_method` function call blocked the event loop for one second. Case closed!

`aioprof` works by continuously profiling your program and hooks into the `asyncio` logging handler to produce reports as see above.

## Installation

```shell
$ pip install aioprof
```


## Getting started

Instrument your `asyncio` program:

```python
import aioprof

aioprof.start()

# start your event loop...
```

Run your program with the `PYTHONASYNCIODEBUG` environment variable enabled:

```shell
PYTHONASYNCIODEBUG=1 python app.py
```


