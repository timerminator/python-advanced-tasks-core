import logging
import time
import  functools
from typing import Callable, Tuple, Type, Optional, Union

from config import config
from exceptions import RequestError

log = logging.getLogger(__name__)




def retry(
    _func: Optional[Callable] = None,
    *,
    max_attempts: int = 3,
    initial_timeout: float = 1.0,
    timeout_multiplier: float = 2.0,
    exceptions: Union[Tuple[Type[BaseException], ...], Type[BaseException]] = (Exception,)
):
    """
    Декоратор для повторных попыток вызова функции при определённых исключениях.
    
    Можно использовать как:
        @retry
        @retry()
        @retry(max_attempts=5, ...)
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timeout = initial_timeout
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    else:
                        log.exception(f"Попытка {attempt} не удалась: {e}. Повтор через {timeout} сек...")
                        time.sleep(timeout)
                        timeout *= timeout_multiplier
                        attempt += 1
        return wrapper

    # Если декоратор вызван без скобок — @retry
    if _func is not None and callable(_func):
        return decorator(_func)

    # Если декоратор вызван с параметрами — @retry(...)
    return decorator


class CustomWeatherFetcher:
    def __init__(self):
        self._call_count = 0
        
    @retry(max_attempts=10)
    def fetch_weather_or_raise_error(
        self,
        url: str,
        timeout: int,
        headers: dict[str, str] | None,
    ) -> dict[str, str | int]:
        """
        Функция, которая в зависимости от номера попытки
        либо выкидывает исключение, либо отрабатывает нормально.

        Такое поведение возможно только для демонстрации,
        перед новой демонстрацией необходимо сбрасывать счётчик.
        """
        self._call_count += 1

        log.debug(
            "Fetching data from %s with headers %s. Will take %ss",
            url,
            headers,
            timeout,
        )
        time.sleep(timeout)
        if self._call_count == config.success_on_attempt:
            return {"temperature": 16, "rain-chance": 42, "sky": "clouds"}
        msg = f"failed to fetch data from {url} with headers {headers}"
        raise RequestError(msg)

    def reset_call_count(self):
        self._call_count = 0


weather_fetcher = CustomWeatherFetcher()
print(weather_fetcher.fetch_weather_or_raise_error("ya.ru", 5, None))
