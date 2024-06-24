import os

environment = os.getenv("ENV", "local")

if environment=="dev":
    from db_config.database_settings_dev import ELASTIC_SEARCH
elif environment=="ops":
    from db_config.database_settings_ops import ELASTIC_SEARCH
else :
    from db_config.database_settings_local import ELASTIC_SEARCH