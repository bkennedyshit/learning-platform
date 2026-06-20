#include "MainWindow.h"
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include <QFileDialog>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSplitter>
#include <QStatusBar>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Loss Landscape 3D - ML Optimization Visualizer");
    resize(1400, 900);
    
    // Initialize function bounds
    m_functionBounds = {
        {"Rosenbrock (Banana Valley)", {-2.0, 2.0, -1.0, 3.0}},
        {"Himmelblau (Multiple Minima)", {-5.0, 5.0, -5.0, 5.0}},
        {"Beale Function", {-4.5, 4.5, -4.5, 4.5}},
        {"Rastrigin (Many Local Minima)", {-5.12, 5.12, -5.12, 5.12}},
        {"Sphere (Simple Bowl)", {-5.0, 5.0, -5.0, 5.0}},
        {"Saddle Point (x² - y²)", {-3.0, 3.0, -3.0, 3.0}}
    };
    
    setupUI();
    setupMenuBar();
    connectSignals();
    
    statusBar()->showMessage("Ready - Select a loss function to begin");
}

MainWindow::~MainWindow()
{
}

void MainWindow::setupUI()
{
    QWidget* centralWidget = new QWidget(this);
    QVBoxLayout* mainLayout = new QVBoxLayout(centralWidget);
    
    m_tabWidget = new QTabWidget();
    m_tabWidget->setTabPosition(QTabWidget::North);
    
    // Tab 1: 3D Surface View
    m_surface3D = new Surface3DWidget();
    m_tabWidget->addTab(m_surface3D, "📊 3D Surface");
    
    // Tab 2: Contour Plot
    m_contourWidget = new ContourWidget();
    m_tabWidget->addTab(m_contourWidget, "🗺️ Contour Map");
    
    // Tab 3: Gradient Field
    m_gradientWidget = new GradientFieldWidget();
    m_tabWidget->addTab(m_gradientWidget, "➡️ Gradient Field");
    
    // Tab 4: Single Optimizer with 3D Path
    QSplitter* optimizerSplitter = new QSplitter(Qt::Horizontal);
    
    // Clone the 3D surface for the optimizer view
    Surface3DWidget* optimizerSurface = new Surface3DWidget();
    optimizerSplitter->addWidget(optimizerSurface);
    
    m_optimizationPath = new OptimizationPath3D();
    m_optimizationPath->setSurface(optimizerSurface->getSurface());
    optimizerSplitter->addWidget(m_optimizationPath);
    
    optimizerSplitter->setSizes({700, 300});
    m_tabWidget->addTab(optimizerSplitter, "🎯 Single Optimizer");
    
    // Store the optimizer surface widget for function updates
    optimizerSurface->setObjectName("optimizerSurface");
    
    // Tab 5: Multi-Optimizer Race
    QSplitter* multiSplitter = new QSplitter(Qt::Vertical);
    
    ContourWidget* raceContour = new ContourWidget();
    raceContour->setObjectName("raceContour");
    multiSplitter->addWidget(raceContour);
    
    m_multiOptimizer = new MultiOptimizer();
    multiSplitter->addWidget(m_multiOptimizer);
    
    multiSplitter->setSizes({400, 400});
    m_tabWidget->addTab(multiSplitter, "🏁 Optimizer Race");
    
    mainLayout->addWidget(m_tabWidget);
    setCentralWidget(centralWidget);
    
    // Set initial function
    m_currentFunctionName = "Rosenbrock (Banana Valley)";
    m_currentFunction = Surface3DWidget::rosenbrock;
    updateAllWidgets();
}

