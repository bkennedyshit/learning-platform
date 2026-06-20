cmake_minimum_required(VERSION 3.21)
project(CalculusVisualizer VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Qt6 packages
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Charts)

# SymEngine for symbolic mathematics
find_package(SymEngine REQUIRED)

set(PROJECT_SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/MainWindow.h
    src/DerivativeEngine.h
    src/DerivativeEngine.cpp
    src/GraphWidget.h
    src/GraphWidget.cpp
    src/ExpressionParser.h
    src/ExpressionParser.cpp
    src/GradientDescentVisualizer.h
    src/GradientDescentVisualizer.cpp
    src/ChainRuleExplorer.h
    src/ChainRuleExplorer.cpp
)

if(WIN32)
    set(APP_ICON_RESOURCE_WINDOWS "${CMAKE_CURRENT_SOURCE_DIR}/resources/app.rc")
    add_executable(CalculusVisualizer WIN32 ${PROJECT_SOURCES} ${APP_ICON_RESOURCE_WINDOWS})
else()
    add_executable(CalculusVisualizer ${PROJECT_SOURCES})
endif()

target_link_libraries(CalculusVisualizer PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
    Qt6::Charts
    symengine
)

target_include_directories(CalculusVisualizer PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${SYMENGINE_INCLUDE_DIRS}
)

# Compiler warnings
if(MSVC)
    target_compile_options(CalculusVisualizer PRIVATE /W4)
else()
    target_compile_options(CalculusVisualizer PRIVATE -Wall -Wextra -pedantic)
endif()

# Installation
install(TARGETS CalculusVisualizer
    BUNDLE DESTINATION .
    RUNTIME DESTINATION bin
)

# Deploy Qt dependencies on Windows
if(WIN32)
    find_program(WINDEPLOYQT_EXECUTABLE windeployqt HINTS "${Qt6_DIR}/../../../bin")
    if(WINDEPLOYQT_EXECUTABLE)
        add_custom_command(TARGET CalculusVisualizer POST_BUILD
            COMMAND "${WINDEPLOYQT_EXECUTABLE}" --no-compiler-runtime "$<TARGET_FILE:CalculusVisualizer>"
            COMMENT "Running windeployqt..."
        )
    endif()
endif()
