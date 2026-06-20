QT += core gui widgets charts

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = ProbabilityStudio
TEMPLATE = app

# C++11 or higher required
CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    src/main.cpp \
    src/MainWindow.cpp \
    src/DistributionWidget.cpp \
    src/SoftmaxVisualizer.cpp \
    src/BayesCalculator.cpp \
    src/CrossEntropyWidget.cpp \
    src/KLDivergenceWidget.cpp \
    src/SamplingVisualizer.cpp \
    src/HypothesisTestWidget.cpp \
    src/ConfusionMatrixWidget.cpp \
    src/AttentionDistWidget.cpp

HEADERS += \
    src/MainWindow.h \
    src/DistributionWidget.h \
    src/SoftmaxVisualizer.h \
    src/BayesCalculator.h \
    src/CrossEntropyWidget.h \
    src/KLDivergenceWidget.h \
    src/SamplingVisualizer.h \
    src/HypothesisTestWidget.h \
    src/ConfusionMatrixWidget.h \
    src/AttentionDistWidget.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
