from collections import deque


class EventQueue:
   
    def __init__(self, max_size: int = 1000):
        self._events = deque(maxlen=max_size)

    def add(self, event: dict) -> None:
        self._events.append(event)

    def add_many(self, events: list[dict]) -> None:
        self._events.extend(events)

    def get_batch(self, size: int) -> list[dict]:
        batch = []

        for _ in range(min(size, len(self._events))):
            batch.append(self._events.popleft())

        return batch

    def size(self) -> int:
        return len(self._events)

    def requeue(self, events: list[dict]) -> None:
        for event in reversed(events):
            self._events.appendleft(event)