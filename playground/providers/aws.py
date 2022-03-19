from datetime import datetime, timedelta
import json
import boto3
from kink import inject

from ..interfaces.queue import IQueue

from typing import Sequence, TypeVar

T = TypeVar("T")


@inject(alias=IQueue)
class SqsQueue(IQueue[T]):
    def __init__(self):
        sqs = boto3.resource("sqs")
        self.queue = sqs.Queue("TODO: Some URL")

    def fetch(self, num_items: int) -> Sequence[T]:
        # TODO: Parse response to ensure type T is requrned
        return self.queue.receive_messages(MaxNumberOfMessages=num_items)

    def queue_data(self, data: T) -> None:
        # TODO: Make work...
        return self.queue.send_message(json.dumps(data))

    def queue_size(self) -> int:
        return self.queue.attributes["ApproximateNumberOfMessages"]

    def time_since_first_item(self) -> timedelta:
        # TODO: Make work...
        return timedelta(seconds=-1)
