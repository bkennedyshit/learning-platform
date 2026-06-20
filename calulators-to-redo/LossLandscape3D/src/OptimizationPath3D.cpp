#include "OptimizationPath3D.h"
#include <QtDataVisualization/QScatter3DSeries>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QLabel>
#include <cmath>

using namespace QtDataVisualization;

OptimizationPath3D::OptimizationPath3D(QWidget *parent)
    : QWidget(parent)
    , m_animationTimer(new QTimer(this))
{
    setupUI();
    
    connect(m_animationTimer, &QTimer::timeout,
            this, &OptimizationPath3D::onAnimationStep);
}

void OptimizationPath3D::setupUI()
{
    QVBoxLayout* mainLayout = new QVBoxLayout(this);
    
    // Control panel
    QGroupBox* controlBox = new QGroupBox("Optimization Controls");
    QVBoxLayout* controlLayout = new QVBoxLayout(controlBox);
    
    // Optimizer selection
    QHBoxLayout* optimizerLayout = new QHBoxLayout();
    optimizerLayout->addWidget(new QLabel("Optimizer:"));
    m_optimizerCombo = new QComboBox();
    m_optimizerCombo->addItem("SGD (Stochastic Gradient Descent)");
    m_optimizerCombo->addItem("Momentum");
    m_optimizerCombo->addItem("Adam");
    m_optimizerCombo->addItem("RMSprop");
    optimizerLayout->addWidget(m_optimizerCombo);
    controlLayout->addLayout(optimizerLayout);
    
    // Learning rate
    QHBoxLayout* lrLayout = new QHBoxLayout();
    lrLayout->addWidget(new QLabel("Learning Rate:"));
    m_learningRateSpin = new QDoubleSpinBox();
    m_learningRateSpin->setRange(0.0001, 1.0);
    m_learningRateSpin->setSingleStep(0.001);
    m_learningRateSpin->setDecimals(4);
    m_learningRateSpin->setValue(0.01);
    lrLayout->addWidget(m_learningRateSpin);
    controlLayout->addLayout(lrLayout);
    
    // Max iterations
    QHBoxLayout* iterLayout = new QHBoxLayout();
    iterLayout->addWidget(new QLabel("Max Iterations:"));
    m_maxIterSpin = new QSpinBox();
    m_maxIterSpin->setRange(10, 10000);
    m_maxIterSpin->setValue(1000);
    iterLayout->addWidget(m_maxIterSpin);
    controlLayout->addLayout(iterLayout);
    
    // Animation speed
    QHBoxLayout* speedLayout = new QHBoxLayout();
    speedLayout->addWidget(new QLabel("Animation Speed (ms):"));
    m_speedSpin = new QSpinBox();
    m_speedSpin->setRange(1, 1000);
    m_speedSpin->setValue(50);
    speedLayout->addWidget(m_speedSpin);
    controlLayout->addLayout(speedLayout);
    
    // Control buttons
    QHBoxLayout* buttonLayout = new QHBoxLayout();
    m_startButton = new QPushButton("Start");
    m_pauseButton = new QPushButton("Pause");
    m_pauseButton->setEnabled(false);
    m_resetButton = new QPushButton("Reset");
    m_stepButton = new QPushButton("Step");
    
    buttonLayout->addWidget(m_startButton);
    buttonLayout->addWidget(m_pauseButton);
    buttonLayout->addWidget(m_resetButton);
    buttonLayout->addWidget(m_stepButton);
    controlLayout->addLayout(buttonLayout);
    
    // Status label
    m_statusLabel = new QLabel("Ready");
    m_statusLabel->setStyleSheet("font-weight: bold; padding: 5px;");
    controlLayout->addWidget(m_statusLabel);
    
    // Info label (optimizer description)
    m_infoLabel = new QLabel();
    m_infoLabel->setWordWrap(true);
    m_infoLabel->setStyleSheet("color: #0066cc; padding: 5px; background-color: #f0f0f0;");
    controlLayout->addWidget(m_infoLabel);
    
    mainLayout->addWidget(controlBox);
    
    // Connect signals
    connect(m_startButton, &QPushButton::clicked,
            this, &OptimizationPath3D::onStartClicked);
    connect(m_pauseButton, &QPushButton::clicked,
            this, &OptimizationPath3D::onPauseClicked);
    connect(m_resetButton, &QPushButton::clicked,
            this, &OptimizationPath3D::onResetClicked);
    connect(m_stepButton, &QPushButton::clicked,
            this, &OptimizationPath3D::onStepClicked);
    connect(m_optimizerCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &OptimizationPath3D::onOptimizerChanged);
    
    // Initialize info
    onOptimizerChanged(0);
}

