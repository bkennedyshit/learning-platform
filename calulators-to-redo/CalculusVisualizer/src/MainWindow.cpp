/**
 * MainWindow.cpp - Implementation of main calculator interface
 */

#include "MainWindow.h"
#include "GraphWidget.h"
#include "DerivativeEngine.h"
#include "GradientDescentVisualizer.h"
#include "ChainRuleExplorer.h"

#include <QMenuBar>
#include <QToolBar>
#include <QStatusBar>
#include <QLabel>
#include <QGroupBox>
#include <QMessageBox>
#include <QFileDialog>
#include <QFont>
#include <QFontDatabase>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , derivativeEngine(std::make_unique<DerivativeEngine>())
{
    setWindowTitle("Calculus Visualizer - Learning Tool");
    resize(1400, 900);
    
    setupUI();
    setupMenuBar();
    setupToolBar();
    setupConnections();
    applyDarkTheme();
    
    statusBar()->showMessage("Ready - Enter an expression to begin", 3000);
}

MainWindow::~MainWindow()
{
    // Smart pointers handle cleanup
}

void MainWindow::setupUI()
{
    centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
    
    auto *mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    
    // Create tab widget for different modes
    tabWidget = new QTabWidget(this);
    
    // Main calculator tab
    QWidget *calculatorTab = new QWidget();
    auto *calculatorLayout = new QVBoxLayout(calculatorTab);
    
    mainSplitter = new QSplitter(Qt::Horizontal, this);
    
    // Left panel - Input and controls
    leftPanel = new QWidget();
    auto *leftLayout = new QVBoxLayout(leftPanel);
    leftLayout->setSpacing(10);
    
    // Expression input group
    auto *inputGroup = new QGroupBox("Expression Input");
    auto *inputLayout = new QVBoxLayout(inputGroup);
    
    expressionInput = new QLineEdit();
    expressionInput->setPlaceholderText("Enter expression: e.g., x^2 + 3*x - 5");
    expressionInput->setFont(QFont("Consolas", 11));
    expressionInput->setMinimumHeight(35);
    
    addExpressionBtn = new QPushButton("Add to Graph");
    addExpressionBtn->setMinimumHeight(35);
    
    inputLayout->addWidget(new QLabel("f(x) ="));
    inputLayout->addWidget(expressionInput);
    inputLayout->addWidget(addExpressionBtn);
    
    // Expression list
    auto *listGroup = new QGroupBox("Active Expressions");
    auto *listLayout = new QVBoxLayout(listGroup);
    
    expressionList = new QListWidget();
    expressionList->setSelectionMode(QAbstractItemView::SingleSelection);
    
    auto *removeBtn = new QPushButton("Remove Selected");
    
    listLayout->addWidget(expressionList);
    listLayout->addWidget(removeBtn);
    
    // Operations group
    auto *opsGroup = new QGroupBox("Calculus Operations");
    auto *opsLayout = new QVBoxLayout(opsGroup);
    
    derivativeBtn = new QPushButton("Compute Derivative (d/dx)");
    integralBtn = new QPushButton("Compute Integral (∫ dx)");
    solveBtn = new QPushButton("Solve for x = 0");
    
    opsLayout->addWidget(derivativeBtn);
    opsLayout->addWidget(integralBtn);
    opsLayout->addWidget(solveBtn);
    
    // Step-by-step output
    auto *stepsGroup = new QGroupBox("Step-by-Step Solution");
    auto *stepsLayout = new QVBoxLayout(stepsGroup);
    
    stepByStepOutput = new QTextEdit();
    stepByStepOutput->setReadOnly(true);
    stepByStepOutput->setFont(QFont("Consolas", 10));
    stepByStepOutput->setPlaceholderText("Step-by-step solutions will appear here...");
    
    stepsLayout->addWidget(stepByStepOutput);
    
    // Assemble left panel
    leftLayout->addWidget(inputGroup);
    leftLayout->addWidget(listGroup);
    leftLayout->addWidget(opsGroup);
    leftLayout->addWidget(stepsGroup, 1);
    
    leftPanel->setMaximumWidth(450);
    
    // Right panel - Graph
    rightPanel = new QWidget();
    auto *rightLayout = new QVBoxLayout(rightPanel);
    rightLayout->setContentsMargins(0, 0, 0, 0);
    
    graphWidget = new GraphWidget();
    
    // Graph controls
    auto *graphControls = new QHBoxLayout();
    zoomInBtn = new QPushButton("Zoom In (+)");
    zoomOutBtn = new QPushButton("Zoom Out (-)");
    resetViewBtn = new QPushButton("Reset View");
    clearBtn = new QPushButton("Clear All");
    exportBtn = new QPushButton("Export Image");
    
    graphControls->addWidget(zoomInBtn);
    graphControls->addWidget(zoomOutBtn);
    graphControls->addWidget(resetViewBtn);
    graphControls->addStretch();
    graphControls->addWidget(clearBtn);
    graphControls->addWidget(exportBtn);
    
    rightLayout->addWidget(graphWidget, 1);
    rightLayout->addLayout(graphControls);
    
    // Add panels to splitter
    mainSplitter->addWidget(leftPanel);
    mainSplitter->addWidget(rightPanel);
    mainSplitter->setStretchFactor(0, 1);
    mainSplitter->setStretchFactor(1, 3);
    
    calculatorLayout->addWidget(mainSplitter);
    
    // Gradient Descent tab
    gradientVisualizer = new GradientDescentVisualizer();
    
    // Chain Rule tab
    chainRuleExplorer = new ChainRuleExplorer();
    
    // Add tabs
    tabWidget->addTab(calculatorTab, "📊 Calculator");
    tabWidget->addTab(gradientVisualizer, "📉 Gradient Descent");
    tabWidget->addTab(chainRuleExplorer, "🔗 Chain Rule Explorer");
    
    mainLayout->addWidget(tabWidget);
    
    connect(removeBtn, &QPushButton::clicked, this, &MainWindow::onRemoveExpression);
}

