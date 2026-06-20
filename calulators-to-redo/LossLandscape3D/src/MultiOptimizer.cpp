#include "MultiOptimizer.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QLabel>
#include <QHeaderView>
#include <QPainter>
#include <QPainterPath>
#include <cmath>
#include <random>

MultiOptimizer::MultiOptimizer(QWidget *parent)
    : QWidget(parent)
    , m_animationTimer(new QTimer(this))
{
    setupUI();
    setupDefaultOptimizers();
    
    connect(m_animationTimer, &QTimer::timeout,
            this, &MultiOptimizer::onAnimationStep);
}

void MultiOptimizer::setupUI()
{
    QVBoxLayout* mainLayout = new QVBoxLayout(this);
    
    // Top controls
    QGroupBox* controlBox = new QGroupBox("Multi-Optimizer Race Controls");
    QHBoxLayout* controlLayout = new QHBoxLayout(controlBox);
    
    m_startButton = new QPushButton("Start Race");
    m_pauseButton = new QPushButton("Pause");
    m_pauseButton->setEnabled(false);
    m_resetButton = new QPushButton("Reset");
    m_stepButton = new QPushButton("Step");
    m_randomStartsButton = new QPushButton("Random Starts");
    
    controlLayout->addWidget(m_startButton);
    controlLayout->addWidget(m_pauseButton);
    controlLayout->addWidget(m_resetButton);
    controlLayout->addWidget(m_stepButton);
    controlLayout->addWidget(m_randomStartsButton);
    
    controlLayout->addWidget(new QLabel("Max Iterations:"));
    m_maxIterSpin = new QSpinBox();
    m_maxIterSpin->setRange(10, 10000);
    m_maxIterSpin->setValue(1000);
    controlLayout->addWidget(m_maxIterSpin);
    
    controlLayout->addWidget(new QLabel("Speed (ms):"));
    m_speedSpin = new QSpinBox();
    m_speedSpin->setRange(10, 1000);
    m_speedSpin->setValue(100);
    controlLayout->addWidget(m_speedSpin);
    
    m_showPathsCheck = new QCheckBox("Show Paths");
    m_showPathsCheck->setChecked(true);
    controlLayout->addWidget(m_showPathsCheck);
    
    mainLayout->addWidget(controlBox);
    
    // Canvas for visualization
    m_canvas = new QWidget();
    m_canvas->setMinimumSize(600, 400);
    m_canvas->setStyleSheet("background-color: white; border: 1px solid black;");
    mainLayout->addWidget(m_canvas, 1);
    
    // Table for optimizer stats
    m_table = new QTableWidget();
    m_table->setColumnCount(7);
    m_table->setHorizontalHeaderLabels({
        "Enabled", "Optimizer", "Color", "Position (x, y)", "Loss", "Iterations", "Status"
    });
    m_table->horizontalHeader()->setStretchLastSection(true);
    m_table->setMaximumHeight(200);
    mainLayout->addWidget(m_table);
    
    // Connect signals
    connect(m_startButton, &QPushButton::clicked,
            this, &MultiOptimizer::onStartClicked);
    connect(m_pauseButton, &QPushButton::clicked,
            this, &MultiOptimizer::onPauseClicked);
    connect(m_resetButton, &QPushButton::clicked,
            this, &MultiOptimizer::onResetClicked);
    connect(m_stepButton, &QPushButton::clicked,
            this, &MultiOptimizer::onStepClicked);
    connect(m_randomStartsButton, &QPushButton::clicked, [this]() {
        setRandomStartPoints(6);
        reset();
    });
    
    connect(m_showPathsCheck, &QCheckBox::toggled, [this](bool checked) {
        m_showPaths = checked;
        update();
    });
    
    connect(m_table, &QTableWidget::cellChanged,
            this, &MultiOptimizer::onOptimizerToggled);
}

void MultiOptimizer::setupDefaultOptimizers()
{
    // Create 6 optimizers with different colors and starting positions
    QVector<OptimizerConfig> defaults = {
        {"SGD", SGD, QColor(255, 0, 0), 0.01, true, -3.0, 2.0},
        {"Momentum", Momentum, QColor(0, 150, 255), 0.01, true, 3.0, 2.0},
        {"Adam", Adam, QColor(0, 200, 0), 0.001, true, -3.0, -2.0},
        {"RMSprop", RMSprop, QColor(255, 165, 0), 0.001, true, 3.0, -2.0},
        {"Adagrad", Adagrad, QColor(148, 0, 211), 0.01, true, 0.0, 3.0},
        {"Adadelta", Adadelta, QColor(255, 20, 147), 0.1, true, 0.0, -3.0}
    };
    
    for (auto& config : defaults) {
        config.currentX = config.startX;
        config.currentY = config.startY;
        config.iterations = 0;
        config.converged = false;
        addOptimizer(config);
    }
    
    updateTable();
}

