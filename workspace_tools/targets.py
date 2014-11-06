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

CORE_LABELS = {
    "ARM7TDMI-S": ["ARM7"],
    "Cortex-M0" : ["M0", "CORTEX_M"],
    "Cortex-M0+": ["M0P", "CORTEX_M"],
    "Cortex-M3" : ["M3", "CORTEX_M"],
    "Cortex-M4" : ["M4", "CORTEX_M"],
    "Cortex-M4F" : ["M4", "CORTEX_M"],
    "Cortex-A9" : ["A9", "CORTEX_A"]
}

import os
import shutil
from workspace_tools.patch import patch

class Target:
    def __init__(self):
        # ARM Core
        self.core = None

        # Is the disk provided by the interface chip of this board virtual?
        self.is_disk_virtual = False

        # list of toolchains that are supported by the mbed SDK for this target
        self.supported_toolchains = None

        # list of extra specific labels
        self.extra_labels = []

        # list of macros (-D)
        self.macros = []

        # Default online compiler:
        self.default_toolchain = "ARM"

        self.name = self.__class__.__name__

        # Code used to determine device' platform
        self.detect_code = ""

    def program_cycle_s(self):
        return 4 if self.is_disk_virtual else 1.5

    def get_labels(self):
        return [self.name] + CORE_LABELS[self.core] + self.extra_labels

    def init_hooks(self, hook, toolchain_name):
        pass


### NXP ###

# This class implements the post-link patching step needed by LPC targets
class LPCTarget(Target):
    def __init__(self):
        Target.__init__(self)

    def init_hooks(self, hook, toolchain_name):
        hook.hook_add_binary("post", self.lpc_patch)

    @staticmethod
    def lpc_patch(t_self, resources, elf, binf):
        t_self.debug("LPC Patch: %s" % os.path.split(binf)[1])
        patch(binf)

