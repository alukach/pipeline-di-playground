from datetime import timedelta
from typing import Sequence, TypeVar, cast
import json

import boto3
from kink import inject

from ..services.queue import IQueue
from ..services.secret import ISecret


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


@inject(alias=ISecret)
class SecretsManager(ISecret[T]):
    def get(self, key: str) -> T:
        # TODO: Make work...
        return cast(T, f"Let's pretend we just loaded '{key}' from SecretsManager")
