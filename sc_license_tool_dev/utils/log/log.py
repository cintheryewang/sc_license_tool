import logging.config
import yaml
import os


def setup_logging(default_path='.\logging_config.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration from a YAML file."""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
            # print(config)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


# 配置日志
setup_logging()


def get_logger(name):
    return logging.getLogger(name)
