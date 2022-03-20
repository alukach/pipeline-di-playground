from collections import deque
from datetime import timedelta
from typing import Sequence, TypeVar, cast

from kink import inject

from ..services.queue import IQueue
from ..services.secret import ISecret


T = TypeVar("T")


@inject(alias=IQueue)
class LocalQueue(IQueue[T]):
    def __init__(self):
        self.queue = deque()

    def fetch(self, num_items: int) -> Sequence[T]:
        return [self.queue.pop() for i in range(num_items)]

    def queue_data(self, data: T) -> None:
        return self.queue.append(data)

    def queue_size(self) -> int:
        return self.queue.count()

    def time_since_first_item(self) -> timedelta:
        return self.queue.TODO


@inject(alias=ISecret)
class DotEnv(ISecret[T]):
    def get(self, key: str) -> T:
        # TODO: Make work
        return cast(T, f"Let's pretend we just loaded '{key}' from a .env file")