void OptimizationPath3D::setSurface(Q3DSurface* surface)
{
    m_surface = surface;
}

void OptimizationPath3D::setLossFunction(LossFunction func)
{
    m_function = func;
}

void OptimizationPath3D::setStartPoint(double x, double y)
{
    m_startX = x;
    m_startY = y;
    m_currentX = x;
    m_currentY = y;
}

void OptimizationPath3D::setOptimizer(OptimizerType type)
{
    m_optimizerType = type;
    m_optimizerCombo->setCurrentIndex(static_cast<int>(type));
}

void OptimizationPath3D::setLearningRate(double lr)
{
    m_learningRate = lr;
    m_learningRateSpin->setValue(lr);
}

void OptimizationPath3D::setMaxIterations(int maxIter)
{
    m_maxIterations = maxIter;
    m_maxIterSpin->setValue(maxIter);
}

void OptimizationPath3D::start()
{
    if (!m_function || !m_surface) return;
    
    m_isRunning = true;
    m_startButton->setEnabled(false);
    m_pauseButton->setEnabled(true);
    m_stepButton->setEnabled(false);
    
    m_animationSpeed = m_speedSpin->value();
    m_animationTimer->start(m_animationSpeed);
    
    m_statusLabel->setText("Running...");
}

void OptimizationPath3D::pause()
{
    m_isRunning = false;
    m_animationTimer->stop();
    
    m_startButton->setEnabled(true);
    m_pauseButton->setEnabled(false);
    m_stepButton->setEnabled(true);
    
    m_statusLabel->setText("Paused");
}

void OptimizationPath3D::reset()
{
    pause();
    
    m_currentX = m_startX;
    m_currentY = m_startY;
    m_currentIteration = 0;
    
    // Reset optimizer state
    m_velocityX = 0.0;
    m_velocityY = 0.0;
    m_m_x = m_m_y = 0.0;
    m_v_x = m_v_y = 0.0;
    m_cache_x = m_cache_y = 0.0;
    
    clearPath();
    addPathPoint(m_currentX, m_currentY);
    
    m_statusLabel->setText("Reset");
    emit iterationCompleted(0, m_currentX, m_currentY, evaluateFunction(m_currentX, m_currentY));
}

void OptimizationPath3D::step()
{
    performOptimizationStep();
}

void OptimizationPath3D::onAnimationStep()
{
    performOptimizationStep();
}

void OptimizationPath3D::performOptimizationStep()
{
    if (!m_function || m_currentIteration >= m_maxIterations) {
        pause();
        m_statusLabel->setText("Finished");
        emit optimizationFinished();
        return;
    }
    
    // Get current gradient
    QPointF grad = computeGradient(m_currentX, m_currentY);
    double gx = grad.x();
    double gy = grad.y();
    
    // Update based on optimizer type
    double dx = 0.0, dy = 0.0;
    
    switch (m_optimizerType) {
        case SGD:
            // Simple gradient descent
            dx = -m_learningRate * gx;
            dy = -m_learningRate * gy;
            break;
        
        case Momentum:
            // Momentum: v = momentum * v - lr * grad
            m_velocityX = m_momentum * m_velocityX - m_learningRate * gx;
            m_velocityY = m_momentum * m_velocityY - m_learningRate * gy;
            dx = m_velocityX;
            dy = m_velocityY;
            break;
        
        case Adam: {
            // Adam optimizer
            m_currentIteration++; // Adam uses 1-indexed iterations
            
            m_m_x = m_beta1 * m_m_x + (1 - m_beta1) * gx;
            m_m_y = m_beta1 * m_m_y + (1 - m_beta1) * gy;
            
            m_v_x = m_beta2 * m_v_x + (1 - m_beta2) * gx * gx;
            m_v_y = m_beta2 * m_v_y + (1 - m_beta2) * gy * gy;
            
            // Bias correction
            double m_x_hat = m_m_x / (1 - std::pow(m_beta1, m_currentIteration));
            double m_y_hat = m_m_y / (1 - std::pow(m_beta1, m_currentIteration));
            double v_x_hat = m_v_x / (1 - std::pow(m_beta2, m_currentIteration));
            double v_y_hat = m_v_y / (1 - std::pow(m_beta2, m_currentIteration));
            
            dx = -m_learningRate * m_x_hat / (std::sqrt(v_x_hat) + m_epsilon);
            dy = -m_learningRate * m_y_hat / (std::sqrt(v_y_hat) + m_epsilon);
            
            m_currentIteration--; // Correct for increment at start
            break;
        }
        
        case RMSprop:
            // RMSprop
            m_cache_x = m_rho * m_cache_x + (1 - m_rho) * gx * gx;
            m_cache_y = m_rho * m_cache_y + (1 - m_rho) * gy * gy;
            
            dx = -m_learningRate * gx / (std::sqrt(m_cache_x) + m_epsilon);
            dy = -m_learningRate * gy / (std::sqrt(m_cache_y) + m_epsilon);
            break;
    }
    
    // Update position
    m_currentX += dx;
    m_currentY += dy;
    m_currentIteration++;
    
    // Add to path
    addPathPoint(m_currentX, m_currentY);
    
    // Update visualization
    updateVisualization();
    
    // Emit progress
    double loss = evaluateFunction(m_currentX, m_currentY);
    emit iterationCompleted(m_currentIteration, m_currentX, m_currentY, loss);
    
    // Update status
    m_statusLabel->setText(QString("Iteration %1/%2 | Loss: %3")
        .arg(m_currentIteration)
        .arg(m_maxIterations)
        .arg(loss, 0, 'f', 4));
    
    // Check convergence
    double gradMag = std::sqrt(gx * gx + gy * gy);
    if (gradMag < 1e-6) {
        pause();
        m_statusLabel->setText("Converged!");
        emit optimizationFinished();
    }
}

