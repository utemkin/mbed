"""
mbed SDK
Copyright (c) 2011-2013 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import uuid
from sys import stdout
from host_test import TestResults, Test


class EchoTest(Test):
    """ This host test will use mbed serial port with 
        baudrate 115200 to perform echo test on that port.
    """

    def __init__(self):
        # Constructors
        TestResults.__init__(self)
        Test.__init__(self)
        
        # Test parameters
        self.TEST_SERIAL_BAUDRATE = 115200
        self.TEST_LOOP_COUNT = 50

        # Initializations
        serial_init_res = self.mbed.init_serial(self.TEST_SERIAL_BAUDRATE)
        if not serial_init_res:
            self.print_result(self.RESULT_IO_SERIAL)
        self.mbed.reset()

    def test(self):
        """ Test function, return True or False to get standard test notification on stdout
        """
        c = self.mbed.serial_readline() # '{{start}}'
        if c is None:
            return self.RESULT_IO_SERIAL
        self.notify(c.strip())

        self.mbed.flush()
        self.notify("HOST: Starting the ECHO test")
        result = True
        for i in range(0, self.TEST_LOOP_COUNT):
            TEST_STRING = str(uuid.uuid4()) + "\n"
            self.mbed.serial_write(TEST_STRING)
            c = self.mbed.serial_readline()
            if c is None:
                return self.RESULT_IO_SERIAL
            if c.strip() != TEST_STRING.strip():
                self.notify('HOST: "%s" != "%s"'% (c, TEST_STRING))
                result = False
            else:
                sys.stdout.write('.')
                stdout.flush()
        return self.RESULT_SUCCESS if result else self.RESULT_FAILURE


if __name__ == '__main__':
    EchoTest().run()
