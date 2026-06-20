#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTabWidget>
#include "Surface3DWidget.h"
#include "ContourWidget.h"
#include "GradientFieldWidget.h"
#include "OptimizationPath3D.h"
#include "MultiOptimizer.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onFunctionChanged(const QString& name);
    void onTabChanged(int index);

private:
    void setupUI();
    void setupMenuBar();
    void connectSignals();
    void updateAllWidgets();
    
    void exportCurrentView();
    void showAbout();
    void showHelp();
    
    QTabWidget* m_tabWidget;
    
    Surface3DWidget* m_surface3D;
    ContourWidget* m_contourWidget;
    GradientFieldWidget* m_gradientWidget;
    OptimizationPath3D* m_optimizationPath;
    MultiOptimizer* m_multiOptimizer;
    
    Surface3DWidget::LossFunction m_currentFunction;
    QString m_currentFunctionName;
    
    struct FunctionBounds {
        double minX, maxX, minY, maxY;
    };
    QMap<QString, FunctionBounds> m_functionBounds;
};

#endif // MAINWINDOW_H
