#include "TangentLineWidget.h"
#include <QPainter>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QCheckBox>
#include <QTimer>
#include <QtMath>
#include <QMouseEvent>
#include <cmath>

TangentLineWidget::TangentLineWidget(QWidget *parent)
    : QWidget(parent)
    , m_tangentX(0.0)
    , m_tangentY(0.0)
    , m_slope(0.0)
    , m_showNormal(false)
    , m_showSecant(false)
    , m_showGrid(true)
    , m_isAnimating(false)
    , m_xMin(-10.0)
    , m_xMax(10.0)
    , m_yMin(-10.0)
    , m_yMax(10.0)
    , m_secantX2(1.0)
{
    setMinimumSize(700, 500);
    
    // Colors
    m_bgColor = QColor(33, 33, 33);
    m_gridColor = QColor(60, 60, 60);
    m_axisColor = QColor(200, 200, 200);
    m_functionColor = QColor(0, 136, 255);
    m_tangentColor = QColor(255, 87, 34);  // Deep Orange
    m_normalColor = QColor(156, 39, 176);  // Purple
    m_secantColor = QColor(255, 235, 59);  // Yellow
    m_pointColor = QColor(76, 175, 80);    // Green
    
    setupUI();
    
    m_animationTimer = new QTimer(this);
    connect(m_animationTimer, &QTimer::timeout, this, &TangentLineWidget::updateAnimation);
}

TangentLineWidget::~TangentLineWidget() {}

void TangentLineWidget::setupUI() {
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(10);
    
    // Visualization area takes most space
    mainLayout->addStretch(1);
    
    // Controls at bottom
    QGroupBox *controlGroup = new QGroupBox("Tangent Line Controls", this);
    QVBoxLayout *controlLayout = new QVBoxLayout(controlGroup);
    
    // X position slider
    QHBoxLayout *sliderLayout = new QHBoxLayout();
    sliderLayout->addWidget(new QLabel("x position:"));
    
    m_xSlider = new QSlider(Qt::Horizontal, controlGroup);
    m_xSlider->setMinimum(-100);
    m_xSlider->setMaximum(100);
    m_xSlider->setValue(0);
    sliderLayout->addWidget(m_xSlider, 3);
    
    m_xLabel = new QLabel("x = 0.00", controlGroup);
    m_xLabel->setStyleSheet("font-weight: bold; min-width: 80px;");
    sliderLayout->addWidget(m_xLabel);
    
    controlLayout->addLayout(sliderLayout);
    
    // Display options
    QHBoxLayout *optionsLayout = new QHBoxLayout();
    
    QCheckBox *normalCheck = new QCheckBox("Show Normal Line", controlGroup);
    connect(normalCheck, &QCheckBox::toggled, this, [this](bool checked) {
        m_showNormal = checked;
        update();
    });
    optionsLayout->addWidget(normalCheck);
    
    QCheckBox *secantCheck = new QCheckBox("Show Secant Line", controlGroup);
    connect(secantCheck, &QCheckBox::toggled, this, [this](bool checked) {
        m_showSecant = checked;
        update();
    });
    optionsLayout->addWidget(secantCheck);
    
    m_animateButton = new QPushButton("▶ Animate", controlGroup);
    m_animateButton->setCheckable(true);
    m_animateButton->setStyleSheet("padding: 8px 16px; font-weight: bold;");
    optionsLayout->addWidget(m_animateButton);
    
    optionsLayout->addStretch();
    
    controlLayout->addLayout(optionsLayout);
    
    // Info display
    QHBoxLayout *infoLayout = new QHBoxLayout();
    
    m_slopeLabel = new QLabel("Slope: m = 0.00", controlGroup);
    m_slopeLabel->setStyleSheet("font-size: 12pt; font-weight: bold; color: #FF5722;");
    infoLayout->addWidget(m_slopeLabel);
    
    infoLayout->addStretch();
    
    m_equationLabel = new QLabel("y = 0.00x + 0.00", controlGroup);
    m_equationLabel->setStyleSheet("font-size: 12pt; font-weight: bold; color: #4CAF50;");
    infoLayout->addWidget(m_equationLabel);
    
    controlLayout->addLayout(infoLayout);
    
    mainLayout->addWidget(controlGroup);
    
    // Instruction label
    QLabel *instructionLabel = new QLabel(
        "💡 <b>Click on the graph</b> to place tangent line or use the slider. "
        "Watch how the slope changes as you move along the curve!",
        this
    );
    instructionLabel->setWordWrap(true);
    instructionLabel->setStyleSheet("background-color: #2d2d2d; padding: 8px; border-radius: 5px;");
    mainLayout->addWidget(instructionLabel);
    
    // Connections
    connect(m_xSlider, &QSlider::valueChanged, this, &TangentLineWidget::onXSliderChanged);
    connect(m_animateButton, &QPushButton::toggled, this, &TangentLineWidget::onAnimationToggled);
}

