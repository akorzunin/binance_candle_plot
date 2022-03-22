
import asyncio
from datetime import datetime, timezone

def compute_timedelta(dt: datetime):
    if dt.tzinfo is None:
        dt = dt.astimezone()
    now = datetime.now(timezone.utc)
    return max((dt - now).total_seconds(), 0)

async def sleep_until(when: datetime, result = None):
    """|coro|
    Sleep until a specified time.
    If the time supplied is in the past this function will yield instantly.
    .. versionadded:: 1.3
    Parameters
    -----------
    when: :class:`datetime.datetime`
        The timestamp in which to sleep until. If the datetime is naive then
        it is assumed to be local time.
    result: Any
        If provided is returned to the caller when the coroutine completes.
    """
    delta = compute_timedelta(when)
    return await asyncio.sleep(delta, result)