void MultiOptimizer::setLossFunction(LossFunction func)
{
    m_function = func;
    
    // Recalculate all losses
    for (auto& opt : m_optimizers) {
        opt.currentLoss = evaluateFunction(opt.currentX, opt.currentY);
    }
    
    updateTable();
    update();
}

void MultiOptimizer::setBounds(double minX, double maxX, double minY, double maxY)
{
    m_minX = minX;
    m_maxX = maxX;
    m_minY = minY;
    m_maxY = maxY;
    update();
}

void MultiOptimizer::addOptimizer(const OptimizerConfig& config)
{
    OptimizerConfig opt = config;
    opt.currentLoss = evaluateFunction(opt.currentX, opt.currentY);
    opt.path.append(QPointF(opt.currentX, opt.currentY));
    m_optimizers.append(opt);
}

void MultiOptimizer::setRandomStartPoints(int count)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> distX(m_minX * 0.8, m_maxX * 0.8);
    std::uniform_real_distribution<> distY(m_minY * 0.8, m_maxY * 0.8);
    
    // Only update starting positions, keep optimizer types
    int actualCount = std::min(count, m_optimizers.size());
    for (int i = 0; i < actualCount; ++i) {
        m_optimizers[i].startX = distX(gen);
        m_optimizers[i].startY = distY(gen);
    }
}

void MultiOptimizer::clearAll()
{
    m_optimizers.clear();
    updateTable();
    update();
}

void MultiOptimizer::startRace()
{
    if (!m_function) return;
    
    m_isRunning = true;
    m_startButton->setEnabled(false);
    m_pauseButton->setEnabled(true);
    m_stepButton->setEnabled(false);
    m_randomStartsButton->setEnabled(false);
    
    m_maxIterations = m_maxIterSpin->value();
    m_animationSpeed = m_speedSpin->value();
    m_animationTimer->start(m_animationSpeed);
    
    emit statusUpdate("Race started!");
}

void MultiOptimizer::pause()
{
    m_isRunning = false;
    m_animationTimer->stop();
    
    m_startButton->setEnabled(true);
    m_pauseButton->setEnabled(false);
    m_stepButton->setEnabled(true);
    m_randomStartsButton->setEnabled(true);
    
    emit statusUpdate("Paused");
}

void MultiOptimizer::reset()
{
    pause();
    
    for (auto& opt : m_optimizers) {
        opt.currentX = opt.startX;
        opt.currentY = opt.startY;
        opt.currentLoss = evaluateFunction(opt.currentX, opt.currentY);
        opt.iterations = 0;
        opt.converged = false;
        
        // Reset optimizer state
        opt.velocityX = opt.velocityY = 0.0;
        opt.m_x = opt.m_y = 0.0;
        opt.v_x = opt.v_y = 0.0;
        opt.cache_x = opt.cache_y = 0.0;
        
        opt.path.clear();
        opt.path.append(QPointF(opt.currentX, opt.currentY));
    }
    
    updateTable();
    update();
    emit statusUpdate("Reset to starting positions");
}

void MultiOptimizer::stepAll()
{
    for (auto& opt : m_optimizers) {
        if (opt.enabled && !opt.converged && opt.iterations < m_maxIterations) {
            performOptimizationStep(opt);
        }
    }
    
    updateTable();
    update();
}

void MultiOptimizer::onAnimationStep()
{
    stepAll();
    
    // Check if all enabled optimizers have finished
    bool allFinished = true;
    for (const auto& opt : m_optimizers) {
        if (opt.enabled && !opt.converged && opt.iterations < m_maxIterations) {
            allFinished = false;
            break;
        }
    }
    
    if (allFinished) {
        pause();
        
        // Find winner (lowest loss)
        double bestLoss = std::numeric_limits<double>::max();
        QString winner;
        for (const auto& opt : m_optimizers) {
            if (opt.enabled && opt.currentLoss < bestLoss) {
                bestLoss = opt.currentLoss;
                winner = opt.name;
            }
        }
        
        emit raceFinished(winner);
        emit statusUpdate("Race finished! Winner: " + winner + 
                         QString(" (Loss: %1)").arg(bestLoss, 0, 'f', 6));
    }
}

