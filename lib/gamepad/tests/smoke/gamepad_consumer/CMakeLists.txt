cmake_minimum_required(VERSION 3.25)

project(DeckShellGamepadConsumer LANGUAGES CXX)

find_package(Qt6 6.8 REQUIRED COMPONENTS Core)
find_package(DeckShellGamepad CONFIG REQUIRED)

add_executable(gamepad_consumer main.cpp)

target_link_libraries(gamepad_consumer
    PRIVATE
        Qt6::Core
        DeckShell::deckshell-gamepad
)

target_compile_features(gamepad_consumer PRIVATE cxx_std_20)
