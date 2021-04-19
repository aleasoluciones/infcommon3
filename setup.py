from setuptools import setup, find_packages

setup(name='infcommon',
      version='0.0.1',
      author='Bifer Team',
      description='Common Infrastructure Utilities',
      platforms='Linux',
      packages=find_packages(exclude=['ez_setup',
                                      'examples',
                                      'tests',
                                      'specs',
                                      'integration_specs']),
      install_requires=['sentry-sdk==1.0.0',
                        'aiocontextvars==0.2.2',
                        'retrying==1.3.3',
                        'psycopg2==2.8.6',
                        'PyYAML==4.2b4',
                        'jsonpickle==1.2'
                        ]
      )

