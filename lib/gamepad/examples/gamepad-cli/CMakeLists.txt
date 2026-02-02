# Gamepad CLI Configuration Tool

cmake_minimum_required(VERSION 3.25)

project(gamepad-cli VERSION 1.0.0)

# Find Qt6
find_package(Qt6 6.8 REQUIRED COMPONENTS Core)

# Qt settings
set(CMAKE_AUTOMOC ON)

# Create executable
add_executable(gamepad-config main.cpp)

# Link libraries
target_link_libraries(gamepad-config
    PRIVATE
        Qt6::Core
        deckshell-gamepad
)

# Set C++ standard
target_compile_features(gamepad-config PRIVATE cxx_std_20)

# Install
install(TARGETS gamepad-config
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Print configuration
message(STATUS "Gamepad CLI tool configured:")
message(STATUS "  - Executable: gamepad-config")
message(STATUS "  - Qt6 version: ${Qt6_VERSION}")
