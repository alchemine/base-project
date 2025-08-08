# Quick validation for README examples

import asyncio
from time import sleep

from src.common.timer import Timer, T
from src.common.depth_logging import D
from src.common.logger import slog, log_info, log_success, log_error, log_warning, log_api, STYLES
from src.common.request_utils import safe_request, async_safe_request


def _timer_examples():
    with Timer("Task 1"):
        sleep(0.01)

    @T
    def add(a, b):
        return a + b

    assert add(2, 3) == 5


@D
def _d_main():
    pass


async def _async_request_example():
    import aiohttp

    async with aiohttp.ClientSession() as session:
        # NOTE: this line is not executed in CI; it's only for import validation
        _ = session


if __name__ == "__main__":
    _timer_examples()
    _d_main()
    print("README examples validated.")
