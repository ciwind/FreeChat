from loguru import logger as _logger


class MyLogger:
    __instance = None
    _logger.remove(handler_id=None)
    _logger.add(f"app.log", rotation="100MB", encoding="utf-8", enqueue=True, retention="10 days")
    _logger.add(lambda msg: print(msg, end=''), level="DEBUG", format="{time} {level} {message}")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(MyLogger, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def info(self, msg, *args, **kwargs):
        return _logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return _logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return _logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return _logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        return _logger.exception(msg, *args, **kwargs)


logger = MyLogger()
if __name__ == '__main__':
    logger.info("中文test")
    logger.debug("中文test")
    logger.warning("中文test")
    logger.error("中文test")
