"""
Logging setup for the wallet checker.
Configures a logger that writes timestamped entries to a file and the console.
"""

import logging
import sys

def setup_logger(log_file='wallet_checker.log'):
    """
    Create a logger that logs INFO and higher to a file and console.
    The log format includes time, thread name, level, and message.
    """
    logger = logging.getLogger("WalletKeyChecker")
    logger.setLevel(logging.INFO)

    # File handler to write logs to file
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    # Console handler for stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Formatter: include time, name, level, thread, and message
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
