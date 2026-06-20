cmake_minimum_required(VERSION 3.16)
project(MatrixCommander VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find Qt
find_package(Qt6 COMPONENTS Core Gui Widgets QUIET)
if (NOT Qt6_FOUND)
    find_package(Qt5 5.15 REQUIRED COMPONENTS Core Gui Widgets)
endif()

# Source files
set(SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/MatrixWidget.cpp
    src/OperationPanel.cpp
    src/MatrixEngineAdapter.cpp
)

set(HEADERS
    src/MainWindow.h
    src/MatrixWidget.h
    src/OperationPanel.h
    src/MatrixEngineAdapter.h
)

# Create executable
if(WIN32)
    add_executable(MatrixCommander WIN32 ${SOURCES} ${HEADERS})
elseif(APPLE)
    add_executable(MatrixCommander MACOSX_BUNDLE ${SOURCES} ${HEADERS})
else()
    add_executable(MatrixCommander ${SOURCES} ${HEADERS})
endif()

# Link Qt libraries
if (Qt6_FOUND)
    target_link_libraries(MatrixCommander PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)
else()
    target_link_libraries(MatrixCommander PRIVATE Qt5::Core Qt5::Gui Qt5::Widgets)
endif()

# Compiler warnings
if(MSVC)
    target_compile_options(MatrixCommander PRIVATE /W4)
else()
    target_compile_options(MatrixCommander PRIVATE -Wall -Wextra -pedantic)
endif()

# Installation
install(TARGETS MatrixCommander
    BUNDLE DESTINATION .
    RUNTIME DESTINATION bin
)

# Windows specific settings
if(WIN32)
    set_target_properties(MatrixCommander PROPERTIES
        WIN32_EXECUTABLE TRUE
    )
endif()

# macOS specific settings
if(APPLE)
    set_target_properties(MatrixCommander PROPERTIES
        MACOSX_BUNDLE_GUI_IDENTIFIER "com.matrixlabs.commander"
        MACOSX_BUNDLE_BUNDLE_NAME "Matrix Commander"
        MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
        MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION}
    )
endif()
