from setuptools import setup, find_packages

setup(name='infcommon',
      version='0.0.1',
      author='Bifer Team',
      description='Common Infrastructure Utilities',
      platforms='Linux',
      packages=find_packages(exclude=['specs',
                                      'integration_specs']),
      install_requires=['sentry-sdk==1.15.0',
                        'aiocontextvars==0.2.2',
                        'PyYAML==6.0',
                        'jsonpickle==3.0.1'
                        ]
      )