void MainWindow::setupMenuBar()
{
    // File menu
    QMenu* fileMenu = menuBar()->addMenu("&File");
    
    QAction* exportAction = new QAction("&Export View...", this);
    exportAction->setShortcut(QKeySequence::Save);
    connect(exportAction, &QAction::triggered, this, &MainWindow::exportCurrentView);
    fileMenu->addAction(exportAction);
    
    fileMenu->addSeparator();
    
    QAction* exitAction = new QAction("E&xit", this);
    exitAction->setShortcut(QKeySequence::Quit);
    connect(exitAction, &QAction::triggered, this, &QWidget::close);
    fileMenu->addAction(exitAction);
    
    // View menu
    QMenu* viewMenu = menuBar()->addMenu("&View");
    
    QAction* surface3DAction = new QAction("&3D Surface", this);
    surface3DAction->setShortcut(QKeySequence("Ctrl+1"));
    connect(surface3DAction, &QAction::triggered, [this]() { m_tabWidget->setCurrentIndex(0); });
    viewMenu->addAction(surface3DAction);
    
    QAction* contourAction = new QAction("&Contour Map", this);
    contourAction->setShortcut(QKeySequence("Ctrl+2"));
    connect(contourAction, &QAction::triggered, [this]() { m_tabWidget->setCurrentIndex(1); });
    viewMenu->addAction(contourAction);
    
    QAction* gradientAction = new QAction("&Gradient Field", this);
    gradientAction->setShortcut(QKeySequence("Ctrl+3"));
    connect(gradientAction, &QAction::triggered, [this]() { m_tabWidget->setCurrentIndex(2); });
    viewMenu->addAction(gradientAction);
    
    QAction* optimizerAction = new QAction("Single &Optimizer", this);
    optimizerAction->setShortcut(QKeySequence("Ctrl+4"));
    connect(optimizerAction, &QAction::triggered, [this]() { m_tabWidget->setCurrentIndex(3); });
    viewMenu->addAction(optimizerAction);
    
    QAction* raceAction = new QAction("Optimizer &Race", this);
    raceAction->setShortcut(QKeySequence("Ctrl+5"));
    connect(raceAction, &QAction::triggered, [this]() { m_tabWidget->setCurrentIndex(4); });
    viewMenu->addAction(raceAction);
    
    // Help menu
    QMenu* helpMenu = menuBar()->addMenu("&Help");
    
    QAction* helpAction = new QAction("&User Guide", this);
    helpAction->setShortcut(QKeySequence::HelpContents);
    connect(helpAction, &QAction::triggered, this, &MainWindow::showHelp);
    helpMenu->addAction(helpAction);
    
    QAction* aboutAction = new QAction("&About", this);
    connect(aboutAction, &QAction::triggered, this, &MainWindow::showAbout);
    helpMenu->addAction(aboutAction);
}

void MainWindow::connectSignals()
{
    // Connect function changes
    connect(m_surface3D, &Surface3DWidget::functionChanged,
            this, &MainWindow::onFunctionChanged);
    
    // Connect tab changes
    connect(m_tabWidget, &QTabWidget::currentChanged,
            this, &MainWindow::onTabChanged);
    
    // Connect optimizer path events
    connect(m_optimizationPath, &OptimizationPath3D::iterationCompleted,
            [this](int iter, double x, double y, double loss) {
                statusBar()->showMessage(QString("Iteration %1: Loss = %2 at (%3, %4)")
                    .arg(iter).arg(loss, 0, 'f', 6).arg(x, 0, 'f', 3).arg(y, 0, 'f', 3));
            });
    
    connect(m_optimizationPath, &OptimizationPath3D::optimizationFinished,
            [this]() {
                statusBar()->showMessage("Optimization complete!", 3000);
            });
    
    // Connect multi-optimizer events
    connect(m_multiOptimizer, &MultiOptimizer::raceFinished,
            [this](const QString& winner) {
                QMessageBox::information(this, "Race Complete",
                    QString("🏆 Winner: %1\n\nThe race has completed!").arg(winner));
            });
    
    connect(m_multiOptimizer, &MultiOptimizer::statusUpdate,
            [this](const QString& status) {
                statusBar()->showMessage(status);
            });
    
    // Connect contour widget point clicks
    connect(m_contourWidget, &ContourWidget::pointClicked,
            [this](double x, double y) {
                m_optimizationPath->setStartPoint(x, y);
                statusBar()->showMessage(QString("Start point set to (%1, %2)")
                    .arg(x, 0, 'f', 2).arg(y, 0, 'f', 2), 2000);
            });
}

void MainWindow::onFunctionChanged(const QString& name)
{
    m_currentFunctionName = name;
    
    // Get the function pointer
    if (name.contains("Rosenbrock")) {
        m_currentFunction = Surface3DWidget::rosenbrock;
    } else if (name.contains("Himmelblau")) {
        m_currentFunction = Surface3DWidget::himmelblau;
    } else if (name.contains("Beale")) {
        m_currentFunction = Surface3DWidget::beale;
    } else if (name.contains("Rastrigin")) {
        m_currentFunction = Surface3DWidget::rastrigin;
    } else if (name.contains("Sphere")) {
        m_currentFunction = Surface3DWidget::sphere;
    } else if (name.contains("Saddle")) {
        m_currentFunction = Surface3DWidget::saddle;
    }
    
    updateAllWidgets();
    statusBar()->showMessage("Function changed to: " + name, 3000);
}

void MainWindow::onTabChanged(int index)
{
    QString tabName = m_tabWidget->tabText(index);
    statusBar()->showMessage("Viewing: " + tabName);
}

