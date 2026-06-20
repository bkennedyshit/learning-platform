/**
 * MainWindow.h - Main application window (Desmos-style interface)
 * Features: Interactive graphing, symbolic math, step-by-step derivatives
 */

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWidget>
#include <QLineEdit>
#include <QTextEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSplitter>
#include <QTabWidget>
#include <QListWidget>
#include <memory>

class GraphWidget;
class DerivativeEngine;
class GradientDescentVisualizer;
class ChainRuleExplorer;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;
    
    // Public slots for tray integration
    void createNewGraph();
    void showGradientDescent();
    void showChainRule();

private slots:
    void onExpressionEntered();
    void onComputeDerivative();
    void onComputeIntegral();
    void onSolveEquation();
    void onShowSteps();
    void onClearGraph();
    void onExportGraph();
    void onAddExpression();
    void onRemoveExpression();
    void onToggleExpression(QListWidgetItem *item);
    void onZoomIn();
    void onZoomOut();
    void onResetView();
    void onAnimateGradient();

private:
    void setupUI();
    void setupMenuBar();
    void setupToolBar();
    void setupConnections();
    void applyDarkTheme();
    
    // UI Components
    QWidget *centralWidget;
    QSplitter *mainSplitter;
    
    // Left panel - Expression input
    QWidget *leftPanel;
    QLineEdit *expressionInput;
    QPushButton *addExpressionBtn;
    QListWidget *expressionList;
    QPushButton *derivativeBtn;
    QPushButton *integralBtn;
    QPushButton *solveBtn;
    QTextEdit *stepByStepOutput;
    
    // Right panel - Graph
    QWidget *rightPanel;
    GraphWidget *graphWidget;
    
    // Toolbar buttons
    QPushButton *clearBtn;
    QPushButton *zoomInBtn;
    QPushButton *zoomOutBtn;
    QPushButton *resetViewBtn;
    QPushButton *exportBtn;
    
    // Tab widget for different modes
    QTabWidget *tabWidget;
    
    // Engine and visualizers
    std::unique_ptr<DerivativeEngine> derivativeEngine;
    GradientDescentVisualizer *gradientVisualizer;
    ChainRuleExplorer *chainRuleExplorer;
    
    // State
    QStringList expressions;
    QString currentExpression;
};

#endif // MAINWINDOW_H
