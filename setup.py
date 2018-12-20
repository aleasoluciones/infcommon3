from setuptools import setup, find_packages

setup(name='infcommon3',
      version='0.0.1',
      author='Bifer Team',
      description='Common Infrastructure Utilities',
      platforms='Linux',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'specs', 'integration_specs'])
      )

