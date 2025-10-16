import logging


def setup_logger(name, log_file="history.log"):
    logging.basicConfig(
        level=logging.INFO,
        filename=log_file,
        format="%(levelname)s-%(name)s-%(asctime)s:%(message)s",
        force=True,
    )
    logger = logging.getLogger(name)
    return logger