void TangentLineWidget::setFunction(const QString &function) {
    m_currentFunction = function;
    calculateFunctionPoints();
    
    // Reset tangent point
    m_tangentX = 0.0;
    m_tangentY = evaluateFunction(m_tangentX);
    m_slope = evaluateDerivative(m_tangentX);
    
    updateLabels();
    update();
}

void TangentLineWidget::resetView() {
    m_xMin = -10.0;
    m_xMax = 10.0;
    m_yMin = -10.0;
    m_yMax = 10.0;
    calculateFunctionPoints();
    update();
}

void TangentLineWidget::setGridVisible(bool visible) {
    m_showGrid = visible;
    update();
}

void TangentLineWidget::calculateFunctionPoints() {
    m_functionPoints.clear();
    
    if (m_currentFunction.isEmpty()) return;
    
    int numPoints = width() * 2;
    double step = (m_xMax - m_xMin) / numPoints;
    
    for (int i = 0; i < numPoints; ++i) {
        double x = m_xMin + i * step;
        double y = evaluateFunction(x);
        
        if (std::isfinite(y) && y > -1e6 && y < 1e6) {
            m_functionPoints.append(QPointF(x, y));
        }
    }
}

double TangentLineWidget::evaluateFunction(double x) {
    // Simple expression evaluator (same as GraphWidget)
    QString f = m_currentFunction.toLower();
    
    if (f == "x^2") return x * x;
    if (f == "x^3") return x * x * x;
    if (f == "x^4") return x * x * x * x;
    if (f.contains("x^3") && f.contains("-")) return x*x*x - 2*x;
    if (f == "sin(x)") return std::sin(x);
    if (f == "cos(x)") return std::cos(x);
    if (f.contains("exp(-x^2)")) return std::exp(-x*x);
    if (f.contains("x^4") && f.contains("4*x^2")) return x*x*x*x - 4*x*x;
    if (f.contains("1/(1+exp(-x))")) return 1.0 / (1.0 + std::exp(-x));
    if (f.contains("x^3/3")) return x*x*x/3.0 - x;
    if (f == "log(x)" && x > 0) return std::log(x);
    if (f == "sqrt(x)" && x >= 0) return std::sqrt(x);
    
    // Default to x^2
    return x * x;
}

double TangentLineWidget::evaluateDerivative(double x) {
    QString f = m_currentFunction.toLower();
    
    if (f == "x^2") return 2 * x;
    if (f == "x^3") return 3 * x * x;
    if (f == "x^4") return 4 * x * x * x;
    if (f.contains("x^3") && f.contains("-")) return 3*x*x - 2;
    if (f == "sin(x)") return std::cos(x);
    if (f == "cos(x)") return -std::sin(x);
    if (f.contains("exp(-x^2)")) return -2*x*std::exp(-x*x);
    if (f.contains("x^4") && f.contains("4*x^2")) return 4*x*x*x - 8*x;
    if (f.contains("1/(1+exp(-x))")) {
        double ex = std::exp(-x);
        return ex / ((1 + ex) * (1 + ex));
    }
    if (f.contains("x^3/3")) return x*x - 1;
    if (f == "log(x)" && x > 0) return 1.0 / x;
    if (f == "sqrt(x)" && x > 0) return 1.0 / (2 * std::sqrt(x));
    
    return 2 * x;
}

void TangentLineWidget::updateLabels() {
    m_xLabel->setText(QString("x = %1").arg(m_tangentX, 0, 'f', 2));
    m_slopeLabel->setText(QString("Slope: m = %1").arg(m_slope, 0, 'f', 3));
    
    // Tangent line equation: y - y0 = m(x - x0)
    // Rearranged: y = mx - mx0 + y0
    double b = m_tangentY - m_slope * m_tangentX;
    
    QString equation;
    if (b >= 0) {
        equation = QString("y = %1x + %2").arg(m_slope, 0, 'f', 2).arg(b, 0, 'f', 2);
    } else {
        equation = QString("y = %1x - %2").arg(m_slope, 0, 'f', 2).arg(-b, 0, 'f', 2);
    }
    m_equationLabel->setText(equation);
}

void TangentLineWidget::paintEvent(QPaintEvent *event) {
    Q_UNUSED(event);
    
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    // Calculate drawing area
    int drawTop = 20;
    int drawBottom = height() - 200;  // Leave space for controls
    int drawHeight = drawBottom - drawTop;
    
    // Background
    QRect drawRect(0, drawTop, width(), drawHeight);
    painter.fillRect(drawRect, m_bgColor);
    
    // Set clip region
    painter.setClipRect(drawRect);
    
    // Draw components
    if (m_showGrid) {
        drawGrid(painter);
    }
    drawAxes(painter);
    
    if (!m_functionPoints.isEmpty()) {
        drawFunction(painter);
    }
    
    if (m_showSecant) {
        drawSecantLine(painter);
    }
    
    drawTangentLine(painter);
    
    if (m_showNormal) {
        drawNormalLine(painter);
    }
    
    // Reset clip
    painter.setClipRect(rect());
    
    drawTangentInfo(painter);
}

