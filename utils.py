import time
from itertools import count
from typing import Iterator

from client import MensaSession
from mensa import Meal


def mass_like(mensa: MensaSession, meal: Meal, n: int | None, interval: float = 2.0) -> Iterator[int]:
    for _ in range(n) if n is not None else count():
        start_time = time.perf_counter()
        yield mensa.like_meal(meal)
        elapsed = time.perf_counter() - start_time

        sleep_time = max(0.0, interval - elapsed)
        if sleep_time > 0:
            time.sleep(sleep_time)
