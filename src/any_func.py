import logging
from decorators import log_function_decorator
from logging_config import logger


# Пример использования декоратора
@log_function_decorator
def example_function(x, y):
    # Тестовые сообщения
    # logger.debug('Это сообщение уровня DEBUG.')
    # logger.info('Это сообщение уровня INFO.')
    # logger.warning('Это сообщение уровня WARNING.')
    # logger.error('Это сообщение уровня ERROR.')
    # logger.critical('Это сообщение уровня CRITICAL.')
    return x / y

# Вызов функции
result = example_function(3, 1)