void MainWindow::updateAllWidgets()
{
    if (!m_currentFunction) return;
    
    auto bounds = m_functionBounds.value(m_currentFunctionName);
    
    // Update contour widget
    m_contourWidget->setLossFunction(m_currentFunction);
    m_contourWidget->setBounds(bounds.minX, bounds.maxX, bounds.minY, bounds.maxY);
    
    // Update gradient field widget
    m_gradientWidget->setLossFunction(m_currentFunction);
    m_gradientWidget->setBounds(bounds.minX, bounds.maxX, bounds.minY, bounds.maxY);
    
    // Update optimization path
    m_optimizationPath->setLossFunction(m_currentFunction);
    m_optimizationPath->setStartPoint(bounds.minX * 0.8, bounds.maxY * 0.8);
    
    // Update optimizer surface
    Surface3DWidget* optimizerSurface = findChild<Surface3DWidget*>("optimizerSurface");
    if (optimizerSurface) {
        optimizerSurface->setLossFunction(m_currentFunctionName);
    }
    
    // Update race contour
    ContourWidget* raceContour = findChild<ContourWidget*>("raceContour");
    if (raceContour) {
        raceContour->setLossFunction(m_currentFunction);
        raceContour->setBounds(bounds.minX, bounds.maxX, bounds.minY, bounds.maxY);
    }
    
    // Update multi-optimizer
    m_multiOptimizer->setLossFunction(m_currentFunction);
    m_multiOptimizer->setBounds(bounds.minX, bounds.maxX, bounds.minY, bounds.maxY);
    m_multiOptimizer->reset();
}

void MainWindow::exportCurrentView()
{
    QString fileName = QFileDialog::getSaveFileName(this,
        "Export View", "",
        "PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*)");
    
    if (!fileName.isEmpty()) {
        // Get current tab widget
        QWidget* currentWidget = m_tabWidget->currentWidget();
        
        QPixmap pixmap = currentWidget->grab();
        if (pixmap.save(fileName)) {
            statusBar()->showMessage("Exported to: " + fileName, 3000);
        } else {
            QMessageBox::warning(this, "Export Failed",
                "Could not save image to file.");
        }
    }
}

void MainWindow::showAbout()
{
    QMessageBox::about(this, "About Loss Landscape 3D",
        "<h2>Loss Landscape 3D</h2>"
        "<p><b>Version 1.0</b></p>"
        "<p>An educational tool for visualizing machine learning optimization algorithms.</p>"
        "<p>This application helps you understand how different optimizers navigate "
        "loss landscapes and why some algorithms perform better than others on "
        "different types of surfaces.</p>"
        "<h3>Features:</h3>"
        "<ul>"
        "<li>Interactive 3D surface visualization</li>"
        "<li>2D contour plots with gradient field overlay</li>"
        "<li>Compare SGD, Momentum, Adam, RMSprop, Adagrad, and Adadelta</li>"
        "<li>Predefined loss functions (Rosenbrock, Himmelblau, Rastrigin, etc.)</li>"
        "<li>Race multiple optimizers simultaneously</li>"
        "</ul>"
        "<p><i>Built with Qt and QtDataVisualization</i></p>");
}

void MainWindow::showHelp()
{
    QMessageBox::information(this, "User Guide",
        "<h2>How to Use Loss Landscape 3D</h2>"
        
        "<h3>📊 3D Surface Tab</h3>"
        "<p>• Select a loss function from the dropdown<br>"
        "• Rotate the surface by dragging with mouse<br>"
        "• Zoom with mouse wheel<br>"
        "• Toggle mesh/solid surface display</p>"
        
        "<h3>🗺️ Contour Map Tab</h3>"
        "<p>• View level curves of the loss function<br>"
        "• Color indicates loss magnitude<br>"
        "• Critical points marked (MIN/MAX/SADDLE)<br>"
        "• Click to set starting point for optimizer</p>"
        
        "<h3>➡️ Gradient Field Tab</h3>"
        "<p>• Arrows show gradient direction<br>"
        "• Arrow color indicates gradient magnitude<br>"
        "• Adjust density and size with sliders<br>"
        "• Shows why gradients point to steepest descent</p>"
        
        "<h3>🎯 Single Optimizer Tab</h3>"
        "<p>• Watch one algorithm optimize in real-time<br>"
        "• Compare SGD, Momentum, Adam, RMSprop<br>"
        "• Adjust learning rate and see effects<br>"
        "• Step through iterations manually</p>"
        
        "<h3>🏁 Optimizer Race Tab</h3>"
        "<p>• Race 6 optimizers simultaneously<br>"
        "• See which algorithm converges fastest<br>"
        "• Enable/disable individual optimizers<br>"
        "• Use Random Starts for fair comparison</p>"
        
        "<h3>Educational Insights</h3>"
        "<p><b>Rosenbrock:</b> Shows why momentum helps in narrow valleys<br>"
        "<b>Himmelblau:</b> Multiple local minima - optimizer may get stuck<br>"
        "<b>Rastrigin:</b> Many local minima - tests global search ability<br>"
        "<b>Saddle Point:</b> See why momentum/Adam escape saddles better than SGD</p>");
}