void TangentLineWidget::drawGrid(QPainter &painter) {
    painter.setPen(QPen(m_gridColor, 1));
    
    int drawTop = 20;
    int drawBottom = height() - 200;
    
    double xRange = m_xMax - m_xMin;
    double yRange = m_yMax - m_yMin;
    
    double xStep = std::pow(10, std::floor(std::log10(xRange / 10)));
    double yStep = std::pow(10, std::floor(std::log10(yRange / 10)));
    
    // Vertical lines
    double x = std::floor(m_xMin / xStep) * xStep;
    while (x <= m_xMax) {
        QPointF p1 = worldToScreen(QPointF(x, m_yMin));
        QPointF p2 = worldToScreen(QPointF(x, m_yMax));
        if (p1.y() >= drawTop && p1.y() <= drawBottom) {
            painter.drawLine(p1, p2);
        }
        x += xStep;
    }
    
    // Horizontal lines
    double y = std::floor(m_yMin / yStep) * yStep;
    while (y <= m_yMax) {
        QPointF p1 = worldToScreen(QPointF(m_xMin, y));
        QPointF p2 = worldToScreen(QPointF(m_xMax, y));
        if (p1.y() >= drawTop && p1.y() <= drawBottom) {
            painter.drawLine(p1, p2);
        }
        y += yStep;
    }
}

void TangentLineWidget::drawAxes(QPainter &painter) {
    painter.setPen(QPen(m_axisColor, 2));
    
    int drawTop = 20;
    int drawBottom = height() - 200;
    
    // X-axis
    if (m_yMin <= 0 && m_yMax >= 0) {
        QPointF p1 = worldToScreen(QPointF(m_xMin, 0));
        QPointF p2 = worldToScreen(QPointF(m_xMax, 0));
        painter.drawLine(p1, p2);
    }
    
    // Y-axis
    if (m_xMin <= 0 && m_xMax >= 0) {
        QPointF p1 = worldToScreen(QPointF(0, m_yMin));
        QPointF p2 = worldToScreen(QPointF(0, m_yMax));
        painter.drawLine(p1, p2);
    }
}

void TangentLineWidget::drawFunction(QPainter &painter) {
    if (m_functionPoints.size() < 2) return;
    
    int drawTop = 20;
    int drawBottom = height() - 200;
    
    QPainterPath path;
    bool firstPoint = true;
    
    for (const QPointF &pt : m_functionPoints) {
        QPointF screenPt = worldToScreen(pt);
        
        if (screenPt.y() >= drawTop && screenPt.y() <= drawBottom) {
            if (firstPoint) {
                path.moveTo(screenPt);
                firstPoint = false;
            } else {
                path.lineTo(screenPt);
            }
        } else {
            firstPoint = true;
        }
    }
    
    painter.setPen(QPen(m_functionColor, 3));
    painter.drawPath(path);
}

void TangentLineWidget::drawTangentLine(QPainter &painter) {
    // Calculate tangent line points
    double x1 = m_xMin;
    double y1 = m_slope * (x1 - m_tangentX) + m_tangentY;
    
    double x2 = m_xMax;
    double y2 = m_slope * (x2 - m_tangentX) + m_tangentY;
    
    QPointF p1 = worldToScreen(QPointF(x1, y1));
    QPointF p2 = worldToScreen(QPointF(x2, y2));
    
    // Draw tangent line
    painter.setPen(QPen(m_tangentColor, 2, Qt::DashLine));
    painter.drawLine(p1, p2);
    
    // Draw point of tangency
    QPointF tangentPoint = worldToScreen(QPointF(m_tangentX, m_tangentY));
    painter.setPen(QPen(Qt::white, 3));
    painter.setBrush(m_pointColor);
    painter.drawEllipse(tangentPoint, 6, 6);
}

void TangentLineWidget::drawNormalLine(QPainter &painter) {
    if (std::abs(m_slope) < 0.0001) return;  // Avoid division by zero
    
    // Normal line has slope -1/m
    double normalSlope = -1.0 / m_slope;
    
    double x1 = m_xMin;
    double y1 = normalSlope * (x1 - m_tangentX) + m_tangentY;
    
    double x2 = m_xMax;
    double y2 = normalSlope * (x2 - m_tangentX) + m_tangentY;
    
    QPointF p1 = worldToScreen(QPointF(x1, y1));
    QPointF p2 = worldToScreen(QPointF(x2, y2));
    
    painter.setPen(QPen(m_normalColor, 2, Qt::DotLine));
    painter.drawLine(p1, p2);
}

