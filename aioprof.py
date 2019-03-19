import asyncio
import logging

from pyinstrument import Profiler
from pyinstrument.renderers.console import ConsoleRenderer


logger = logging.getLogger(__file__)


def start(loop=None, interval=0.001):
    profiler = AsyncioProfiler(interval=interval)

    log_handler = AsyncioLogHandler(profiler, loop=loop)
    logging.getLogger("asyncio").addHandler(log_handler)

    profiler.start()


class AsyncioLogHandler(logging.StreamHandler):
    def __init__(self, profiler, loop=None):
        super().__init__()
        self.profiler = profiler
        self.loop = loop

    def emit(self, record):
        super().emit(record)
        if record.msg == "Executing %s took %.3f seconds":
            if not self.loop:
                loop = asyncio.get_event_loop()

            if hasattr(loop._current_handle._callback, "__self__"):
                self.report(loop._current_handle._callback.__self__)

    def report(self, task):
        self.profiler.frame_records = self.profiler.filter_frame_records_by_task(task)

        self.profiler.stop()

        logger.warning(
            self.profiler.output(
                ConsoleRenderer(unicode=True, color=False, show_all=True)
            )
        )

        self.profiler.frame_records = []
        self.profiler.start()


class AsyncioProfiler(Profiler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _profile(self, frame, event, arg):
        len_frame_records = len(self.frame_records)

        super()._profile(frame, event, arg)

        task = asyncio.Task.current_task()

        if len(self.frame_records) > len_frame_records:
            self.frame_records[-1] = self.frame_records[-1] + (task,)

    def filter_frame_records_by_task(self, task):
        return [x for x in self.frame_records if x[2] == task]
