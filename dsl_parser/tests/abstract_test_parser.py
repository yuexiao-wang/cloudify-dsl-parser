########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'ran'

import tempfile
import shutil
import unittest
import os
import uuid
from dsl_parser.parser import DSLParsingException, DSLParsingLogicException
from dsl_parser.parser import parse, parse_from_file


class AbstractTestParser(unittest.TestCase):

    BASIC_APPLICATION_TEMPLATE = """
application_template:
    name: testApp
    topology:
        -   name: testNode
            type: test_type
            properties:
                key: "val"
        """

    BASIC_INTERFACE_AND_PLUGIN = """
interfaces:
    test_interface1:
        operations:
            -   "install"
            -   "terminate"

plugins:
    test_plugin:
        properties:
            interface: "test_interface1"
            url: "http://test_url.zip"
            """

    BASIC_TYPE = """
types:
    test_type:
        interfaces:
            -   test_interface1
        properties:
            install_agent: 'false'
            """

    MINIMAL_APPLICATION_TEMPLATE = BASIC_APPLICATION_TEMPLATE + """
types:
    test_type: {}
    """

    APPLICATION_TEMPLATE = BASIC_APPLICATION_TEMPLATE + BASIC_INTERFACE_AND_PLUGIN + BASIC_TYPE

    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._temp_dir)

    def make_file_with_name(self, content, filename):
        filename_path = os.path.join(self._temp_dir, filename)
        with open(filename_path, 'w') as f:
            f.write(content)
        return filename_path

    def make_yaml_file(self, content):
        filename = 'tempfile{0}.yaml'.format(uuid.uuid4())
        return self.make_file_with_name(content, filename)

    def create_yaml_with_imports(self, contents):
        yaml = """
imports:"""
        for content in contents:
            filename = self.make_yaml_file(content)
            yaml += """
    -   {0}""".format(filename)
        return yaml

    def _assert_dsl_parsing_exception_error_code(self, dsl, expected_error_code, exception_type=DSLParsingException,
                                                parsing_method=parse):
        try:
            parsing_method(dsl)
            self.fail()
        except exception_type, ex:
            self.assertEquals(expected_error_code, ex.err_code)
            return ex