void TangentLineWidget::drawSecantLine(QPainter &painter) {
    double y1 = evaluateFunction(m_tangentX);
    double y2 = evaluateFunction(m_secantX2);
    
    QPointF p1 = worldToScreen(QPointF(m_tangentX, y1));
    QPointF p2 = worldToScreen(QPointF(m_secantX2, y2));
    
    painter.setPen(QPen(m_secantColor, 2));
    painter.drawLine(p1, p2);
    
    // Draw endpoints
    painter.setBrush(m_secantColor);
    painter.drawEllipse(p1, 4, 4);
    painter.drawEllipse(p2, 4, 4);
}

void TangentLineWidget::drawTangentInfo(QPainter &painter) {
    int infoY = height() - 185;
    
    painter.setPen(m_tangentColor);
    painter.setFont(QFont("Arial", 10, QFont::Bold));
    
    QString info = QString("Point: (%1, %2) | f'(%3) = %4")
                      .arg(m_tangentX, 0, 'f', 2)
                      .arg(m_tangentY, 0, 'f', 2)
                      .arg(m_tangentX, 0, 'f', 2)
                      .arg(m_slope, 0, 'f', 3);
    
    painter.drawText(10, infoY, info);
}

QPointF TangentLineWidget::worldToScreen(const QPointF &worldPoint) const {
    int drawTop = 20;
    int drawBottom = height() - 200;
    int drawHeight = drawBottom - drawTop;
    
    double sx = (worldPoint.x() - m_xMin) / (m_xMax - m_xMin) * width();
    double sy = drawTop + (m_yMax - worldPoint.y()) / (m_yMax - m_yMin) * drawHeight;
    return QPointF(sx, sy);
}

QPointF TangentLineWidget::screenToWorld(const QPointF &screenPoint) const {
    int drawTop = 20;
    int drawBottom = height() - 200;
    int drawHeight = drawBottom - drawTop;
    
    double wx = m_xMin + (screenPoint.x() / width()) * (m_xMax - m_xMin);
    double wy = m_yMax - ((screenPoint.y() - drawTop) / drawHeight) * (m_yMax - m_yMin);
    return QPointF(wx, wy);
}

void TangentLineWidget::onXSliderChanged(int value) {
    m_tangentX = value / 10.0;  // Scale to -10 to 10
    m_tangentY = evaluateFunction(m_tangentX);
    m_slope = evaluateDerivative(m_tangentX);
    m_secantX2 = m_tangentX + 0.5;
    
    updateLabels();
    update();
}

void TangentLineWidget::onAnimationToggled(bool checked) {
    m_isAnimating = checked;
    
    if (checked) {
        m_animateButton->setText("⏸ Pause");
        m_animationTimer->start(30);  // ~33 FPS
    } else {
        m_animateButton->setText("▶ Animate");
        m_animationTimer->stop();
    }
}

void TangentLineWidget::updateAnimation() {
    // Animate by moving the slider
    static double animX = -10.0;
    static double direction = 0.1;
    
    animX += direction;
    
    if (animX >= 10.0 || animX <= -10.0) {
        direction = -direction;
    }
    
    m_xSlider->setValue((int)(animX * 10));
}

void TangentLineWidget::mousePressEvent(QMouseEvent *event) {
    if (event->button() == Qt::LeftButton) {
        int drawTop = 20;
        int drawBottom = height() - 200;
        
        if (event->pos().y() >= drawTop && event->pos().y() <= drawBottom) {
            QPointF worldPos = screenToWorld(event->pos());
            m_tangentX = worldPos.x();
            m_tangentY = evaluateFunction(m_tangentX);
            m_slope = evaluateDerivative(m_tangentX);
            m_secantX2 = m_tangentX + 0.5;
            
            m_xSlider->setValue((int)(m_tangentX * 10));
            updateLabels();
            update();
        }
    }
}

void TangentLineWidget::mouseMoveEvent(QMouseEvent *event) {
    // Optional: could implement drag behavior
}

void TangentLineWidget::wheelEvent(QWheelEvent *event) {
    // Zoom functionality
    double zoomFactor = event->angleDelta().y() > 0 ? 0.9 : 1.1;
    
    double xRange = (m_xMax - m_xMin) * zoomFactor;
    double yRange = (m_yMax - m_yMin) * zoomFactor;
    
    double xCenter = (m_xMin + m_xMax) / 2;
    double yCenter = (m_yMin + m_yMax) / 2;
    
    m_xMin = xCenter - xRange / 2;
    m_xMax = xCenter + xRange / 2;
    m_yMin = yCenter - yRange / 2;
    m_yMax = yCenter + yRange / 2;
    
    calculateFunctionPoints();
    update();
    
    event->accept();
}
