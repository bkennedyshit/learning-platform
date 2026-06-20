#include "OptimizationVisualizer.h"
#include <QPainter>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QtMath>
#include <QMouseEvent>
#include <cmath>
#include <algorithm>

OptimizationVisualizer::OptimizationVisualizer(QWidget *parent)
    : QWidget(parent)
    , m_currentX(5.0)
    , m_currentY(0.0)
    , m_learningRate(0.1)
    , m_iteration(0)
    , m_isRunning(false)
    , m_velocity(0.0)
    , m_momentum(0.9)
    , m_m(0.0)
    , m_v(0.0)
    , m_t(0)
    , m_xMin(-10.0)
    , m_xMax(10.0)
    , m_yMin(-5.0)
    , m_yMax(50.0)
    , m_algorithm(GradientDescent)
{
    setMinimumSize(800, 600);
    
    // Colors
    m_bgColor = QColor(33, 33, 33);
    m_surfaceColor = QColor(100, 150, 255, 40);
    m_pathColor = QColor(255, 193, 7);  // Amber
    m_pointColor = QColor(244, 67, 54);  // Red
    m_contourColor = QColor(100, 150, 255, 80);
    
    setupUI();
    
    m_animationTimer = new QTimer(this);
    connect(m_animationTimer, &QTimer::timeout, this, &OptimizationVisualizer::updateStep);
}

OptimizationVisualizer::~OptimizationVisualizer() {}

void OptimizationVisualizer::setupUI() {
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(10);
    
    // Top controls
    QGroupBox *controlGroup = new QGroupBox("Optimization Controls", this);
    QVBoxLayout *controlLayout = new QVBoxLayout(controlGroup);
    
    // First row: Function and algorithm selection
    QHBoxLayout *selectionLayout = new QHBoxLayout();
    
    selectionLayout->addWidget(new QLabel("Function:"));
    m_functionPreset = new QComboBox(controlGroup);
    m_functionPreset->addItems({
        "x^2 (Simple Bowl)",
        "x^4 - 4*x^2 (Double Well)",
        "x^3/3 - x (Saddle)",
        "(x-2)^2 + 1 (Shifted Bowl)",
        "sin(x) + x^2/10 (Noisy)"
    });
    selectionLayout->addWidget(m_functionPreset, 1);
    
    selectionLayout->addWidget(new QLabel("Algorithm:"));
    m_algorithmSelector = new QComboBox(controlGroup);
    m_algorithmSelector->addItems({
        "Gradient Descent",
        "Momentum (β=0.9)",
        "Adam Optimizer"
    });
    selectionLayout->addWidget(m_algorithmSelector, 1);
    
    controlLayout->addLayout(selectionLayout);
    
    // Second row: Learning rate
    QHBoxLayout *lrLayout = new QHBoxLayout();
    lrLayout->addWidget(new QLabel("Learning Rate:"));
    
    m_learningRateSlider = new QSlider(Qt::Horizontal, controlGroup);
    m_learningRateSlider->setMinimum(1);
    m_learningRateSlider->setMaximum(100);
    m_learningRateSlider->setValue(10);
    lrLayout->addWidget(m_learningRateSlider, 2);
    
    m_learningRateLabel = new QLabel("α = 0.10", controlGroup);
    m_learningRateLabel->setStyleSheet("font-weight: bold; min-width: 80px;");
    lrLayout->addWidget(m_learningRateLabel);
    
    controlLayout->addLayout(lrLayout);
    
    // Third row: Control buttons
    QHBoxLayout *buttonLayout = new QHBoxLayout();
    
    m_startButton = new QPushButton("▶ Start", controlGroup);
    m_startButton->setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;");
    buttonLayout->addWidget(m_startButton);
    
    m_stopButton = new QPushButton("⏸ Pause", controlGroup);
    m_stopButton->setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 10px;");
    m_stopButton->setEnabled(false);
    buttonLayout->addWidget(m_stopButton);
    
    m_resetButton = new QPushButton("↻ Reset", controlGroup);
    m_resetButton->setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;");
    buttonLayout->addWidget(m_resetButton);
    
    controlLayout->addLayout(buttonLayout);
    
    // Status labels
    QHBoxLayout *statusLayout = new QHBoxLayout();
    
    m_iterationLabel = new QLabel("Iteration: 0", controlGroup);
    m_iterationLabel->setStyleSheet("font-size: 12pt; font-weight: bold; color: #0078d4;");
    statusLayout->addWidget(m_iterationLabel);
    
    statusLayout->addStretch();
    
    m_valueLabel = new QLabel("f(x) = 0.000", controlGroup);
    m_valueLabel->setStyleSheet("font-size: 12pt; font-weight: bold; color: #4CAF50;");
    statusLayout->addWidget(m_valueLabel);
    
    controlLayout->addLayout(statusLayout);
    
    mainLayout->addWidget(controlGroup);
    
    // Visualization area (will be painted)
    mainLayout->addStretch(1);
    
    // Info panel
    QLabel *infoLabel = new QLabel(
        "💡 <b>How it works:</b> Click to set starting point. Watch the optimizer find the minimum! "
        "Try different learning rates to see convergence behavior.",
        this
    );
    infoLabel->setWordWrap(true);
    infoLabel->setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 5px;");
    mainLayout->addWidget(infoLabel);
    
    // Connections
    connect(m_startButton, &QPushButton::clicked, this, &OptimizationVisualizer::startOptimization);
    connect(m_stopButton, &QPushButton::clicked, this, &OptimizationVisualizer::stopOptimization);
    connect(m_resetButton, &QPushButton::clicked, this, &OptimizationVisualizer::resetOptimization);
    connect(m_learningRateSlider, &QSlider::valueChanged, this, &OptimizationVisualizer::onLearningRateChanged);
    connect(m_algorithmSelector, QOverload<int>::of(&QComboBox::currentIndexChanged), 
            this, &OptimizationVisualizer::onAlgorithmChanged);
    connect(m_functionPreset, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &OptimizationVisualizer::onFunctionPresetChanged);
}

