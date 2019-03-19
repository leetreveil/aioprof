import asyncio

# from asyncio import async
import time

import pytest

from aioprof import AsyncioProfiler, start

import time


def test_basic():
    prof = AsyncioProfiler()
    prof.start()

    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def a():
        time.sleep(0.1)

    tasks = [asyncio.ensure_future(a())]

    loop.run_until_complete(asyncio.wait(tasks))

    prof.stop()

    for t in tasks:
        records = prof.filter_frame_records_by_task(t)
        assert len(records) > 0
