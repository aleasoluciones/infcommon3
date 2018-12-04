# -*- coding: utf-8 -*-

import sys
import types
import importlib
import traceback
import os
import fnmatch
import re
from datetime import datetime


TOTALS_TESTS_PASSED = 0
LAST_CALL = None
GREEN_COLOR = "\033[0;32m"
WHITE_COLOR = "\033[0;39m"
RED_COLOR = "\033[91m"


def find_and_call_functions_from():
    global TOTALS_TESTS_PASSED
    global LAST_CALL

    factories = []
    current_working_directory = os.getcwd()

    for root, _, filenames in os.walk(current_working_directory):
        for filename in fnmatch.filter(filenames, '*factory.py'):
            factory_relative_path = ".{}".format(os.path.join(root, filename).replace(current_working_directory, ''))
            if 'src' not in factory_relative_path and 'build' not in factory_relative_path:
                factories.append(factory_relative_path)

    initial_time = datetime.utcnow()

    for factory_file in factories:
        a_factory = _import_module(factory_file)
        for element_name in dir(a_factory):
            element = getattr(a_factory, element_name)
            if callable(element):
                if isinstance(element, types.FunctionType) and not element_name.startswith('__'):
                    LAST_CALL = "===> Exception in Factory file: {} Testing to call: {}".format(factory_file, element_name)
                    element()
                    TOTALS_TESTS_PASSED += 1
                    sys.stdout.write(GREEN_COLOR)
                    sys.stdout.write(".")
                    sys.stdout.write(WHITE_COLOR)

    elapsed_time = datetime.utcnow() - initial_time
    print('')
    print(GREEN_COLOR)
    print("{} examples ran in {:.4f} seconds{}".format(TOTALS_TESTS_PASSED, elapsed_time.total_seconds(), WHITE_COLOR))


def _import_module(module_name):
    try:
        file_to_import = re.sub('\./.+?/', '', module_name).replace('/', '.').replace('.py', '')
        return importlib.import_module(file_to_import)
    except Exception:
        file_to_import = re.sub('\./', '', module_name).replace('/', '.').replace('.py', '')
        return importlib.import_module(file_to_import)
    #https://stackoverflow.com/questions/4821104/python-dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported


def run():
    try:
        find_and_call_functions_from()
        sys.exit(0)
    except Exception as exc:
        print('')
        print(RED_COLOR)
        print("{} -> {}".format(LAST_CALL, exc))
        print()
        traceback.print_exc()
        print(WHITE_COLOR)
        print('')
        sys.exit(1)
