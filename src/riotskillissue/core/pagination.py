from typing import TypeVar, AsyncIterator, Callable, Optional, Protocol, Any, List
import asyncio

T = TypeVar("T")

class PaginatedMethod(Protocol):
    async def __call__(self, *, start: int, count: int, **kwargs: Any) -> List[Any]: ...

async def paginate(
    method: Callable[..., Any],
    *,
    start: int = 0,
    count: int = 100,
    max_results: Optional[int] = None,
    **kwargs: Any,
) -> AsyncIterator[T]:
    """
    Async iterator for paginated endpoints using start/count.

    Usage:
        async for match_id in paginate(client.match.get_ids_by_puuid, puuid="...", count=100):
            print(match_id)

    Args:
        method: The API method to call.
        start: Initial offset.
        count: items per page (passed to method as 'count').
        max_results: Total items to yield before stopping (``None`` = unlimited).
        **kwargs: Arguments passed to the method (e.g. puuid, region).
    """

    current_start = start
    yielded = 0

    while max_results is None or yielded < max_results:
        # Determine batch size
        remaining = (max_results - yielded) if max_results is not None else count
        batch_size = min(count, remaining)
        
        # Call API
        # 1. Method accepts 'start' and 'count'
        # 2. Method returns a list
        results = await method(start=current_start, count=batch_size, **kwargs)
        
        if not results:
            break
            
        for item in results:
            yield item
            yielded += 1
            if max_results is not None and yielded >= max_results:
                return
                
        # Prepare next page
        current_start += len(results)
        
        if len(results) < batch_size and len(results) < count:
             break
