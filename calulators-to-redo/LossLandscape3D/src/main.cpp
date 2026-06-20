#include "MainWindow.h"
#include <QApplication>
#include <QSurfaceFormat>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // Set application metadata
    app.setApplicationName("Loss Landscape 3D");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("ML Education Tools");
    
    // Configure OpenGL surface format for 3D rendering
    QSurfaceFormat format;
    format.setDepthBufferSize(24);
    format.setStencilBufferSize(8);
    format.setVersion(3, 3);
    format.setProfile(QSurfaceFormat::CoreProfile);
    format.setSamples(4); // Anti-aliasing
    QSurfaceFormat::setDefaultFormat(format);
    
    // Create and show main window
    MainWindow window;
    window.show();
    
    return app.exec();
}