void MainWindow::setupMenuBar()
{
    QMenuBar *menuBar = new QMenuBar(this);
    setMenuBar(menuBar);
    
    // File menu
    QMenu *fileMenu = menuBar->addMenu("&File");
    QAction *newAction = fileMenu->addAction("&New Graph");
    newAction->setShortcut(QKeySequence::New);
    connect(newAction, &QAction::triggered, this, &MainWindow::createNewGraph);
    
    QAction *exportAction = fileMenu->addAction("&Export Graph");
    exportAction->setShortcut(QKeySequence::Save);
    connect(exportAction, &QAction::triggered, this, &MainWindow::onExportGraph);
    
    fileMenu->addSeparator();
    QAction *quitAction = fileMenu->addAction("&Quit");
    quitAction->setShortcut(QKeySequence::Quit);
    connect(quitAction, &QAction::triggered, this, &QWidget::close);
    
    // View menu
    QMenu *viewMenu = menuBar->addMenu("&View");
    viewMenu->addAction("Zoom &In", this, &MainWindow::onZoomIn, QKeySequence::ZoomIn);
    viewMenu->addAction("Zoom &Out", this, &MainWindow::onZoomOut, QKeySequence::ZoomOut);
    viewMenu->addAction("&Reset View", this, &MainWindow::onResetView, tr("Ctrl+0"));
    
    // Tools menu
    QMenu *toolsMenu = menuBar->addMenu("&Tools");
    toolsMenu->addAction("&Gradient Descent", this, &MainWindow::showGradientDescent, tr("Ctrl+G"));
    toolsMenu->addAction("&Chain Rule Explorer", this, &MainWindow::showChainRule, tr("Ctrl+C"));
    
    // Help menu
    QMenu *helpMenu = menuBar->addMenu("&Help");
    helpMenu->addAction("&About", [this]() {
        QMessageBox::about(this, "About Calculus Visualizer",
            "<h2>Calculus Visualizer v1.0</h2>"
            "<p>An advanced mathematical learning tool combining:</p>"
            "<ul>"
            "<li>Desmos-style interactive graphing</li>"
            "<li>TI-Nspire CAS symbolic computation</li>"
            "<li>Step-by-step derivative solutions</li>"
            "<li>Gradient descent visualization</li>"
            "<li>Chain rule breakdown for backpropagation</li>"
            "</ul>"
            "<p>Built with Qt6 and C++20</p>");
    });
}

