/* mbed Microcontroller Library
 * Copyright (c) 2006-2013 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "mbed_assert.h"
#include "analogin_api.h"

#if DEVICE_ANALOGIN

#include "cmsis.h"
#include "pinmap.h"
#include "PeripheralNames.h"
#include "fsl_adc_hal.h"
#include "fsl_clock_manager.h"
#include "PeripheralPins.h"

#define MAX_FADC 6000000

void analogin_init(analogin_t *obj, PinName pin) {
    obj->adc = (ADCName)pinmap_peripheral(pin, PinMap_ADC);
    MBED_ASSERT(obj->adc != (ADCName)NC);

    uint32_t instance = obj->adc >> ADC_INSTANCE_SHIFT;

    clock_manager_set_gate(kClockModuleADC, instance, true);

    uint32_t bus_clock;
    clock_manager_get_frequency(kBusClock, &bus_clock);
    uint32_t clkdiv;
    for (clkdiv = 0; clkdiv < 4; clkdiv++) {
        if ((bus_clock >> clkdiv) <= MAX_FADC)
            break;
    }
    if (clkdiv == 4) {
        clkdiv = 0x7; //Set max div
    }
    /* adc is enabled/triggered when reading. */
    adc_hal_set_clock_source_mode(instance, (adc_clock_source_mode_t)(clkdiv >> 2));
    adc_hal_set_clock_divider_mode(instance, (adc_clock_divider_mode_t)(clkdiv & 0x3));
    adc_hal_set_reference_voltage_mode(instance, kAdcVoltageVref);
    adc_hal_set_resolution_mode(instance, kAdcSingleDiff16);
    adc_hal_configure_continuous_conversion(instance, false);
    adc_hal_configure_hw_trigger(instance, false); /* sw trigger */
    adc_hal_configure_hw_average(instance, true);
    adc_hal_set_hw_average_mode(instance, kAdcHwAverageCount4);
    adc_hal_set_group_mux(instance, kAdcChannelMuxB); /* only B channels are avail */

    pinmap_pinout(pin, PinMap_ADC);
}

uint16_t analogin_read_u16(analogin_t *obj) {
    uint32_t instance = obj->adc >> ADC_INSTANCE_SHIFT;
    /* sw trigger (SC1A) */
    adc_hal_enable(instance, 0, (adc_channel_mode_t)(obj->adc & 0xF), false);
    while (!adc_hal_is_conversion_completed(instance, 0));
    return adc_hal_get_conversion_value(instance, 0);
}

float analogin_read(analogin_t *obj) {
    uint16_t value = analogin_read_u16(obj);
    return (float)value * (1.0f / (float)0xFFFF);
}

#endif
