import logging

_web_logger: logging.Logger = None
def setup_logger(file_name: str):
    global _web_logger
    logging.basicConfig(level=logging.INFO)
    _web_logger = logging.getLogger(file_name)
    return _web_logger

def get_logger():
    if _web_logger is None:
        raise ValueError("Web logger is not defined")
    return _web_logger

