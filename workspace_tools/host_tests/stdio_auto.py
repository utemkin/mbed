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

import re
import random
from time import time
from host_test import DefaultTest


class StdioTest(DefaultTest):
    PATTERN_INT_VALUE = "Your value was: (-?\d+)"
    re_detect_int_value = re.compile(PATTERN_INT_VALUE)

    def test(self):
        test_result = True

        c = self.mbed.serial_readline() # {{start}} preamble
        if c is None:
            return self.RESULT_IO_SERIAL
        self.notify(c)

        for i in range(0, 10):
            random_integer = random.randint(-99999, 99999)
            self.notify("HOST: Generated number: " + str(random_integer))
            start = time()
            self.mbed.serial_write(str(random_integer) + "\n")

            serial_stdio_msg = self.mbed.serial_readline()
            if c is None:
                return self.RESULT_IO_SERIAL
            delay_time = time() - start
            self.notify(serial_stdio_msg.strip())

            # Searching for reply with scanned values
            m = self.re_detect_int_value.search(serial_stdio_msg)
            if m and len(m.groups()):
                int_value = m.groups()[0]
                int_value_cmp = random_integer == int(int_value)
                test_result = test_result and int_value_cmp
                self.notify("HOST: Number %s read after %.3f sec ... [%s]"% (int_value, delay_time, "OK" if int_value_cmp else "FAIL"))
            else:
                test_result = False
                break
        return self.RESULT_SUCCESS if test_result else self.RESULT_FAILURE


if __name__ == '__main__':
    StdioTest().run()
