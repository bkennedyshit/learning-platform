QT       += core gui widgets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    src/main.cpp \
    src/MainWindow.cpp \
    src/MatrixWidget.cpp \
    src/OperationPanel.cpp \
    src/MatrixEngineAdapter.cpp

HEADERS += \
    src/MainWindow.h \
    src/MatrixWidget.h \
    src/OperationPanel.h \
    src/MatrixEngineAdapter.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

# Enable warnings
QMAKE_CXXFLAGS += -Wall -Wextra

# Output directories
DESTDIR = $$PWD/build
OBJECTS_DIR = $$PWD/build/obj
MOC_DIR = $$PWD/build/moc
RCC_DIR = $$PWD/build/rcc
UI_DIR = $$PWD/build/ui

# Windows-specific settings
win32 {
    RC_ICONS = resources/icon.ico
    VERSION = 1.0.0.0
}

# macOS-specific settings
macx {
    ICON = resources/icon.icns
}
