from typing import TypeVar, AsyncIterator, Callable, Protocol, Any, List
import asyncio

T = TypeVar("T")

class PaginatedMethod(Protocol):
    async def __call__(self, *, start: int, count: int, **kwargs: Any) -> List[Any]: ...

async def paginate(
    method: Callable[..., Any],
    *,
    start: int = 0,
    count: int = 100, # Default page size
    max_results: int = float('inf'),
    **kwargs: Any
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
        max_results: Total items to yield before stopping.
        **kwargs: Arguments passed to the method (e.g. puuid, region).
    """
    
    current_start = start
    yielded = 0
    
    while yielded < max_results:
        # Determine batch size
        remaining = max_results - yielded
        batch_size = min(count, remaining) # Don't fetch more than needed if we hit max_results
        
        # Call API
        # Assumptions:
        # 1. Method accepts 'start' and 'count'
        # 2. Method returns a list
        results = await method(start=current_start, count=batch_size, **kwargs)
        
        if not results:
            break
            
        for item in results:
            yield item
            yielded += 1
            if yielded >= max_results:
                return
                
        # Prepare next page
        current_start += len(results)
        
        # Optimization: If response < batch_size, we probably exhausted the list.
        # But Riot APIs sometimes return fewer items than requested if filtering, 
        # so this heuristic is risky. 
        # Safest is to keep going until empty list if we asked for full page.
        if len(results) < batch_size and len(results) < count:
             break
