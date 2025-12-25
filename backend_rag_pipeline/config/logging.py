import logging
import sys
import os
from datetime import datetime
from typing import Optional


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Setup comprehensive logging configuration for the application
    """
    # Determine log level
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create logger
    logger = logging.getLogger("rag_agent")
    logger.setLevel(numeric_level)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(console_formatter)

    # Create file handler if logging directory exists or can be created
    log_dir = os.getenv("LOG_DIR", "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    log_filename = os.path.join(
        log_dir,
        f"rag_agent_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(detailed_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Add error file handler for errors only
    error_filename = os.path.join(
        log_dir,
        f"rag_agent_errors_{datetime.now().strftime('%Y%m%d')}.log"
    )
    error_handler = logging.FileHandler(error_filename)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)

    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False

    # Log application startup
    logger.info("Logging system initialized")
    logger.info(f"Log level set to: {log_level}")
    logger.info(f"Log file: {log_filename}")
    logger.info(f"Error log file: {error_filename}")

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    """
    return logging.getLogger(name)


def setup_monitoring() -> dict:
    """
    Setup basic monitoring configuration
    Returns monitoring configuration for use in the application
    """
    monitoring_config = {
        "metrics_enabled": os.getenv("METRICS_ENABLED", "false").lower() == "true",
        "metrics_endpoint": os.getenv("METRICS_ENDPOINT", "/metrics"),
        "log_queries": os.getenv("LOG_QUERIES", "true").lower() == "true",
        "log_performance": os.getenv("LOG_PERFORMANCE", "true").lower() == "true",
        "performance_threshold_ms": int(os.getenv("PERFORMANCE_THRESHOLD_MS", "2000")),
    }

    logger = get_logger("monitoring")
    logger.info("Monitoring system initialized")
    logger.info(f"Metrics enabled: {monitoring_config['metrics_enabled']}")
    logger.info(f"Log queries: {monitoring_config['log_queries']}")
    logger.info(f"Log performance: {monitoring_config['log_performance']}")
    logger.info(f"Performance threshold: {monitoring_config['performance_threshold_ms']}ms")

    return monitoring_config


# Global logger instance
logger = setup_logging()

# Global monitoring configuration
monitoring = setup_monitoring()