#!/usr/bin/python
# -*-coding:utf-8-*-
# Author:Citron
"""
  Generate different log files according to different options
"""
import yaml
import os
import logging.config
import logging

_LOG_DIR_NAME="log"
def setup_logging(
        default_path='log_config.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    '''
       Setup logging configuration
    '''
    if not os.path.exists(_LOG_DIR_NAME):
        os.mkdir(_LOG_DIR_NAME)
    path=default_path
    value=os.getenv(env_key,None)
    if  value:
        path=value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


