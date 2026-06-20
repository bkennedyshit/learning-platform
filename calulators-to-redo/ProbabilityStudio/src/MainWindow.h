#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTabWidget>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void showAbout();
    void showHelp();

private:
    void createMenus();
    void setupTabs();
    
    QTabWidget *tabWidget;
};

#endif // MAINWINDOW_H