void OptimizationVisualizer::setFunction(const QString &function) {
    m_currentFunction = function;
    resetOptimization();
}

void OptimizationVisualizer::startOptimization() {
    m_isRunning = true;
    m_startButton->setEnabled(false);
    m_stopButton->setEnabled(true);
    m_animationTimer->start(50);  // 20 FPS
}

void OptimizationVisualizer::stopOptimization() {
    m_isRunning = false;
    m_startButton->setEnabled(true);
    m_stopButton->setEnabled(false);
    m_animationTimer->stop();
}

void OptimizationVisualizer::resetOptimization() {
    stopOptimization();
    m_currentX = 5.0;
    m_iteration = 0;
    m_velocity = 0.0;
    m_m = 0.0;
    m_v = 0.0;
    m_t = 0;
    m_path.clear();
    m_losses.clear();
    
    m_currentY = evaluateFunction(m_currentX);
    m_path.append(QPointF(m_currentX, m_currentY));
    m_losses.append(m_currentY);
    
    m_iterationLabel->setText("Iteration: 0");
    m_valueLabel->setText(QString("f(x) = %1").arg(m_currentY, 0, 'f', 3));
    
    update();
}

void OptimizationVisualizer::updateStep() {
    // Perform optimization step based on algorithm
    switch (m_algorithm) {
        case GradientDescent:
            performGradientDescentStep();
            break;
        case Momentum:
            performMomentumStep();
            break;
        case Adam:
            performAdamStep();
            break;
    }
    
    m_iteration++;
    m_currentY = evaluateFunction(m_currentX);
    
    m_path.append(QPointF(m_currentX, m_currentY));
    m_losses.append(m_currentY);
    
    // Update UI
    m_iterationLabel->setText(QString("Iteration: %1").arg(m_iteration));
    m_valueLabel->setText(QString("f(x=%1) = %2").arg(m_currentX, 0, 'f', 3).arg(m_currentY, 0, 'f', 3));
    
    update();
    
    // Stop if converged or diverged
    double gradient = std::abs(evaluateDerivative(m_currentX));
    if (gradient < 0.001 || m_iteration > 1000 || std::abs(m_currentX) > 100) {
        stopOptimization();
        
        if (gradient < 0.001) {
            m_valueLabel->setText(m_valueLabel->text() + " ✅ CONVERGED!");
        }
    }
}

void OptimizationVisualizer::performGradientDescentStep() {
    double gradient = evaluateDerivative(m_currentX);
    m_currentX -= m_learningRate * gradient;
}

void OptimizationVisualizer::performMomentumStep() {
    double gradient = evaluateDerivative(m_currentX);
    m_velocity = m_momentum * m_velocity - m_learningRate * gradient;
    m_currentX += m_velocity;
}

void OptimizationVisualizer::performAdamStep() {
    double gradient = evaluateDerivative(m_currentX);
    
    m_t++;
    
    // Update biased first moment estimate
    m_m = 0.9 * m_m + 0.1 * gradient;
    
    // Update biased second moment estimate
    m_v = 0.999 * m_v + 0.001 * gradient * gradient;
    
    // Compute bias-corrected estimates
    double m_hat = m_m / (1 - std::pow(0.9, m_t));
    double v_hat = m_v / (1 - std::pow(0.999, m_t));
    
    // Update parameters
    m_currentX -= m_learningRate * m_hat / (std::sqrt(v_hat) + 1e-8);
}

