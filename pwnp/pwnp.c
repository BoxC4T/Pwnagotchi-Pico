// /**
//  * Copyright (c) 2022 Raspberry Pi (Trading) Ltd.
//  *
//  * SPDX-License-Identifier: BSD-3-Clause
//  */

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include <stdlib.h> // malloc() free()
#include "EPD_2in13_V3.h"
#include "fonts.h"
#include "GUI_Paint.h"
static bool init_pico();
static bool init_battery();
static bool init_screen();
static void main_loop();
UBYTE *BlackImage;

int main() {
    if (init_pico() == true) {
        if (init_battery() == true) {
            if (init_screen() == true) {
                //sleep_ms(1000);
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
    if(DEV_Module_Init()!=0){
        return false;
    }
    EPD_2in13_V3_Init();
    EPD_2in13_V3_Clear();
    UWORD Imagesize = ((EPD_2in13_V3_WIDTH % 8 == 0)? (EPD_2in13_V3_WIDTH / 8 ): (EPD_2in13_V3_WIDTH / 8 + 1)) * EPD_2in13_V3_HEIGHT;
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        return false;
    }
    
    Paint_NewImage(BlackImage, EPD_2in13_V3_WIDTH, EPD_2in13_V3_HEIGHT, 270, WHITE);  	
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);
    Paint_DrawString_EN(140, 15, "FUCK YOU", &Font12, BLACK, WHITE);
    EPD_2in13_V3_Display_Base(BlackImage);
    sleep_ms(250);
    Paint_DrawString_EN(140, 30, "FUCK YOU", &Font16, WHITE, BLACK);
    EPD_2in13_V3_Display_Base(BlackImage);
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    sleep_ms(250);
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
    sleep_ms(250);
    return true;
}
void main_loop(){
    Paint_DrawString_EN(140, 15, "Testing", &Font12, BLACK, WHITE);
    EPD_2in13_V3_Display_Base(BlackImage);
    sleep_ms(250);
    Paint_DrawString_EN(140, 30, "Testing", &Font16, WHITE, BLACK);
    EPD_2in13_V3_Display_Base(BlackImage);
}