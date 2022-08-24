from setuptools import setup, find_packages

setup(name='infcommon',
      version='0.0.1',
      author='Bifer Team',
      description='Common Infrastructure Utilities',
      platforms='Linux',
      packages=find_packages(exclude=['specs',
                                      'integration_specs']),
      install_requires=['sentry-sdk==1.9.5',
                        'aiocontextvars==0.2.2',
                        'PyYAML==6.0',
                        'jsonpickle==2.0.0'
                        ]
      )
