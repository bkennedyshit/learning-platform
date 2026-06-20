QT += core gui widgets charts

CONFIG += c++20

# Project metadata
TARGET = CalculusVisualizer
TEMPLATE = app
VERSION = 1.0.0

# Compiler flags
QMAKE_CXXFLAGS += -Wall -Wextra -pedantic

# SymEngine library
win32 {
    LIBS += -lsymengine
    INCLUDEPATH += C:/SymEngine/include
    LIBS += -LC:/SymEngine/lib
} else {
    CONFIG += link_pkgconfig
    PKGCONFIG += symengine
}

# Source files
SOURCES += \
    src/main.cpp \
    src/MainWindow.cpp \
    src/DerivativeEngine.cpp \
    src/GraphWidget.cpp \
    src/ExpressionParser.cpp \
    src/GradientDescentVisualizer.cpp \
    src/ChainRuleExplorer.cpp

HEADERS += \
    src/MainWindow.h \
    src/DerivativeEngine.h \
    src/GraphWidget.h \
    src/ExpressionParser.h \
    src/GradientDescentVisualizer.h \
    src/ChainRuleExplorer.h

# Include path
INCLUDEPATH += src

# Output directories
DESTDIR = build
OBJECTS_DIR = build/obj
MOC_DIR = build/moc
RCC_DIR = build/rcc
UI_DIR = build/ui

# Default rules for deployment
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