class LPC11C24(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11XX_11CXX', 'LPC11CXX']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]

class LPC1114(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11XX_11CXX', 'LPC11XX']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CR"]
        self.default_toolchain = "uARM"

class LPC11U24(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX', 'LPC11U24_401']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]
        self.default_toolchain = "uARM"
        self.detect_code = "1040"

class OC_MBUINO(LPC11U24):
    def __init__(self):
        LPC11U24.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX']
        self.macros = ['TARGET_LPC11U24']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]
        self.default_toolchain = "uARM"

class LPC11U24_301(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]

class LPC11U35_401(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CR"]
        self.default_toolchain = "uARM"

class LPC11U35_501(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX', 'MCU_LPC11U35_501']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CR"]
        self.default_toolchain = "uARM"

class LPC11U37_501(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CR"]
        self.default_toolchain = "uARM"

class LPCCAPPUCCINO(LPC11U37_501):
    def __init__(self):
        LPC11U37_501.__init__(self)

class ARCH_GPRS(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX', 'LPC11U37_501']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO"]

class LPC11U68(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['NXP', 'LPC11U6X']
        self.supported_toolchains = ["uARM", "GCC_CR", "GCC_ARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO"]
        self.detect_code = "1168"

class LPC1347(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC13XX']
        self.supported_toolchains = ["ARM", "GCC_ARM","IAR"]

class LPC1549(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC15XX']
        self.supported_toolchains = ["uARM", "GCC_CR", "GCC_ARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO"]
        self.detect_code = "1549"

class LPC1768(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC176X', 'MBED_LPC1768']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CS", "GCC_CR", "IAR"]
        self.detect_code = "1010"

class ARCH_PRO(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC176X']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CS", "GCC_CR", "IAR"]
        self.macros = ['TARGET_LPC1768']
        self.supported_form_factors = ["ARDUINO"]
        
class UBLOX_C027(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC176X']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CS", "GCC_CR", "IAR"]
        self.macros = ['TARGET_LPC1768']
        self.supported_form_factors = ["ARDUINO"]

class LPC2368(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "ARM7TDMI-S"
        self.extra_labels = ['NXP', 'LPC23XX']
        self.supported_toolchains = ["ARM", "GCC_ARM", "GCC_CR"]

class LPC810(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['NXP', 'LPC81X']
        self.supported_toolchains = ["uARM"]
        self.default_toolchain = "uARM"
        self.is_disk_virtual = True

class LPC812(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['NXP', 'LPC81X']
        self.supported_toolchains = ["uARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True
        self.detect_code = "1050"

class LPC824(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['NXP', 'LPC82X']
        self.supported_toolchains = ["uARM", "GCC_ARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True

class SSCI824(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['NXP', 'LPC82X']
        self.supported_toolchains = ["uARM"]
        self.default_toolchain = "uARM"
        self.is_disk_virtual = True

class LPC4088(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['NXP', 'LPC408X']
        self.supported_toolchains = ["ARM", "GCC_CR", "GCC_ARM"]
        self.is_disk_virtual = True

    def init_hooks(self, hook, toolchain_name):
        if toolchain_name in ['ARM_STD', 'ARM_MICRO']:
            hook.hook_add_binary("post", self.binary_hook)

    @staticmethod
    def binary_hook(t_self, resources, elf, binf):
        if not os.path.isdir(binf):
            # Regular binary file, nothing to do
            LPCTarget.lpc_patch(t_self, resources, elf, binf)
            return
        outbin = open(binf + ".temp", "wb")
        partf = open(os.path.join(binf, "ER_IROM1"), "rb")
        # Pad the fist part (internal flash) with 0xFF to 512k
        data = partf.read()
        outbin.write(data)
        outbin.write('\xFF' * (512*1024 - len(data)))
        partf.close()
        # Read and append the second part (external flash) in chunks of fixed size
        chunksize = 128 * 1024
        partf = open(os.path.join(binf, "ER_IROM2"), "rb")
        while True:
            data = partf.read(chunksize)
            outbin.write(data)
            if len(data) < chunksize:
                break
        partf.close()
        outbin.close()
        # Remove the directory with the binary parts and rename the temporary
        # file to 'binf'
        shutil.rmtree(binf, True)
        os.rename(binf + '.temp', binf)
        t_self.debug("Generated custom binary file (internal flash + SPIFI)")
        LPCTarget.lpc_patch(t_self, resources, elf, binf)

class LPC4330_M4(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['NXP', 'LPC43XX', 'LPC4330']
        self.supported_toolchains = ["ARM", "GCC_CR", "IAR", "GCC_ARM"]

class LPC4330_M0(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC43XX', 'LPC4330']
        self.supported_toolchains = ["ARM", "GCC_CR", "IAR"]

class LPC4337(LPCTarget):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['NXP', 'LPC43XX', 'LPC4337']
        self.supported_toolchains = ["ARM"]

class LPC1800(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC43XX']
        self.supported_toolchains = ["ARM", "GCC_CR", "IAR"]

        
### Freescale ###

class KL05Z(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['Freescale', 'KLXX']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "IAR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True

class KL25Z(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['Freescale', 'KLXX']
        self.supported_toolchains = ["ARM", "GCC_CW_EWL", "GCC_CW_NEWLIB", "GCC_ARM","IAR"]
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True
        self.detect_code = "0200"

class KL43Z(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['Freescale', 'KLXX']
        self.supported_toolchains = ["GCC_ARM", "ARM"]
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True

class KL46Z(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['Freescale', 'KLXX']
        self.supported_toolchains = ["GCC_ARM", "ARM", "IAR"]
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True
        self.detect_code = "0220"

class K20D50M(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4"
        self.extra_labels = ['Freescale']
        self.supported_toolchains = ["GCC_ARM", "ARM", "IAR"]
        self.is_disk_virtual = True
        self.detect_code = "0230"

class K22F(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['Freescale', 'KPSDK_MCUS', 'KPSDK_CODE']
        self.macros = ["CPU_MK22FN512VLH12", "FSL_RTOS_MBED"]
        self.supported_toolchains = ["ARM", "GCC_ARM", "IAR"]
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True

class K64F(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['Freescale', 'KPSDK_MCUS', 'KPSDK_CODE', 'MCU_K64F', 'FRDM']
        self.macros = ["CPU_MK64FN1M0VMD12", "FSL_RTOS_MBED"]
        self.supported_toolchains = ["ARM", "GCC_ARM", "IAR"]
        self.supported_form_factors = ["ARDUINO"]
        self.is_disk_virtual = True
        self.default_toolchain = "ARM"
        self.detect_code = "0240"
        
class MTS_GAMBIT(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['Freescale', 'KPSDK_MCUS', 'KPSDK_CODE', 'MCU_K64F']
        self.supported_toolchains = ["ARM", "GCC_ARM"]
        self.macros = ["CPU_MK64FN1M0VMD12", "FSL_RTOS_MBED", "TARGET_K64F"]
        self.is_disk_virtual = True
        self.default_toolchain = "ARM"

        
### STMicro ###

class NUCLEO_F030R8(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['STM', 'STM32F0', 'STM32F030R8']
        self.supported_toolchains = ["ARM", "uARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0725"

class NUCLEO_F072RB(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['STM', 'STM32F0', 'STM32F072RB']
        self.supported_toolchains = ["ARM", "uARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0730"

class NUCLEO_F091RC(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['STM', 'STM32F0', 'STM32F091RC']
        self.supported_toolchains = ["ARM", "uARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0731"

class NUCLEO_F103RB(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['STM', 'STM32F1', 'STM32F103RB']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0700"

class NUCLEO_F302R8(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F3', 'STM32F302R8']
        self.supported_toolchains = ["ARM", "uARM", "IAR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0705"

class NUCLEO_F334R8(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F3', 'STM32F334R8']
        self.supported_toolchains = ["ARM", "uARM", "IAR", "GCC_ARM"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0735"

class NUCLEO_F401RE(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F4', 'STM32F401RE']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "IAR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0720"

class NUCLEO_F411RE(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F4', 'STM32F411RE']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "IAR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0740"

class NUCLEO_L053R8(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['STM', 'STM32L0', 'STM32L053R8']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "IAR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0715"

class NUCLEO_L152RE(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['STM', 'STM32L1', 'STM32L152RE']
        self.supported_toolchains = ["ARM", "uARM", "IAR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO", "MORPHO"]
        self.detect_code = "0710"

class STM32F3XX(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4"
        self.extra_labels = ['STM', 'STM32F3XX']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]
        self.default_toolchain = "uARM"

class STM32F407(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F4', 'STM32F4XX']
        self.supported_toolchains = ["ARM", "GCC_ARM", "IAR"]

class ARCH_MAX(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F4', 'STM32F407', 'STM32F407VG']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]

class DISCO_F051R8(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['STM', 'STM32F0', 'STM32F051', 'STM32F051R8']
        self.supported_toolchains = ["GCC_ARM"]
        self.default_toolchain = "uARM"

class DISCO_F100RB(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['STM', 'STM32F1', 'STM32F100RB']
        self.supported_toolchains = ["GCC_ARM"]
        self.default_toolchain = "uARM"

class DISCO_F303VC(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F3', 'STM32F303', 'STM32F303VC']
        self.supported_toolchains = ["GCC_ARM"]
        self.default_toolchain = "uARM"

class DISCO_F334C8(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F3', 'STM32F334C8']
        self.supported_toolchains = ["GCC_ARM",]
        self.default_toolchain = "GCC_ARM"
        self.detect_code = "0735"

class DISCO_F407VG(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F4', 'STM32F407', 'STM32F407VG']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]

class DISCO_F429ZI(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.extra_labels = ['STM', 'STM32F4', 'STM32F429', 'STM32F429ZI']
        self.supported_toolchains = ["GCC_ARM"]
        self.default_toolchain = "GCC_ARM"

class DISCO_L053C8(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0+"
        self.extra_labels = ['STM', 'STM32L0', 'STM32L053C8']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]
        self.default_toolchain = "uARM"


### Nordic ###

class NRF51822(Target):
    # the following is a list of possible Nordic softdevices in decreasing order
    # of preference.
    EXPECTED_SOFTDEVICES_WITH_OFFSETS = [
        {
            'name' : 's110_nrf51822_7.1.0_softdevice.hex',
            'offset' : 0x16000
        },
        {
            'name' : 's110_nrf51822_7.0.0_softdevice.hex',
            'offset' : 0x16000
        },
        {
            'name' : 's110_nrf51822_6.0.0_softdevice.hex',
            'offset' : 0x14000
        }
    ]
    OUTPUT_EXT = '.hex'

    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ["NORDIC", "NRF51822_MKIT", "MCU_NRF51822", "MCU_NORDIC_16K"]
        self.supported_toolchains = ["ARM", "GCC_ARM"]
        self.is_disk_virtual = True
        self.detect_code = "1070"

    def program_cycle_s(self):
        return 6

    def init_hooks(self, hook, toolchain_name):
        if toolchain_name in ['ARM_STD', 'ARM_MICRO', 'GCC_ARM']:
            hook.hook_add_binary("post", self.binary_hook)

    @staticmethod
    def binary_hook(t_self, resources, elf, binf):
        for hexf in resources.hex_files:
            found = False
            for softdeviceAndOffsetEntry in NRF51822.EXPECTED_SOFTDEVICES_WITH_OFFSETS:
                if hexf.find(softdeviceAndOffsetEntry['name']) != -1:
                    found = True
                    break
            if found:
                break
        else:
            t_self.debug("Hex file not found. Aborting.")
            return

        # Merge user code with softdevice
        t_self.debug("Patching Hex file %s" % softdeviceAndOffsetEntry['name'])
        from intelhex import IntelHex
        binh = IntelHex()
        binh.loadbin(binf, offset=softdeviceAndOffsetEntry['offset'])

        sdh = IntelHex(hexf)
        sdh.merge(binh)

        with open(binf.replace(".bin", ".hex"), "w") as f:
            sdh.tofile(f, format='hex')

class NRF51822_OTA(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ["NORDIC", "NRF51822_MKIT", "MCU_NRF51822", "MCU_NORDIC_16K", "NRF51822"]
        self.macros = ['TARGET_NRF51822', 'TARGET_OTA_ENABLED']
        self.supported_toolchains = ["ARM", "GCC_ARM"]
        self.is_disk_virtual = True

class NRF51_DK(NRF51822):
    def __init__(self):
        NRF51822.__init__(self)
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_32K']
        self.macros = ['TARGET_NRF51822']
        self.supported_form_factors = ["ARDUINO"]

class NRF51_DK_OTA(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_32K', "NRF51_DK"]
        self.macros = ['TARGET_NRF51822', 'TARGET_NRF51_DK', 'TARGET_OTA_ENABLED']
        self.supported_toolchains = ["ARM", "GCC_ARM"]
        self.is_disk_virtual = True

class NRF51_DONGLE(NRF51822):
    def __init__(self):
        NRF51822.__init__(self)
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_32K']
        self.macros = ['TARGET_NRF51822']
        self.supported_form_factors = ["ARDUINO"]

class ARCH_BLE(NRF51822):
    def __init__(self):
        NRF51822.__init__(self)
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_16K']
        self.macros = ['TARGET_NRF51822']
        self.supported_form_factors = ["ARDUINO"]

class HRM1017(NRF51822):
    def __init__(self):
        NRF51822.__init__(self)
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_16K']
        self.macros = ['TARGET_NRF51822']

class RBLAB_NRF51822(NRF51822):
    def __init__(self):
        NRF51822.__init__(self)
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_16K']
        self.macros = ['TARGET_NRF51822']
        self.supported_form_factors = ["ARDUINO"]

class RBLAB_BLENANO(NRF51822):
    def __init__(self):
        NRF51822.__init__(self)
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_16K']
        self.macros = ['TARGET_NRF51822']

class XADOW_M0(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX', 'MCU_LPC11U35_501']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CR"]
        self.default_toolchain = "uARM"

class WALLBOT_BLE(NRF51822):
    def __init__(self):
        NRF51822.__init__(self)
        self.extra_labels = ['NORDIC', 'MCU_NRF51822', 'MCU_NORDIC_16K']
        self.macros = ['TARGET_NRF51822']

<<<<<<< HEAD
class ARCH_PRO(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC176X']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CS", "GCC_CR", "IAR"]
        self.macros = ['TARGET_LPC1768']
        self.supported_form_factors = ["ARDUINO"]


class LPC1768_MINI_DK2(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M3"
        self.extra_labels = ['NXP', 'LPC176X']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CS", "GCC_CR", "IAR"]
        self.macros = ['TARGET_LPC1768']


class ARCH_GPRS(LPCTarget):
    def __init__(self):
        LPCTarget.__init__(self)
        self.core = "Cortex-M0"
        self.extra_labels = ['NXP', 'LPC11UXX', 'LPC11U37_501']
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CR"]
        self.default_toolchain = "uARM"
        self.supported_form_factors = ["ARDUINO"]


class LPCCAPPUCCINO(LPC11U37_501):
    def __init__(self):
        LPC11U37_501.__init__(self)

=======
### ARM ###
>>>>>>> upstream/master

class ARM_MPS2(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-M4F"
        self.macros = ['CMSDK_CM4']
        self.supported_toolchains = ["ARM", "GCC_ARM"]
        self.default_toolchain = "ARM"

class RZ_A1H(Target):
    def __init__(self):
        Target.__init__(self)
        self.core = "Cortex-A9"
        self.extra_labels = ['RENESAS', 'MBRZA1H']
        self.supported_toolchains = ["ARM"]
        self.supported_form_factors = ["ARDUINO"]
        self.default_toolchain = "ARM"

# Get a single instance for each target
TARGETS = [

    ### NXP ###
    LPC11C24(),
    LPC11U24(),
    OC_MBUINO(),    # LPC11U24
    LPC11U24_301(),
    LPC11U35_401(),
    LPC11U35_501(),
    LPC11U37_501(),
    LPCCAPPUCCINO(),# LPC11U37_501
    ARCH_GPRS(),    # LPC11U37_501
    LPC11U68(),
    LPC1114(),
    LPC1347(),
    LPC1549(),
    LPC1768(),
    ARCH_PRO(),     # LPC1768
    UBLOX_C027(),   # LPC1768
    LPC2368(),
    LPC810(),
    LPC812(),
    LPC824(),
    SSCI824(),      # LPC824
    LPC4088(),
    LPC4330_M4(),
    LPC4330_M0(),
    LPC4337(),

    ### Freescale ###
    KL05Z(),
    KL25Z(),
    KL43Z(),
    KL46Z(),
    K20D50M(),
    K22F(),
    K64F(),
    MTS_GAMBIT(),   # FRDM K64F
    
    ### STMicro ###
    NUCLEO_F030R8(),
    NUCLEO_F072RB(),
    NUCLEO_F091RC(),
    NUCLEO_F103RB(),
    NUCLEO_F302R8(),
    NUCLEO_F334R8(),
    NUCLEO_F401RE(),
    NUCLEO_F411RE(),
    NUCLEO_L053R8(),
    NUCLEO_L152RE(),
    STM32F3XX(),
    STM32F407(),
    DISCO_F051R8(),
    DISCO_F100RB(),
    DISCO_F303VC(),
    DISCO_F334C8(),
    DISCO_F407VG(), # STM32F407
    ARCH_MAX(),     # STM32F407
    DISCO_F429ZI(),
    DISCO_L053C8(),
    
    ### Nordic ###
    NRF51822(),
    NRF51822_OTA(), # nRF51822
    NRF51_DK(),
<<<<<<< HEAD
    NRF51_DK_OTA(),
    ARCH_PRO(),
    LPC1768_MINI_DK2(),
    ARCH_GPRS(),
    LPCCAPPUCCINO(),
    HRM1017(),
=======
    NRF51_DK_OTA(), # nRF51822
    NRF51_DONGLE(),
    ARCH_BLE(),     # nRF51822
    HRM1017(),      # nRF51822
    RBLAB_NRF51822(),# nRF51822
    RBLAB_BLENANO(),# nRF51822
    XADOW_M0(),     # nRF51822
    WALLBOT_BLE(),  # nRF51822
    
    ### ARM ###
>>>>>>> upstream/master
    ARM_MPS2(),
    RZ_A1H(),
    RBLAB_NRF51822(),
    RBLAB_BLENANO(),
    OC_MBUINO(),
    MTS_GAMBIT(),
    ARCH_MAX(),
    DISCO_F429ZI(),
]

# Map each target name to its unique instance
TARGET_MAP = {}
for t in TARGETS:
    TARGET_MAP[t.name] = t

TARGET_NAMES = TARGET_MAP.keys()

# Some targets with different name have the same exporters
EXPORT_MAP = {}
