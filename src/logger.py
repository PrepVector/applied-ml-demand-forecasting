# src/utils/logger.py

import logging
import os


class ProjectLogger:
    """
    ProjectLogger class for setting up logging and writing logs to a file.
    """

    LOG_FILE_PATH = "logs/global_log.log"

    def __init__(self):
        """
        Initialize the ProjectLogger.
        """
        # Ensure logs directory exists
        os.makedirs(os.path.dirname(self.LOG_FILE_PATH), exist_ok=True)

        # Set up logging configuration
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(self.LOG_FILE_PATH), logging.StreamHandler()],
        )

        # Get logger instance
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        return self.logger
