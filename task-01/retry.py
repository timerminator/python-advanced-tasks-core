import time
import functools
from typing import Callable, Tuple, Type, Union

class retry:
    def __init__(
        self,
        max_attempts: int = 3,
        initial_timeout: float = 1.0,
        timeout_multiplier: float = 2.0,
        exceptions: Union[Tuple[Type[BaseException], ...], Type[BaseException]] = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.initial_timeout = initial_timeout
        self.timeout_multiplier = timeout_multiplier
        self.exceptions = exceptions

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timeout = self.initial_timeout
            attempt = 1
            while attempt <= self.max_attempts:
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    if attempt == self.max_attempts:
                        raise
                    print(f"[retry] Попытка {attempt} не удалась: {e}. Повтор через {timeout} сек...")
                    time.sleep(timeout)
                    timeout *= self.timeout_multiplier
                    attempt += 1
        return wrapper