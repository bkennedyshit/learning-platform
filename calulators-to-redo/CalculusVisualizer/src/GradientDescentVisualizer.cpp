/**
 * GradientDescentVisualizer.cpp - Implementation of gradient descent visualization
 */

#include "GradientDescentVisualizer.h"
#include "GraphWidget.h"
#include "ExpressionParser.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QFormLayout>
#include <cmath>

GradientDescentVisualizer::GradientDescentVisualizer(QWidget *parent)
    : QWidget(parent)
    , learningRate(0.1)
    , maxIterations(100)
    , currentIteration(0)
    , isAnimating(false)
{
    setupUI();
    setupConnections();
}

GradientDescentVisualizer::~GradientDescentVisualizer()
{
}

void GradientDescentVisualizer::setupUI()
{
    auto *mainLayout = new QVBoxLayout(this);
    
    // Top controls
    auto *controlsGroup = new QGroupBox("Gradient Descent Parameters");
    auto *controlsLayout = new QFormLayout(controlsGroup);
    
    functionInput = new QLineEdit("x**2 - 4*x + 3");
    functionInput->setPlaceholderText("Enter function (e.g., x^2 - 4*x + 3)");
    
    learningRateSpinBox = new QDoubleSpinBox();
    learningRateSpinBox->setRange(0.001, 1.0);
    learningRateSpinBox->setValue(0.1);
    learningRateSpinBox->setSingleStep(0.01);
    learningRateSpinBox->setDecimals(3);
    
    maxIterationsSpinBox = new QSpinBox();
    maxIterationsSpinBox->setRange(10, 1000);
    maxIterationsSpinBox->setValue(100);
    
    animationSpeedSlider = new QSlider(Qt::Horizontal);
    animationSpeedSlider->setRange(10, 1000);
    animationSpeedSlider->setValue(100);
    animationSpeedSlider->setTickPosition(QSlider::TicksBelow);
    animationSpeedSlider->setTickInterval(100);
    
    controlsLayout->addRow("Function f(x):", functionInput);
    controlsLayout->addRow("Learning Rate α:", learningRateSpinBox);
    controlsLayout->addRow("Max Iterations:", maxIterationsSpinBox);
    controlsLayout->addRow("Animation Speed:", animationSpeedSlider);
    
    // Buttons
    auto *buttonLayout = new QHBoxLayout();
    startBtn = new QPushButton("▶ Start");
    stopBtn = new QPushButton("⏸ Pause");
    resetBtn = new QPushButton("↻ Reset");
    stepBtn = new QPushButton("→ Step");
    
    stopBtn->setEnabled(false);
    
    buttonLayout->addWidget(startBtn);
    buttonLayout->addWidget(stopBtn);
    buttonLayout->addWidget(stepBtn);
    buttonLayout->addWidget(resetBtn);
    buttonLayout->addStretch();
    
    // Status display
    auto *statusGroup = new QGroupBox("Optimization Status");
    auto *statusLayout = new QVBoxLayout(statusGroup);
    
    iterationLabel = new QLabel("Iteration: 0 / 0");
    currentValueLabel = new QLabel("Current: x = 0.000, f(x) = 0.000");
    statusLabel = new QLabel("Status: Ready");
    
    statusLayout->addWidget(iterationLabel);
    statusLayout->addWidget(currentValueLabel);
    statusLayout->addWidget(statusLabel);
    
    // Graph
    graphWidget = new GraphWidget();
    graphWidget->setMinimumHeight(400);
    
    // Assemble layout
    mainLayout->addWidget(controlsGroup);
    mainLayout->addLayout(buttonLayout);
    mainLayout->addWidget(statusGroup);
    mainLayout->addWidget(graphWidget, 1);
    
    // Animation timer
    animationTimer = new QTimer(this);
    connect(animationTimer, &QTimer::timeout, this, &GradientDescentVisualizer::updateAnimation);
    
    // Initial function plot
    onFunctionChanged();
}

void GradientDescentVisualizer::setupConnections()
{
    connect(startBtn, &QPushButton::clicked, this, &GradientDescentVisualizer::onStartAnimation);
    connect(stopBtn, &QPushButton::clicked, this, &GradientDescentVisualizer::onStopAnimation);
    connect(resetBtn, &QPushButton::clicked, this, &GradientDescentVisualizer::onResetAnimation);
    connect(stepBtn, &QPushButton::clicked, this, &GradientDescentVisualizer::onStepAnimation);
    connect(learningRateSpinBox, QOverload<double>::of(&QDoubleSpinBox::valueChanged),
            this, &GradientDescentVisualizer::onLearningRateChanged);
    connect(functionInput, &QLineEdit::returnPressed, this, &GradientDescentVisualizer::onFunctionChanged);
}

