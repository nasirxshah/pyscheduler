from datetime import datetime
from typing import Callable
import threading
import asyncio
import logging

logger = logging.getLogger("scheduler")


class Scheduler:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def every(self, interval=1):
        return Every(self, interval)

    async def run(self, threaded=False):
        _tasks = []
        for task in self.tasks:
            _tasks.append(asyncio.create_task(task.run(threaded=threaded)))

        for _task in _tasks:
            await _task


class Every:
    def __init__(self, scheduler: Scheduler, interval=1) -> None:
        self.interval = interval
        self.step = 0
        self.scheduler = scheduler

    @property
    def hour(self):
        self.step = 3600 * self.interval
        return At(self.scheduler, self.step)

    @property
    def minute(self):
        self.step = 60 * self.interval
        return At(self.scheduler, self.step)

    @property
    def second(self):
        self.step = 1 * self.interval
        return At(self.scheduler, self.step)


class At:
    def __init__(self, scheduler: Scheduler, step) -> None:
        self.scheduler = scheduler
        self.step = step

    def at(self, hms):
        hour, minute, second = tuple(map(int, hms.split(":")))
        _now = datetime.now()
        _at = datetime(_now.year, _now.month, _now.day, hour, minute, second)

        return Task(self.scheduler, self.step, _at)


class Task:
    def __init__(self, scheduler: Scheduler, step, starts_at) -> None:
        self.scheduler = scheduler
        self.step = step
        self.starts_at = starts_at

    def do(self, target: Callable, args=(), kwargs={}):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.scheduler.tasks.append(self)

    def __str__(self) -> str:
        return f"Task[target={self.target.__name__}]"

    async def run(self, threaded=False):
        if self.starts_at > datetime.now():
            logger.debug(f"{self} waiting...")
            await asyncio.sleep((self.starts_at - datetime.now()).total_seconds()-self.step)

        while True:
            logger.debug(f"{self} sleeping for {self.step}")
            await asyncio.sleep(self.step)
            logger.debug(f"{self} started")
            if threaded:
                thread = threading.Thread(
                    target=self.target, args=self.args, kwargs=self.kwargs)
                thread.start()
            else:
                self.target(*self.args, **self.kwargs)
            logger.debug(f"{self} done")