void MainWindow::setupToolBar()
{
    QToolBar *toolBar = addToolBar("Main Toolbar");
    toolBar->setMovable(false);
    
    toolBar->addAction("New", this, &MainWindow::createNewGraph);
    toolBar->addAction("Clear", this, &MainWindow::onClearGraph);
    toolBar->addSeparator();
    toolBar->addAction("Derivative", this, &MainWindow::onComputeDerivative);
    toolBar->addAction("Integral", this, &MainWindow::onComputeIntegral);
    toolBar->addSeparator();
    toolBar->addAction("Steps", this, &MainWindow::onShowSteps);
}

void MainWindow::setupConnections()
{
    connect(expressionInput, &QLineEdit::returnPressed, this, &MainWindow::onAddExpression);
    connect(addExpressionBtn, &QPushButton::clicked, this, &MainWindow::onAddExpression);
    connect(derivativeBtn, &QPushButton::clicked, this, &MainWindow::onComputeDerivative);
    connect(integralBtn, &QPushButton::clicked, this, &MainWindow::onComputeIntegral);
    connect(solveBtn, &QPushButton::clicked, this, &MainWindow::onSolveEquation);
    connect(clearBtn, &QPushButton::clicked, this, &MainWindow::onClearGraph);
    connect(exportBtn, &QPushButton::clicked, this, &MainWindow::onExportGraph);
    connect(zoomInBtn, &QPushButton::clicked, this, &MainWindow::onZoomIn);
    connect(zoomOutBtn, &QPushButton::clicked, this, &MainWindow::onZoomOut);
    connect(resetViewBtn, &QPushButton::clicked, this, &MainWindow::onResetView);
    connect(expressionList, &QListWidget::itemDoubleClicked, this, &MainWindow::onToggleExpression);
}

void MainWindow::applyDarkTheme()
{
    // Additional stylesheet for specific widgets
    QString styleSheet = R"(
        QGroupBox {
            font-weight: bold;
            border: 1px solid #555;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        QPushButton {
            background-color: #2c5aa0;
            border: none;
            border-radius: 4px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3567b8;
        }
        QPushButton:pressed {
            background-color: #1e4278;
        }
        QLineEdit {
            border: 1px solid #555;
            border-radius: 4px;
            padding: 5px;
            background-color: #2a2a2a;
        }
        QLineEdit:focus {
            border: 1px solid #2c5aa0;
        }
        QTextEdit {
            border: 1px solid #555;
            border-radius: 4px;
            background-color: #2a2a2a;
        }
        QListWidget {
            border: 1px solid #555;
            border-radius: 4px;
            background-color: #2a2a2a;
        }
        QListWidget::item:selected {
            background-color: #2c5aa0;
        }
    )";
    setStyleSheet(styleSheet);
}

// Public slots
void MainWindow::createNewGraph()
{
    onClearGraph();
    tabWidget->setCurrentIndex(0);
    expressionInput->setFocus();
    statusBar()->showMessage("Ready for new graph", 2000);
}

void MainWindow::showGradientDescent()
{
    tabWidget->setCurrentIndex(1);
    statusBar()->showMessage("Gradient Descent Visualizer", 2000);
}

void MainWindow::showChainRule()
{
    tabWidget->setCurrentIndex(2);
    statusBar()->showMessage("Chain Rule Explorer", 2000);
}

// Private slots
void MainWindow::onExpressionEntered()
{
    currentExpression = expressionInput->text();
    statusBar()->showMessage("Expression: " + currentExpression, 3000);
}

void MainWindow::onAddExpression()
{
    QString expr = expressionInput->text().trimmed();
    if (expr.isEmpty()) {
        statusBar()->showMessage("Please enter an expression", 2000);
        return;
    }
    
    // Add to list
    expressions.append(expr);
    expressionList->addItem(expr);
    
    // Plot on graph
    graphWidget->addFunction(expr);
    
    expressionInput->clear();
    statusBar()->showMessage("Added: " + expr, 2000);
}

