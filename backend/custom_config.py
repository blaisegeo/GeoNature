# coding: utf8

from default_config import Config
class CustomConfig(Config):
    '''
    GeoNature backend customisation configuration file
    In this this file you can override any setting from default_config.py
    '''

    # Database
    SQLALCHEMY_DATABASE_URI = "postgresql://onf_admin:Martine50=@localhost:5432/geonature2db"

    # Application
    URL_APPLICATION = 'http://my_url.com/geonature'          # Replace my_url.com by your domain or IP
    API_ENDPOINT = 'http://my_url.com/geonature/api'         # Replace my_url.com by your domain or IP