void GradientDescentVisualizer::onStartAnimation()
{
    if (!isAnimating) {
        initializeOptimization();
        isAnimating = true;
        startBtn->setEnabled(false);
        stopBtn->setEnabled(true);
        stepBtn->setEnabled(false);
        
        int interval = 1100 - animationSpeedSlider->value(); // Invert so higher = faster
        animationTimer->start(interval);
        
        statusLabel->setText("Status: <span style='color: #4a9eff;'>Running...</span>");
    }
}

void GradientDescentVisualizer::onStopAnimation()
{
    if (isAnimating) {
        isAnimating = false;
        animationTimer->stop();
        startBtn->setEnabled(true);
        stopBtn->setEnabled(false);
        stepBtn->setEnabled(true);
        statusLabel->setText("Status: <span style='color: orange;'>Paused</span>");
    }
}

void GradientDescentVisualizer::onResetAnimation()
{
    onStopAnimation();
    currentIteration = 0;
    trajectory.clear();
    graphWidget->clear();
    onFunctionChanged();
    statusLabel->setText("Status: Ready");
    iterationLabel->setText("Iteration: 0 / 0");
    currentValueLabel->setText("Current: x = 0.000, f(x) = 0.000");
}

void GradientDescentVisualizer::onStepAnimation()
{
    if (currentIteration == 0) {
        initializeOptimization();
    }
    
    if (currentIteration < maxIterations) {
        performGradientStep();
        updateVisualization();
        currentIteration++;
        
        iterationLabel->setText(QString("Iteration: %1 / %2")
            .arg(currentIteration).arg(maxIterations));
        currentValueLabel->setText(QString("Current: x = %1, f(x) = %2")
            .arg(currentX, 0, 'f', 3).arg(currentY, 0, 'f', 3));
        
        double gradient = computeGradient(currentX);
        if (std::abs(gradient) < 1e-6) {
            statusLabel->setText("Status: <span style='color: #00ff00;'>Converged!</span>");
        }
    }
}

void GradientDescentVisualizer::onLearningRateChanged(double value)
{
    learningRate = value;
}

void GradientDescentVisualizer::onFunctionChanged()
{
    currentFunction = functionInput->text();
    graphWidget->clear();
    graphWidget->addFunction(currentFunction);
    onResetAnimation();
}

void GradientDescentVisualizer::initializeOptimization()
{
    currentFunction = functionInput->text();
    learningRate = learningRateSpinBox->value();
    maxIterations = maxIterationsSpinBox->value();
    
    // Start from a random point or fixed point
    currentX = 5.0; // Starting point
    currentY = evaluateFunction(currentX);
    currentIteration = 0;
    
    trajectory.clear();
    trajectory.push_back({currentX, currentY});
    
    // Plot function
    graphWidget->clear();
    graphWidget->addFunction(currentFunction);
}

double GradientDescentVisualizer::evaluateFunction(double x)
{
    ExpressionParser parser;
    return parser.evaluate(currentFunction, x);
}

double GradientDescentVisualizer::computeGradient(double x)
{
    // Numerical gradient using finite differences
    const double h = 1e-6;
    double fxph = evaluateFunction(x + h);
    double fx = evaluateFunction(x);
    return (fxph - fx) / h;
}

void GradientDescentVisualizer::performGradientStep()
{
    double gradient = computeGradient(currentX);
    
    // Gradient descent update: x_new = x_old - α * ∇f(x)
    currentX = currentX - learningRate * gradient;
    currentY = evaluateFunction(currentX);
    
    trajectory.push_back({currentX, currentY});
}

void GradientDescentVisualizer::updateVisualization()
{
    // This would update the graph with current position marker
    // For now, just update labels
    iterationLabel->setText(QString("Iteration: %1 / %2")
        .arg(currentIteration + 1).arg(maxIterations));
    currentValueLabel->setText(QString("Current: x = %1, f(x) = %2")
        .arg(currentX, 0, 'f', 3).arg(currentY, 0, 'f', 3));
    
    double gradient = computeGradient(currentX);
    statusLabel->setText(QString("Status: Running... (gradient = %1)")
        .arg(gradient, 0, 'e', 2));
    
    // Check convergence
    if (std::abs(gradient) < 1e-6) {
        onStopAnimation();
        statusLabel->setText("Status: <span style='color: #00ff00;'>Converged!</span>");
    }
    
    if (currentIteration >= maxIterations) {
        onStopAnimation();
        statusLabel->setText("Status: <span style='color: orange;'>Max iterations reached</span>");
    }
}

void GradientDescentVisualizer::updateAnimation()
{
    onStepAnimation();
}
