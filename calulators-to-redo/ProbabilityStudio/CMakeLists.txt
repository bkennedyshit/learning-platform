cmake_minimum_required(VERSION 3.16)

project(ProbabilityStudio VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable automatic MOC, UIC and RCC processing
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Find Qt packages
find_package(Qt6 COMPONENTS Core Gui Widgets Charts REQUIRED)

# If Qt6 not found, try Qt5
if(NOT Qt6_FOUND)
    find_package(Qt5 5.15 COMPONENTS Core Gui Widgets Charts REQUIRED)
endif()

# Source files
set(SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/DistributionWidget.cpp
    src/SoftmaxVisualizer.cpp
    src/BayesCalculator.cpp
    src/CrossEntropyWidget.cpp
    src/KLDivergenceWidget.cpp
    src/SamplingVisualizer.cpp
    src/HypothesisTestWidget.cpp
    src/ConfusionMatrixWidget.cpp
    src/AttentionDistWidget.cpp
)

# Header files
set(HEADERS
    src/MainWindow.h
    src/DistributionWidget.h
    src/SoftmaxVisualizer.h
    src/BayesCalculator.h
    src/CrossEntropyWidget.h
    src/KLDivergenceWidget.h
    src/SamplingVisualizer.h
    src/HypothesisTestWidget.h
    src/ConfusionMatrixWidget.h
    src/AttentionDistWidget.h
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Link Qt libraries
if(Qt6_FOUND)
    target_link_libraries(${PROJECT_NAME} PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::Charts
    )
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        Qt5::Charts
    )
endif()

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

# Platform-specific settings
if(WIN32)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        WIN32_EXECUTABLE TRUE
    )
endif()

# Install target
install(TARGETS ${PROJECT_NAME}
    BUNDLE DESTINATION .
    RUNTIME DESTINATION bin
)
