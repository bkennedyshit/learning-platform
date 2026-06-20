/**
 * Calculus Visualizer - Advanced Mathematical Learning Tool
 * Combines Desmos-style graphing with TI-Nspire CAS functionality
 * for learning calculus and backpropagation concepts
 */

#include "MainWindow.h"
#include <QApplication>
#include <QSystemTrayIcon>
#include <QMenu>
#include <QIcon>
#include <QStyle>
#include <QMessageBox>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // Application metadata
    app.setApplicationName("Calculus Visualizer");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("Learning Tools");
    app.setOrganizationDomain("calculus.visualizer");
    
    // Set application-wide dark palette
    QPalette darkPalette;
    darkPalette.setColor(QPalette::Window, QColor(30, 30, 30));
    darkPalette.setColor(QPalette::WindowText, QColor(230, 230, 230));
    darkPalette.setColor(QPalette::Base, QColor(25, 25, 25));
    darkPalette.setColor(QPalette::AlternateBase, QColor(35, 35, 35));
    darkPalette.setColor(QPalette::ToolTipBase, QColor(230, 230, 230));
    darkPalette.setColor(QPalette::ToolTipText, QColor(230, 230, 230));
    darkPalette.setColor(QPalette::Text, QColor(230, 230, 230));
    darkPalette.setColor(QPalette::Button, QColor(40, 40, 40));
    darkPalette.setColor(QPalette::ButtonText, QColor(230, 230, 230));
    darkPalette.setColor(QPalette::BrightText, Qt::red);
    darkPalette.setColor(QPalette::Link, QColor(42, 130, 218));
    darkPalette.setColor(QPalette::Highlight, QColor(42, 130, 218));
    darkPalette.setColor(QPalette::HighlightedText, Qt::black);
    app.setPalette(darkPalette);
    
    // Create main window
    MainWindow mainWindow;
    mainWindow.show();
    
    // System tray integration
    if (QSystemTrayIcon::isSystemTrayAvailable()) {
        QSystemTrayIcon *trayIcon = new QSystemTrayIcon(&mainWindow);
        trayIcon->setIcon(app.style()->standardIcon(QStyle::SP_ComputerIcon));
        trayIcon->setToolTip("Calculus Visualizer");
        
        // Tray menu
        QMenu *trayMenu = new QMenu(&mainWindow);
        
        QAction *showAction = trayMenu->addAction("Show Calculator");
        QObject::connect(showAction, &QAction::triggered, [&mainWindow]() {
            mainWindow.show();
            mainWindow.raise();
            mainWindow.activateWindow();
        });
        
        QAction *newGraphAction = trayMenu->addAction("New Graph");
        QObject::connect(newGraphAction, &QAction::triggered, [&mainWindow]() {
            mainWindow.show();
            mainWindow.createNewGraph();
        });
        
        trayMenu->addSeparator();
        
        QAction *gradientDescentAction = trayMenu->addAction("Gradient Descent Demo");
        QObject::connect(gradientDescentAction, &QAction::triggered, [&mainWindow]() {
            mainWindow.show();
            mainWindow.showGradientDescent();
        });
        
        QAction *chainRuleAction = trayMenu->addAction("Chain Rule Explorer");
        QObject::connect(chainRuleAction, &QAction::triggered, [&mainWindow]() {
            mainWindow.show();
            mainWindow.showChainRule();
        });
        
        trayMenu->addSeparator();
        
        QAction *quitAction = trayMenu->addAction("Quit");
        QObject::connect(quitAction, &QAction::triggered, &app, &QApplication::quit);
        
        trayIcon->setContextMenu(trayMenu);
        
        // Double-click to show window
        QObject::connect(trayIcon, &QSystemTrayIcon::activated, 
                        [&mainWindow](QSystemTrayIcon::ActivationReason reason) {
            if (reason == QSystemTrayIcon::DoubleClick) {
                mainWindow.show();
                mainWindow.raise();
                mainWindow.activateWindow();
            }
        });
        
        trayIcon->show();
        trayIcon->showMessage("Calculus Visualizer", 
                             "Application started. Learning calculus made visual!",
                             QSystemTrayIcon::Information, 2000);
    }
    
    return app.exec();
}
