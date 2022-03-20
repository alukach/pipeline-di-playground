from abc import abstractmethod
from typing import Protocol, TypeVar

T = TypeVar("T", covariant=True)


class ISecret(Protocol[T]):
    @abstractmethod
    def get(self, key: str) -> T:
        ...
