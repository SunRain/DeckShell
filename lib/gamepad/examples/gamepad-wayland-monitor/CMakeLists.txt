cmake_minimum_required(VERSION 3.16)

project(gamepad-wayland-monitor VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

# Find Qt6
find_package(Qt6 6.8 REQUIRED COMPONENTS Core)

# Sources
set(SOURCES
    main.cpp
)

# Executable
add_executable(gamepad-wayland-monitor ${SOURCES})

# Link libraries
target_link_libraries(gamepad-wayland-monitor PRIVATE
    Qt6::Core
    deckshell-gamepad-treeland
)

# Install
install(TARGETS gamepad-wayland-monitor
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
