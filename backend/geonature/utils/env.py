
""" Helpers to manipulate the execution environment """

import os
import sys
import pip
import json

from pathlib import Path
from collections import ChainMap, namedtuple

import toml

from flask_sqlalchemy import SQLAlchemy

from geonature.utils.config_schema import GnGeneralSchemaConf, GnPySchemaConf
from geonature.utils.errors import ConfigError


ROOT_DIR = Path(__file__).absolute().parent.parent.parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'
DEFAULT_VIRTUALENV_DIR = BACKEND_DIR / "venv"
GEONATURE_VERSION = (ROOT_DIR / 'VERSION').read_text().strip()
DEFAULT_CONFIG_FIlE = Path('/etc/geonature/custom_config.toml')

DB = SQLAlchemy()

GN_MODULE_FILES = ('manifest.toml', 'backend/gn_module_main.py')

def in_virtualenv():
    """ Return if we are in a virtualenv """
    return hasattr(sys, 'real_prefix')


def virtualenv_status():
    """ Return if we are in a virtualenv or not, and if it's allowed """
    VirtualenvStatus = namedtuple(  # pytlint: disable=C0101
        'VirtualenvStatus',
        'in_venv no_venv_allowed'
    )

    return VirtualenvStatus(
        in_virtualenv(),  # Are we in a venv ?
        os.environ.get('GEONATURE_NO_VIRTUALENV')  # By pass venv check ?
    )


def venv_path(*children):
    """ Return the path to the current virtualenv

        If additional arguments are passed, they are concatenated to the path.
    """
    if not in_virtualenv():
        raise EnvironmentError(
            'This function can only be called in a virtualenv'
        )
    path = sys.exec_prefix
    return Path(os.path.join(path, *children))


def venv_site_packages():
    """ Return the path to the virtualenv site-packages dir """

    venv = venv_path()
    for path in sys.path:
        if path.startswith(str(venv)) and path.endswith('site-packages'):
            return Path(path)


def add_geonature_pth_file():
    """ Return the path to the virtualenv site-packages dir

        Returns a tuple (path, bool), where path is the Path object to
        the .pth file and bool is wether or not the line was added.
    """
    path = venv_site_packages() / 'geonature.pth'
    try:
        if path.is_file() and path.read_text():
            return path, False

        with path.open('a') as f:
            f.write(str(BACKEND_DIR) + "\n")
    except OSError:
        return path, False

    return path, True


def install_geonature_command():
    """ Install an alias of geonature_cmd.py in the virtualenv bin dir """
    add_geonature_pth_file()
    python_executable = venv_path('bin', 'python')

    cmd_path = venv_path('bin', 'geonature')
    with cmd_path.open('w') as f:
        f.writelines([
            "#!{}\n".format(python_executable),
            "import geonature.core.command\n",
            "geonature.core.command.main()\n"
        ])
    cmd_path.chmod(0o777)

def create_frontend_config(conf_file):
    if not os.path.isfile(conf_file):
        raise FileNotFoundError

    conf_toml = toml.load(conf_file)
    configs_gn, configerrors = GnGeneralSchemaConf().load(conf_toml)
    if configerrors:
        raise ConfigError(conf_file, configerrors)

    with open(
        str(ROOT_DIR / 'frontend/src/conf/frontend-config.ts'), 'w'
    ) as outputfile:
        outputfile.write("export const AppConfig = ")
        json.dump(configs_gn, outputfile, indent=True)


def get_config_file_path(config_file=None):
    """ Return the config file path by checking several sources

        1 - Parameter passed
        2 - GEONATURE_CONFIG_FILE env var
        3 - Default config file value
    """
    config_file = config_file or os.environ.get('GEONATURE_CONFIG_FILE')
    return Path(config_file or DEFAULT_CONFIG_FIlE)


def load_config(config_file=None):
    """ Load the geonature configuration from a given file """

    # load and validate configuration
    config_file = str(get_config_file_path(config_file))
    conf_toml = toml.load([config_file])

    # Load backend command only settings
    configs_py, configerrors = GnPySchemaConf().load(conf_toml)
    if configerrors:
        raise ConfigError(config_file, configerrors)

    # Settings also exported to backend
    configs_gn, configerrors = GnGeneralSchemaConf().load(conf_toml)
    if configerrors:
        raise ConfigError(config_file, configerrors)

    return ChainMap({}, configs_py, configs_gn)


def import_requirements(req_file):
    with open(req_file, 'r') as requirements:
        for req in requirements:
            if pip.main(["install", req]) == 1:
                raise Exception('Package {} not installed'.format(req))
