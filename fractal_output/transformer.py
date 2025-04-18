from abc import ABC, abstractmethod
from .resource import Item, Collection, Null


class Transformer(ABC):
    available_includes = []
    default_includes = []

    @abstractmethod
    async def transform(self, source):
        raise NotImplementedError

    def item(self, source, transformer):
        return Item(source, transformer)

    def collection(self, source, transformer):
        return Collection(source, transformer)

    def null(self):
        return Null()