void MainWindow::onRemoveExpression()
{
    auto *item = expressionList->currentItem();
    if (!item) return;
    
    QString expr = item->text();
    int row = expressionList->row(item);
    
    expressions.removeAt(row);
    delete expressionList->takeItem(row);
    graphWidget->removeFunction(expr);
    
    statusBar()->showMessage("Removed: " + expr, 2000);
}

void MainWindow::onToggleExpression(QListWidgetItem *item)
{
    QString expr = item->text();
    graphWidget->toggleFunction(expr);
}

void MainWindow::onComputeDerivative()
{
    QString expr = expressionInput->text().trimmed();
    if (expr.isEmpty() && expressionList->currentItem()) {
        expr = expressionList->currentItem()->text();
    }
    
    if (expr.isEmpty()) {
        statusBar()->showMessage("No expression selected", 2000);
        return;
    }
    
    QString derivative = derivativeEngine->computeDerivative(expr);
    QString steps = derivativeEngine->getSteps();
    
    stepByStepOutput->setHtml(
        "<h3>Derivative of: " + expr + "</h3>" +
        "<p><b>Result:</b> d/dx(" + expr + ") = " + derivative + "</p>" +
        "<hr>" +
        "<h4>Step-by-Step Solution:</h4>" +
        steps
    );
    
    // Add derivative to graph
    graphWidget->addFunction(derivative, Qt::red);
    
    statusBar()->showMessage("Derivative computed", 2000);
}

void MainWindow::onComputeIntegral()
{
    QString expr = expressionInput->text().trimmed();
    if (expr.isEmpty() && expressionList->currentItem()) {
        expr = expressionList->currentItem()->text();
    }
    
    if (expr.isEmpty()) {
        statusBar()->showMessage("No expression selected", 2000);
        return;
    }
    
    QString integral = derivativeEngine->computeIntegral(expr);
    
    stepByStepOutput->setHtml(
        "<h3>Integral of: " + expr + "</h3>" +
        "<p><b>Result:</b> ∫(" + expr + ") dx = " + integral + " + C</p>"
    );
    
    statusBar()->showMessage("Integral computed", 2000);
}

void MainWindow::onSolveEquation()
{
    QString expr = expressionInput->text().trimmed();
    if (expr.isEmpty() && expressionList->currentItem()) {
        expr = expressionList->currentItem()->text();
    }
    
    if (expr.isEmpty()) {
        statusBar()->showMessage("No expression selected", 2000);
        return;
    }
    
    QStringList solutions = derivativeEngine->solve(expr);
    
    QString html = "<h3>Solutions for: " + expr + " = 0</h3><ul>";
    for (const QString &sol : solutions) {
        html += "<li>x = " + sol + "</li>";
    }
    html += "</ul>";
    
    stepByStepOutput->setHtml(html);
    statusBar()->showMessage("Equation solved", 2000);
}

void MainWindow::onShowSteps()
{
    QString steps = derivativeEngine->getSteps();
    if (!steps.isEmpty()) {
        stepByStepOutput->setHtml(steps);
    }
}

void MainWindow::onClearGraph()
{
    graphWidget->clear();
    expressionList->clear();
    expressions.clear();
    stepByStepOutput->clear();
    expressionInput->clear();
    statusBar()->showMessage("Graph cleared", 2000);
}

void MainWindow::onExportGraph()
{
    QString fileName = QFileDialog::getSaveFileName(this, "Export Graph",
        QString(), "PNG Image (*.png);;PDF Document (*.pdf)");
    
    if (!fileName.isEmpty()) {
        if (graphWidget->exportImage(fileName)) {
            statusBar()->showMessage("Graph exported to: " + fileName, 3000);
        } else {
            QMessageBox::warning(this, "Export Failed", "Could not export graph");
        }
    }
}

void MainWindow::onZoomIn()
{
    graphWidget->zoomIn();
    statusBar()->showMessage("Zoomed in", 1000);
}

void MainWindow::onZoomOut()
{
    graphWidget->zoomOut();
    statusBar()->showMessage("Zoomed out", 1000);
}

void MainWindow::onResetView()
{
    graphWidget->resetView();
    statusBar()->showMessage("View reset", 1000);
}

void MainWindow::onAnimateGradient()
{
    showGradientDescent();
}
