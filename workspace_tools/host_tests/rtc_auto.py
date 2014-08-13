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
from host_test import DefaultTest
from time import strftime, gmtime
from sys import stdout

class RTCTest(DefaultTest):
    PATTERN_RTC_VALUE = "^\[(\d+)\] \[(\d+-\d+-\d+ \d+:\d+:\d+ [AaPpMm]{2})\]\\n"
    re_detect_rtc_value = re.compile(PATTERN_RTC_VALUE)

    def run(self):
        test_result = True
        if self.mbed.serial_timeout(None) is None:
            self.print_result("ioerr_serial")
            return
        for i in range(0, 5):
            c = self.mbed.serial_read(38)   # 38 len("[1256729742] [2009-10-28 11:35:42 AM]\n"
            if c is None:
                self.print_result("ioerr_serial")
                return
            stdout.flush()
            m = self.re_detect_rtc_value.search(c)
            if m and len(m.groups()):
                sec = m.groups()[0]
                time_str = m.groups()[1]
                correct_time_str = strftime("%Y-%m-%d %H:%M:%S %p", gmtime(float(sec)))
                test_result = test_result and (time_str == correct_time_str)
                result_msg = "OK" if (time_str == correct_time_str) else "FAIL"
                print "Got RTC time: " + c[:-1] + " ... " + result_msg

        if test_result: # All numbers are the same
            self.print_result('success')
        else:
            self.print_result('failure')
        stdout.flush()

if __name__ == '__main__':
    RTCTest().run()
