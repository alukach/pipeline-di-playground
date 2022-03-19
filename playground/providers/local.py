from collections import deque
from datetime import timedelta
from typing import Sequence, TypeVar

from kink import inject

from ..interfaces.queue import IQueue


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