void OptimizationVisualizer::onLearningRateChanged(int value) {
    m_learningRate = value / 100.0;
    m_learningRateLabel->setText(QString("α = %1").arg(m_learningRate, 0, 'f', 2));
}

void OptimizationVisualizer::onAlgorithmChanged(int index) {
    m_algorithm = static_cast<Algorithm>(index);
    resetOptimization();
}

void OptimizationVisualizer::onFunctionPresetChanged(int index) {
    QStringList functions = {
        "x^2",
        "x^4 - 4*x^2",
        "x^3/3 - x",
        "(x-2)^2 + 1",
        "sin(x) + x^2/10"
    };
    
    if (index >= 0 && index < functions.size()) {
        m_currentFunction = functions[index];
        resetOptimization();
    }
}

double OptimizationVisualizer::evaluateFunction(double x) {
    // Evaluate based on current function preset
    int preset = m_functionPreset->currentIndex();
    
    switch (preset) {
        case 0:  // x^2
            return x * x;
        case 1:  // x^4 - 4*x^2
            return x*x*x*x - 4*x*x;
        case 2:  // x^3/3 - x
            return x*x*x/3.0 - x;
        case 3:  // (x-2)^2 + 1
            return (x-2)*(x-2) + 1;
        case 4:  // sin(x) + x^2/10
            return std::sin(x) + x*x/10.0;
        default:
            return x * x;
    }
}

double OptimizationVisualizer::evaluateDerivative(double x) {
    int preset = m_functionPreset->currentIndex();
    
    switch (preset) {
        case 0:  // 2x
            return 2 * x;
        case 1:  // 4x^3 - 8x
            return 4*x*x*x - 8*x;
        case 2:  // x^2 - 1
            return x*x - 1;
        case 3:  // 2(x-2)
            return 2*(x-2);
        case 4:  // cos(x) + x/5
            return std::cos(x) + x/5.0;
        default:
            return 2 * x;
    }
}

void OptimizationVisualizer::paintEvent(QPaintEvent *event) {
    Q_UNUSED(event);
    
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Draw background
    painter.fillRect(rect(), m_bgColor);
    
    // Calculate drawing area (leave space for controls)
    int drawTop = 200;  // Space for controls
    int drawBottom = height() - 60;  // Space for info
    int drawHeight = drawBottom - drawTop;
    
    // Draw contours and surface
    drawSurface(painter);
    drawContours(painter);
    
    // Draw optimization path
    if (!m_path.isEmpty()) {
        drawGradientPath(painter);
        drawCurrentPoint(painter);
    }
    
    drawInfo(painter);
}

void OptimizationVisualizer::drawSurface(QPainter &painter) {
    int drawTop = 200;
    int drawBottom = height() - 60;
    
    // Draw function curve
    QPainterPath path;
    bool first = true;
    
    for (int screenX = 0; screenX < width(); screenX += 2) {
        double x = m_xMin + (screenX / (double)width()) * (m_xMax - m_xMin);
        double y = evaluateFunction(x);
        
        if (y >= m_yMin && y <= m_yMax) {
            int screenY = drawTop + (int)((m_yMax - y) / (m_yMax - m_yMin) * (drawBottom - drawTop));
            
            if (first) {
                path.moveTo(screenX, screenY);
                first = false;
            } else {
                path.lineTo(screenX, screenY);
            }
        }
    }
    
    // Fill under curve
    QPainterPath fillPath = path;
    fillPath.lineTo(width(), drawBottom);
    fillPath.lineTo(0, drawBottom);
    fillPath.closeSubpath();
    
    painter.fillPath(fillPath, m_surfaceColor);
    painter.setPen(QPen(QColor(100, 150, 255), 2));
    painter.drawPath(path);
}

void OptimizationVisualizer::drawContours(QPainter &painter) {
    // Draw horizontal lines at different function values
    painter.setPen(QPen(m_contourColor, 1, Qt::DashLine));
    
    int drawTop = 200;
    int drawBottom = height() - 60;
    
    for (double y = 0; y <= m_yMax; y += 10) {
        if (y >= m_yMin && y <= m_yMax) {
            int screenY = drawTop + (int)((m_yMax - y) / (m_yMax - m_yMin) * (drawBottom - drawTop));
            painter.drawLine(0, screenY, width(), screenY);
            
            painter.setPen(QColor(150, 150, 150));
            painter.drawText(5, screenY - 2, QString::number(y, 'f', 0));
            painter.setPen(QPen(m_contourColor, 1, Qt::DashLine));
        }
    }
}

