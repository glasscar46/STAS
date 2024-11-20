import logging
import functools


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_method(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            logger.error(f'Error in {func.__name__}: {e}')
            raise
    return wrapper