'''
This module provides default configuration and the global instance for the utils.Config class.
'''
import os.path as path
from sys import stderr

import yaml
from pycslib.utils import Toucan

import utils.log as log_cfg
from utils import Config

# default values
# from utils.toucan import Toucan
from utils.toucan_monitor import ToucanMonitor

LOG_DIR = path.join(path.dirname(__file__), 'logs')

_DEFAULT = {
    'logging': {
        'root': {
            'file': path.join(LOG_DIR, 'aucote.log'),
            'level': 'info',
            'max_file_size': 10 * 1024 * 1024,
            'max_files': 5,
            'format': '%(levelname)s %(asctime)s %(funcName)s: %(message)s',
            'propagate': True
        },
        'storage': {
            'file': path.join(LOG_DIR, 'storage.log'),
            'level': 'info',
            'max_file_size': 10 * 1024 * 1024,
            'max_files': 10,
            'format': '%(levelname)s %(asctime)s %(message)s',
            'propagate': False
        },
        'pycslib': {
            'file': path.join(LOG_DIR, 'pycslib.log'),
            'level': 'info',
            'max_file_size': 10 * 1024 * 1024,
            'max_files': 10,
            'format': '%(levelname)s %(asctime)s %(message)s',
            'propagate': False
        }
    },
    'fixtures': {
        'exploits': {
            'filename': 'fixtures/exploits/exploits.csv'
        }
    },
    'topdis': {
        'api': {
            'host': 'localhost',
            'port': 1234
        },
        'fetch_os': False
    },
    'toucan': {
        'enable': True,
        'api': 'http://toucan:3000',
        'min_retry_time': 5,
        'max_retry_time': 60 * 5,
        'max_retry_count': 20
    },
    'pid_file': 'aucote.pid',
    'default_config': 'aucote_cfg_default.yaml',
}

# global cfg
cfg = Config(_DEFAULT)


async def start_toucan(default_config):
    """
    Initialize Toucan

    Args:
        default_config:

    Returns:
        None

    """
    Toucan.min_retry_time = cfg['toucan.min_retry_time']
    Toucan.max_retry_time = cfg['toucan.max_retry_time']
    Toucan.max_retry_count = cfg['toucan.max_retry_count']

    cfg.toucan = Toucan(api=cfg['toucan.api'], prefix='aucote')

    # Add toucan monitor
    cfg.toucan_monitor = ToucanMonitor(toucan=cfg.toucan)
    cfg.toucan_monitor.start()

    if cfg['rabbit.enable']:
        await cfg.start_rabbit(cfg['rabbit.host'], int(cfg['rabbit.port']), cfg['rabbit.username'],
                               cfg['rabbit.password'])

    if cfg['toucan.push_default']:
        with open(default_config, "r") as file:
            config = yaml.safe_load(file)

        await cfg.toucan.async_push_config(config, overwrite=cfg['toucan.overwrite'])


async def load(file_name=None):
    '''
    Initializes this module.
    Needs to be called before other functions are used.
    '''

    if file_name is None:
        # by default search for "confg.yaml" in application dir
        file_name = path.join(path.dirname(__file__), 'aucote_cfg.yaml')

    file_name = path.abspath(file_name)
    # at this point logs do not work, print info to stdout
    print("Reading configuration from file:", file_name)
    try:
        cfg.load(file_name, _DEFAULT)
    except Exception:
        stderr.write("Cannot load configuration file {0}".format(file_name))
        exit()

    await log_cfg.config(cfg['logging'])

    default_config_filename = cfg['default_config']

    if cfg['toucan.enable']:
        await start_toucan(default_config_filename)
    else:
        try:
            cfg.load(default_config_filename, cfg.cfg)
        except Exception:
            stderr.write("Cannot load configuration file {0}".format(default_config_filename))
            exit()