void OptimizationVisualizer::drawGradientPath(QPainter &painter) {
    if (m_path.size() < 2) return;
    
    int drawTop = 200;
    int drawBottom = height() - 60;
    
    // Draw path with gradient colors
    for (int i = 0; i < m_path.size() - 1; ++i) {
        QPointF p1 = m_path[i];
        QPointF p2 = m_path[i + 1];
        
        int x1 = (int)((p1.x() - m_xMin) / (m_xMax - m_xMin) * width());
        int y1 = drawTop + (int)((m_yMax - p1.y()) / (m_yMax - m_yMin) * (drawBottom - drawTop));
        
        int x2 = (int)((p2.x() - m_xMin) / (m_xMax - m_xMin) * width());
        int y2 = drawTop + (int)((m_yMax - p2.y()) / (m_yMax - m_yMin) * (drawBottom - drawTop));
        
        // Color fades from start to end
        int alpha = 100 + (155 * i) / m_path.size();
        QColor lineColor = m_pathColor;
        lineColor.setAlpha(alpha);
        
        painter.setPen(QPen(lineColor, 3));
        painter.drawLine(x1, y1, x2, y2);
        
        // Draw small circles at each step
        painter.setBrush(lineColor);
        painter.drawEllipse(QPoint(x1, y1), 4, 4);
    }
}

void OptimizationVisualizer::drawCurrentPoint(QPainter &painter) {
    if (m_path.isEmpty()) return;
    
    int drawTop = 200;
    int drawBottom = height() - 60;
    
    QPointF current = m_path.last();
    
    int x = (int)((current.x() - m_xMin) / (m_xMax - m_xMin) * width());
    int y = drawTop + (int)((m_yMax - current.y()) / (m_yMax - m_yMin) * (drawBottom - drawTop));
    
    // Draw pulsing point
    painter.setPen(QPen(Qt::white, 3));
    painter.setBrush(m_pointColor);
    int radius = m_isRunning ? 8 + (m_iteration % 10) : 8;
    painter.drawEllipse(QPoint(x, y), radius, radius);
    
    // Draw label
    painter.setPen(Qt::white);
    painter.setFont(QFont("Arial", 10, QFont::Bold));
    QString label = QString("x=%1").arg(current.x(), 0, 'f', 2);
    painter.drawText(x + 15, y - 10, label);
}

void OptimizationVisualizer::drawInfo(QPainter &painter) {
    // Draw algorithm info
    painter.setPen(Qt::white);
    painter.setFont(QFont("Arial", 10));
    
   int y = height() - 40;
    
    QString algoName[] = {"Gradient Descent", "Momentum", "Adam"};
    QString info = QString("Algorithm: %1 | Learning Rate: %2 | Steps: %3")
                      .arg(algoName[m_algorithm])
                      .arg(m_learningRate, 0, 'f', 2)
                      .arg(m_path.size());
    
    painter.drawText(10, y, info);
}

void OptimizationVisualizer::mousePressEvent(QMouseEvent *event) {
    if (event->button() == Qt::LeftButton && event->pos().y() > 200) {
        // Set new starting point
        int drawTop = 200;
        int drawBottom = height() - 60;
        
        double x = m_xMin + (event->pos().x() / (double)width()) * (m_xMax - m_xMin);
        double y = m_yMax - ((event->pos().y() - drawTop) / (double)(drawBottom - drawTop)) * (m_yMax - m_yMin);
        
        stopOptimization();
        m_currentX = x;
        m_iteration = 0;
        m_velocity = 0.0;
        m_m = 0.0;
        m_v = 0.0;
        m_t = 0;
        m_path.clear();
        m_losses.clear();
        
        m_currentY = evaluateFunction(m_currentX);
        m_path.append(QPointF(m_currentX, m_currentY));
        m_losses.append(m_currentY);
        
        update();
    }
}

QPointF OptimizationVisualizer::worldToScreen(const QPointF &worldPoint) const {
    int drawTop = 200;
    int drawBottom = height() - 60;
    
    double sx = (worldPoint.x() - m_xMin) / (m_xMax - m_xMin) * width();
    double sy = drawTop + (m_yMax - worldPoint.y()) / (m_yMax - m_yMin) * (drawBottom - drawTop);
    return QPointF(sx, sy);
}

QPointF OptimizationVisualizer::screenToWorld(const QPointF &screenPoint) const {
    int drawTop = 200;
    int drawBottom = height() - 60;
    
    double wx = m_xMin + (screenPoint.x() / width()) * (m_xMax - m_xMin);
    double wy = m_yMax - ((screenPoint.y() - drawTop) / (drawBottom - drawTop)) * (m_yMax - m_yMin);
    return QPointF(wx, wy);
}