void MultiOptimizer::performOptimizationStep(OptimizerConfig& opt)
{
    QPointF grad = computeGradient(opt.currentX, opt.currentY);
    double gx = grad.x();
    double gy = grad.y();
    
    double dx = 0.0, dy = 0.0;
    
    switch (opt.type) {
        case SGD:
            dx = -opt.learningRate * gx;
            dy = -opt.learningRate * gy;
            break;
        
        case Momentum:
            opt.velocityX = opt.momentum * opt.velocityX - opt.learningRate * gx;
            opt.velocityY = opt.momentum * opt.velocityY - opt.learningRate * gy;
            dx = opt.velocityX;
            dy = opt.velocityY;
            break;
        
        case Adam: {
            int t = opt.iterations + 1;
            
            opt.m_x = opt.beta1 * opt.m_x + (1 - opt.beta1) * gx;
            opt.m_y = opt.beta1 * opt.m_y + (1 - opt.beta1) * gy;
            
            opt.v_x = opt.beta2 * opt.v_x + (1 - opt.beta2) * gx * gx;
            opt.v_y = opt.beta2 * opt.v_y + (1 - opt.beta2) * gy * gy;
            
            double m_x_hat = opt.m_x / (1 - std::pow(opt.beta1, t));
            double m_y_hat = opt.m_y / (1 - std::pow(opt.beta1, t));
            double v_x_hat = opt.v_x / (1 - std::pow(opt.beta2, t));
            double v_y_hat = opt.v_y / (1 - std::pow(opt.beta2, t));
            
            dx = -opt.learningRate * m_x_hat / (std::sqrt(v_x_hat) + opt.epsilon);
            dy = -opt.learningRate * m_y_hat / (std::sqrt(v_y_hat) + opt.epsilon);
            break;
        }
        
        case RMSprop:
            opt.cache_x = opt.rho * opt.cache_x + (1 - opt.rho) * gx * gx;
            opt.cache_y = opt.rho * opt.cache_y + (1 - opt.rho) * gy * gy;
            
            dx = -opt.learningRate * gx / (std::sqrt(opt.cache_x) + opt.epsilon);
            dy = -opt.learningRate * gy / (std::sqrt(opt.cache_y) + opt.epsilon);
            break;
        
        case Adagrad:
            opt.cache_x += gx * gx;
            opt.cache_y += gy * gy;
            
            dx = -opt.learningRate * gx / (std::sqrt(opt.cache_x) + opt.epsilon);
            dy = -opt.learningRate * gy / (std::sqrt(opt.cache_y) + opt.epsilon);
            break;
        
        case Adadelta: {
            double rho = 0.95;
            
            // Accumulate gradient
            opt.cache_x = rho * opt.cache_x + (1 - rho) * gx * gx;
            opt.cache_y = rho * opt.cache_y + (1 - rho) * gy * gy;
            
            // Compute update
            dx = -std::sqrt(opt.v_x + opt.epsilon) / std::sqrt(opt.cache_x + opt.epsilon) * gx;
            dy = -std::sqrt(opt.v_y + opt.epsilon) / std::sqrt(opt.cache_y + opt.epsilon) * gy;
            
            // Accumulate updates
            opt.v_x = rho * opt.v_x + (1 - rho) * dx * dx;
            opt.v_y = rho * opt.v_y + (1 - rho) * dy * dy;
            break;
        }
    }
    
    // Update position
    opt.currentX += dx;
    opt.currentY += dy;
    opt.iterations++;
    
    // Evaluate new loss
    opt.currentLoss = evaluateFunction(opt.currentX, opt.currentY);
    
    // Add to path
    opt.path.append(QPointF(opt.currentX, opt.currentY));
    
    // Check convergence
    double gradMag = std::sqrt(gx * gx + gy * gy);
    if (gradMag < m_convergenceThreshold) {
        opt.converged = true;
    }
    
    emit iterationCompleted(m_optimizers.indexOf(opt));
}

QPointF MultiOptimizer::computeGradient(double x, double y) const
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

double MultiOptimizer::evaluateFunction(double x, double y) const
{
    if (!m_function) return 0.0;
    return m_function(x, y);
}

