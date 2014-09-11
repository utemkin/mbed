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

import random
import re
from host_test import DefaultTest
from time import time
from sys import stdout

class StdioTest(DefaultTest):
    PATTERN_INT_VALUE = "Your value was: (-?\d+)"
    re_detect_int_value = re.compile(PATTERN_INT_VALUE)

    def run(self):
        test_result = True

        # Let's wait for Mbed to print its readiness, usually "{{start}}"
        if self.mbed.serial_timeout(None) is None:
            self.print_result("ioerr_serial")
            return

        c = self.mbed.serial_read(len('{{start}}'))
        if c is None:
            self.print_result("ioerr_serial")
            return
        print c
        stdout.flush()

        if self.mbed.serial_timeout(1) is None:
            self.print_result("ioerr_serial")
            return

        for i in range(1, 5):
            random_integer = random.randint(-99999, 99999)
            print "Generated number: " + str(random_integer)
            stdout.flush()
            self.mbed.serial_write(str(random_integer) + "\n")
            serial_stdio_msg = ""

            ip_msg_timeout = self.mbed.options.timeout
            start_serial_pool = time();
            while (time() - start_serial_pool) < ip_msg_timeout:
                c = self.mbed.serial_read(512)
                if c is None:
                    self.print_result("ioerr_serial")
                    return
                stdout.write(c)
                stdout.flush()
                serial_stdio_msg += c
                # Searching for reply with scanned values
                m = self.re_detect_int_value.search(serial_stdio_msg)
                if m and len(m.groups()):
                    duration = time() - start_serial_pool
                    print "Number: " + str(m.groups()[0])
                    test_result = test_result and (random_integer == int(m.groups()[0]))
                    stdout.flush()
                    break
            else:
                print "Error: No data from MUT sent"
                self.print_result('error')
                exit(-2)

        if test_result: # All numbers are the same
            self.print_result('success')
        else:
            self.print_result('failure')

if __name__ == '__main__':
    StdioTest().run()
