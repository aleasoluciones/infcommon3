2019-11-20
==========
* Internal. Generic factory test: Manage when the function has defaults and/or required arguments

2019-11-19
==========
* Internal. Add execution of sql statements using transactions at PostgresClient

2019-11-04
==========
* Internal. Generic factory test: check if function has requried arguments

2019-09-11
==========
* Feature. Add mysql client to infcommon module

2019-08-14
==========
* Feature. Always return variable value if present in environment variables

2019-06-11
==========
* Internal. Do not initialize Sentry if SENTRE_DSN environment variable is '' or None

2019-04-09
==========
* Add path to yaml_reader singleton id

2019-03-12
==========
* Internal. Logger class check TEST_MODE variable before log

2019-01-09
==========
* Internal. Update PyYAML

2018-12-21
==========
* Internal. directory_yaml_loader can raise DuplicatedKeyError(Exception) (no RuntimeError)

2018-12-20
==========
* Update readme with more detailed information
* Update python modules at requirements and requirements-dev
* Update travis jobs to use python 3.5, 3.6 and 3.7-dev
* Add DirectoryYamlLoader to infcommon.yaml_loaders

2018-06-13
==========
* Added factory.
* Created mysqlclient. Compatible with python2 and python3.
* Update raven library.
