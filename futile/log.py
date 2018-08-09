import os
import sys
import logging
import logging.handlers


def get_logger(name, level=logging.DEBUG):
    """
    生成一个logger，日志会交给上层的logger处理
    """
    logger = logging.getLogger(name)
    logger.propagate = True
    if not logger.handlers:
        handler = logging.NullHandler()
        logger.addHandler(handler)
        # handler 不设置级别
        logger.setLevel(level)
    return logger


def init_log(script_name,
             console_level=logging.INFO,
             file_level=logging.DEBUG,
             additional_handlers=None):
    root_logger = logging.getLogger('')
    root_logger.handlers = []
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(threadName)s-%(levelname)s - %(message)s - %(filename)s:%(lineno)d')

    # add console logger
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)
    root_logger.addHandler(console_handler)

    # add file logger
    home = os.environ.get('HOME')
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=f'{home}/log/{script_name}.log',
        when='D',
        backupCount=7,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)
    root_logger.addHandler(file_handler)

    if additional_handlers:
        for handler in additional_handlers:
            root_logger.addHandler(handler)
