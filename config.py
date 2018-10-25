import os
class Config(object):
    """
    Common configurations
    """
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DATABASE_URL='dbname=jaystore user=postgres password=testia'
    DEBUG = True
    SECRET_KEY = "keepitasecret"

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "itsasecret"

class TestingConfig(Config):
    """
    Testing configurations
    """

    DATABASE_URL='dbname=testdb user=postgres password=testia'

    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
