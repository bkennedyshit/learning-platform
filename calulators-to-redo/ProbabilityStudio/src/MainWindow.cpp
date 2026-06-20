#include "MainWindow.h"
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include <QStatusBar>

// Import all widgets
#include "DistributionWidget.h"
#include "SoftmaxVisualizer.h"
#include "BayesCalculator.h"
#include "CrossEntropyWidget.h"
#include "KLDivergenceWidget.h"
#include "SamplingVisualizer.h"
#include "HypothesisTestWidget.h"
#include "ConfusionMatrixWidget.h"
#include "AttentionDistWidget.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Probability Studio - ML Statistics & Distribution Toolkit");
    resize(1450, 950);
    
    setupTabs();
    createMenus();
    
    statusBar()->showMessage("Ready - Select a tab to explore probability and ML statistics concepts");
}

MainWindow::~MainWindow()
{
}

void MainWindow::setupTabs()
{
    tabWidget = new QTabWidget(this);
    tabWidget->setTabPosition(QTabWidget::North);
    tabWidget->setMovable(true);
    
    // Core Distributions (NEW!)
    tabWidget->addTab(new DistributionWidget(this), "📊 Distributions");
    tabWidget->addTab(new SoftmaxVisualizer(this), "🔥 Softmax & Temperature");
    tabWidget->addTab(new BayesCalculator(this), "🎯 Bayes' Theorem");
    
    // ML Loss & Divergence
    tabWidget->addTab(new CrossEntropyWidget(this), "📉 Cross-Entropy Loss");
    tabWidget->addTab(new KLDivergenceWidget(this), "📐 KL Divergence");
    
    // Statistical Testing
    tabWidget->addTab(new SamplingVisualizer(this), "🎲 Central Limit Theorem");
    tabWidget->addTab(new HypothesisTestWidget(this), "🔬 Hypothesis Testing");
    
    // ML Evaluation
    tabWidget->addTab(new ConfusionMatrixWidget(this), "✅ Confusion Matrix");
    tabWidget->addTab(new AttentionDistWidget(this), "👁️ Attention Weights");
    
    setCentralWidget(tabWidget);
}

void MainWindow::createMenus()
{
    // File menu
    QMenu *fileMenu = menuBar()->addMenu("&File");
    
    QAction *exitAction = new QAction("E&xit", this);
    exitAction->setShortcut(QKeySequence::Quit);
    connect(exitAction, &QAction::triggered, this, &QWidget::close);
    fileMenu->addAction(exitAction);
    
    // Help menu
    QMenu *helpMenu = menuBar()->addMenu("&Help");
    
    QAction *helpAction = new QAction("&User Guide", this);
    helpAction->setShortcut(QKeySequence::HelpContents);
    connect(helpAction, &QAction::triggered, this, &MainWindow::showHelp);
    helpMenu->addAction(helpAction);
    
    helpMenu->addSeparator();
    
    QAction *aboutAction = new QAction("&About", this);
    connect(aboutAction, &QAction::triggered, this, &MainWindow::showAbout);
    helpMenu->addAction(aboutAction);
}

void MainWindow::showAbout()
{
    QMessageBox::about(this, "About Probability Studio",
        "<h2>Probability Studio v1.0</h2>"
        "<p><b>Interactive ML Statistics & Probability Distribution Toolkit</b></p>"
        "<p>Explore fundamental probability and statistics concepts used in machine learning:</p>"
        "<ul>"
        "<li><b>Distributions:</b> Normal, Binomial, Poisson, Exponential, Uniform</li>"
        "<li><b>Softmax:</b> Temperature control for LLM sampling</li>"
        "<li><b>Bayes' Theorem:</b> Bayesian inference and belief updating</li>"
        "<li><b>Cross-Entropy:</b> Classification loss functions</li>"
        "<li><b>KL Divergence:</b> Distribution similarity metrics</li>"
        "<li><b>Central Limit Theorem:</b> Sampling distributions</li>"
        "<li><b>Hypothesis Testing:</b> Statistical significance (t-tests, p-values)</li>"
        "<li><b>Confusion Matrix:</b> Classification metrics (precision, recall, F1)</li>"
        "<li><b>Attention Weights:</b> Transformer attention visualization</li>"
        "</ul>"
        "<p>Built with Qt6 for hands-on learning of ML fundamentals.</p>"
        "<p><i>Perfect for students, ML practitioners, and anyone learning statistics!</i></p>"
    );
}

void MainWindow::showHelp()
{
    QMessageBox::information(this, "Probability Studio - User Guide",
        "<h3>Quick Start Guide</h3>"
        "<p><b>Navigation:</b> Use tabs at the top to switch between different visualizations.</p>"
        
        "<p><b>📊 Distributions:</b><br>"
        "Select a distribution type and adjust parameters with sliders. "
        "Toggle between PDF/PMF and CDF views to see probability density and cumulative probability.</p>"
        
        "<p><b>🔥 Softmax Temperature:</b><br>"
        "Critical for LLM text generation! Adjust temperature to see how it affects output randomness. "
        "Low temperature (0.1) = deterministic, high temperature (2.0) = creative/random.</p>"
        
        "<p><b>🎯 Bayes' Theorem:</b><br>"
        "Adjust prior belief, likelihood, and evidence to see how the posterior probability updates. "
        "Try the example scenarios to understand real-world applications.</p>"
        
        "<p><b>📉 Cross-Entropy Loss:</b><br>"
        "Drag probability sliders to see how prediction confidence affects loss. "
        "Used to train neural network classifiers.</p>"
        
        "<p><b>📐 KL Divergence:</b><br>"
        "Measure how one probability distribution differs from another. "
        "Fundamental for variational autoencoders (VAEs) and policy optimization.</p>"
        
        "<p><b>🎲 Central Limit Theorem:</b><br>"
        "Draw samples from different distributions and watch how sample means converge to normal distribution.</p>"
        
        "<p><b>🔬 Hypothesis Testing:</b><br>"
        "Perform t-tests to determine statistical significance. "
        "Adjust sample sizes and effect sizes to see p-values change.</p>"
        
        "<p><b>✅ Confusion Matrix:</b><br>"
        "Evaluate binary classifiers with precision, recall, F1-score, and accuracy metrics. "
        "Adjust true/false positives and negatives.</p>"
        
        "<p><b>👁️ Attention Weights:</b><br>"
        "Visualize how transformer attention mechanisms work. "
        "See query-key attention scores and their softmax-normalized weights.</p>"
        
        "<p><i>Tip: Hover over controls for tooltips. Experiment with extreme values to build intuition!</i></p>"
    );
}