void MultiOptimizer::updateTable()
{
    m_table->setRowCount(m_optimizers.size());
    
    for (int i = 0; i < m_optimizers.size(); ++i) {
        const auto& opt = m_optimizers[i];
        
        // Enabled checkbox
        QTableWidgetItem* enabledItem = new QTableWidgetItem();
        enabledItem->setCheckState(opt.enabled ? Qt::Checked : Qt::Unchecked);
        m_table->setItem(i, 0, enabledItem);
        
        // Optimizer name
        m_table->setItem(i, 1, new QTableWidgetItem(opt.name));
        
        // Color indicator
        QTableWidgetItem* colorItem = new QTableWidgetItem();
        colorItem->setBackground(opt.color);
        m_table->setItem(i, 2, colorItem);
        
        // Position
        QString posStr = QString("(%1, %2)")
            .arg(opt.currentX, 0, 'f', 3)
            .arg(opt.currentY, 0, 'f', 3);
        m_table->setItem(i, 3, new QTableWidgetItem(posStr));
        
        // Loss
        QString lossStr = QString::number(opt.currentLoss, 'f', 6);
        m_table->setItem(i, 4, new QTableWidgetItem(lossStr));
        
        // Iterations
        m_table->setItem(i, 5, new QTableWidgetItem(QString::number(opt.iterations)));
        
        // Status
        QString status = opt.converged ? "✓ Converged" : 
                        (opt.iterations >= m_maxIterations ? "Max Iter" : "Running");
        m_table->setItem(i, 6, new QTableWidgetItem(status));
    }
}

void MultiOptimizer::paintEvent(QPaintEvent* event)
{
    QWidget::paintEvent(event);
    
    QPainter painter(m_canvas);
    painter.setRenderHint(QPainter::Antialiasing);
    
    drawStartPoints(painter);
    
    if (m_showPaths) {
        drawPaths(painter);
    }
    
    // Draw current positions
    for (const auto& opt : m_optimizers) {
        if (!opt.enabled) continue;
        
        QPoint pos = worldToScreen(opt.currentX, opt.currentY);
        
        painter.setPen(QPen(opt.color, 2));
        painter.setBrush(opt.color);
        painter.drawEllipse(pos, 6, 6);
        
        // Draw label
        painter.setPen(opt.color);
        QFont font = painter.font();
        font.setPointSize(8);
        font.setBold(true);
        painter.setFont(font);
        painter.drawText(pos.x() + 10, pos.y() - 5, opt.name);
    }
}

void MultiOptimizer::drawPaths(QPainter& painter)
{
    for (const auto& opt : m_optimizers) {
        if (!opt.enabled || opt.path.size() < 2) continue;
        
        QPainterPath path;
        QPoint start = worldToScreen(opt.path[0].x(), opt.path[0].y());
        path.moveTo(start);
        
        for (int i = 1; i < opt.path.size(); ++i) {
            QPoint pt = worldToScreen(opt.path[i].x(), opt.path[i].y());
            path.lineTo(pt);
        }
        
        painter.setPen(QPen(opt.color, 2, Qt::SolidLine));
        painter.drawPath(path);
    }
}

void MultiOptimizer::drawStartPoints(QPainter& painter)
{
    for (const auto& opt : m_optimizers) {
        if (!opt.enabled) continue;
        
        QPoint pos = worldToScreen(opt.startX, opt.startY);
        
        painter.setPen(QPen(opt.color, 2, Qt::DashLine));
        painter.setBrush(Qt::white);
        painter.drawEllipse(pos, 4, 4);
    }
}

QPoint MultiOptimizer::worldToScreen(double x, double y) const
{
    int width = m_canvas->width();
    int height = m_canvas->height();
    
    double worldWidth = m_maxX - m_minX;
    double worldHeight = m_maxY - m_minY;
    
    int screenX = ((x - m_minX) / worldWidth) * width;
    int screenY = ((m_maxY - y) / worldHeight) * height;
    
    return QPoint(screenX, screenY);
}

QPointF MultiOptimizer::screenToWorld(const QPoint& screen) const
{
    int width = m_canvas->width();
    int height = m_canvas->height();
    
    double worldWidth = m_maxX - m_minX;
    double worldHeight = m_maxY - m_minY;
    
    double x = m_minX + (screen.x() / (double)width) * worldWidth;
    double y = m_maxY - (screen.y() / (double)height) * worldHeight;
    
    return QPointF(x, y);
}

QString MultiOptimizer::getOptimizerStats(const OptimizerConfig& opt) const
{
    return QString("%1: Iter=%2, Loss=%3, Pos=(%4, %5)")
        .arg(opt.name)
        .arg(opt.iterations)
        .arg(opt.currentLoss, 0, 'f', 6)
        .arg(opt.currentX, 0, 'f', 3)
        .arg(opt.currentY, 0, 'f', 3);
}

void MultiOptimizer::onStartClicked()
{
    startRace();
}

void MultiOptimizer::onPauseClicked()
{
    pause();
}

void MultiOptimizer::onResetClicked()
{
    reset();
}

void MultiOptimizer::onStepClicked()
{
    stepAll();
}

void MultiOptimizer::onOptimizerToggled(int row, int column)
{
    if (column == 0 && row < m_optimizers.size()) {
        QTableWidgetItem* item = m_table->item(row, 0);
        m_optimizers[row].enabled = (item->checkState() == Qt::Checked);
        update();
    }
}
