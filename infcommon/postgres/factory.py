# -*- coding: utf-8 -*-

import os

from infcommon.factory import Factory
from infcommon.postgres.postgres import PostgresClient

def postgres_client_from_connection_parameters(user, password, host, port, db_name):
    connection_uri = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(user=user, password=password, host=host, port=port, db_name=db_name)
    return Factory.instance('posgres_client_from_connection_parameters',
                            lambda: PostgresClient(connection_uri)
                           )

def postgres_client_from_connection_os_variable(db_uri_os_valiable_name='LOCAL_PG_DB_URI'):
    connection_uri = os.getenv(db_uri_os_valiable_name)
    return Factory.instance('posgres_client_from_connection_parameters',
                            lambda: PostgresClient(connection_uri)
                           )
