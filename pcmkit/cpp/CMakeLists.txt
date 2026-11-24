cmake_minimum_required(VERSION 3.16)
project(pcmkit_consumer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT PCM_LIB)
  message(FATAL_ERROR "PCM_LIB must point at libpcmkit_ffi.a")
endif()

add_executable(consumer tests/consumer.cpp)
target_include_directories(consumer PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/../include")
target_link_libraries(consumer PRIVATE "${PCM_LIB}" pthread dl m)

# Module 7 turns this on in a heavier workflow. The default CI build stays light.
option(PCM_SANITIZERS "Enable AddressSanitizer and UBSan" OFF)
if(PCM_SANITIZERS)
  target_compile_options(consumer PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
  target_link_options(consumer PRIVATE -fsanitize=address,undefined)
endif()
