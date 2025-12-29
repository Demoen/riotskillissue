import asyncio
from typing import TypeVar, Iterable, Awaitable, List

T = TypeVar("T")

async def gather_limited(tasks: Iterable[Awaitable[T]], limit: int = 10) -> List[T]:
    """
    Run tasks concurrently with a limit on the number of active tasks.
    Useful for batching requests without overwhelming the local event loop or 
    exceeding simplified concurrency limits.
    
    Args:
        tasks: Iterable of awaitables.
        limit: Max concurrent tasks.
        
    Returns:
        List of results in order.
    """
    sem = asyncio.Semaphore(limit)

    async def run_with_sem(task: Awaitable[T]) -> T:
        async with sem:
            return await task

    return await asyncio.gather(*(run_with_sem(t) for t in tasks))
