/**
 * Copyright (c) 2022 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
static bool init_pico();
static bool init_battery();
static bool init_screen();
static void main_loop();


int main() {
    if (init_pico()) {
        if (init_battery()) {
            if (init_screen()) {
                sleep_ms(1000);
                main_loop();
            }
        }
    }
    return 1;    
}

bool init_pico(){
    stdio_init_all();
    if (cyw43_arch_init()) {
        printf("Wi-Fi init failed");
        return false;
    }
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    sleep_ms(250);
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
    sleep_ms(250);
    return true;
}
bool init_battery(){
    return true;
}
bool init_screen(){
    return true;
}
void main_loop(){
    while (true){
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    sleep_ms(1000);
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
    sleep_ms(1000);
    }
}
