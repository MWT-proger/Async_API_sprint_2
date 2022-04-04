from abc import ABC, abstractmethod


class BaseService(ABC):

    @abstractmethod
    async def get_by_id(self, id: str):
        pass

    @abstractmethod
    async def get_specific_data(self,
                                query_search: str = None,
                                sort: str = None,
                                filter_genre: str = None,
                                page_size: int = 50,
                                page_number: int = 1,
                                ):
        pass
