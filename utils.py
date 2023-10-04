import random
from typing import List, Union

from pyrogram.types import Message


async def rand_delete(arr_m: List[Message], rand: Union[float, List[float]] = 0.5):
    if isinstance(rand, float):
        rand = [rand for _ in arr_m]
    for m, t in zip(arr_m, rand):
        if random.random() > t:
            await m.delete()
