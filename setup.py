from setuptools import setup, find_packages

setup(name='infcommon',
      version='0.0.1',
      author='Bifer Team',
      description='Common Infrastructure Utilities',
      platforms='Linux',
      packages=find_packages(exclude=['tests', 'integration_tests', 'specs', 'integration_specs']),
      install_requires=['raven==6.10.0',
                        'mysqlclient==1.4.1',
                        'retrying==1.3.3',
                        'psycopg2==2.7.7',
                        'psycopg2-binary==2.7.7',
                        'PyYAML==4.2b4',
                        ]
      )

