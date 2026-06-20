#include <QApplication>
#include "MainWindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // Set application metadata
    QCoreApplication::setApplicationName("Probability Studio");
    QCoreApplication::setOrganizationName("ML Education");
    QCoreApplication::setApplicationVersion("1.0.0");
    
    MainWindow window;
    window.show();
    
    return app.exec();
}
