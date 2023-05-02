add_executable(pwnp
pwnp.c
        )

target_link_libraries(pwnp
        pico_stdlib              # for core functionality
        pico_cyw43_arch_none     # we need Wifi to access the GPIO, but we don't need anything else
        )

# create map/bin/hex file etc.
pico_add_extra_outputs(pwnp)
