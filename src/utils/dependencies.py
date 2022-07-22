async def offset_limit_paginator(offset: int = 0, limit: int = 100):
    return {"offset": offset, "limit": limit}
