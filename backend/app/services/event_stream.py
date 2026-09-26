import asyncio
import json
from collections import defaultdict
from collections.abc import AsyncIterator
from typing import Any


class EventStream:
    def __init__(self) -> None:
        self._events: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._queues: dict[str, list[asyncio.Queue[dict[str, Any] | None]]] = defaultdict(
            list)
        self._completed: set[str] = set()

    def publish(self, run_id: str, event: dict[str, Any]) -> None:
        self._events[run_id].append(event)
        for queue in self._queues[run_id]:
            queue.put_nowait(event)

    def complete(self, run_id: str) -> None:
        self._completed.add(run_id)
        for queue in self._queues[run_id]:
            queue.put_nowait(None)

    async def subscribe(self, run_id: str) -> AsyncIterator[str]:
        queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
        for event in self._events[run_id]:
            await queue.put(event)
        if run_id in self._completed:
            await queue.put(None)
        self._queues[run_id].append(queue)
        try:
            while True:
                event = await queue.get()
                if event is None:
                    break
                yield json.dumps(event, default=str)
        finally:
            self._queues[run_id].remove(queue)


stream = EventStream()