QPointF OptimizationPath3D::computeGradient(double x, double y) const
{
    if (!m_function) return QPointF(0, 0);
    
    double h = 0.001;
    
    double fx1 = m_function(x + h, y);
    double fx0 = m_function(x - h, y);
    double fy1 = m_function(x, y + h);
    double fy0 = m_function(x, y - h);
    
    double dx = (fx1 - fx0) / (2 * h);
    double dy = (fy1 - fy0) / (2 * h);
    
    return QPointF(dx, dy);
}

double OptimizationPath3D::evaluateFunction(double x, double y) const
{
    if (!m_function) return 0.0;
    return m_function(x, y);
}

void OptimizationPath3D::addPathPoint(double x, double y)
{
    double z = evaluateFunction(x, y);
    m_path.append({x, y, z});
}

void OptimizationPath3D::clearPath()
{
    m_path.clear();
    
    // Clear 3D items (simplified - in full implementation, would manage custom items)
    for (auto* item : m_pathItems) {
        // m_surface->removeCustomItem(item); // Would need proper custom item management
        delete item;
    }
    m_pathItems.clear();
}

void OptimizationPath3D::updateVisualization()
{
    // In a full implementation, this would add a sphere or line segment to the 3D surface
    // For now, the path is stored and could be visualized separately
    
    // Could create a QScatter3DSeries to show the path as points
    // or custom 3D items to draw lines between consecutive points
}

QString OptimizationPath3D::getOptimizerName() const
{
    switch (m_optimizerType) {
        case SGD: return "SGD";
        case Momentum: return "Momentum";
        case Adam: return "Adam";
        case RMSprop: return "RMSprop";
        default: return "Unknown";
    }
}

QString OptimizationPath3D::getOptimizerDescription() const
{
    switch (m_optimizerType) {
        case SGD:
            return "Basic gradient descent. Updates: θ = θ - α∇f(θ). "
                   "Simple but can be slow and gets stuck in saddle points.";
        
        case Momentum:
            return "Adds velocity to overcome local minima: v = βv - α∇f(θ), θ = θ + v. "
                   "Helps escape saddle points and accelerates convergence.";
        
        case Adam:
            return "Adaptive learning rate with momentum (1st & 2nd moments). "
                   "Combines benefits of Momentum and RMSprop. Usually the best choice for deep learning.";
        
        case RMSprop:
            return "Adapts learning rate per parameter using moving average of squared gradients. "
                   "Good for non-stationary objectives and recurrent networks.";
        
        default:
            return "";
    }
}

void OptimizationPath3D::onStartClicked()
{
    if (m_path.isEmpty()) {
        reset();
    }
    start();
}

void OptimizationPath3D::onPauseClicked()
{
    pause();
}

void OptimizationPath3D::onResetClicked()
{
    reset();
}

void OptimizationPath3D::onStepClicked()
{
    step();
}

void OptimizationPath3D::onOptimizerChanged(int index)
{
    m_optimizerType = static_cast<OptimizerType>(index);
    m_infoLabel->setText(getOptimizerDescription());
    
    // Adjust default learning rates for different optimizers
    switch (m_optimizerType) {
        case SGD:
            m_learningRateSpin->setValue(0.01);
            break;
        case Momentum:
            m_learningRateSpin->setValue(0.01);
            break;
        case Adam:
            m_learningRateSpin->setValue(0.001);
            break;
        case RMSprop:
            m_learningRateSpin->setValue(0.001);
            break;
    }
    
    emit optimizerInfo(getOptimizerDescription());
}
