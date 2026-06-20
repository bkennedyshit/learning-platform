cmake_minimum_required(VERSION 3.16)
project(LossLandscape3D VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find Qt6
find_package(Qt6 REQUIRED COMPONENTS
    Core
    Gui
    Widgets
    DataVisualization
)

# Source files
set(SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/Surface3DWidget.cpp
    src/ContourWidget.cpp
    src/GradientFieldWidget.cpp
    src/OptimizationPath3D.cpp
    src/MultiOptimizer.cpp
)

set(HEADERS
    src/MainWindow.h
    src/Surface3DWidget.h
    src/ContourWidget.h
    src/GradientFieldWidget.h
    src/OptimizationPath3D.h
    src/MultiOptimizer.h
)

# Create executable
add_executable(${PROJECT_NAME}
    ${SOURCES}
    ${HEADERS}
)

# Link Qt libraries
target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
    Qt6::DataVisualization
)

# Platform-specific settings
if(WIN32)
    # Windows: Set executable to be GUI application (not console)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        WIN32_EXECUTABLE ON
    )
endif()

if(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_BUNDLE ON
    )
endif()

# Installation rules
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
    BUNDLE DESTINATION .
)

# Optional: Copy Qt DLLs on Windows
if(WIN32)
    # This helps with deployment - Qt provides windeployqt tool
    find_program(WINDEPLOYQT_EXECUTABLE windeployqt HINTS "${Qt6_DIR}/../../../bin")
    if(WINDEPLOYQT_EXECUTABLE)
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
            COMMAND ${WINDEPLOYQT_EXECUTABLE} $<TARGET_FILE:${PROJECT_NAME}>
            COMMENT "Running windeployqt..."
        )
    endif()
endif()
