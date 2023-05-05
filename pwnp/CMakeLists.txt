add_executable(pwnp
pwnp.c
        )

include_directories(../lib/Config)
include_directories(../lib/GUI)
include_directories(../lib/e-Paper)
include_directories(../lib/Fonts)

target_link_libraries(pwnp
        pico_stdlib              # for core functionality
        pico_cyw43_arch_none
        ePaper 
        GUI 
        Fonts 
        Config 
        hardware_spi
        )
#pico_enable_stdio_usb(pwnp 1)
pico_enable_stdio_uart(pwnp 1)
# create map/bin/hex file etc.
pico_add_extra_outputs(pwnp)
